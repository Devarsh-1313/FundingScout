import requests
import sys
from datetime import datetime
import json

class InvestorDBAPITester:
    def __init__(self, base_url="https://capital-compass-22.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    resp_data = response.json() if response.content else {}
                    self.test_results.append({"test": name, "status": "PASSED", "details": f"Status {response.status_code}"})
                except:
                    resp_data = {}
                    self.test_results.append({"test": name, "status": "PASSED", "details": f"Status {response.status_code}"})
                return True, resp_data
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.text[:200]
                    print(f"   Response: {error_detail}")
                    self.test_results.append({"test": name, "status": "FAILED", "details": f"Expected {expected_status}, got {response.status_code}: {error_detail}"})
                except:
                    self.test_results.append({"test": name, "status": "FAILED", "details": f"Expected {expected_status}, got {response.status_code}"})
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({"test": name, "status": "FAILED", "details": f"Exception: {str(e)}"})
            return False, {}

    def test_dashboard_stats(self):
        """Test dashboard stats endpoint"""
        success, response = self.run_test(
            "Dashboard Stats",
            "GET",
            "/stats",
            200
        )
        if success:
            required_fields = ["total_investors", "total_vc", "total_angel", "new_last_24h", "total_news", "total_events"]
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                print(f"   Warning: Missing fields in response: {missing_fields}")
                return False
            
            print(f"   Total Investors: {response.get('total_investors', 0)}")
            print(f"   VCs: {response.get('total_vc', 0)}")
            print(f"   Angels: {response.get('total_angel', 0)}")
            print(f"   New (24h): {response.get('new_last_24h', 0)}")
            return True
        return False

    def test_investor_list(self):
        """Test investor listing with pagination"""
        success, response = self.run_test(
            "Investor List",
            "GET",
            "/investors",
            200,
            params={"page": 1, "limit": 10}
        )
        if success:
            required_fields = ["investors", "total", "page", "limit", "total_pages"]
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                print(f"   Warning: Missing pagination fields: {missing_fields}")
                return False
                
            investors = response.get("investors", [])
            print(f"   Found {len(investors)} investors out of {response.get('total', 0)} total")
            
            # Check if we have the expected ~1500 investors
            total = response.get('total', 0)
            if total < 100:
                print(f"   Warning: Expected ~1500 investors, found only {total}")
                return False
            
            # Check first investor structure
            if investors and len(investors) > 0:
                first_inv = investors[0]
                required_inv_fields = ["name", "institution", "investor_type", "id"]
                missing_inv_fields = [field for field in required_inv_fields if field not in first_inv]
                if missing_inv_fields:
                    print(f"   Warning: Missing investor fields: {missing_inv_fields}")
                    return False
                
                print(f"   Sample investor: {first_inv.get('name', 'N/A')} from {first_inv.get('institution', 'N/A')}")
                return True
            else:
                print("   Warning: No investors returned")
                return False
        return False

    def test_investor_search(self):
        """Test investor search functionality"""
        success, response = self.run_test(
            "Investor Search",
            "GET",
            "/investors",
            200,
            params={"search": "venture", "limit": 5}
        )
        if success:
            investors = response.get("investors", [])
            print(f"   Search for 'venture' returned {len(investors)} results")
            return True
        return False

    def test_investor_filters(self):
        """Test investor filtering"""
        success, response = self.run_test(
            "Investor Filters",
            "GET",
            "/investors",
            200,
            params={"investor_type": "VC", "limit": 5}
        )
        if success:
            investors = response.get("investors", [])
            print(f"   Filter for VCs returned {len(investors)} results")
            if investors:
                # Check if all returned investors are VCs
                non_vc = [inv for inv in investors if inv.get("investor_type") != "VC"]
                if non_vc:
                    print(f"   Warning: Found non-VC investors in VC filter: {len(non_vc)}")
                    return False
            return True
        return False

    def test_investor_profile(self):
        """Test individual investor profile"""
        # First get a list to find a valid investor ID
        success, response = self.run_test(
            "Get Investor for Profile Test",
            "GET", 
            "/investors",
            200,
            params={"limit": 1}
        )
        
        if not success or not response.get("investors"):
            print("   Cannot test profile - no investors found")
            return False
            
        investor_id = response["investors"][0].get("id")
        if not investor_id:
            print("   Cannot test profile - no investor ID found")
            return False
            
        success, profile = self.run_test(
            "Investor Profile",
            "GET",
            f"/investors/{investor_id}",
            200
        )
        
        if success:
            required_fields = ["name", "institution", "investor_type", "id"]
            missing_fields = [field for field in required_fields if field not in profile]
            if missing_fields:
                print(f"   Warning: Missing profile fields: {missing_fields}")
                return False
            
            print(f"   Profile loaded for: {profile.get('name', 'N/A')}")
            return True
        return False

    def test_new_updated_investors(self):
        """Test new & updated investors endpoint"""
        success, response = self.run_test(
            "New & Updated Investors",
            "GET",
            "/investors/new-updated",
            200
        )
        if success:
            investors = response.get("investors", [])
            count = response.get("count", 0)
            print(f"   Found {count} new/updated investors in last 24h")
            return True
        return False

    def test_csv_export(self):
        """Test CSV export functionality"""
        success, _ = self.run_test(
            "CSV Export",
            "GET",
            "/investors/export-csv",
            200,
            params={"limit": "10"}
        )
        return success

    def test_idea_match(self):
        """Test AI idea matching"""
        test_data = {
            "description": "AI-powered fintech app for SME lending in India",
            "stage": "Seed",
            "target_raise": 1000000,
            "geography": "India"
        }
        
        success, response = self.run_test(
            "Idea Match AI",
            "POST",
            "/idea-match",
            200,
            data=test_data
        )
        
        if success:
            matches = response.get("matches", [])
            extracted_sectors = response.get("extracted_sectors", [])
            print(f"   Found {len(matches)} potential matches")
            print(f"   Extracted sectors: {extracted_sectors}")
            
            if matches and len(matches) > 0:
                top_match = matches[0]
                score = top_match.get("match_score", 0)
                name = top_match.get("name", "N/A")
                print(f"   Top match: {name} (score: {score})")
                return True
            return len(matches) > 0
        return False

    def test_news_api(self):
        """Test news aggregator API"""
        success, response = self.run_test(
            "News Articles",
            "GET",
            "/news",
            200,
            params={"limit": 5}
        )
        
        if success:
            articles = response.get("articles", [])
            total = response.get("total", 0)
            print(f"   Found {len(articles)} articles out of {total} total")
            return True
        return False

    def test_events_api(self):
        """Test events tracker API"""
        success, response = self.run_test(
            "Events",
            "GET",
            "/events",
            200
        )
        
        if success:
            events = response.get("events", [])
            print(f"   Found {len(events)} events")
            return True
        return False

    def test_govt_schemes_api(self):
        """Test government schemes API"""
        success, response = self.run_test(
            "Government Schemes",
            "GET",
            "/govt-schemes",
            200
        )
        
        if success:
            schemes = response.get("schemes", [])
            print(f"   Found {len(schemes)} government schemes")
            return True
        return False

    def test_accelerators_api(self):
        """Test accelerators API"""
        success, response = self.run_test(
            "Accelerators",
            "GET",
            "/accelerators",
            200
        )
        
        if success:
            accelerators = response.get("accelerators", [])
            print(f"   Found {len(accelerators)} accelerators")
            return True
        return False

    def test_startups_api(self):
        """Test startups API"""
        success, response = self.run_test(
            "Startups List",
            "GET",
            "/startups",
            200
        )
        
        if success:
            startups = response.get("startups", [])
            total = response.get("total", 0)
            print(f"   Found {len(startups)} startups out of {total} total")
            return True
        return False

    def test_create_startup(self):
        """Test startup creation"""
        test_startup = {
            "founder_name": "Test Founder",
            "startup_name": "Test Startup Inc",
            "description": "A test startup for API validation",
            "website_url": "https://example.com",
            "stage": "Seed",
            "sector": "SaaS"
        }
        
        success, response = self.run_test(
            "Create Startup",
            "POST",
            "/startups",
            200,
            data=test_startup
        )
        
        if success:
            startup_id = response.get("id")
            print(f"   Created startup with ID: {startup_id}")
            return True
        return False

    def test_email_api(self):
        """Test email sending API"""
        # Note: This will try to send a real email, but should work even if email fails
        test_email = {
            "recipient_email": "test@example.com",
            "subject": "Test API Email",
            "html_content": "This is a test email from API testing",
            "sender_name": "API Tester"
        }
        
        success, response = self.run_test(
            "Send Email",
            "POST",
            "/send-email",
            200,
            data=test_email
        )
        
        if success:
            message = response.get("message", "")
            print(f"   Email response: {message}")
            return True
        return False

def main():
    print("=" * 60)
    print("🚀 TESTING INVESTOR DATABASE API")
    print("=" * 60)
    
    tester = InvestorDBAPITester()
    
    # Core functionality tests
    print("\n📊 TESTING CORE FUNCTIONALITY")
    tester.test_dashboard_stats()
    tester.test_investor_list()
    tester.test_investor_search()
    tester.test_investor_filters()
    tester.test_investor_profile()
    tester.test_new_updated_investors()
    
    # Feature tests
    print("\n🔍 TESTING KEY FEATURES")
    tester.test_csv_export()
    tester.test_idea_match()
    
    # Content APIs
    print("\n📰 TESTING CONTENT APIS")
    tester.test_news_api()
    tester.test_events_api()
    tester.test_govt_schemes_api()
    tester.test_accelerators_api()
    
    # Interactive features
    print("\n💼 TESTING INTERACTIVE FEATURES")
    tester.test_startups_api()
    tester.test_create_startup()
    tester.test_email_api()
    
    # Print final results
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    # Print failed tests
    failed_tests = [t for t in tester.test_results if t["status"] == "FAILED"]
    if failed_tests:
        print("\n❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"  - {test['test']}: {test['details']}")
    else:
        print("\n🎉 ALL TESTS PASSED!")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())