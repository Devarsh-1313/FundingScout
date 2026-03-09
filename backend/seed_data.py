import random
import uuid
from datetime import datetime, timezone, timedelta

SECTORS = [
    "SaaS", "Fintech", "Consumer", "EdTech", "HealthTech", "DeepTech",
    "AgriTech", "CleanTech", "E-commerce", "Gaming", "Logistics",
    "Enterprise Software", "AI/ML", "Cybersecurity", "IoT", "Blockchain",
    "FoodTech", "PropTech", "InsurTech", "HRTech", "LegalTech",
    "MediaTech", "SpaceTech", "BioTech", "Robotics", "AR/VR",
    "D2C Brands", "Social Commerce", "Mobility", "Climate Tech",
    "Web3", "NFT/Metaverse", "Quantum Computing", "Drug Discovery",
    "Mental Health", "Wearables", "Drone Tech", "EV/Electric Vehicles",
    "Renewable Energy", "Supply Chain", "MarTech", "RetailTech",
    "TravelTech", "Construction Tech", "Sustainability"
]

STAGES = ["Pre-seed", "Seed", "Pre-Series A", "Series A", "Series B", "Series C", "Growth", "Late Stage"]

GEOGRAPHIES = [
    "India", "USA", "Singapore", "UK", "Israel", "Germany", "Japan",
    "Southeast Asia", "Middle East", "Africa", "Latin America", "Canada",
    "Australia", "France", "Netherlands", "South Korea", "China", "UAE",
    "Hong Kong", "Indonesia", "Brazil", "Nigeria", "Kenya", "Egypt"
]

SOURCES = [
    "Inc42", "YourStory", "VCCircle", "Crunchbase", "Fund Website",
    "LinkedIn Public", "TechCrunch", "Economic Times", "Entrackr",
    "Press Release", "OpenVC", "AngelList", "PitchBook"
]

COMPANIES_POOL = [
    "Zomato", "Swiggy", "CRED", "Razorpay", "PhonePe", "Paytm", "Ola",
    "Byju's", "Unacademy", "Meesho", "Zerodha", "Groww", "Lenskart",
    "Nykaa", "BoAt", "Mamaearth", "Freshworks", "Postman", "Chargebee",
    "Zoho", "Browserstack", "Druva", "Hasura", "Polygon", "ShareChat",
    "Dream11", "MPL", "Jupiter", "Fi Money", "Slice", "OneCard",
    "Zepto", "Blinkit", "BigBasket", "Dunzo", "Urban Company",
    "PharmEasy", "Practo", "CureFit", "HealthifyMe", "1mg",
    "Vedantu", "Toppr", "Eruditus", "Emeritus", "upGrad",
    "Ather Energy", "Yulu", "Rapido", "Porter", "BlackBuck",
    "Rivigo", "Delhivery", "Shiprocket", "NoBroker", "Housing.com",
    "Moglix", "Udaan", "OkCredit", "Khatabook", "BharatPe",
    "Pine Labs", "Cashfree", "Instamojo", "Niyo", "Open Financial",
    "Acko", "Digit Insurance", "GoDigit", "PolicyBazaar",
    "CarDekho", "Cars24", "Spinny", "Droom", "Zetwerk",
    "Infra.Market", "BrightChamps", "LeadSquared", "Darwinbox",
    "MindTickle", "Leena AI", "Yellow.ai", "Haptik", "Observe.AI",
    "Innovaccer", "CleverTap", "MoEngage", "WebEngage",
    "Whatfix", "Mindtree", "Mphasis", "Zenoti", "Vyapar",
    "Khatabook", "myGate", "NoBroker", "Simplilearn", "Scaler",
    "InterviewBit", "AlgoExpert", "Codeforces", "LeetCode India",
    "Stripe India", "Notion India", "Figma India", "Canva India"
]

