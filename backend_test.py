import requests
import sys
import json
from datetime import datetime

class WeddingAuthTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None
        self.user_id = None
        self.wedding_id = None
        self.test_username = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        
        if headers:
            default_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
        if params:
            print(f"   Params: {params}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.content:
                    try:
                        response_data = response.json()
                        print(f"Response: {json.dumps(response_data, indent=2)}")
                        return True, response_data
                    except:
                        print(f"Response: {response.text[:200]}")
                        return True, {}
                return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error Response: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Error Response: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test the basic /api/test endpoint"""
        return self.run_test("Health Check", "GET", "api/test", 200)

    def test_user_registration(self):
        """Test user registration with session-based auth"""
        timestamp = datetime.now().strftime('%H%M%S')
        self.test_username = f"testuser_{timestamp}"
        test_data = {
            "username": self.test_username,
            "password": "password123"
        }
        success, response = self.run_test(
            "User Registration",
            "POST",
            "api/auth/register",
            200,
            data=test_data
        )
        
        if success and response:
            # Store session_id and user info for subsequent tests
            self.session_id = response.get('session_id')
            self.user_id = response.get('user_id')
            print(f"   Stored session_id: {self.session_id}")
            print(f"   Stored user_id: {self.user_id}")
            
            # Verify response structure
            expected_fields = ['session_id', 'user_id', 'username', 'success']
            missing_fields = [field for field in expected_fields if field not in response]
            if missing_fields:
                print(f"⚠️  Missing expected fields: {missing_fields}")
                return False, response
                
        return success, response

    def test_user_login(self):
        """Test user login with existing credentials"""
        # Use a different timestamp for login test
        timestamp = datetime.now().strftime('%H%M%S') + "_login"
        login_username = f"testuser_{timestamp}"
        test_data = {
            "username": login_username,
            "password": "password123"
        }
        
        # First register a user for login test
        reg_success, reg_response = self.run_test(
            "User Registration for Login Test",
            "POST",
            "api/auth/register",
            200,
            data=test_data
        )
        
        if not reg_success:
            return False, {}
            
        # Now test login
        success, response = self.run_test(
            "User Login",
            "POST",
            "api/auth/login",
            200,
            data=test_data
        )
        
        if success and response:
            # Verify response structure
            expected_fields = ['session_id', 'user_id', 'username', 'success']
            missing_fields = [field for field in expected_fields if field not in response]
            if missing_fields:
                print(f"⚠️  Missing expected fields: {missing_fields}")
                return False, response
                
        return success, response

    def test_protected_route_without_auth(self):
        """Test protected route without authentication"""
        return self.run_test(
            "Protected Route (No Auth)",
            "GET",
            "api/profile",
            422,  # FastAPI returns 422 for missing required parameter
            params={}
        )

    def test_protected_route_with_auth(self):
        """Test protected route with authentication"""
        if not self.session_id:
            print("⚠️  No session_id available for auth test")
            return False, {}
            
        return self.run_test(
            "Protected Route (With Auth)",
            "GET",
            "api/profile",
            200,
            params={"session_id": self.session_id}
        )

    def test_wedding_data_creation(self):
        """Test wedding data creation with authentication"""
        if not self.session_id:
            print("⚠️  No session_id available for wedding creation")
            return False, {}
            
        wedding_data = {
            "session_id": self.session_id,
            "couple_name_1": "Emma Wilson",
            "couple_name_2": "James Anderson",
            "wedding_date": "2025-08-15",
            "venue_name": "Sunset Garden Estate",
            "venue_location": "123 Wedding Lane, Romance City",
            "their_story": "Emma and James met at a coffee shop and have been inseparable ever since. Their love story is one of laughter, adventure, and endless support for each other.",
            "schedule_events": [
                {"time": "14:00", "event": "Ceremony", "location": "Garden Pavilion"},
                {"time": "17:00", "event": "Cocktail Hour", "location": "Terrace"},
                {"time": "18:30", "event": "Reception", "location": "Grand Ballroom"}
            ],
            "gallery_photos": [],
            "bridal_party": [{"name": "Sarah Johnson", "role": "Maid of Honor", "photo": ""}],
            "groom_party": [{"name": "Michael Brown", "role": "Best Man", "photo": ""}],
            "faqs": [{"question": "What should I wear?", "answer": "Semi-formal attire is recommended"}],
            "theme": "classic"
        }
        
        success, response = self.run_test(
            "Wedding Data Creation",
            "POST",
            "api/wedding",
            200,
            data=wedding_data
        )
        
        if success and response:
            self.wedding_id = response.get('id')
            print(f"   Stored wedding_id: {self.wedding_id}")
            
        return success, response

    def test_wedding_data_retrieval(self):
        """Test wedding data retrieval with authentication"""
        if not self.session_id:
            print("⚠️  No session_id available for wedding retrieval")
            return False, {}
            
        return self.run_test(
            "Wedding Data Retrieval",
            "GET",
            "api/wedding",
            200,
            params={"session_id": self.session_id}
        )

    def test_wedding_data_update(self):
        """Test wedding data update with authentication"""
        if not self.session_id:
            print("⚠️  No session_id available for wedding update")
            return False, {}
            
        updated_data = {
            "session_id": self.session_id,
            "couple_name_1": "Emma Wilson",
            "couple_name_2": "James Anderson",
            "wedding_date": "2025-08-15",
            "venue_name": "Updated Sunset Garden Estate",
            "venue_location": "456 Updated Wedding Lane, Romance City",
            "their_story": "Updated: Emma and James met at a coffee shop and have been inseparable ever since.",
            "theme": "rustic"
        }
        
        return self.run_test(
            "Wedding Data Update",
            "PUT",
            "api/wedding",
            200,
            data=updated_data
        )

    def test_public_wedding_access(self):
        """Test public wedding access without authentication"""
        if not self.wedding_id:
            print("⚠️  No wedding_id available for public access test")
            return False, {}
            
        return self.run_test(
            "Public Wedding Access",
            "GET",
            f"api/wedding/public/{self.wedding_id}",
            200
        )

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        test_data = {
            "username": "nonexistent_user_12345",
            "password": "wrong_password_67890"
        }
        return self.run_test(
            "Invalid Login Test",
            "POST",
            "api/auth/login",
            401,
            data=test_data
        )

    def test_duplicate_registration(self):
        """Test registration with existing username"""
        if not self.test_username:
            print("⚠️  No test username available for duplicate registration test")
            return False, {}
            
        test_data = {
            "username": self.test_username,
            "password": "different_password"
        }
        return self.run_test(
            "Duplicate Registration Test",
            "POST",
            "api/auth/register",
            400,
            data=test_data
        )

def main():
    print("🚀 Starting Wedding Cards Backend Authentication Tests")
    print("=" * 60)
    
    # Setup
    tester = WeddingAuthTester()
    
    # Test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("User Registration", tester.test_user_registration),
        ("User Login", tester.test_user_login),
        ("Protected Route (No Auth)", tester.test_protected_route_without_auth),
        ("Protected Route (With Auth)", tester.test_protected_route_with_auth),
        ("Wedding Data Creation", tester.test_wedding_data_creation),
        ("Wedding Data Retrieval", tester.test_wedding_data_retrieval),
        ("Wedding Data Update", tester.test_wedding_data_update),
        ("Public Wedding Access", tester.test_public_wedding_access),
        ("Invalid Login Test", tester.test_invalid_login),
        ("Duplicate Registration Test", tester.test_duplicate_registration)
    ]
    
    print(f"\n📋 Running {len(tests)} test scenarios...")
    
    failed_tests = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success, response = test_func()
            if not success:
                print(f"❌ {test_name} failed")
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Backend Authentication Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if failed_tests:
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
    
    if tester.tests_passed == tester.tests_run:
        print("✅ All backend authentication tests passed!")
        return 0
    else:
        print("❌ Some backend authentication tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())