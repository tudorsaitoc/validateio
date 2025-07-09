#!/usr/bin/env python3
"""
Cloud Run startup wrapper for ValidateIO
Ensures proper port configuration
"""
import os
import sys
import uvicorn

# Set API_PORT from PORT if available
if 'PORT' in os.environ:
    os.environ['API_PORT'] = os.environ['PORT']
    print(f"Setting API_PORT to {os.environ['PORT']}")

# Set minimal environment if not production
if os.environ.get('ENVIRONMENT') != 'production':
    os.environ['ENVIRONMENT'] = 'production'
    
# Set required secrets if missing (for startup only)
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'temporary-secret-key-for-startup'
if not os.environ.get('JWT_SECRET_KEY'):
    os.environ['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY', 'temporary-jwt-key')

# Import the app
try:
    from main import app
    print("✅ App imported successfully")
except ImportError as e:
    print(f"⚠️  Import error, using fallback: {e}")
    # Fall back to simple app if main fails
    from main_simple import app
    print("✅ Using simple app as fallback")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting ValidateIO on port {port}...")
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)