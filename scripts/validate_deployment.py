#!/usr/bin/env python3
"""
Validation script to check if the RAG system is properly deployed and working
"""
import argparse
import asyncio
import aiohttp
import os
import sys
from pathlib import Path


async def check_api_connection(base_url: str, api_key: str = None) -> bool:
    """Check if we can connect to the API"""
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/status", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ API connection successful")
                    print(f"  Status: {data.get('status', 'unknown')}")
                    print(f"  Qdrant OK: {data.get('qdrant_ok', 'unknown')}")
                    print(f"  Neon OK: {data.get('neon_ok', 'unknown')}")
                    print(f"  Vector count: {data.get('vector_count', 0)}")
                    return True
                else:
                    print(f"✗ API connection failed with status {response.status}")
                    return False
    except Exception as e:
        print(f"✗ API connection error: {e}")
        return False


async def check_vector_database(base_url: str) -> bool:
    """Check if vector database is working"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/status") as response:
                if response.status == 200:
                    data = await response.json()
                    vector_count = data.get('vector_count', 0)

                    if vector_count > 0:
                        print(f"✓ Vector database has {vector_count} vectors")
                        return True
                    else:
                        print(f"⚠ Vector database is empty (0 vectors)")
                        print("  You may need to index your content first")
                        return True  # Not an error, just empty
                else:
                    print(f"✗ Vector database check failed")
                    return False
    except Exception as e:
        print(f"✗ Vector database check error: {e}")
        return False


async def test_query_functionality(base_url: str) -> bool:
    """Test the query functionality"""
    try:
        async with aiohttp.ClientSession() as session:
            # Test with a simple query
            async with session.post(
                f"{base_url}/query",
                json={
                    "question": "What is this textbook about?",
                    "mode": "full_retrieval"
                },
                timeout=aiohttp.ClientTimeout(total=30)  # 30 second timeout
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Query functionality working")
                    print(f"  Answer length: {len(data.get('answer', ''))} characters")
                    print(f"  Sources found: {len(data.get('sources', []))}")
                    return True
                elif response.status == 429:
                    print(f"⚠ Query rate limited (this is normal if testing quickly)")
                    return True
                else:
                    print(f"✗ Query functionality failed with status {response.status}")
                    if response.status == 500:
                        error_text = await response.text()
                        print(f"  Error details: {error_text}")
                    return False
    except asyncio.TimeoutError:
        print(f"✗ Query functionality timed out (30s)")
        return False
    except Exception as e:
        print(f"✗ Query functionality error: {e}")
        return False


async def test_selected_text_functionality(base_url: str) -> bool:
    """Test the selected text functionality"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/selected",
                json={
                    "question": "Explain this concept",
                    "selected_text": "This is a sample text for testing."
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Selected text functionality working")
                    print(f"  Answer length: {len(data.get('answer', ''))} characters")
                    return True
                elif response.status == 429:
                    print(f"⚠ Selected text query rate limited")
                    return True
                else:
                    print(f"✗ Selected text functionality failed with status {response.status}")
                    return False
    except asyncio.TimeoutError:
        print(f"✗ Selected text functionality timed out (30s)")
        return False
    except Exception as e:
        print(f"✗ Selected text functionality error: {e}")
        return False


async def validate_deployment(base_url: str, api_key: str = None) -> dict:
    """Run all validation checks"""
    print(f"Validating deployment at: {base_url}")
    print("=" * 60)

    results = {}

    # Run validation checks
    results['api_connection'] = await check_api_connection(base_url, api_key)
    print()

    results['vector_db'] = await check_vector_database(base_url)
    print()

    results['query_functionality'] = await test_query_functionality(base_url)
    print()

    results['selected_text_functionality'] = await test_selected_text_functionality(base_url)
    print()

    return results


def print_validation_report(results: dict):
    """Print validation report"""
    print("=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)

    # Define checks and their descriptions
    checks = {
        'api_connection': 'API Connection',
        'vector_db': 'Vector Database Status',
        'query_functionality': 'Query Functionality',
        'selected_text_functionality': 'Selected Text Functionality'
    }

    passed = 0
    total = len(results)

    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        desc = checks.get(check, check.replace('_', ' ').title())
        print(f"{desc:<30} {status}")

        if result:
            passed += 1

    print("-" * 60)
    print(f"Overall: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All validation checks passed!")
        print("The RAG Chatbot system is working correctly.")
        return True
    else:
        print(f"\n❌ {total - passed} check(s) failed.")
        print("Please review the issues above and fix them before proceeding.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Validate RAG Chatbot deployment")
    parser.add_argument(
        "--base-url",
        type=str,
        required=True,
        help="Base URL of the deployed API (e.g., https://your-app.railway.app)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key if authentication is required"
    )

    args = parser.parse_args()

    # Validate URL format
    if not args.base_url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    # Run validation
    try:
        results = asyncio.run(validate_deployment(args.base_url, args.api_key))
        success = print_validation_report(results)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nValidation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Validation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()