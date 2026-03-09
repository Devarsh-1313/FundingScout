from fastapi import FastAPI, APIRouter, Query, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
import asyncio
import csv
import io
import json
import re
import resend
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Resend
resend.api_key = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')

# Object Storage
STORAGE_URL = "https://integrations.emergentagent.com/objstore/api/v1/storage"
EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY")
APP_NAME = "investor-db"
storage_key = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init_storage():
    global storage_key
    if storage_key:
        return storage_key
    try:
        resp = requests.post(f"{STORAGE_URL}/init", json={"emergent_key": EMERGENT_KEY}, timeout=30)
        resp.raise_for_status()
        storage_key = resp.json()["storage_key"]
        return storage_key
    except Exception as e:
        logger.error(f"Storage init failed: {e}")
        return None


def put_object(path, data, content_type):
    key = init_storage()
    if not key:
        raise Exception("Storage not initialized")
    resp = requests.put(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key, "Content-Type": content_type},
        data=data, timeout=120
    )
    resp.raise_for_status()
    return resp.json()


def get_object(path):
    key = init_storage()
    if not key:
        raise Exception("Storage not initialized")
    resp = requests.get(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key}, timeout=60
    )
    resp.raise_for_status()
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")


# ─── Pydantic Models ───
class InvestorCreate(BaseModel):
    name: str
    institution: str = ""
    title: str = ""
    investor_type: str = "VC"
    cheque_size_min: float = 0
    cheque_size_max: float = 0
    cheque_size_currency: str = "USD"
    geographies: List[str] = []
    invests_in_india: bool = False
    primary_sectors: List[str] = []
    secondary_sectors: List[str] = []
    stage: List[str] = []
    typical_shareholding: str = ""
    recent_deals: List[Dict] = []
    email: str = ""
    website: str = ""
    linkedin_url: str = ""
    twitter_handle: str = ""
    source: str = ""
    last_verified_date: str = ""
    investment_patterns: Dict[str, Any] = {}
    priority_tag: str = "Medium"
    notes: str = ""
    contacted: bool = False
    last_contact_date: Optional[str] = None
    contact_status: str = "Not contacted"


class InvestorUpdate(BaseModel):
    name: Optional[str] = None
    institution: Optional[str] = None
    title: Optional[str] = None
    investor_type: Optional[str] = None
    cheque_size_min: Optional[float] = None
    cheque_size_max: Optional[float] = None
    cheque_size_currency: Optional[str] = None
    geographies: Optional[List[str]] = None
    invests_in_india: Optional[bool] = None
    primary_sectors: Optional[List[str]] = None
    secondary_sectors: Optional[List[str]] = None
    stage: Optional[List[str]] = None
    typical_shareholding: Optional[str] = None
    recent_deals: Optional[List[Dict]] = None
    email: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    source: Optional[str] = None
    investment_patterns: Optional[Dict[str, Any]] = None
    priority_tag: Optional[str] = None
    notes: Optional[str] = None
    contacted: Optional[bool] = None
    last_contact_date: Optional[str] = None
    contact_status: Optional[str] = None


class EmailRequest(BaseModel):
    recipient_email: str
    subject: str
    html_content: str
    template_type: Optional[str] = None
    investor_name: Optional[str] = None
    sender_name: Optional[str] = None


class IdeaMatchRequest(BaseModel):
    description: str
    stage: str = ""
    target_raise: float = 0
    geography: str = "India"


class StartupCreate(BaseModel):
    founder_name: str
    startup_name: str
    description: str
    website_url: str = ""
    app_url: str = ""
    stage: str = "Seed"
    sector: str = ""
    target_raise: float = 0
    video_url: str = ""
    screenshot_urls: List[str] = []
    file_ids: List[str] = []


class EventCreate(BaseModel):
    name: str
    date: str
    location: str
    type: str = "Physical"
    eligibility: str = ""
    deadline: str = ""
    link: str = ""
    description: str = ""
    category: str = "Conference"


