#!/usr/bin/env python3
"""
Testing script to validate RAG Chatbot deployment
"""
import asyncio
import argparse
import aiohttp
import time
import sys
from typing import Dict, Any, List


async def test_health_check(session: aiohttp.ClientSession, base_url: str) -> bool:
    """Test the health check endpoint"""
    try:
        async with session.get(f"{base_url}/status") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Health check passed: {data['status']}")
                print(f"  - Qdrant OK: {data['qdrant_ok']}")
                print(f"  - Neon OK: {data['neon_ok']}")
                print(f"  - Vector count: {data['vector_count']}")
                return True
            else:
                print(f"✗ Health check failed with status {response.status}")
                return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


async def test_metrics(session: aiohttp.ClientSession, base_url: str) -> bool:
    """Test the metrics endpoint"""
    try:
        async with session.get(f"{base_url}/metrics") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Metrics check passed")
                print(f"  - Avg latency: {data['avg_latency_ms']:.2f}ms")
                print(f"  - Success rate: {data['success_rate']:.2f}%")
                print(f"  - Total requests: {data['total_requests']}")
                return True
            else:
                print(f"✗ Metrics check failed with status {response.status}")
                return False
    except Exception as e:
        print(f"✗ Metrics check error: {e}")
        return False


async def test_query(session: aiohttp.ClientSession, base_url: str) -> bool:
    """Test the query endpoint with a simple question"""
    try:
        start_time = time.time()
        async with session.post(
            f"{base_url}/query",
            json={"question": "What is this textbook about?", "mode": "full_retrieval"}
        ) as response:
            elapsed = (time.time() - start_time) * 1000

            if response.status == 200:
                data = await response.json()
                print(f"✓ Query test passed (response time: {elapsed:.2f}ms)")
                print(f"  - Answer length: {len(data['answer'])} chars")
                print(f"  - Sources found: {len(data['sources'])}")
                print(f"  - Model used: {data['meta']['model']}")
                return True
            elif response.status == 429:
                print(f"✗ Query test failed - rate limited")
                return False
            else:
                print(f"✗ Query test failed with status {response.status}")
                if response.status == 500:
                    error_text = await response.text()
                    print(f"  - Error: {error_text}")
                return False
    except Exception as e:
        print(f"✗ Query test error: {e}")
        return False


async def test_selected_text(session: aiohttp.ClientSession, base_url: str) -> bool:
    """Test the selected text endpoint"""
    try:
        async with session.post(
            f"{base_url}/selected",
            json={
                "question": "Explain this concept",
                "selected_text": "This is a sample text for testing purposes."
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Selected text test passed")
                print(f"  - Answer length: {len(data['answer'])} chars")
                return True
            elif response.status == 429:
                print(f"✗ Selected text test failed - rate limited")
                return False
            else:
                print(f"✗ Selected text test failed with status {response.status}")
                return False
    except Exception as e:
        print(f"✗ Selected text test error: {e}")
        return False


async def run_deployment_tests(base_url: str) -> Dict[str, bool]:
    """Run all deployment tests"""
    print(f"Testing deployment at: {base_url}")
    print("=" * 50)

    results = {}

    async with aiohttp.ClientSession() as session:
        # Run tests in sequence
        results['health'] = await test_health_check(session, base_url)
        print()

        results['metrics'] = await test_metrics(session, base_url)
        print()

        results['query'] = await test_query(session, base_url)
        print()

        results['selected_text'] = await test_selected_text(session, base_url)
        print()

    return results


def print_summary(results: Dict[str, bool]):
    """Print test summary"""
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(results.values())
    total = len(results)

    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test.replace('_', ' ').title()}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Deployment is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the deployment.")
        return False


async def main():
    parser = argparse.ArgumentParser(description="Test RAG Chatbot deployment")
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:8000",
        help="Base URL of the deployed API (default: http://localhost:8000)"
    )

    args = parser.parse_args()

    # Validate URL format
    if not args.base_url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    results = await run_deployment_tests(args.base_url)
    success = print_summary(results)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())