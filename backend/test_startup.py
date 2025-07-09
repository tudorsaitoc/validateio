#!/usr/bin/env python3
"""Test if the app can start up properly"""

import sys
import traceback

print("Testing ValidateIO startup...")
print("=" * 50)

# Test imports
try:
    print("1. Testing basic imports...")
    import logging
    from datetime import datetime
    print("✅ Standard library imports OK")
except Exception as e:
    print(f"❌ Standard library import error: {e}")
    sys.exit(1)

try:
    print("\n2. Testing FastAPI imports...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    print("✅ FastAPI imports OK")
except Exception as e:
    print(f"❌ FastAPI import error: {e}")
    print("Run: pip install fastapi")
    sys.exit(1)

try:
    print("\n3. Testing app imports...")
    from app.core.config import settings
    print(f"✅ Settings loaded: {settings.PROJECT_NAME}")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Debug: {settings.DEBUG}")
except Exception as e:
    print(f"❌ App import error: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n4. Testing database connection...")
    from app.db.session import AsyncSessionLocal
    print("✅ Database session configured")
except Exception as e:
    print(f"❌ Database setup error: {e}")
    traceback.print_exc()

try:
    print("\n5. Testing API router...")
    from app.api.v1.api import api_router
    print("✅ API router imported")
except Exception as e:
    print(f"❌ API router error: {e}")
    traceback.print_exc()

print("\n" + "=" * 50)
print("Startup test complete!")
print("\nIf all checks passed, the app should deploy successfully.")
print("If any failed, fix those issues first.")