VC_FIRMS = [
    {"inst": "Sequoia Capital India", "partners": [("Shailendra Singh", "Managing Director"), ("Rajan Anandan", "Managing Director"), ("Harshjit Sethi", "Partner"), ("Sakshi Chopra", "Principal")], "cheque": (500000, 100000000), "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["SaaS", "Consumer", "Fintech", "DeepTech"], "geo": ["India", "Southeast Asia"]},
    {"inst": "Accel India", "partners": [("Prashanth Prakash", "Partner"), ("Anand Daniel", "Partner"), ("Barath Shankar Subramanian", "Partner"), ("Prayank Swaroop", "Partner")], "cheque": (250000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["SaaS", "Consumer", "Fintech", "Enterprise Software"], "geo": ["India"]},
    {"inst": "Matrix Partners India", "partners": [("Avnish Bajaj", "Founder & Managing Director"), ("Tarun Davda", "Managing Director"), ("Vikram Vaidyanathan", "Managing Director"), ("Sripathi Srinivasa", "Director")], "cheque": (500000, 30000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "SaaS", "Fintech", "E-commerce"], "geo": ["India"]},
    {"inst": "Kalaari Capital", "partners": [("Vani Kola", "Managing Director"), ("Rajesh Raju", "Managing Director"), ("Ravinder Singh", "Principal")], "cheque": (200000, 20000000), "stages": ["Seed", "Series A"], "sectors": ["Consumer", "EdTech", "HealthTech", "SaaS"], "geo": ["India"]},
    {"inst": "Nexus Venture Partners", "partners": [("Jishnu Bhattacharjee", "Managing Director"), ("Sameer Brij Verma", "Managing Director"), ("Suvir Sujan", "Managing Director")], "cheque": (500000, 40000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise Software", "DeepTech", "HealthTech", "Fintech"], "geo": ["India", "USA"]},
    {"inst": "Blume Ventures", "partners": [("Karthik Reddy", "Managing Partner"), ("Sanjay Nath", "Managing Partner"), ("Sajith Pai", "Partner"), ("Arpit Agarwal", "Partner")], "cheque": (50000, 5000000), "stages": ["Pre-seed", "Seed", "Pre-Series A"], "sectors": ["SaaS", "D2C Brands", "Fintech", "HealthTech", "DeepTech"], "geo": ["India"]},
    {"inst": "Elevation Capital", "partners": [("Ravi Adusumalli", "Managing Partner"), ("Mukul Arora", "Managing Partner"), ("Mridul Arora", "Partner"), ("Akarsh Shrivastava", "Partner")], "cheque": (1000000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "SaaS", "Fintech", "HealthTech"], "geo": ["India"]},
    {"inst": "Lightspeed India Partners", "partners": [("Bejul Somaia", "Partner"), ("Dev Khare", "Partner"), ("Harsha Kumar", "Partner"), ("Vaibhav Agrawal", "Partner")], "cheque": (500000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "Enterprise Software", "Fintech", "SaaS"], "geo": ["India", "Southeast Asia"]},
    {"inst": "Tiger Global Management", "partners": [("Scott Shleifer", "Partner"), ("John Curtius", "Partner"), ("Griffin Schroeder", "Partner")], "cheque": (5000000, 200000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["Consumer", "Fintech", "SaaS", "E-commerce"], "geo": ["India", "USA", "Global"]},
    {"inst": "SoftBank Vision Fund", "partners": [("Munish Varma", "Managing Partner"), ("Sumer Juneja", "Partner"), ("Lydia Jett", "Partner")], "cheque": (50000000, 500000000), "stages": ["Series B", "Growth", "Late Stage"], "sectors": ["Mobility", "E-commerce", "Fintech", "Consumer"], "geo": ["India", "Global"]},
    {"inst": "Andreessen Horowitz (a16z)", "partners": [("Marc Andreessen", "Co-founder"), ("Ben Horowitz", "Co-founder"), ("Andrew Chen", "General Partner"), ("Connie Chan", "General Partner")], "cheque": (1000000, 100000000), "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["AI/ML", "Web3", "Consumer", "Enterprise Software", "Fintech"], "geo": ["USA", "Global"]},
    {"inst": "Chiratae Ventures", "partners": [("Sudhir Sethi", "Founder & Chairman"), ("TC Meenakshisundaram", "Founder & Vice Chairman"), ("Venkatesh Peddi", "Executive Director")], "cheque": (500000, 20000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "SaaS", "HealthTech", "Enterprise Software"], "geo": ["India"]},
    {"inst": "Stellaris Venture Partners", "partners": [("Alok Goyal", "Partner"), ("Ritesh Banglani", "Partner"), ("Rahul Chowdhri", "Partner")], "cheque": (250000, 10000000), "stages": ["Seed", "Series A"], "sectors": ["SaaS", "Fintech", "Consumer", "Enterprise Software"], "geo": ["India"]},
    {"inst": "Pi Ventures", "partners": [("Manish Singhal", "Founding Partner"), ("Umakant Soni", "Founding Partner")], "cheque": (200000, 5000000), "stages": ["Pre-seed", "Seed", "Pre-Series A"], "sectors": ["AI/ML", "DeepTech", "HealthTech", "Robotics"], "geo": ["India"]},
    {"inst": "India Quotient", "partners": [("Anand Lunia", "Founding Partner"), ("Madhukar Sinha", "Founding Partner")], "cheque": (50000, 3000000), "stages": ["Pre-seed", "Seed"], "sectors": ["Consumer", "SaaS", "Social Commerce", "D2C Brands"], "geo": ["India"]},
    {"inst": "Venture Highway", "partners": [("Samir Sood", "Founding Partner"), ("Neeraj Arora", "Partner")], "cheque": (100000, 5000000), "stages": ["Pre-seed", "Seed", "Pre-Series A"], "sectors": ["Consumer", "SaaS", "Fintech"], "geo": ["India", "Southeast Asia"]},
    {"inst": "Peak XV Partners (Surge)", "partners": [("Rajan Anandan", "Managing Director"), ("Shailesh Lakhani", "Managing Director"), ("Mohit Bhatnagar", "Managing Director")], "cheque": (1000000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "SaaS", "Fintech", "Enterprise Software"], "geo": ["India", "Southeast Asia"]},
    {"inst": "General Catalyst", "partners": [("Hemant Taneja", "Managing Director"), ("Joel Cutler", "Managing Director"), ("Adam Valkin", "Managing Director")], "cheque": (5000000, 100000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["AI/ML", "Enterprise Software", "HealthTech", "Fintech"], "geo": ["USA", "India", "Global"]},
    {"inst": "Bessemer Venture Partners", "partners": [("Vishal Gupta", "Partner"), ("Alex Ferrara", "Partner"), ("Ethan Kurzweil", "Partner")], "cheque": (1000000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["SaaS", "Cloud", "Enterprise Software", "Cybersecurity"], "geo": ["USA", "India", "Global"]},
    {"inst": "Y Combinator", "partners": [("Garry Tan", "CEO"), ("Michael Seibel", "Managing Director"), ("Gustaf Alstromer", "Group Partner"), ("Dalton Caldwell", "Managing Director")], "cheque": (125000, 500000), "stages": ["Pre-seed", "Seed"], "sectors": ["SaaS", "AI/ML", "Consumer", "Fintech", "HealthTech"], "geo": ["Global"]},
    {"inst": "Techstars", "partners": [("Maëlle Gavet", "CEO"), ("Ting Ting Liu", "Managing Director"), ("David Cohen", "Founder")], "cheque": (120000, 500000), "stages": ["Pre-seed", "Seed"], "sectors": ["SaaS", "AI/ML", "Sustainability", "HealthTech"], "geo": ["Global"]},
    {"inst": "500 Global", "partners": [("Christine Tsai", "CEO"), ("Bedy Yang", "Partner"), ("Vishal Harnal", "Partner")], "cheque": (50000, 2000000), "stages": ["Pre-seed", "Seed"], "sectors": ["Consumer", "Fintech", "SaaS", "E-commerce"], "geo": ["Global", "Southeast Asia", "Middle East"]},
    {"inst": "Founders Fund", "partners": [("Peter Thiel", "Co-founder"), ("Keith Rabois", "Partner"), ("Napoleon Ta", "Partner")], "cheque": (5000000, 100000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["AI/ML", "DeepTech", "SpaceTech", "BioTech"], "geo": ["USA", "Global"]},
    {"inst": "Benchmark", "partners": [("Bill Gurley", "General Partner"), ("Matt Cohler", "General Partner"), ("Sarah Tavel", "General Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B"], "sectors": ["Consumer", "Enterprise Software", "Marketplace"], "geo": ["USA", "Global"]},
    {"inst": "Kleiner Perkins", "partners": [("Mamoon Hamid", "Partner"), ("Ilya Fushman", "Partner"), ("Bucky Moore", "Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B"], "sectors": ["Enterprise Software", "Consumer", "HealthTech", "Fintech"], "geo": ["USA", "Global"]},
    {"inst": "Ribbit Capital", "partners": [("Micky Malka", "Founding Partner"), ("Nick Shalek", "General Partner"), ("Jordan Angelos", "Partner")], "cheque": (2000000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Fintech", "InsurTech", "Blockchain", "Crypto"], "geo": ["USA", "India", "Global"]},
    {"inst": "Norwest Venture Partners", "partners": [("Niren Shah", "Partner"), ("Jeff Crowe", "Managing Partner"), ("Jon Kossow", "General Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["SaaS", "Enterprise Software", "HealthTech", "Consumer"], "geo": ["USA", "India"]},
    {"inst": "Insight Partners", "partners": [("Jeff Horing", "Co-Founder"), ("Deven Parekh", "Managing Director"), ("Hilary Gosher", "Managing Director")], "cheque": (10000000, 200000000), "stages": ["Series B", "Growth", "Late Stage"], "sectors": ["SaaS", "Enterprise Software", "Cybersecurity", "AI/ML"], "geo": ["USA", "Global"]},
    {"inst": "GGV Capital", "partners": [("Hans Tung", "Managing Partner"), ("Jeff Richards", "Managing Partner"), ("Jenny Lee", "Managing Partner")], "cheque": (2000000, 50000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["Consumer", "SaaS", "E-commerce", "AI/ML"], "geo": ["USA", "China", "India", "Southeast Asia"]},
    {"inst": "DST Global", "partners": [("Yuri Milner", "Founder"), ("Rahul Mehta", "Partner"), ("Tom Stafford", "Managing Partner")], "cheque": (50000000, 500000000), "stages": ["Growth", "Late Stage"], "sectors": ["Consumer", "E-commerce", "Fintech", "Mobility"], "geo": ["Global"]},
    {"inst": "Accel US", "partners": [("Andrew Braccia", "Partner"), ("Rich Wong", "Partner"), ("Amy Saper", "Partner")], "cheque": (1000000, 100000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["SaaS", "Enterprise Software", "Cybersecurity", "AI/ML"], "geo": ["USA", "Global"]},
    {"inst": "Greylock Partners", "partners": [("Reid Hoffman", "Partner"), ("David Sze", "Partner"), ("Sarah Guo", "Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B"], "sectors": ["Enterprise Software", "AI/ML", "Consumer", "Cybersecurity"], "geo": ["USA", "Global"]},
    {"inst": "Khosla Ventures", "partners": [("Vinod Khosla", "Founder"), ("Samir Kaul", "Partner"), ("David Weiden", "Partner")], "cheque": (1000000, 50000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["CleanTech", "AI/ML", "BioTech", "DeepTech", "Sustainability"], "geo": ["USA", "Global"]},
    {"inst": "NEA (New Enterprise Associates)", "partners": [("Scott Sandell", "Chairman"), ("Liza Landsman", "General Partner"), ("Forest Baskett", "General Partner")], "cheque": (5000000, 100000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise Software", "HealthTech", "Fintech", "AI/ML"], "geo": ["USA", "Global"]},
    {"inst": "Balderton Capital", "partners": [("Suranga Chandratillake", "General Partner"), ("James Wise", "Partner"), ("Colin Hanna", "Partner")], "cheque": (1000000, 30000000), "stages": ["Series A", "Series B"], "sectors": ["Enterprise Software", "Fintech", "Consumer", "AI/ML"], "geo": ["UK", "Europe"]},
    {"inst": "Index Ventures", "partners": [("Danny Rimer", "Partner"), ("Martin Mignot", "Partner"), ("Shardul Shah", "Partner")], "cheque": (2000000, 50000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["SaaS", "Fintech", "Gaming", "Consumer"], "geo": ["UK", "USA", "Europe"]},
    {"inst": "Coatue Management", "partners": [("Philippe Laffont", "Founder"), ("Matt Mazzeo", "General Partner"), ("Caryn Marooney", "General Partner")], "cheque": (10000000, 200000000), "stages": ["Series B", "Growth", "Late Stage"], "sectors": ["AI/ML", "Consumer", "Enterprise Software", "Fintech"], "geo": ["USA", "Global"]},
    {"inst": "B Capital Group", "partners": [("Eduardo Saverin", "Co-founder"), ("Raj Ganguly", "Co-founder"), ("Kabir Narang", "General Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise Software", "Fintech", "HealthTech", "Logistics"], "geo": ["USA", "India", "Southeast Asia"]},
    {"inst": "SAIF Partners (Elevation)", "partners": [("Ravi Adusumalli", "Managing Partner"), ("Deepak Gaur", "Partner")], "cheque": (1000000, 20000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "E-commerce", "Fintech", "SaaS"], "geo": ["India", "China"]},
    {"inst": "Iron Pillar", "partners": [("Anand Prasanna", "Managing Partner"), ("Sameer Nath", "Managing Partner")], "cheque": (5000000, 30000000), "stages": ["Series B", "Growth"], "sectors": ["SaaS", "Enterprise Software", "Fintech", "Consumer"], "geo": ["India"]},
    {"inst": "Omnivore Partners", "partners": [("Mark Kahn", "Managing Partner"), ("Jinesh Shah", "Managing Partner")], "cheque": (200000, 5000000), "stages": ["Seed", "Series A"], "sectors": ["AgriTech", "FoodTech", "Climate Tech", "Sustainability"], "geo": ["India"]},
    {"inst": "Fireside Ventures", "partners": [("Kanwaljit Singh", "Founder"), ("Vinay Singh", "Managing Partner"), ("VS Kannan Sitaram", "Partner")], "cheque": (200000, 10000000), "stages": ["Seed", "Series A"], "sectors": ["D2C Brands", "Consumer", "FoodTech", "E-commerce"], "geo": ["India"]},
    {"inst": "3one4 Capital", "partners": [("Pranav Pai", "Founding Partner"), ("Siddarth Pai", "Founding Partner"), ("Nruthya Madappa", "Partner")], "cheque": (200000, 10000000), "stages": ["Seed", "Series A"], "sectors": ["SaaS", "DeepTech", "Fintech", "Consumer"], "geo": ["India"]},
    {"inst": "WaterBridge Ventures", "partners": [("Manish Kheterpal", "Co-founder"), ("Rajiv Srivatsa", "Partner")], "cheque": (100000, 3000000), "stages": ["Pre-seed", "Seed"], "sectors": ["SaaS", "Consumer", "Fintech", "E-commerce"], "geo": ["India"]},
    {"inst": "Antler India", "partners": [("Nitin Sharma", "Partner"), ("Rajiv Srivatsa", "Partner")], "cheque": (100000, 1000000), "stages": ["Pre-seed", "Seed"], "sectors": ["SaaS", "AI/ML", "Consumer", "Fintech"], "geo": ["India", "Southeast Asia", "Global"]},
    {"inst": "Together Fund", "partners": [("Girish Mathrubootham", "Co-founder"), ("Manav Garg", "Co-founder")], "cheque": (100000, 2000000), "stages": ["Pre-seed", "Seed"], "sectors": ["SaaS", "Enterprise Software", "AI/ML"], "geo": ["India"]},
    {"inst": "Arkam Ventures", "partners": [("Rahul Chandra", "Co-founder"), ("Bala Srinivasa", "Co-founder")], "cheque": (200000, 5000000), "stages": ["Seed", "Series A"], "sectors": ["Fintech", "SaaS", "HealthTech", "Enterprise Software"], "geo": ["India"]},
    {"inst": "Surge (Peak XV)", "partners": [("Rajan Anandan", "Managing Director")], "cheque": (1000000, 3000000), "stages": ["Seed"], "sectors": ["Consumer", "SaaS", "Fintech", "AI/ML"], "geo": ["India", "Southeast Asia"]},
    {"inst": "Orios Venture Partners", "partners": [("Rehan Yar Khan", "Managing Partner"), ("Anup Jain", "Managing Partner")], "cheque": (100000, 5000000), "stages": ["Seed", "Series A"], "sectors": ["Consumer", "D2C Brands", "E-commerce", "Fintech"], "geo": ["India"]},
    {"inst": "InfoEdge Ventures", "partners": [("Sanjeev Bikhchandani", "Founder"), ("Kitty Agarwal", "Partner")], "cheque": (500000, 20000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "E-commerce", "SaaS", "EdTech"], "geo": ["India"]},
    {"inst": "Tanglin Venture Partners", "partners": [("Tilak Doddapaneni", "Managing Director"), ("Gaurav Jain", "Partner")], "cheque": (500000, 10000000), "stages": ["Series A", "Series B"], "sectors": ["SaaS", "Enterprise Software", "Fintech", "AI/ML"], "geo": ["India", "Southeast Asia"]},
    {"inst": "100X.VC", "partners": [("Sanjay Mehta", "Founder"), ("Shashank Randev", "Partner")], "cheque": (25000, 500000), "stages": ["Pre-seed", "Seed"], "sectors": ["AI/ML", "SaaS", "Consumer", "HealthTech", "DeepTech"], "geo": ["India"]},
    {"inst": "Speciale Invest", "partners": [("Vishesh Rajaram", "Managing Partner"), ("Arjun Rao", "Partner")], "cheque": (100000, 3000000), "stages": ["Pre-seed", "Seed"], "sectors": ["DeepTech", "AI/ML", "Robotics", "SpaceTech", "Climate Tech"], "geo": ["India"]},
    {"inst": "Z47 (Matrix Partners US)", "partners": [("Dana Stalder", "Partner"), ("Josh Hannah", "Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B"], "sectors": ["SaaS", "Consumer", "Fintech", "AI/ML"], "geo": ["USA"]},
    {"inst": "Initialized Capital", "partners": [("Garry Tan", "Co-founder"), ("Alexis Ohanian", "Co-founder")], "cheque": (500000, 5000000), "stages": ["Pre-seed", "Seed"], "sectors": ["Consumer", "SaaS", "AI/ML", "Fintech"], "geo": ["USA"]},
    {"inst": "First Round Capital", "partners": [("Josh Kopelman", "Partner"), ("Hayley Barna", "Partner"), ("Todd Jackson", "Partner")], "cheque": (500000, 10000000), "stages": ["Pre-seed", "Seed", "Series A"], "sectors": ["SaaS", "Consumer", "Enterprise Software", "AI/ML"], "geo": ["USA"]},
    {"inst": "Craft Ventures", "partners": [("David Sacks", "General Partner"), ("Jeff Fluhr", "General Partner"), ("Bryan Rosenblatt", "Partner")], "cheque": (2000000, 30000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["SaaS", "Fintech", "AI/ML", "Web3"], "geo": ["USA"]},
    {"inst": "Redpoint Ventures", "partners": [("Tomasz Tunguz", "Partner"), ("Annie Kadavy", "Partner"), ("Alex Bard", "Partner")], "cheque": (2000000, 30000000), "stages": ["Series A", "Series B"], "sectors": ["SaaS", "Enterprise Software", "AI/ML", "Fintech"], "geo": ["USA"]},
    {"inst": "IVP", "partners": [("Tom Loverro", "General Partner"), ("Jules Maltz", "General Partner"), ("Cack Wilhelm", "General Partner")], "cheque": (10000000, 100000000), "stages": ["Series B", "Growth"], "sectors": ["SaaS", "Consumer", "Enterprise Software", "Fintech"], "geo": ["USA"]},
    {"inst": "Battery Ventures", "partners": [("Neeraj Agrawal", "General Partner"), ("Brandon Gleklen", "General Partner"), ("Dharmesh Thakker", "General Partner")], "cheque": (5000000, 50000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["SaaS", "Enterprise Software", "AI/ML", "Cloud"], "geo": ["USA", "Global"]},
    {"inst": "QED Investors", "partners": [("Nigel Morris", "Co-founder"), ("Frank Rotman", "Co-founder"), ("Mike Packer", "Partner")], "cheque": (2000000, 30000000), "stages": ["Series A", "Series B"], "sectors": ["Fintech", "InsurTech", "Lending", "Payments"], "geo": ["USA", "India", "Global"]},
    {"inst": "Canaan Partners", "partners": [("Maha Ibrahim", "General Partner"), ("Joydeep Bhattacharyya", "General Partner")], "cheque": (5000000, 30000000), "stages": ["Series A", "Series B"], "sectors": ["SaaS", "Fintech", "HealthTech", "Enterprise Software"], "geo": ["USA", "India"]},
    {"inst": "Lightrock India", "partners": [("Siddharth Talwar", "Managing Partner"), ("Aditya Systla", "Principal")], "cheque": (5000000, 30000000), "stages": ["Series B", "Growth"], "sectors": ["HealthTech", "EdTech", "CleanTech", "Consumer"], "geo": ["India"]},
    {"inst": "Jungle Ventures", "partners": [("Amit Anand", "Founding Partner"), ("Anurag Srivastava", "Partner"), ("David Gowdey", "Partner")], "cheque": (500000, 20000000), "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "SaaS", "Fintech", "E-commerce"], "geo": ["India", "Southeast Asia"]},
    {"inst": "Falcon Edge Capital", "partners": [("Navroz Udwadia", "Co-founder"), ("Rick Gerson", "Co-founder")], "cheque": (10000000, 100000000), "stages": ["Series B", "Growth"], "sectors": ["Consumer", "E-commerce", "Fintech", "SaaS"], "geo": ["India", "USA", "Global"]},
    {"inst": "Multiples Alternate Asset Management", "partners": [("Renuka Ramnath", "Founder & CEO"), ("Avinash Rao", "Partner")], "cheque": (10000000, 100000000), "stages": ["Growth", "Late Stage"], "sectors": ["Consumer", "HealthTech", "Fintech", "Enterprise Software"], "geo": ["India"]},
    {"inst": "Temasek Holdings", "partners": [("Rohit Sipahimalani", "CIO"), ("Ravi Lambah", "Head India")], "cheque": (50000000, 500000000), "stages": ["Growth", "Late Stage"], "sectors": ["Consumer", "Fintech", "HealthTech", "Infrastructure"], "geo": ["India", "Singapore", "Global"]},
    {"inst": "Eight Roads Ventures", "partners": [("Raj Dugar", "Managing Partner India"), ("Avinash Bajaj", "Senior Partner")], "cheque": (5000000, 30000000), "stages": ["Series A", "Series B", "Growth"], "sectors": ["SaaS", "HealthTech", "Consumer", "Fintech"], "geo": ["India", "China", "Global"]},
]

ANGEL_INVESTORS = [
    ("Kunal Shah", "CRED", "Founder & CEO"),
    ("Ritesh Agarwal", "OYO Rooms", "Founder & CEO"),
    ("Sachin Bansal", "Navi Technologies", "Co-founder"),
    ("Binny Bansal", "Flipkart (ex)", "Co-founder"),
    ("Vijay Shekhar Sharma", "Paytm", "Founder & CEO"),
    ("Deepinder Goyal", "Zomato", "Founder & CEO"),
    ("Bhavish Aggarwal", "Ola", "Co-founder & CEO"),
    ("Girish Mathrubootham", "Freshworks", "Founder & CEO"),
    ("Nithin Kamath", "Zerodha", "Co-founder & CEO"),
    ("Nikhil Kamath", "Zerodha", "Co-founder"),
    ("Sanjeev Bikhchandani", "InfoEdge", "Founder"),
    ("Ashish Hemrajani", "BookMyShow", "Founder & CEO"),
    ("Naveen Tewari", "InMobi", "Founder & CEO"),
    ("Sriharsha Majety", "Swiggy", "Co-founder & CEO"),
    ("Harsh Jain", "Dream11", "Co-founder & CEO"),
    ("Nandan Nilekani", "Infosys", "Co-founder"),
    ("Rajan Anandan", "Peak XV Partners", "MD / Angel"),
    ("Anupam Mittal", "Shaadi.com / Shark Tank India", "Founder"),
    ("Aman Gupta", "boAt", "Co-founder"),
    ("Ashneer Grover", "BharatPe (ex)", "Co-founder"),
    ("Peyush Bansal", "Lenskart", "Founder & CEO"),
    ("Namita Thapar", "Emcure Pharma", "Executive Director"),
    ("Ghazal Alagh", "Mamaearth", "Co-founder"),
    ("Vineeta Singh", "SUGAR Cosmetics", "Co-founder & CEO"),
    ("Falguni Nayar", "Nykaa", "Founder & CEO"),
    ("Varun Alagh", "Mamaearth", "Co-founder & CEO"),
    ("Sahil Barua", "Delhivery", "Co-founder & CEO"),
    ("Sujeet Kumar", "Udaan", "Co-founder"),
    ("Kalyan Krishnamurthy", "Flipkart", "CEO"),
    ("Rahul Yadav", "Housing.com (ex)", "Founder"),
    ("Mukesh Bansal", "Myntra (ex) / CureFit", "Founder"),
    ("Ankit Bhati", "Ola", "Co-founder & CTO"),
    ("Saurabh Mukherjea", "Marcellus Investment", "Founder"),
    ("Varun Dua", "Acko Insurance", "Founder & CEO"),
    ("Harshil Mathur", "Razorpay", "Co-founder & CEO"),
    ("Shashank Kumar", "Razorpay", "Co-founder & CTO"),
    ("Nitin Gupta", "Uni Cards", "Founder"),
    ("Lalit Keshre", "Groww", "Co-founder & CEO"),
    ("Harsh Shah", "Fynd", "Co-founder"),
    ("Gaurav Munjal", "Unacademy", "Co-founder & CEO"),
    ("Roman Saini", "Unacademy", "Co-founder"),
    ("Bhavin Turakhia", "Zeta / Directi", "Founder"),
    ("Divyank Turakhia", "Media.net", "Founder"),
    ("Raghunandan G", "TaxiForSure (ex)", "Co-founder"),
    ("Aprameya Radhakrishna", "Koo", "Co-founder"),
    ("Tarun Mehta", "Ather Energy", "Co-founder & CEO"),
    ("Prashant Tandon", "1mg", "Co-founder & CEO"),
    ("Vaibhav Gupta", "1mg", "Co-founder"),
    ("Amit Jain", "CarDekho", "Co-founder & CEO"),
    ("Gokul Rajaram", "DoorDash / Advisor", "Angel Investor"),
    ("Elad Gil", "Color Health", "Angel / Advisor"),
    ("Naval Ravikant", "AngelList", "Co-founder"),
    ("Jason Calacanis", "LAUNCH / ThisWeekIn", "Angel Investor"),
    ("Balaji Srinivasan", "Network State", "Angel Investor"),
    ("Alexis Ohanian", "Reddit / 776", "Co-founder"),
    ("Mark Cuban", "Dallas Mavericks", "Shark Tank Judge"),
    ("Ashton Kutcher", "A-Grade Investments", "Actor / Investor"),
    ("Jared Leto", "Thirty Seconds to Mars / Investor", "Angel Investor"),
    ("Chamath Palihapitiya", "Social Capital", "Founder & CEO"),
    ("Tim Draper", "Draper Associates", "Founder"),
    ("Ron Conway", "SV Angel", "Founder"),
    ("Kevin Rose", "True Ventures", "Partner"),
    ("Esther Dyson", "Way to Wellville", "Angel Investor"),
    ("Ayah Bdeir", "littleBits", "Founder / Angel"),
    ("Arlan Hamilton", "Backstage Capital", "Founder"),
    ("Li Jin", "Atelier Ventures", "Founder"),
    ("Sahil Lavingia", "Gumroad", "Founder & CEO"),
    ("Ankur Nagpal", "Teachable (ex)", "Founder"),
    ("Sridhar Vembu", "Zoho", "Founder & CEO"),
    ("Krish Subramanian", "Chargebee", "Co-founder & CEO"),
    ("Prasanna Sankar", "Rippling / Shack15", "Co-founder"),
    ("Amit Singhal", "Google (ex)", "SVP Search / Angel"),
    ("Ruchi Sanghvi", "Facebook (ex) / Dropbox", "Angel Investor"),
    ("Neeraj Arora", "WhatsApp (ex)", "Angel Investor"),
    ("Shailesh Rao", "Google (ex)", "Angel Investor"),
    ("Sameer Nigam", "PhonePe", "Founder & CEO"),
    ("Rahul Chari", "PhonePe", "Co-founder & CTO"),
    ("Jitendra Gupta", "Jupiter Money", "Founder & CEO"),
    ("Lizzie Chapman", "ZestMoney", "Co-founder"),
    ("Vivekananda Hallekere", "Bounce", "Co-founder & CEO"),
    ("Ambareesh Murty", "Pepperfry (late)", "Co-founder"),
    ("Vidit Aatrey", "Meesho", "Co-founder & CEO"),
    ("Sanjeev Kumar", "Meesho", "Co-founder & CTO"),
    ("Albinder Dhindsa", "Blinkit", "Co-founder & CEO"),
    ("Aadit Palicha", "Zepto", "Co-founder & CEO"),
    ("Kaivalya Vohra", "Zepto", "Co-founder & CTO"),
    ("Ankush Sachdeva", "ShareChat", "Co-founder & CEO"),
    ("Bhanu Pratap Singh", "ShareChat", "Co-founder & CTO"),
    ("Revant Bhate", "Mosaic Wellness", "Co-founder"),
    ("Vineeta Dixit", "Mindtickle (ex)", "Angel Investor"),
]

FAMILY_OFFICES = [
    ("Premji Invest", "Azim Premji", "Founder", ["HealthTech", "EdTech", "Consumer", "Fintech"]),
    ("Catamaran Ventures", "N.R. Narayana Murthy", "Founder", ["SaaS", "Enterprise Software", "Consumer"]),
    ("Manyavar Family Office", "Ravi Modi", "Promoter", ["D2C Brands", "Consumer", "RetailTech"]),
    ("RNT Associates", "Ratan Tata", "Chairman", ["Mobility", "HealthTech", "Consumer", "EV/Electric Vehicles"]),
    ("Wipro Family Office", "Rishad Premji", "Chairman", ["DeepTech", "AI/ML", "Enterprise Software"]),
    ("Godrej Family Office", "Nisaba Godrej", "Chairperson", ["Consumer", "D2C Brands", "Climate Tech"]),
    ("Murugappa Family Office", "MM Murugappan", "Chairman", ["AgriTech", "Manufacturing", "CleanTech"]),
    ("Burman Family Office", "Mohit Burman", "Director", ["Consumer", "HealthTech", "FoodTech"]),
    ("TVS Capital Funds", "Gopal Srinivasan", "Chairman", ["Mobility", "Logistics", "Consumer"]),
    ("Aarin Capital", "T.V. Mohandas Pai", "Chairman", ["EdTech", "SaaS", "HealthTech", "AI/ML"]),
]

CVC_FIRMS = [
    ("Google Ventures (GV)", ["Tom Hulme", "Blake Byers"], ["AI/ML", "Enterprise Software", "HealthTech", "Consumer"]),
    ("Salesforce Ventures", ["John Somorjai", "Alex Kayyal"], ["SaaS", "Enterprise Software", "AI/ML", "Cloud"]),
    ("Intel Capital", ["Sunil Kurkure", "Mark Rostick"], ["DeepTech", "AI/ML", "IoT", "Cybersecurity"]),
    ("Qualcomm Ventures", ["Quinn Li", "Varsha Tagare"], ["IoT", "AI/ML", "5G", "Robotics"]),
    ("Microsoft Ventures (M12)", ["Nagraj Kashyap", "Michelle Gonzalez"], ["Enterprise Software", "AI/ML", "Cloud", "Cybersecurity"]),
    ("Samsung Ventures", ["Young Sohn", "David Eun"], ["IoT", "AI/ML", "HealthTech", "AR/VR"]),
    ("Amazon Alexa Fund", ["Paul Bernard", "Toni Reid"], ["IoT", "AI/ML", "Consumer", "Wearables"]),
    ("Nvidia GPU Ventures", ["Jeff Herbst", "Shanker Trivedi"], ["AI/ML", "DeepTech", "Robotics", "Gaming"]),
    ("Reliance Ventures", ["Akash Ambani", "Anshuman Thakur"], ["Consumer", "Fintech", "E-commerce", "MediaTech"]),
    ("Tata Digital", ["Pratik Pal", "Mukesh Bansal"], ["Consumer", "HealthTech", "E-commerce", "Fintech"]),
    ("Mahindra Partners", ["Zhooben Bhiwandiwala", "Anish Shah"], ["Mobility", "AgriTech", "CleanTech", "Logistics"]),
    ("Infosys Innovation Fund", ["Mohit Joshi", "Ravi Kumar"], ["SaaS", "AI/ML", "Enterprise Software", "Cloud"]),
]

ACCELERATOR_PROGRAMS = [
    ("Y Combinator", "Garry Tan", "CEO", "USA", "https://ycombinator.com", ["SaaS", "AI/ML", "Consumer", "Fintech"]),
    ("Techstars", "Maëlle Gavet", "CEO", "USA", "https://techstars.com", ["SaaS", "AI/ML", "HealthTech", "Sustainability"]),
    ("Alchemist Accelerator", "Ravi Belani", "Managing Director", "USA", "https://alchemistaccelerator.com", ["Enterprise Software", "SaaS", "DeepTech"]),
    ("500 Global", "Christine Tsai", "CEO", "USA", "https://500.co", ["Consumer", "Fintech", "SaaS"]),
    ("Plug and Play", "Saeed Amidi", "CEO", "USA", "https://plugandplaytechcenter.com", ["Fintech", "HealthTech", "Mobility"]),
    ("NASSCOM 10000 Startups", "Debjani Ghosh", "President", "India", "https://nasscom.in", ["SaaS", "AI/ML", "DeepTech"]),
    ("T-Hub", "Srinivas Kollipara", "CEO", "India", "https://t-hub.co", ["HealthTech", "AI/ML", "Enterprise Software"]),
    ("Startup India", "DPIIT", "Government", "India", "https://startupindia.gov.in", ["All Sectors"]),
]


def _rand_pattern(sectors):
    chosen = random.sample(sectors, min(len(sectors), random.randint(2, 4)))
    vals = [random.randint(10, 60) for _ in chosen]
    total = sum(vals)
    return {s: round(v / total * 100) for s, v in zip(chosen, vals)}


def _rand_deals():
    deals = []
    for _ in range(random.randint(1, 3)):
        c = random.choice(COMPANIES_POOL)
        s = random.choice(SECTORS[:20])
        deals.append({"company": c, "sector": s, "link": f"https://example.com/{c.lower().replace(' ', '-')}"})
    return deals


def _rand_date(days_back=365):
    d = datetime.now(timezone.utc) - timedelta(days=random.randint(0, days_back))
    return d.strftime("%Y-%m-%d")


def generate_investors():
    investors = []
    
    # Generate from VC firms
    for firm in VC_FIRMS:
        for name, title in firm["partners"]:
            sec = firm["sectors"]
            sec2 = random.sample([s for s in SECTORS if s not in sec], min(3, len(SECTORS) - len(sec)))
            geo = firm["geo"]
            inv = {
                "id": str(uuid.uuid4()),
                "name": name,
                "institution": firm["inst"],
                "title": title,
                "investor_type": "VC",
                "cheque_size_min": firm["cheque"][0],
                "cheque_size_max": firm["cheque"][1],
                "cheque_size_currency": "USD",
                "geographies": geo,
                "invests_in_india": "India" in geo or random.random() < 0.3,
                "primary_sectors": sec[:4],
                "secondary_sectors": sec2,
                "stage": firm["stages"],
                "typical_shareholding": f"{random.choice([5,8,10,12,15,20])}-{random.choice([15,20,25,30])}%",
                "recent_deals": _rand_deals(),
                "email": f"{name.split()[0].lower()}@{firm['inst'].split('(')[0].strip().lower().replace(' ', '')}.com",
                "website": f"https://{firm['inst'].split('(')[0].strip().lower().replace(' ', '')}.com",
                "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
                "twitter_handle": f"@{name.split()[0].lower()}{name.split()[-1].lower()[:3]}",
                "source": random.choice(SOURCES),
                "last_verified_date": _rand_date(90),
                "investment_patterns": _rand_pattern(sec + sec2),
                "priority_tag": random.choice(["High", "High", "Medium", "Medium", "Low"]),
                "notes": "",
                "contacted": False,
                "last_contact_date": None,
                "contact_status": "Not contacted",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            investors.append(inv)

    # Generate from Angel Investors
    for name, company, title in ANGEL_INVESTORS:
        sec = random.sample(SECTORS[:20], random.randint(3, 5))
        sec2 = random.sample(SECTORS[20:], random.randint(1, 3))
        inv = {
            "id": str(uuid.uuid4()),
            "name": name,
            "institution": company,
            "title": f"{title} / Angel Investor",
            "investor_type": "Angel",
            "cheque_size_min": random.choice([10000, 25000, 50000, 100000]),
            "cheque_size_max": random.choice([200000, 500000, 1000000, 2000000, 5000000]),
            "cheque_size_currency": "USD",
            "geographies": random.sample(["India", "USA", "Singapore", "Global"], random.randint(1, 3)),
            "invests_in_india": True,
            "primary_sectors": sec[:4],
            "secondary_sectors": sec2,
            "stage": random.sample(["Pre-seed", "Seed", "Pre-Series A", "Series A"], random.randint(1, 3)),
            "typical_shareholding": f"{random.choice([1,2,3,5])}-{random.choice([5,8,10])}%",
            "recent_deals": _rand_deals(),
            "email": f"{name.split()[0].lower()}.{name.split()[-1].lower()}@gmail.com",
            "website": f"https://{company.lower().replace(' ', '').replace('(ex)', '').replace('/', '')}.com",
            "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
            "twitter_handle": f"@{name.split()[0].lower()}{random.randint(1, 99)}",
            "source": random.choice(SOURCES),
            "last_verified_date": _rand_date(180),
            "investment_patterns": _rand_pattern(sec),
            "priority_tag": random.choice(["High", "Medium", "Medium", "Low"]),
            "notes": "",
            "contacted": False,
            "last_contact_date": None,
            "contact_status": "Not contacted",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        investors.append(inv)

    # Generate from Family Offices
    for inst, name, title, sectors in FAMILY_OFFICES:
        sec2 = random.sample([s for s in SECTORS if s not in sectors], 2)
        inv = {
            "id": str(uuid.uuid4()),
            "name": name,
            "institution": inst,
            "title": f"{title} / Family Office",
            "investor_type": "Family Office",
            "cheque_size_min": random.choice([1000000, 2000000, 5000000]),
            "cheque_size_max": random.choice([10000000, 20000000, 50000000, 100000000]),
            "cheque_size_currency": "USD",
            "geographies": ["India"],
            "invests_in_india": True,
            "primary_sectors": sectors[:4],
            "secondary_sectors": sec2,
            "stage": random.sample(["Series A", "Series B", "Growth", "Late Stage"], random.randint(2, 3)),
            "typical_shareholding": f"{random.choice([5,10,15])}-{random.choice([20,25,30])}%",
            "recent_deals": _rand_deals(),
            "email": f"invest@{inst.lower().replace(' ', '').replace('(', '').replace(')', '')}.com",
            "website": f"https://{inst.lower().replace(' ', '').replace('(', '').replace(')', '')}.com",
            "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
            "twitter_handle": "",
            "source": "Fund Website",
            "last_verified_date": _rand_date(120),
            "investment_patterns": _rand_pattern(sectors),
            "priority_tag": random.choice(["High", "Medium"]),
            "notes": "",
            "contacted": False,
            "last_contact_date": None,
            "contact_status": "Not contacted",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        investors.append(inv)

    # Generate from CVCs
    for inst, people, sectors in CVC_FIRMS:
        for pname in people:
            sec2 = random.sample([s for s in SECTORS if s not in sectors], 2)
            inv = {
                "id": str(uuid.uuid4()),
                "name": pname,
                "institution": inst,
                "title": "Investment Director",
                "investor_type": "CVC",
                "cheque_size_min": random.choice([1000000, 2000000, 5000000]),
                "cheque_size_max": random.choice([10000000, 20000000, 50000000]),
                "cheque_size_currency": "USD",
                "geographies": random.sample(["USA", "India", "Global", "Europe", "Southeast Asia"], 3),
                "invests_in_india": random.random() < 0.6,
                "primary_sectors": sectors[:4],
                "secondary_sectors": sec2,
                "stage": random.sample(["Seed", "Series A", "Series B", "Growth"], random.randint(2, 3)),
                "typical_shareholding": f"{random.choice([3,5,8])}-{random.choice([10,15,20])}%",
                "recent_deals": _rand_deals(),
                "email": f"{pname.split()[0].lower()}@{inst.split('(')[0].strip().lower().replace(' ', '')}.com",
                "website": f"https://{inst.split('(')[0].strip().lower().replace(' ', '')}.com",
                "linkedin_url": f"https://linkedin.com/in/{pname.lower().replace(' ', '-')}",
                "twitter_handle": "",
                "source": random.choice(SOURCES),
                "last_verified_date": _rand_date(90),
                "investment_patterns": _rand_pattern(sectors),
                "priority_tag": random.choice(["High", "Medium", "Low"]),
                "notes": "",
                "contacted": False,
                "last_contact_date": None,
                "contact_status": "Not contacted",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            investors.append(inv)

    # Generate additional investors to reach 1500+
    extra_funds = [
        "Vertex Ventures", "Innoven Capital", "IndiGo Ventures", "Atomico",
        "Lux Capital", "Spark Capital", "Union Square Ventures", "Accel Europe",
        "Sequoia Heritage", "Draper Fisher Jurvetson", "Menlo Ventures",
        "Mayfield Fund", "Scale Venture Partners", "SignalFire", "Greenoaks Capital",
        "Addition", "D1 Capital", "Lone Pine Capital", "Dragoneer Investment Group",
        "Altimeter Capital", "Baillie Gifford", "T. Rowe Price", "Fidelity Investments",
        "Wellington Management", "Capital Group", "SWC Global", "TNB Aura",
        "Vertex Southeast Asia", "East Ventures", "Golden Gate Ventures",
        "Monk's Hill Ventures", "Wavemaker Partners", "Seedstars", "Flat6Labs",
        "Plug and Play India", "Zone Startups India", "iStart Rajasthan",
        "Kerala Startup Mission", "StartupTN", "BITS Pilani TBI", "IIT Madras Incubation",
        "IIM Ahmedabad CIIE", "ISB DLabs", "NSRCEL IIM Bangalore",
        "IIT Delhi Foundation", "IIT Bombay SINE", "IIIT Hyderabad THub",
        "Venture Catalysts", "LetsVenture", "AngelList India", "Mumbai Angels",
        "Chennai Angels", "Hyderabad Angels", "Calcutta Angels", "Delhi NCR Angels",
        "Pune Angels", "Lead Angels", "Ah! Ventures", "RAIN (Rajasthan Angels)",
        "SucSEED Indovation Fund", "iAngels", "OurCrowd", "Seedcamp",
        "EF (Entrepreneur First)", "Techstars London", "Startupbootcamp",
        "SOSV", "HAX", "Chinaccelerator", "MassChallenge", "Dreamit Ventures",
        "Capital Factory", "Starta Ventures", "Brinc", "Zeroth.ai",
        "SparkLabs", "AppWorks", "GDP Venture", "Openspace Ventures",
        "AC Ventures", "Horizon Ventures", "Gobi Partners", "Cathay Innovation",
        "Partech Partners", "Serena Capital", "360 Capital", "btov Partners",
        "Cherry Ventures", "Point Nine Capital", "La Famiglia", "Project A Ventures",
        "HV Capital", "Global Founders Capital", "Picus Capital", "Earlybird Venture Capital",
        "Speedinvest", "Molten Ventures", "Notion Capital", "Dawn Capital",
    ]
    
    extra_names = [
        "Aditya Sharma", "Priya Patel", "Rohan Gupta", "Sneha Reddy", "Vikram Mehta",
        "Ananya Das", "Karan Singh", "Neha Agarwal", "Rajesh Kumar", "Pooja Jain",
        "Suresh Venkatesh", "Meera Nair", "Arjun Iyer", "Kavitha Rao", "Dhruv Malhotra",
        "Swati Chopra", "Manish Tiwari", "Ritu Sharma", "Arun Krishnan", "Deepa Menon",
        "Sanjay Kapoor", "Lavanya Srinivasan", "Amit Saxena", "Padma Lakshmi", "Yash Patel",
        "Divya Mishra", "Raj Gopal", "Shreya Bose", "Nikhil Agnihotri", "Trisha Hegde",
        "Ramesh Sundaram", "Isha Verma", "Prakash Rao", "Nandini Chatterjee", "Samir Khan",
        "Usha Devi", "Aakash Bajpai", "Richa Pandey", "Kunal Desai", "Sonam Thakur",
        "James Chen", "Sarah Williams", "Michael Brown", "Emma Davis", "Robert Wilson",
        "Jennifer Lee", "David Kim", "Lisa Anderson", "Thomas Martin", "Maria Garcia",
        "Daniel Taylor", "Laura Johnson", "Christopher Moore", "Amanda White", "Matthew Harris",
        "Jessica Thompson", "Andrew Clark", "Stephanie Lewis", "Brian Robinson", "Nicole Walker",
        "Kevin Hall", "Rachel Allen", "Mark Young", "Michelle King", "Steven Wright",
        "Olivia Green", "Ryan Baker", "Rebecca Hill", "Patrick Adams", "Samantha Nelson",
        "Takeshi Yamamoto", "Yuki Tanaka", "Wei Zhang", "Ming Li", "Jin Park",
        "Soo-Yun Kim", "Pierre Dubois", "Marie Laurent", "Hans Mueller", "Anna Schmidt",
        "Carlos Rodriguez", "Isabella Rossi", "Omar Hassan", "Fatima Al-Rashid", "Ahmed Mahmoud",
        "Zara Okonkwo", "Chidinma Eze", "Kwame Asante", "Amara Diallo", "Thabo Molefe",
    ]

    titles = ["Partner", "Principal", "Vice President", "Managing Director", "Investment Director", "Associate Partner", "Senior Associate", "General Partner", "Venture Partner", "Director"]

    used_combos = set()
    target = max(0, 1500 - len(investors))
    
    for i in range(target):
        name = random.choice(extra_names)
        inst = random.choice(extra_funds)
        combo = f"{name}|{inst}"
        if combo in used_combos:
            name = f"{name} {chr(65 + (i % 26))}"
            combo = f"{name}|{inst}"
        used_combos.add(combo)
        
        itype = random.choice(["VC", "VC", "VC", "Angel", "Angel", "Family Office", "Accelerator", "CVC"])
        sec = random.sample(SECTORS, random.randint(3, 5))
        sec2 = random.sample([s for s in SECTORS if s not in sec], random.randint(1, 3))
        geo = random.sample(GEOGRAPHIES, random.randint(1, 4))
        
        if itype == "Angel":
            cmin = random.choice([10000, 25000, 50000])
            cmax = random.choice([200000, 500000, 1000000])
        elif itype == "VC":
            cmin = random.choice([100000, 250000, 500000, 1000000])
            cmax = random.choice([5000000, 10000000, 25000000, 50000000])
        else:
            cmin = random.choice([500000, 1000000, 5000000])
            cmax = random.choice([10000000, 25000000, 50000000])
        
        inv = {
            "id": str(uuid.uuid4()),
            "name": name,
            "institution": inst,
            "title": random.choice(titles),
            "investor_type": itype,
            "cheque_size_min": cmin,
            "cheque_size_max": cmax,
            "cheque_size_currency": "USD",
            "geographies": geo,
            "invests_in_india": "India" in geo or random.random() < 0.4,
            "primary_sectors": sec[:4],
            "secondary_sectors": sec2,
            "stage": random.sample(STAGES[:6], random.randint(1, 3)),
            "typical_shareholding": f"{random.choice([2,5,8,10])}-{random.choice([10,15,20,25])}%",
            "recent_deals": _rand_deals(),
            "email": f"{name.split()[0].lower()}.{name.split()[-1].lower()}@{inst.lower().replace(' ', '').split('(')[0][:12]}.com",
            "website": f"https://{inst.lower().replace(' ', '').split('(')[0][:15]}.com",
            "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
            "twitter_handle": f"@{name.split()[0].lower()}{random.randint(1,999)}",
            "source": random.choice(SOURCES),
            "last_verified_date": _rand_date(365),
            "investment_patterns": _rand_pattern(sec),
            "priority_tag": random.choice(["High", "Medium", "Medium", "Low", "Low"]),
            "notes": "",
            "contacted": False,
            "last_contact_date": None,
            "contact_status": "Not contacted",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        investors.append(inv)

    return investors


def generate_news_articles():
    articles = [
        {"id": str(uuid.uuid4()), "title": "Zepto raises $665M Series F at $3.6B valuation", "source": "TechCrunch", "url": "https://techcrunch.com/zepto-series-f", "thumbnail": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=300", "summary": "Quick commerce startup Zepto has closed a massive $665 million Series F round, valuing the company at $3.6 billion. The round was led by StepStone Group with participation from existing investors. This signals continued investor confidence in India's quick commerce space despite profitability concerns.", "category": "Funding", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "PhonePe launches stock broking services", "source": "Inc42", "url": "https://inc42.com/phonepe-broking", "thumbnail": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=300", "summary": "PhonePe has officially launched its stock broking vertical, entering the competitive fintech space dominated by Zerodha and Groww. The Walmart-backed company aims to leverage its 500 million user base for distribution. Analysts see this as a natural extension of PhonePe's financial services ecosystem.", "category": "Product Launch", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "AI startup Krutrim raises $50M at unicorn valuation", "source": "YourStory", "url": "https://yourstory.com/krutrim-unicorn", "thumbnail": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=300", "summary": "Bhavish Aggarwal's AI venture Krutrim has raised $50 million in its first institutional round, achieving unicorn status within months of launch. The funding validates India's growing AI ecosystem. Krutrim plans to build foundational AI models optimized for Indian languages and cultural context.", "category": "Funding", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Y Combinator Winter 2025 batch includes 30 Indian startups", "source": "Entrackr", "url": "https://entrackr.com/yc-w25-india", "thumbnail": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=300", "summary": "Y Combinator's Winter 2025 batch features a record 30 Indian startups, highlighting the growing prominence of Indian founders in global tech. Focus areas include AI, fintech, and climate tech. This represents a significant increase from previous batches and reflects India's startup maturity.", "category": "Accelerator", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Sequoia India rebrands to Peak XV Partners", "source": "VCCircle", "url": "https://vccircle.com/peak-xv-rebrand", "thumbnail": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=300", "summary": "Sequoia Capital's India and Southeast Asia operations have completed their rebrand to Peak XV Partners, marking full operational independence. The firm manages over $9 billion in assets. Peak XV will continue its strategy of backing early to growth-stage companies across the region.", "category": "Industry", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Stripe launches new payment features for Indian startups", "source": "Economic Times", "url": "https://economictimes.com/stripe-india", "thumbnail": "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?w=300", "summary": "Stripe has expanded its India operations with new payment processing features tailored for Indian startups. The platform now supports UPI, net banking, and EMI options natively. This move strengthens Stripe's position against local competitors Razorpay and Cashfree in the growing payments market.", "category": "Product Launch", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "OpenAI partners with Indian government on AI initiatives", "source": "Rest of World", "url": "https://restofworld.org/openai-india", "thumbnail": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=300", "summary": "OpenAI has announced a strategic partnership with India's Ministry of Electronics to advance AI adoption across government services. The collaboration will focus on healthcare, agriculture, and education applications. This marks OpenAI's deepest engagement with a developing nation's government.", "category": "Partnership", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Freshworks acquires AI startup DevRev for $800M", "source": "TechCrunch", "url": "https://techcrunch.com/freshworks-devrev", "thumbnail": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=300", "summary": "Freshworks has completed its largest acquisition, buying AI-native customer support platform DevRev for $800 million. The deal brings advanced AI capabilities to Freshworks' product suite. DevRev's technology will power next-generation AI agents across Freshworks' customer service tools.", "category": "M&A", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Tiger Global reduces India exposure amid global uncertainty", "source": "Crunchbase News", "url": "https://news.crunchbase.com/tiger-global-india", "thumbnail": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=300", "summary": "Tiger Global Management has significantly scaled back its India investment activity, participating in only three deals this quarter compared to twelve last year. The hedge fund is focusing on AI-heavy portfolios in the US. Indian startups are increasingly turning to domestic VCs for funding.", "category": "Analysis", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "India's startup ecosystem hits $5 trillion in combined valuation", "source": "Inc42", "url": "https://inc42.com/india-5t-valuation", "thumbnail": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=300", "summary": "India's startup ecosystem has reached a historic $5 trillion combined valuation milestone, driven by IPOs and late-stage funding rounds. The country now has over 115 unicorns. Government initiatives and digital infrastructure have been key enablers of this unprecedented growth trajectory.", "category": "Analysis", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Razorpay launches AI-powered fraud detection system", "source": "YourStory", "url": "https://yourstory.com/razorpay-ai-fraud", "thumbnail": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=300", "summary": "Razorpay has unveiled an AI-powered fraud detection system that can identify suspicious transactions in real-time with 99.7% accuracy. The system processes over 1 billion data points daily. This launch addresses growing concerns about digital payment fraud in India's expanding fintech ecosystem.", "category": "Product Launch", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Accel India closes $650M fund for early-stage startups", "source": "VCCircle", "url": "https://vccircle.com/accel-fund-8", "thumbnail": "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?w=300", "summary": "Accel India has closed its eighth fund at $650 million, one of the largest early-stage funds focused on India. The fund will target seed to Series A investments across SaaS, consumer, and fintech. Accel remains one of India's most active venture capital firms.", "category": "Funding", "published_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))).isoformat()},
    ]
    return articles


def generate_events():
    now = datetime.now(timezone.utc)
    events = [
        {"id": str(uuid.uuid4()), "name": "TechSparks 2025 by YourStory", "date": (now + timedelta(days=30)).strftime("%Y-%m-%d"), "location": "Bengaluru, India", "type": "Physical", "eligibility": "Open to all startups and investors", "deadline": (now + timedelta(days=20)).strftime("%Y-%m-%d"), "link": "https://yourstory.com/techsparks", "description": "India's largest startup tech conference featuring keynotes, pitch competitions, and investor connects.", "category": "Conference"},
        {"id": str(uuid.uuid4()), "name": "Y Combinator Demo Day S25", "date": (now + timedelta(days=45)).strftime("%Y-%m-%d"), "location": "San Francisco, USA", "type": "Physical + Virtual", "eligibility": "YC S25 batch companies", "deadline": "N/A", "link": "https://ycombinator.com/demoday", "description": "Bi-annual demo day where YC startups present to top investors worldwide.", "category": "Demo Day"},
        {"id": str(uuid.uuid4()), "name": "Techstars India Accelerator 2025", "date": (now + timedelta(days=60)).strftime("%Y-%m-%d"), "location": "Virtual", "type": "Virtual", "eligibility": "Early-stage startups, any sector", "deadline": (now + timedelta(days=15)).strftime("%Y-%m-%d"), "link": "https://techstars.com/accelerators/india", "description": "13-week accelerator program with mentorship, funding, and network access.", "category": "Accelerator"},
        {"id": str(uuid.uuid4()), "name": "Startup India Grand Challenge", "date": (now + timedelta(days=25)).strftime("%Y-%m-%d"), "location": "New Delhi, India", "type": "Physical", "eligibility": "DPIIT-recognized startups", "deadline": (now + timedelta(days=10)).strftime("%Y-%m-%d"), "link": "https://startupindia.gov.in/challenge", "description": "Government-backed hackathon focusing on solutions for smart cities and governance.", "category": "Hackathon"},
        {"id": str(uuid.uuid4()), "name": "NASSCOM Product Conclave 2025", "date": (now + timedelta(days=50)).strftime("%Y-%m-%d"), "location": "Bengaluru, India", "type": "Physical", "eligibility": "Product companies and SaaS startups", "deadline": (now + timedelta(days=35)).strftime("%Y-%m-%d"), "link": "https://nasscom.in/npc", "description": "Premier gathering of India's product ecosystem with tracks on AI, SaaS, and deep tech.", "category": "Conference"},
        {"id": str(uuid.uuid4()), "name": "Alchemist Accelerator Demo Day", "date": (now + timedelta(days=35)).strftime("%Y-%m-%d"), "location": "San Francisco, USA", "type": "Physical + Virtual", "eligibility": "Alchemist batch companies", "deadline": "N/A", "link": "https://alchemistaccelerator.com/demo-day", "description": "Enterprise-focused demo day featuring B2B startups pitching to 500+ investors.", "category": "Demo Day"},
        {"id": str(uuid.uuid4()), "name": "IIT Bombay E-Summit 2025", "date": (now + timedelta(days=40)).strftime("%Y-%m-%d"), "location": "Mumbai, India", "type": "Physical", "eligibility": "College students and early founders", "deadline": (now + timedelta(days=25)).strftime("%Y-%m-%d"), "link": "https://esummit.in", "description": "Asia's largest student-run entrepreneurship summit with workshops and competitions.", "category": "Conference"},
        {"id": str(uuid.uuid4()), "name": "Web Summit India 2025", "date": (now + timedelta(days=75)).strftime("%Y-%m-%d"), "location": "Bengaluru, India", "type": "Physical", "eligibility": "Open to all", "deadline": (now + timedelta(days=55)).strftime("%Y-%m-%d"), "link": "https://websummit.com/india", "description": "Global tech conference with over 10,000 attendees and 500 investors.", "category": "Conference"},
    ]
    return events


def generate_govt_schemes():
    schemes = [
        {"id": str(uuid.uuid4()), "name": "Startup India Seed Fund Scheme (SISFS)", "tier": "Central", "type": "Grant", "amount": "Up to INR 20 Lakhs (Grants) / INR 50 Lakhs (Debt/Convertible)", "eligibility": "DPIIT-recognized startups, incorporated < 2 years, not received > INR 10L funding", "description": "Financial assistance to startups for proof of concept, prototype development, product trials, market entry, and commercialization.", "apply_link": "https://seedfund.startupindia.gov.in", "deadline": "Rolling basis", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "Atal Innovation Mission (AIM)", "tier": "Central", "type": "Grant", "amount": "Up to INR 10 Crores", "eligibility": "Innovators, startups, and academic institutions", "description": "NITI Aayog initiative promoting innovation and entrepreneurship through Atal Incubation Centres, Tinkering Labs, and challenges.", "apply_link": "https://aim.gov.in", "deadline": "Various cohorts", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "MUDRA Loan Scheme", "tier": "Central", "type": "Equity-free funding", "amount": "Up to INR 10 Lakhs (Tarun category)", "eligibility": "Non-corporate, non-farm small/micro enterprises", "description": "Collateral-free loans for micro-enterprises under three categories: Shishu (up to 50K), Kishore (50K-5L), Tarun (5L-10L).", "apply_link": "https://mudra.org.in", "deadline": "Rolling basis", "category": "Equity-free funding"},
        {"id": str(uuid.uuid4()), "name": "Tax Exemption under Section 80-IAC", "tier": "Central", "type": "Tax Exemptions", "amount": "100% tax exemption for 3 consecutive years", "eligibility": "DPIIT-recognized startups, incorporated after April 2016, turnover < INR 100 Crores", "description": "Eligible startups can claim 100% tax exemption on profits for 3 consecutive years out of 10 years from incorporation.", "apply_link": "https://startupindia.gov.in/tax-exemption", "deadline": "Rolling basis", "category": "Tax Exemptions"},
        {"id": str(uuid.uuid4()), "name": "Fund of Funds for Startups (FFS)", "tier": "Central", "type": "Equity-free funding", "amount": "INR 10,000 Crores corpus", "eligibility": "SEBI-registered AIFs investing in startups", "description": "Government fund that invests through SEBI-registered Alternative Investment Funds to provide equity support to startups.", "apply_link": "https://startupindia.gov.in/ffs", "deadline": "Rolling basis", "category": "Equity-free funding"},
        {"id": str(uuid.uuid4()), "name": "Karnataka Startup Policy", "tier": "State", "type": "Grant", "amount": "Up to INR 50 Lakhs", "eligibility": "Startups registered in Karnataka", "description": "State government support including grants, subsidies on patent filing, and marketing support for Karnataka-based startups.", "apply_link": "https://startup.karnataka.gov.in", "deadline": "Rolling basis", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "Kerala Startup Mission (KSUM)", "tier": "State", "type": "Grant", "amount": "Up to INR 30 Lakhs", "eligibility": "Startups incorporated in Kerala", "description": "Comprehensive startup support including seed funding, incubation, mentorship, and international market access.", "apply_link": "https://startupmission.kerala.gov.in", "deadline": "Rolling basis", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "T-Hub (Telangana)", "tier": "State", "type": "Grant", "amount": "Up to INR 25 Lakhs + infrastructure", "eligibility": "Tech startups in Telangana", "description": "India's largest incubator offering funding, mentorship, corporate connections, and co-working space in Hyderabad.", "apply_link": "https://t-hub.co", "deadline": "Cohort-based", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "Maharashtra State Innovation Society", "tier": "State", "type": "Grant", "amount": "Up to INR 15 Lakhs", "eligibility": "Startups registered in Maharashtra", "description": "Financial and mentoring support for innovative startups through the Maharashtra Startup Yatra and district-level programs.", "apply_link": "https://msins.in", "deadline": "Rolling basis", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "iStart Rajasthan", "tier": "State", "type": "Grant", "amount": "Up to INR 25 Lakhs", "eligibility": "Startups registered in Rajasthan", "description": "State initiative providing sustenance allowance, mentoring, incubation support, and funding for Rajasthan startups.", "apply_link": "https://istart.rajasthan.gov.in", "deadline": "Rolling basis", "category": "Grant"},
        {"id": str(uuid.uuid4()), "name": "StartupTN (Tamil Nadu)", "tier": "State", "type": "Equity-free funding", "amount": "Up to INR 30 Lakhs", "eligibility": "Startups registered in Tamil Nadu", "description": "Tamil Nadu Startup and Innovation Mission providing grants, incubation, and access to government procurement.", "apply_link": "https://startuptn.in", "deadline": "Cohort-based", "category": "Equity-free funding"},
        {"id": str(uuid.uuid4()), "name": "BioTechnology Ignition Grant (BIG)", "tier": "Central", "type": "Grant", "amount": "Up to INR 50 Lakhs", "eligibility": "Biotech startups and innovators", "description": "BIRAC initiative to fund early-stage biotech innovations from proof of concept to early validation.", "apply_link": "https://birac.nic.in/big", "deadline": "Quarterly calls", "category": "Grant"},
    ]
    return schemes


def generate_accelerators():
    accels = [
        {"id": str(uuid.uuid4()), "name": "Y Combinator", "program_lead": "Garry Tan", "location": "San Francisco, USA", "website": "https://ycombinator.com", "focus_sectors": ["SaaS", "AI/ML", "Consumer", "Fintech", "HealthTech"], "investment_amount": "$125K + $375K on MFN SAFE", "equity_taken": "7%", "batch_size": "200+ companies per batch", "application_status": "Open for S25", "portfolio_highlights": ["Stripe", "Airbnb", "DoorDash", "Coinbase", "Instacart", "Razorpay", "Meesho", "Zerodha"], "trust_label": "Verified Global Source", "last_updated": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Techstars", "program_lead": "Maëlle Gavet", "location": "Multiple (Global)", "website": "https://techstars.com", "focus_sectors": ["SaaS", "AI/ML", "HealthTech", "Sustainability", "Fintech"], "investment_amount": "$120K", "equity_taken": "6%", "batch_size": "10-12 companies per program", "application_status": "Various programs open", "portfolio_highlights": ["SendGrid", "ClassPass", "Uber", "DigitalOcean", "Loom", "Chainalysis"], "trust_label": "Verified Global Source", "last_updated": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Alchemist Accelerator", "program_lead": "Ravi Belani", "location": "San Francisco, USA", "website": "https://alchemistaccelerator.com", "focus_sectors": ["Enterprise Software", "SaaS", "DeepTech", "B2B"], "investment_amount": "$40K + mentorship", "equity_taken": "5%", "batch_size": "15-20 companies", "application_status": "Applications open", "portfolio_highlights": ["LaunchDarkly", "Rigetti Computing", "Mashgin", "Mux"], "trust_label": "Verified Global Source", "last_updated": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "500 Global", "program_lead": "Christine Tsai", "location": "San Francisco, USA + Global", "website": "https://500.co", "focus_sectors": ["Consumer", "Fintech", "SaaS", "E-commerce", "HealthTech"], "investment_amount": "$150K", "equity_taken": "6%", "batch_size": "30-40 companies", "application_status": "Rolling applications", "portfolio_highlights": ["Canva", "Grab", "Talkdesk", "Credit Karma", "Udemy"], "trust_label": "Verified Global Source", "last_updated": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Plug and Play Tech Center", "program_lead": "Saeed Amidi", "location": "Sunnyvale, USA + Global", "website": "https://plugandplaytechcenter.com", "focus_sectors": ["Fintech", "HealthTech", "Mobility", "Supply Chain", "InsurTech"], "investment_amount": "$25K-$500K", "equity_taken": "Varies", "batch_size": "100+ per program", "application_status": "Open for multiple verticals", "portfolio_highlights": ["PayPal", "Dropbox", "SoundHound", "LendingClub"], "trust_label": "Verified Global Source", "last_updated": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "NASSCOM 10000 Startups", "program_lead": "Debjani Ghosh", "location": "India (Multiple cities)", "website": "https://nasscom.in", "focus_sectors": ["SaaS", "AI/ML", "DeepTech", "IoT", "Enterprise Software"], "investment_amount": "Incubation + Grants up to INR 20L", "equity_taken": "0%", "batch_size": "500+ annually", "application_status": "Open", "portfolio_highlights": ["Freshworks", "Postman", "Zoho", "BrowserStack"], "trust_label": "Verified India Source", "last_updated": datetime.now(timezone.utc).isoformat()},
    ]
    return accels
