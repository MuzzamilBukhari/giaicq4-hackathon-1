"""
End-to-End Test for RAG System
This tests the complete flow from API request to response
"""
import requests
import json
import sys
from datetime import datetime

# Backend API endpoint - adjust based on your setup
BACKEND_URL = "http://localhost:8000/api/v1/chat"

# Test data
TEST_QUERIES = [
    {
        "query": "What is Physical AI?",
        "session_id": "test_session_123",
        "metadata": None
    },
    {
        "query": "Explain humanoid robotics",
        "session_id": "test_session_123",
        "metadata": {"context": "Previous discussion about Physical AI"}
    }
]

def print_separator(title=""):
    """Print a separator line"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def test_api_connection():
    """Test if the backend API is accessible"""
    print_separator("Testing Backend API Connection")
    
    try:
        # Try to reach the health endpoint first
        health_url = BACKEND_URL.replace('/chat', '/health')
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend API is accessible")
            print(f"   Health endpoint: {health_url}")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"⚠️  Backend API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to backend API at {BACKEND_URL}")
        print("   Make sure the backend is running:")
        print("   1. cd to the project root")
        print("   2. Run: python -m uvicorn src.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {str(e)}")
        return False

def test_chat_endpoint(query_data):
    """Test the chat endpoint with specific query"""
    print_separator(f"Testing Query: '{query_data['query']}'")
    
    try:
        # Make POST request
        print("📤 Sending request to backend...")
        print(f"   URL: {BACKEND_URL}")
        print(f"   Payload: {json.dumps(query_data, indent=2)}")
        
        response = requests.post(
            BACKEND_URL,
            json=query_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📥 Response received:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        # Check if request was successful
        if response.status_code == 200:
            print("   ✅ Request successful!\n")
            
            # Parse JSON response
            response_data = response.json()
            
            # Validate response structure
            print("🔍 Validating response structure...")
            required_fields = ['answer', 'sources', 'session_id', 'timestamp']
            missing_fields = [field for field in required_fields if field not in response_data]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
            else:
                print("   ✅ All required fields present")
            
            # Display response details
            print(f"\n📝 Response Details:")
            print(f"   Answer: {response_data.get('answer', 'N/A')[:200]}...")
            print(f"   Sources count: {len(response_data.get('sources', []))}")
            print(f"   Session ID: {response_data.get('session_id', 'N/A')}")
            print(f"   Timestamp: {response_data.get('timestamp', 'N/A')}")
            
            if response_data.get('sources'):
                print(f"\n   Sources:")
                for idx, source in enumerate(response_data['sources'], 1):
                    print(f"     {idx}. {source}")
            
            return True
        else:
            print(f"   ❌ Request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out (>30 seconds)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request error: {str(e)}")
        return False
    except json.JSONDecodeError:
        print("   ❌ Response is not valid JSON")
        print(f"   Raw response: {response.text}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        return False

def test_request_validation():
    """Test request validation (edge cases)"""
    print_separator("Testing Request Validation")
    
    edge_cases = [
        {
            "name": "Empty query",
            "data": {"query": "", "session_id": "test"},
            "expected_status": 422  # Validation error
        },
        {
            "name": "Very long query (>2000 chars)",
            "data": {"query": "a" * 2500, "session_id": "test"},
            "expected_status": 400  # Bad request
        },
        {
            "name": "Missing session_id",
            "data": {"query": "test query"},
            "expected_status": 200  # Should work (session_id might be optional)
        }
    ]
    
    for test_case in edge_cases:
        print(f"\nTest: {test_case['name']}")
        try:
            response = requests.post(
                BACKEND_URL,
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            print(f"   Status: {response.status_code} (expected: {test_case['expected_status']})")
            if response.status_code == test_case['expected_status']:
                print("   ✅ Validation works as expected")
            else:
                print(f"   ⚠️  Unexpected status code")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def check_frontend_api_url():
    """Check if frontend is using the correct API URL"""
    print_separator("Checking Frontend Configuration")
    
    try:
        # Read the RAGWidget.js file
        widget_path = "docusaurus-project/src/components/RAGWidget/RAGWidget.js"
        with open(widget_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for endpoint configuration
        if "endpoint = '/api/v1/chat'" in content:
            print("✅ Frontend default endpoint: '/api/v1/chat'")
            print("   ⚠️  Note: This is a relative URL")
            print("   Make sure to configure proxy or use absolute URL in production")
        
        # Check for fetch call
        if "fetch(endpoint" in content:
            print("✅ Frontend uses fetch to call the API")
        
        # Check request body structure
        if '"query": newInputValue' in content or 'query: newInputValue' in content:
            print("✅ Frontend sends 'query' field (matches backend)")
        
        if '"session_id": sessionId' in content or 'session_id: sessionId' in content:
            print("✅ Frontend sends 'session_id' field")
        
        # Check response handling
        if 'responseData.answer' in content:
            print("✅ Frontend expects 'answer' field in response")
        
        if 'responseData.sources' in content:
            print("✅ Frontend expects 'sources' field in response")
        
    except FileNotFoundError:
        print(f"❌ Could not find frontend widget file")
    except Exception as e:
        print(f"❌ Error checking frontend: {str(e)}")

def main():
    """Run all tests"""
    print_separator("🚀 RAG System End-to-End Test")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Backend URL: {BACKEND_URL}")
    
    # Step 1: Check frontend configuration
    check_frontend_api_url()
    
    # Step 2: Test backend connectivity
    if not test_api_connection():
        print("\n❌ Cannot proceed with tests - backend is not accessible")
        print("\nTo start the backend, run:")
        print("  cd 'c:/Muzzamil/Learning/GIAIC/4th quarter/hackathon/hackathon-book'")
        print("  python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Step 3: Test chat endpoint with sample queries
    results = []
    for query_data in TEST_QUERIES:
        result = test_chat_endpoint(query_data)
        results.append(result)
    
    # Step 4: Test validation
    test_request_validation()
    
    # Summary
    print_separator("📊 Test Summary")
    total_tests = len(results)
    passed = sum(results)
    print(f"Total query tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {total_tests - passed}")
    
    if passed == total_tests:
        print("\n✅ All tests passed! The system is working end-to-end.")
    else:
        print(f"\n⚠️  {total_tests - passed} test(s) failed. Check the logs above.")
    
    print_separator()

if __name__ == "__main__":
    main()
