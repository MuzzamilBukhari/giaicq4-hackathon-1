"""
Test script to verify the authentication routes are working correctly
"""
import requests
import json

def test_auth_routes():
    print("Testing Authentication Routes...")

    # Use the correct backend URL
    base_url = "http://localhost:8000"  # Adjust if needed

    # Test data
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword123",
        "hardware_exp": "beginner",
        "software_exp": "intermediate",
        "robotics_level": "beginner",
        "goals": "Learning ROS2 fundamentals"
    }

    print("\n1. Testing POST /api/auth/signup endpoint...")
    try:
        response = requests.post(f"{base_url}/api/auth/signup", json=user_data, timeout=10)
        print(f"Signup Status: {response.status_code}")
        print(f"Signup Response: {response.text[:200]}...")  # First 200 chars

        if response.status_code == 201:
            # Try to parse as JSON to make sure it's valid
            try:
                response_json = response.json()
                token = response_json.get("token")
                print(f"✓ Signup successful! Token received: {bool(token)}")
            except json.JSONDecodeError as e:
                print(f"✗ Signup response is not valid JSON: {e}")
                return
        else:
            print(f"✗ Signup failed with status {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ Signup request failed: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"✗ Signup response is not valid JSON: {e}")
        return

    print("\n2. Testing POST /api/auth/login endpoint...")
    try:
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text[:200]}...")  # First 200 chars

        if response.status_code == 200:
            # Try to parse as JSON to make sure it's valid
            try:
                response_json = response.json()
                token = response_json.get("token")
                print(f"✓ Login successful! Token received: {bool(token)}")
            except json.JSONDecodeError as e:
                print(f"✗ Login response is not valid JSON: {e}")
                return
        else:
            print(f"✗ Login failed with status {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ Login request failed: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"✗ Login response is not valid JSON: {e}")
        return

    print("\n3. Testing GET /api/auth/profile endpoint (with token)...")
    try:
        # Use the token from login
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        if login_response.status_code == 200:
            token = login_response.json().get("token")
            headers = {"Authorization": f"Bearer {token}"}

            response = requests.get(f"{base_url}/api/auth/profile", headers=headers, timeout=10)
            print(f"Profile Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    profile_data = response.json()
                    print(f"✓ Profile access successful! User: {profile_data.get('email')}")
                except json.JSONDecodeError as e:
                    print(f"✗ Profile response is not valid JSON: {e}")
            else:
                print(f"✗ Profile access failed with status {response.status_code}")
        else:
            print("✗ Could not get token for profile test")
    except requests.exceptions.RequestException as e:
        print(f"✗ Profile request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"✗ Profile response is not valid JSON: {e}")

    print("\n4. Testing that /api/auth endpoints return JSON (not HTML)...")
    try:
        # Test a non-existent auth endpoint to ensure we get JSON error, not HTML
        response = requests.get(f"{base_url}/api/auth/nonexistent", timeout=10)
        print(f"Non-existent endpoint Status: {response.status_code}")

        # Check if response is JSON (not HTML)
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            print("✓ Non-existent endpoint returns JSON (not HTML)")
        else:
            print(f"✗ Non-existent endpoint returns {content_type}, not JSON")
            print(f"Response preview: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"✗ Non-existent endpoint test failed: {e}")

    print("\nAuthentication routes test completed!")

if __name__ == "__main__":
    test_auth_routes()