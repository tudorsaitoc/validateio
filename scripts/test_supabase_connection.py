#!/usr/bin/env python3
"""
Test Supabase Connection Script
================================
This script verifies that your Supabase connection is working correctly.
It checks authentication, database connectivity, and basic operations.
"""

import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import asyncpg

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.config import settings


class SupabaseConnectionTester:
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_anon_key = settings.SUPABASE_ANON_KEY
        self.supabase_service_key = settings.SUPABASE_SERVICE_KEY
        self.database_url = str(settings.DATABASE_URL) if settings.DATABASE_URL else None
        self.test_results = []
        
    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f" {text}")
        print(f"{'='*60}")
        
    def print_test(self, test_name: str, success: bool, message: str = ""):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if message:
            print(f"     └─ {message}")
        self.test_results.append((test_name, success, message))
        
    def test_environment_variables(self):
        """Test if all required environment variables are set"""
        self.print_header("Testing Environment Variables")
        
        vars_to_check = {
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_ANON_KEY": self.supabase_anon_key,
            "SUPABASE_SERVICE_KEY": self.supabase_service_key,
            "DATABASE_URL": self.database_url
        }
        
        all_set = True
        for var_name, var_value in vars_to_check.items():
            if var_value:
                self.print_test(f"{var_name} is set", True, f"Value: {var_value[:20]}...")
            else:
                self.print_test(f"{var_name} is set", False, "Not found in environment")
                all_set = False
                
        return all_set
        
    def test_supabase_client_connection(self):
        """Test Supabase client connection"""
        self.print_header("Testing Supabase Client Connection")
        
        if not self.supabase_url or not self.supabase_anon_key:
            self.print_test("Supabase client initialization", False, 
                          "Missing SUPABASE_URL or SUPABASE_ANON_KEY")
            return False
            
        try:
            # Create Supabase client
            supabase: Client = create_client(self.supabase_url, self.supabase_anon_key)
            self.print_test("Supabase client created", True)
            
            # Test a simple query
            result = supabase.table('users').select("*").limit(1).execute()
            self.print_test("Query users table", True, 
                          f"Successfully queried users table")
            return True
            
        except Exception as e:
            self.print_test("Supabase client connection", False, str(e))
            return False
            
    async def test_direct_database_connection(self):
        """Test direct database connection using asyncpg"""
        self.print_header("Testing Direct Database Connection")
        
        if not self.database_url:
            self.print_test("Direct database connection", False, 
                          "DATABASE_URL not configured")
            return False
            
        try:
            # Parse the database URL for asyncpg
            db_url = self.database_url.replace('postgresql://', 'postgres://')
            
            # Connect to the database
            conn = await asyncpg.connect(db_url)
            self.print_test("Database connection established", True)
            
            # Test a simple query
            version = await conn.fetchval('SELECT version()')
            self.print_test("PostgreSQL version query", True, 
                          f"Version: {version.split(',')[0]}")
            
            # Check if tables exist
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            table_names = [t['table_name'] for t in tables]
            self.print_test("Database tables query", True, 
                          f"Found {len(table_names)} tables: {', '.join(table_names[:5])}...")
            
            await conn.close()
            return True
            
        except Exception as e:
            self.print_test("Direct database connection", False, str(e))
            return False
            
    def test_supabase_auth(self):
        """Test Supabase authentication"""
        self.print_header("Testing Supabase Authentication")
        
        if not self.supabase_url or not self.supabase_anon_key:
            self.print_test("Supabase auth test", False, 
                          "Missing required credentials")
            return False
            
        try:
            supabase: Client = create_client(self.supabase_url, self.supabase_anon_key)
            
            # Test anonymous access
            self.print_test("Anonymous access", True, 
                          "Client created with anon key")
            
            # Note: We can't test user signup/login without actually creating users
            # This would be done in integration tests
            
            return True
            
        except Exception as e:
            self.print_test("Supabase auth test", False, str(e))
            return False
            
    def generate_summary(self):
        """Generate test summary"""
        self.print_header("Test Summary")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, success, _ in self.test_results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        
        if failed_tests > 0:
            print(f"\n⚠️  Some tests failed. Please check your configuration.")
            print("\nFailed tests:")
            for test_name, success, message in self.test_results:
                if not success:
                    print(f"  - {test_name}: {message}")
        else:
            print(f"\n✅ All tests passed! Your Supabase connection is working correctly.")
            
        print(f"\nTimestamp: {datetime.now().isoformat()}")
        

async def main():
    """Main function to run all tests"""
    print("\n🚀 ValidateIO Supabase Connection Test")
    print("=====================================")
    
    # Load environment variables
    load_dotenv()
    
    # Create tester instance
    tester = SupabaseConnectionTester()
    
    # Run tests
    env_ok = tester.test_environment_variables()
    
    if env_ok:
        tester.test_supabase_client_connection()
        await tester.test_direct_database_connection()
        tester.test_supabase_auth()
    else:
        print("\n⚠️  Please set up your environment variables first!")
        print("Copy .env.example to .env and fill in your Supabase credentials.")
    
    # Generate summary
    tester.generate_summary()
    
    # Return exit code based on results
    failed_tests = sum(1 for _, success, _ in tester.test_results if not success)
    return 1 if failed_tests > 0 else 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)