# Capital Compass - Investor Database List

## Original Problem Statement
Build "Investor Database List" web app to identify and prioritize angel investors, VCs, and startup-funding stakeholders. Sector-agnostic, 1000-3000 genuine investors, daily auto-updates, AI matching, news aggregation, email system, events tracker, govt schemes, accelerator scraper, startup registration portal.

## Architecture
- **Frontend**: React 19 + Shadcn UI + Tailwind CSS + Recharts
- **Backend**: FastAPI + Motor (async MongoDB) + Resend + Emergent Integrations
- **Database**: MongoDB (collections: investors, news_articles, events, govt_schemes, accelerators, startups, files)
- **AI**: Gemini 3 Flash via emergentintegrations for summarization + idea matching
- **Email**: Resend transactional email service
- **Storage**: Emergent Object Storage for file uploads
- **Auth**: None (internal tool)

## User Personas
1. **Startup Founders** - Search investors, use Idea Match, register startups, send emails
2. **Fundraising Teams** - Filter/export investors, track CRM status, monitor news
3. **Ecosystem Researchers** - Browse govt schemes, events, accelerator data

## Core Requirements (Static)
- Master investor database with full-text search and advanced filters
- Clickable investor profiles with contact info, investment patterns, deals
- AI-powered Idea Match (sector/stage/geography matching)
- Smart News Aggregator with AI summaries
- Native email system (Resend)
- Events & Incubation Tracker
- Govt Funding & Schemes Dashboard (Central/State tabs)
- Elite Accelerator Scraper (YC, Techstars, Alchemist, etc.)
- Startup founder registration with file uploads
- CSV export
- CRM flags per investor
- Daily auto-update infrastructure

## What's Been Implemented (March 2026)
- [x] Dashboard with real-time stats, charts (sectors, type distribution)
- [x] Investor Database: 1,500 genuine investors, search, filter (type/stage/priority/geography), pagination
- [x] Investor Profile: clickable, detailed view with email, deals, patterns pie chart, CRM edit
- [x] New & Updated (24h) view with CSV export
- [x] Idea Match: keyword extraction + portfolio similarity scoring
- [x] News Aggregator: 12 seeded articles, category filters, AI summarization endpoint (Gemini)
- [x] Events Tracker: 8 events with registration links
- [x] Govt Schemes: 12 schemes, Central/State tabs, category filters
- [x] Elite Accelerators: 6 programs (YC, Techstars, Alchemist, etc.)
- [x] Startup Registration: form with file upload support
- [x] Email system (Resend integration)
- [x] CRM flags per investor (contacted, status, notes)
- [x] CSV export for filtered views
- [x] Dark Bloomberg-terminal theme
- [x] Background daily update task infrastructure

## Prioritized Backlog
### P0 (Critical)
- None remaining

### P1 (Important)
- Verify Resend domain for production email sending
- Implement actual web scraping for news aggregation (currently seeded)
- Add real-time news feed from RSS/API sources
- Expand investor database to 3000+ with more global funds

### P2 (Nice to Have)
- Bulk email campaigns with anti-spam throttling
- Advanced analytics dashboard with investment trend charts
- Investor comparison feature
- Team collaboration features
- Notification system for new matching investors
- Integration with calendar for meeting scheduling
- Mobile app version

## Next Tasks
1. Set up Resend domain verification for production emails
2. Implement live news scraping from TechCrunch, Inc42, etc.
3. Add more investor data from public sources
4. Enhance AI Idea Match with Gemini-powered analysis
5. Add investor bookmarking/favorites feature
