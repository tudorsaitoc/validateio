#!/usr/bin/env python3
"""Test if the app starts correctly"""

import os
import sys

print("Testing ValidateIO startup...")
print(f"PORT environment variable: {os.getenv('PORT', 'Not set')}")

try:
    # Test basic imports
    from fastapi import FastAPI
    print("✅ FastAPI imported")
    
    # Test app creation
    from main import app
    print("✅ App imported successfully")
    
    # Test if we can start uvicorn
    import uvicorn
    print("✅ Uvicorn imported")
    
    # Show what port we'll use
    port = int(os.getenv('PORT', 8080))
    print(f"Will listen on port: {port}")
    
except Exception as e:
    print(f"❌ Error during import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nApp should be able to start!")