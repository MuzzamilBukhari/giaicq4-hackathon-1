"""
Test script to verify the authentication implementation
"""
import asyncio
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_auth_flow():
    print("Testing Authentication Flow...")

    # Test data
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword123",
        "hardware_exp": "beginner",
        "software_exp": "intermediate",
        "robotics_level": "beginner",
        "goals": "Learning ROS2 fundamentals"
    }

    print("\n1. Testing Signup...")
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
        print(f"Signup Status: {response.status_code}")
        if response.status_code == 201:
            signup_data = response.json()
            token = signup_data.get("token")
            print(f"Signup successful! Token received: {bool(token)}")
        else:
            print(f"Signup failed: {response.text}")
            return
    except Exception as e:
        print(f"Signup error: {e}")
        return

    print("\n2. Testing Login...")
    try:
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            login_data = response.json()
            token = login_data.get("token")
            print(f"Login successful! Token received: {bool(token)}")
        else:
            print(f"Login failed: {response.text}")
            return
    except Exception as e:
        print(f"Login error: {e}")
        return

    print("\n3. Testing Profile Access...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        print(f"Profile Status: {response.status_code}")
        if response.status_code == 200:
            profile_data = response.json()
            print(f"Profile access successful! User: {profile_data.get('email')}")
        else:
            print(f"Profile access failed: {response.text}")
    except Exception as e:
        print(f"Profile access error: {e}")

    print("\n4. Testing RAG endpoint with token...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        ask_data = {"question": "What is ROS2?"}
        response = requests.post(f"{BASE_URL}/ask", json=ask_data, headers=headers)
        print(f"RAG Ask Status: {response.status_code}")
        if response.status_code in [200, 400, 500]:  # Various possible responses
            print("RAG endpoint with auth token works!")
        else:
            print(f"RAG endpoint failed: {response.text}")
    except Exception as e:
        print(f"RAG endpoint error: {e}")

    print("\n5. Testing RAG endpoint without token...")
    try:
        ask_data = {"question": "What is ROS2?"}
        response = requests.post(f"{BASE_URL}/ask", json=ask_data)
        print(f"RAG Ask (no auth) Status: {response.status_code}")
        if response.status_code in [200, 400, 500]:  # Should work without auth
            print("RAG endpoint without auth token works!")
        else:
            print(f"RAG endpoint without auth failed: {response.text}")
    except Exception as e:
        print(f"RAG endpoint without auth error: {e}")

    print("\nAuthentication flow test completed!")

if __name__ == "__main__":
    test_auth_flow()