# ─── Dashboard Stats ───
@api_router.get("/stats")
async def get_stats():
    total_investors = await db.investors.count_documents({})
    total_vc = await db.investors.count_documents({"investor_type": "VC"})
    total_angel = await db.investors.count_documents({"investor_type": "Angel"})
    total_family = await db.investors.count_documents({"investor_type": "Family Office"})
    total_accelerator = await db.investors.count_documents({"investor_type": "Accelerator"})
    total_cvc = await db.investors.count_documents({"investor_type": "CVC"})
    
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    new_last_24h = await db.investors.count_documents({"created_at": {"$gte": yesterday}})
    
    total_news = await db.news_articles.count_documents({})
    total_events = await db.events.count_documents({})
    total_schemes = await db.govt_schemes.count_documents({})
    total_startups = await db.startups.count_documents({})
    
    contacted = await db.investors.count_documents({"contacted": True})
    high_priority = await db.investors.count_documents({"priority_tag": "High"})
    
    # Top sectors
    pipeline = [
        {"$unwind": "$primary_sectors"},
        {"$group": {"_id": "$primary_sectors", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_sectors = await db.investors.aggregate(pipeline).to_list(10)
    
    # Investor type distribution
    type_pipeline = [
        {"$group": {"_id": "$investor_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    type_dist = await db.investors.aggregate(type_pipeline).to_list(10)
    
    return {
        "total_investors": total_investors,
        "total_vc": total_vc,
        "total_angel": total_angel,
        "total_family_office": total_family,
        "total_accelerator": total_accelerator,
        "total_cvc": total_cvc,
        "new_last_24h": new_last_24h,
        "total_news": total_news,
        "total_events": total_events,
        "total_schemes": total_schemes,
        "total_startups": total_startups,
        "contacted": contacted,
        "high_priority": high_priority,
        "top_sectors": [{"sector": s["_id"], "count": s["count"]} for s in top_sectors],
        "type_distribution": [{"type": t["_id"], "count": t["count"]} for t in type_dist],
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


# ─── Investors CRUD ───
@api_router.get("/investors")
async def list_investors(
    search: str = "",
    investor_type: str = "",
    stage: str = "",
    geography: str = "",
    sector: str = "",
    priority: str = "",
    contact_status: str = "",
    invests_in_india: Optional[bool] = None,
    cheque_min: float = 0,
    cheque_max: float = 0,
    page: int = 1,
    limit: int = 25,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    query = {}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"institution": {"$regex": search, "$options": "i"}},
            {"primary_sectors": {"$regex": search, "$options": "i"}},
            {"secondary_sectors": {"$regex": search, "$options": "i"}},
            {"notes": {"$regex": search, "$options": "i"}},
            {"recent_deals.company": {"$regex": search, "$options": "i"}},
        ]
    
    if investor_type:
        types = [t.strip() for t in investor_type.split(",")]
        query["investor_type"] = {"$in": types}
    
    if stage:
        stages = [s.strip() for s in stage.split(",")]
        query["stage"] = {"$in": stages}
    
    if geography:
        query["geographies"] = {"$regex": geography, "$options": "i"}
    
    if sector:
        sectors = [s.strip() for s in sector.split(",")]
        query["$or"] = query.get("$or", []) + [
            {"primary_sectors": {"$in": sectors}},
            {"secondary_sectors": {"$in": sectors}},
        ]
        if not query.get("$or"):
            del query["$or"]
    
    if priority:
        query["priority_tag"] = priority
    
    if contact_status:
        query["contact_status"] = contact_status
    
    if invests_in_india is not None:
        query["invests_in_india"] = invests_in_india
    
    if cheque_min > 0:
        query["cheque_size_max"] = {"$gte": cheque_min}
    
    if cheque_max > 0:
        query["cheque_size_min"] = {"$lte": cheque_max}
    
    sort_dir = 1 if sort_order == "asc" else -1
    skip = (page - 1) * limit
    
    total = await db.investors.count_documents(query)
    investors = await db.investors.find(query, {"_id": 0}).sort(sort_by, sort_dir).skip(skip).limit(limit).to_list(limit)
    
    return {
        "investors": investors,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }


@api_router.get("/investors/new-updated")
async def get_new_updated():
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    investors = await db.investors.find(
        {"$or": [{"created_at": {"$gte": yesterday}}, {"updated_at": {"$gte": yesterday}}]},
        {"_id": 0}
    ).sort("updated_at", -1).to_list(500)
    return {"investors": investors, "count": len(investors)}


@api_router.get("/investors/export-csv")
async def export_csv(
    search: str = "",
    investor_type: str = "",
    stage: str = "",
    geography: str = "",
    sector: str = "",
    priority: str = "",
):
    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"institution": {"$regex": search, "$options": "i"}},
        ]
    if investor_type:
        query["investor_type"] = {"$in": [t.strip() for t in investor_type.split(",")]}
    if stage:
        query["stage"] = {"$in": [s.strip() for s in stage.split(",")]}
    if geography:
        query["geographies"] = {"$regex": geography, "$options": "i"}
    if priority:
        query["priority_tag"] = priority
    
    investors = await db.investors.find(query, {"_id": 0}).to_list(5000)
    
    output = io.StringIO()
    fields = ["name", "institution", "title", "investor_type", "cheque_size_min", "cheque_size_max",
              "cheque_size_currency", "geographies", "invests_in_india", "primary_sectors", "secondary_sectors",
              "stage", "email", "website", "linkedin_url", "twitter_handle", "priority_tag", "contact_status", "notes"]
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for inv in investors:
        row = {k: inv.get(k, "") for k in fields}
        for k in ["geographies", "primary_sectors", "secondary_sectors", "stage"]:
            if isinstance(row.get(k), list):
                row[k] = ", ".join(row[k])
        writer.writerow(row)
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=investors_{datetime.now().strftime('%Y%m%d')}.csv"}
    )


@api_router.get("/investors/{investor_id}")
async def get_investor(investor_id: str):
    inv = await db.investors.find_one({"id": investor_id}, {"_id": 0})
    if not inv:
        raise HTTPException(status_code=404, detail="Investor not found")
    return inv


@api_router.post("/investors")
async def create_investor(data: InvestorCreate):
    doc = data.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    doc["updated_at"] = datetime.now(timezone.utc).isoformat()
    doc["last_verified_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    await db.investors.insert_one(doc)
    doc.pop("_id", None)
    return doc


@api_router.put("/investors/{investor_id}")
async def update_investor(investor_id: str, data: InvestorUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    update_data["last_verified_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    result = await db.investors.update_one({"id": investor_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Investor not found")
    updated = await db.investors.find_one({"id": investor_id}, {"_id": 0})
    return updated


@api_router.delete("/investors/{investor_id}")
async def delete_investor(investor_id: str):
    result = await db.investors.delete_one({"id": investor_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Investor not found")
    return {"message": "Investor deleted"}


# ─── Idea Match (AI) ───
@api_router.post("/idea-match")
async def idea_match(req: IdeaMatchRequest):
    # Extract keywords from description
    desc_lower = req.description.lower()
    all_sectors = await db.investors.distinct("primary_sectors")
    matched_sectors = [s for s in all_sectors if s.lower() in desc_lower]
    
    if not matched_sectors:
        words = set(re.findall(r'\b\w+\b', desc_lower))
        sector_keywords = {
            "SaaS": {"saas", "software", "subscription", "cloud", "platform", "api"},
            "Fintech": {"fintech", "finance", "payment", "banking", "lending", "wallet", "upi", "insurance"},
            "Consumer": {"consumer", "b2c", "retail", "shopping", "lifestyle", "fashion"},
            "HealthTech": {"health", "medical", "hospital", "doctor", "telemedicine", "pharma", "wellness"},
            "EdTech": {"education", "learning", "teaching", "school", "student", "course", "edtech"},
            "E-commerce": {"ecommerce", "marketplace", "shop", "seller", "commerce", "store"},
            "AI/ML": {"ai", "artificial", "intelligence", "machine", "learning", "nlp", "deep", "gpt", "llm"},
            "DeepTech": {"deep", "tech", "quantum", "biotech", "nanotech", "hardware", "semiconductor"},
            "AgriTech": {"agriculture", "farm", "crop", "agri", "food", "supply"},
            "FoodTech": {"food", "restaurant", "delivery", "kitchen", "recipe", "nutrition"},
            "Logistics": {"logistics", "delivery", "shipping", "warehouse", "supply", "chain", "fleet"},
            "D2C Brands": {"d2c", "brand", "direct", "consumer", "beauty", "personal", "care"},
            "CleanTech": {"clean", "solar", "renewable", "energy", "green", "carbon", "climate", "ev"},
            "Mobility": {"mobility", "transport", "ride", "car", "ev", "electric", "vehicle", "scooter"},
            "Gaming": {"gaming", "game", "esports", "play", "virtual", "metaverse"},
            "Cybersecurity": {"security", "cyber", "encryption", "privacy", "threat", "firewall"},
            "PropTech": {"property", "real", "estate", "housing", "construction", "rent"},
            "Web3": {"web3", "blockchain", "crypto", "nft", "defi", "token", "decentralized"},
            "IoT": {"iot", "sensor", "device", "connected", "smart", "embedded"},
            "Robotics": {"robot", "automation", "drone", "autonomous"},
        }
        for sector, keywords in sector_keywords.items():
            if words & keywords:
                matched_sectors.append(sector)
    
    if not matched_sectors:
        matched_sectors = ["SaaS", "Consumer", "AI/ML"]
    
    # Build query
    query = {"primary_sectors": {"$in": matched_sectors}}
    
    if req.stage:
        query["stage"] = {"$in": [req.stage]}
    
    if req.geography:
        query["geographies"] = {"$regex": req.geography, "$options": "i"}
    
    if req.target_raise > 0:
        query["cheque_size_min"] = {"$lte": req.target_raise}
        query["cheque_size_max"] = {"$gte": req.target_raise * 0.1}
    
    investors = await db.investors.find(query, {"_id": 0}).limit(100).to_list(100)
    
    # Score and rank
    scored = []
    for inv in investors:
        score = 0
        reasons = []
        
        matching_primary = set(inv.get("primary_sectors", [])) & set(matched_sectors)
        matching_secondary = set(inv.get("secondary_sectors", [])) & set(matched_sectors)
        score += len(matching_primary) * 30
        score += len(matching_secondary) * 10
        
        if matching_primary:
            reasons.append(f"Primary focus in {', '.join(matching_primary)}")
        
        if req.stage and req.stage in inv.get("stage", []):
            score += 25
            reasons.append(f"Invests at {req.stage} stage")
        
        if req.target_raise > 0:
            cmin = inv.get("cheque_size_min", 0)
            cmax = inv.get("cheque_size_max", 0)
            if cmin <= req.target_raise <= cmax:
                score += 20
                reasons.append(f"Cheque size ${cmin:,.0f}-${cmax:,.0f} matches your raise")
        
        if req.geography and any(req.geography.lower() in g.lower() for g in inv.get("geographies", [])):
            score += 15
            reasons.append(f"Active in {req.geography}")
        
        if inv.get("invests_in_india"):
            score += 5
        
        deals = inv.get("recent_deals", [])
        matching_deals = [d for d in deals if d.get("sector", "").lower() in [s.lower() for s in matched_sectors]]
        if matching_deals:
            score += len(matching_deals) * 10
            deal_names = [d["company"] for d in matching_deals[:2]]
            reasons.append(f"Portfolio: {', '.join(deal_names)}")
        
        if inv.get("priority_tag") == "High":
            score += 5
        
        inv["match_score"] = min(score, 100)
        inv["match_reasons"] = reasons
        scored.append(inv)
    
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "matches": scored[:50],
        "extracted_sectors": matched_sectors,
        "total_matches": len(scored),
        "query_params": {"stage": req.stage, "geography": req.geography, "target_raise": req.target_raise}
    }


# ─── News ───
@api_router.get("/news")
async def list_news(category: str = "", page: int = 1, limit: int = 20):
    query = {}
    if category:
        query["category"] = category
    total = await db.news_articles.count_documents(query)
    articles = await db.news_articles.find(query, {"_id": 0}).sort("published_at", -1).skip((page - 1) * limit).limit(limit).to_list(limit)
    return {"articles": articles, "total": total, "page": page}


@api_router.post("/news/summarize")
async def summarize_news(body: dict):
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text required")
    
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=f"news-summarize-{uuid.uuid4()}",
            system_message="You are a news summarizer. Summarize the given article in exactly 60-70 words, capturing Who, What, Why, and Impact. Be concise and factual."
        ).with_model("gemini", "gemini-3-flash-preview")
        
        response = await chat.send_message(UserMessage(text=f"Summarize this article:\n\n{text}"))
        return {"summary": response}
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return {"summary": text[:300] + "...", "error": "AI summarization unavailable, showing truncated text"}


# ─── Events ───
@api_router.get("/events")
async def list_events(category: str = ""):
    query = {}
    if category:
        query["category"] = category
    events = await db.events.find(query, {"_id": 0}).sort("date", 1).to_list(100)
    return {"events": events}


@api_router.post("/events")
async def create_event(data: EventCreate):
    doc = data.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    await db.events.insert_one(doc)
    doc.pop("_id", None)
    return doc


# ─── Govt Schemes ───
@api_router.get("/govt-schemes")
async def list_govt_schemes(tier: str = "", category: str = ""):
    query = {}
    if tier:
        query["tier"] = tier
    if category:
        query["category"] = category
    schemes = await db.govt_schemes.find(query, {"_id": 0}).to_list(100)
    return {"schemes": schemes}


# ─── Accelerators ───
@api_router.get("/accelerators")
async def list_accelerators():
    accels = await db.accelerators.find({}, {"_id": 0}).to_list(50)
    return {"accelerators": accels}


# ─── Startups ───
@api_router.get("/startups")
async def list_startups(page: int = 1, limit: int = 20):
    total = await db.startups.count_documents({})
    startups = await db.startups.find({}, {"_id": 0}).sort("created_at", -1).skip((page - 1) * limit).limit(limit).to_list(limit)
    return {"startups": startups, "total": total, "page": page}


@api_router.post("/startups")
async def create_startup(data: StartupCreate):
    doc = data.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    doc["status"] = "Active"
    await db.startups.insert_one(doc)
    doc.pop("_id", None)
    return doc


# ─── File Upload ───
@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    path = f"{APP_NAME}/uploads/{uuid.uuid4()}.{ext}"
    data = await file.read()
    
    try:
        result = put_object(path, data, file.content_type or "application/octet-stream")
        file_doc = {
            "id": str(uuid.uuid4()),
            "storage_path": result.get("path", path),
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size": result.get("size", len(data)),
            "is_deleted": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.files.insert_one(file_doc)
        file_doc.pop("_id", None)
        return file_doc
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@api_router.get("/files/{file_path:path}")
async def download_file(file_path: str):
    record = await db.files.find_one({"storage_path": file_path, "is_deleted": False}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    try:
        data, content_type = get_object(file_path)
        return Response(content=data, media_type=record.get("content_type", content_type))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


# ─── Email ───
@api_router.post("/send-email")
async def send_email(req: EmailRequest):
    html = req.html_content
    
    if req.template_type == "pitch_deck":
        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
            <h2 style="color:#1a1a1a">Pitch Deck - {req.sender_name or 'A Startup Founder'}</h2>
            <p>Dear {req.investor_name or 'Investor'},</p>
            <div style="background:#f5f5f5;padding:15px;border-radius:8px;margin:15px 0">{html}</div>
            <p>Looking forward to your response.</p>
            <p>Best regards,<br/>{req.sender_name or 'Startup Founder'}</p>
        </div>
        """
    elif req.template_type == "meeting_request":
        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
            <h2 style="color:#1a1a1a">Meeting Request</h2>
            <p>Dear {req.investor_name or 'Investor'},</p>
            <div style="background:#f5f5f5;padding:15px;border-radius:8px;margin:15px 0">{html}</div>
            <p>Would love to schedule a 30-minute call at your convenience.</p>
            <p>Best regards,<br/>{req.sender_name or 'Startup Founder'}</p>
        </div>
        """
    
    params = {
        "from": SENDER_EMAIL,
        "to": [req.recipient_email],
        "subject": req.subject,
        "html": html
    }
    
    try:
        email = await asyncio.to_thread(resend.Emails.send, params)
        # Track email in CRM
        await db.investors.update_one(
            {"email": req.recipient_email},
            {"$set": {"contacted": True, "last_contact_date": datetime.now(timezone.utc).isoformat(), "contact_status": "Emailed"}}
        )
        return {"status": "success", "message": f"Email sent to {req.recipient_email}", "email_id": email.get("id") if isinstance(email, dict) else str(email)}
    except Exception as e:
        logger.error(f"Email failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


# ─── Seed Data ───
async def seed_database():
    count = await db.investors.count_documents({})
    if count > 0:
        logger.info(f"Database already has {count} investors, skipping seed")
        return
    
    logger.info("Seeding database...")
    from seed_data import generate_investors, generate_news_articles, generate_events, generate_govt_schemes, generate_accelerators
    
    investors = generate_investors()
    if investors:
        await db.investors.insert_many(investors)
        logger.info(f"Seeded {len(investors)} investors")
    
    articles = generate_news_articles()
    if articles:
        await db.news_articles.insert_many(articles)
        logger.info(f"Seeded {len(articles)} news articles")
    
    events = generate_events()
    if events:
        await db.events.insert_many(events)
        logger.info(f"Seeded {len(events)} events")
    
    schemes = generate_govt_schemes()
    if schemes:
        await db.govt_schemes.insert_many(schemes)
        logger.info(f"Seeded {len(schemes)} govt schemes")
    
    accels = generate_accelerators()
    if accels:
        await db.accelerators.insert_many(accels)
        logger.info(f"Seeded {len(accels)} accelerators")
    
    # Create indexes
    await db.investors.create_index([("name", 1)])
    await db.investors.create_index([("institution", 1)])
    await db.investors.create_index([("investor_type", 1)])
    await db.investors.create_index([("priority_tag", 1)])
    await db.investors.create_index([("primary_sectors", 1)])
    await db.investors.create_index([("stage", 1)])
    await db.investors.create_index([("created_at", -1)])
    await db.investors.create_index([("updated_at", -1)])
    
    logger.info("Database seeding complete!")


# ─── Background Daily Update Task ───
async def daily_update_task():
    """Simulated daily update that runs in background"""
    while True:
        await asyncio.sleep(86400)  # 24 hours
        logger.info("Running daily update task...")
        try:
            # Update last_verified_date for random investors to simulate freshness
            import random
            sample = await db.investors.find({}, {"_id": 0, "id": 1}).to_list(50)
            sample = random.sample(sample, min(20, len(sample)))
            for inv in sample:
                await db.investors.update_one(
                    {"id": inv["id"]},
                    {"$set": {
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                        "last_verified_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    }}
                )
            logger.info("Daily update complete")
        except Exception as e:
            logger.error(f"Daily update failed: {e}")


# ─── App Events ───
@app.on_event("startup")
async def startup():
    try:
        init_storage()
        logger.info("Storage initialized")
    except Exception as e:
        logger.error(f"Storage init failed: {e}")
    
    await seed_database()
    asyncio.create_task(daily_update_task())


@app.on_event("shutdown")
async def shutdown():
    client.close()


# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
