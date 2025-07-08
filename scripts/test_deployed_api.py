#!/usr/bin/env python3
"""
Test Deployed API Endpoints
===========================
This script tests the deployed ValidateIO API endpoints to ensure
they are accessible and functioning correctly.
"""

import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import requests
from urllib.parse import urljoin


class APIEndpointTester:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.test_results = []
        self.auth_token = None
        
        # Set headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if api_key:
            self.session.headers['X-API-Key'] = api_key
            
    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f" {text}")
        print(f"{'='*60}")
        
    def print_test(self, test_name: str, success: bool, message: str = "", 
                   response_time: Optional[float] = None):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f" ({response_time:.2f}s)" if response_time else ""
        print(f"{status} | {test_name}{time_str}")
        if message:
            print(f"     └─ {message}")
        self.test_results.append((test_name, success, message, response_time))
        
    def make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Tuple[Optional[requests.Response], float]:
        """Make HTTP request and return response with timing"""
        url = urljoin(self.base_url, endpoint)
        
        # Add auth token if available
        if self.auth_token and headers is None:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
        elif self.auth_token and headers:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        start_time = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=30
            )
            elapsed_time = time.time() - start_time
            return response, elapsed_time
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"     └─ Error: {str(e)}")
            return None, elapsed_time
            
    def test_health_check(self):
        """Test health check endpoint"""
        self.print_header("Testing Health Check")
        
        # Test root endpoint
        response, elapsed = self.make_request('GET', '/')
        if response and response.status_code == 200:
            self.print_test("Root endpoint", True, 
                          f"Status: {response.status_code}", elapsed)
        else:
            self.print_test("Root endpoint", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
        # Test health endpoint
        response, elapsed = self.make_request('GET', '/health')
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.print_test("Health endpoint", True, 
                              f"Status: healthy, Version: {data.get('version', 'unknown')}", 
                              elapsed)
            except:
                self.print_test("Health endpoint", False, 
                              "Invalid JSON response")
        else:
            self.print_test("Health endpoint", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
    def test_api_docs(self):
        """Test API documentation endpoints"""
        self.print_header("Testing API Documentation")
        
        # Test OpenAPI docs
        response, elapsed = self.make_request('GET', '/docs')
        if response and response.status_code == 200:
            self.print_test("Swagger UI docs", True, 
                          "Documentation accessible", elapsed)
        else:
            self.print_test("Swagger UI docs", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
        # Test OpenAPI schema
        response, elapsed = self.make_request('GET', '/openapi.json')
        if response and response.status_code == 200:
            try:
                schema = response.json()
                self.print_test("OpenAPI schema", True, 
                              f"API version: {schema.get('info', {}).get('version', 'unknown')}", 
                              elapsed)
            except:
                self.print_test("OpenAPI schema", False, 
                              "Invalid JSON response")
        else:
            self.print_test("OpenAPI schema", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        self.print_header("Testing Authentication Endpoints")
        
        # Test user registration
        test_user = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        response, elapsed = self.make_request('POST', '/api/v1/auth/register', data=test_user)
        if response and response.status_code in [200, 201, 409]:  # 409 if user exists
            if response.status_code == 409:
                self.print_test("User registration", True, 
                              "Endpoint working (user already exists)", elapsed)
            else:
                self.print_test("User registration", True, 
                              "New user created successfully", elapsed)
        else:
            self.print_test("User registration", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
        # Test login
        login_data = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
        
        response, elapsed = self.make_request('POST', '/api/v1/auth/login', 
                                            data=login_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.auth_token = data.get('access_token')
                self.print_test("User login", True, 
                              "Login successful, token received", elapsed)
            except:
                self.print_test("User login", False, 
                              "Invalid response format")
        else:
            self.print_test("User login", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
    def test_validation_endpoints(self):
        """Test validation endpoints"""
        self.print_header("Testing Validation Endpoints")
        
        # Test validation creation
        validation_data = {
            "idea_description": "An AI-powered platform for testing business ideas",
            "target_market": "Entrepreneurs and startups",
            "problem_solved": "Validating business ideas before investing resources"
        }
        
        response, elapsed = self.make_request('POST', '/api/v1/validations', 
                                            data=validation_data)
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                validation_id = data.get('id')
                self.print_test("Create validation", True, 
                              f"Validation created with ID: {validation_id}", elapsed)
                
                # Test get validation
                if validation_id:
                    response, elapsed = self.make_request('GET', 
                                                        f'/api/v1/validations/{validation_id}')
                    if response and response.status_code == 200:
                        self.print_test("Get validation", True, 
                                      "Validation retrieved successfully", elapsed)
                    else:
                        self.print_test("Get validation", False, 
                                      f"Status: {response.status_code if response else 'No response'}")
            except Exception as e:
                self.print_test("Create validation", False, 
                              f"Error processing response: {str(e)}")
        elif response and response.status_code == 401:
            self.print_test("Create validation", False, 
                          "Authentication required - please check auth setup")
        else:
            self.print_test("Create validation", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
        # Test list validations
        response, elapsed = self.make_request('GET', '/api/v1/validations')
        if response and response.status_code == 200:
            try:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('total', 0)
                self.print_test("List validations", True, 
                              f"Retrieved {count} validations", elapsed)
            except:
                self.print_test("List validations", False, 
                              "Invalid response format")
        else:
            self.print_test("List validations", False, 
                          f"Status: {response.status_code if response else 'No response'}")
            
    def test_performance(self):
        """Test API performance"""
        self.print_header("Testing API Performance")
        
        # Test response times for multiple requests
        endpoints = [
            ('GET', '/health'),
            ('GET', '/api/v1/validations'),
        ]
        
        for method, endpoint in endpoints:
            times = []
            for i in range(5):
                _, elapsed = self.make_request(method, endpoint)
                times.append(elapsed)
                
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            performance_ok = avg_time < 2.0  # 2 second threshold
            self.print_test(f"Performance {endpoint}", performance_ok,
                          f"Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
            
    def generate_summary(self):
        """Generate test summary"""
        self.print_header("Test Summary")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, success, _, _ in self.test_results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\nAPI Base URL: {self.base_url}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        
        # Calculate average response time
        response_times = [t for _, _, _, t in self.test_results if t is not None]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response_time:.2f}s")
        
        if failed_tests > 0:
            print(f"\n⚠️  Some tests failed. Please check your deployment.")
            print("\nFailed tests:")
            for test_name, success, message, _ in self.test_results:
                if not success:
                    print(f"  - {test_name}: {message}")
        else:
            print(f"\n✅ All tests passed! Your API is working correctly.")
            
        print(f"\nTimestamp: {datetime.now().isoformat()}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test ValidateIO API endpoints')
    parser.add_argument('url', help='API base URL (e.g., https://api.validateio.com)')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--skip-auth', action='store_true', 
                        help='Skip authentication tests')
    parser.add_argument('--skip-performance', action='store_true', 
                        help='Skip performance tests')
    
    args = parser.parse_args()
    
    print("\n🚀 ValidateIO API Endpoint Test")
    print("===============================")
    
    # Create tester instance
    tester = APIEndpointTester(args.url, args.api_key)
    
    # Run tests
    tester.test_health_check()
    tester.test_api_docs()
    
    if not args.skip_auth:
        tester.test_auth_endpoints()
        
    tester.test_validation_endpoints()
    
    if not args.skip_performance:
        tester.test_performance()
    
    # Generate summary
    tester.generate_summary()
    
    # Return exit code based on results
    failed_tests = sum(1 for _, success, _, _ in tester.test_results if not success)
    return 1 if failed_tests > 0 else 0


if __name__ == "__main__":
    sys.exit(main())