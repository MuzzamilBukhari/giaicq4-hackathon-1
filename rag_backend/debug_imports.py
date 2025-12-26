#!/usr/bin/env python3
"""
Test script to debug the import issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test imports that are used in the API call path
try:
    from services.generator import generate_answer
    print("SUCCESS: services.generator import successful")
except Exception as e:
    print(f"ERROR: services.generator import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from services.session_logger import log_message
    print("SUCCESS: services.session_logger import successful")
except Exception as e:
    print(f"ERROR: services.session_logger import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from routes.ask import ask_endpoint
    print("SUCCESS: routes.ask import successful")
except Exception as e:
    print(f"ERROR: routes.ask import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    # Test the full call path
    import asyncio
    async def test_full_path():
        try:
            result = await generate_answer("hello", "test_session", mode="global")
            print(f"SUCCESS: Full path successful: {type(result)}")
        except Exception as e:
            print(f"ERROR: Full path failed: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(test_full_path())
except Exception as e:
    print(f"ERROR: Full path test setup failed: {e}")
    import traceback
    traceback.print_exc()