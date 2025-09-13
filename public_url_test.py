#!/usr/bin/env python3

import requests
import sys
import json

class PublicURLTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                    return True, response_data
                except:
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

    def test_custom_url_access(self):
        """Test accessing wedding data by custom URL"""
        return self.run_test(
            "Custom URL Access (sridhar-sneha-wedding)",
            "GET",
            "api/wedding/public/custom/sridhar-sneha-wedding",
            200
        )

    def test_user_id_access(self):
        """Test accessing wedding data by user ID"""
        # Using the sridhar user ID from the JSON file
        sridhar_user_id = "fb2403e9-9e05-4c51-895b-4173f6fc9d7e"
        return self.run_test(
            "User ID Access (Sridhar)",
            "GET",
            f"api/wedding/public/user/{sridhar_user_id}",
            200
        )

    def test_nonexistent_custom_url(self):
        """Test accessing non-existent custom URL"""
        return self.run_test(
            "Non-existent Custom URL",
            "GET",
            "api/wedding/public/custom/nonexistent-wedding",
            404
        )

    def test_nonexistent_user_id(self):
        """Test accessing non-existent user ID"""
        return self.run_test(
            "Non-existent User ID",
            "GET",
            "api/wedding/public/user/nonexistent-user-id",
            404
        )

def main():
    print("🚀 Starting Public URL Wedding Cards Tests")
    print("=" * 60)
    
    # Setup
    tester = PublicURLTester()
    
    # Test sequence
    tests = [
        ("Custom URL Access", tester.test_custom_url_access),
        ("User ID Access", tester.test_user_id_access),
        ("Non-existent Custom URL", tester.test_nonexistent_custom_url),
        ("Non-existent User ID", tester.test_nonexistent_user_id)
    ]
    
    print(f"\n📋 Running {len(tests)} public URL test scenarios...")
    
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
    print(f"📊 Public URL Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if failed_tests:
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
    
    if tester.tests_passed == tester.tests_run:
        print("✅ All public URL tests passed!")
        return 0
    else:
        print("❌ Some public URL tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())