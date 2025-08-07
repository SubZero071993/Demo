#!/usr/bin/env python3
"""
Clinical Assets Dashboard Backend API Test Suite
Tests all backend endpoints with comprehensive coverage
"""

import requests
import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Any
import os

# Get backend URL from frontend environment
BACKEND_URL = "https://5bc8f861-ac6a-494a-bbbc-4ca6643d6305.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_basic_api_health(self):
        """Test basic API health endpoints"""
        print("\n=== Testing Basic API Health ===")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "status" in data:
                    self.log_test("Root endpoint (/api/)", True, f"Status: {data.get('status')}")
                else:
                    self.log_test("Root endpoint (/api/)", False, "Missing expected fields in response")
            else:
                self.log_test("Root endpoint (/api/)", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Root endpoint (/api/)", False, f"Exception: {str(e)}")
        
        # Test health endpoint
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and "database" in data:
                    self.log_test("Health endpoint (/api/health)", True, f"DB: {data.get('database')}")
                else:
                    self.log_test("Health endpoint (/api/health)", False, "Missing expected fields")
            else:
                self.log_test("Health endpoint (/api/health)", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Health endpoint (/api/health)", False, f"Exception: {str(e)}")
    
    def test_dashboard_module(self):
        """Test dashboard module endpoints"""
        print("\n=== Testing Dashboard Module ===")
        
        endpoints = [
            ("/dashboard/status", "Dashboard status"),
            ("/dashboard/overview", "Dashboard overview"),
            ("/dashboard/alerts", "Dashboard alerts"),
            ("/dashboard/metrics", "Dashboard metrics")
        ]
        
        for endpoint, description in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(description, True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
    
    def test_schedule_module(self):
        """Test schedule module CRUD operations"""
        print("\n=== Testing Schedule Module ===")
        
        # Test GET appointments (empty initially)
        try:
            response = self.session.get(f"{self.base_url}/schedule/appointments")
            if response.status_code == 200:
                appointments = response.json()
                self.log_test("Get appointments", True, f"Found {len(appointments)} appointments")
            else:
                self.log_test("Get appointments", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get appointments", False, f"Exception: {str(e)}")
        
        # Test CREATE appointment
        appointment_data = {
            "title": "Equipment Calibration",
            "date": (date.today() + timedelta(days=1)).isoformat(),
            "time": "10:00",
            "location": "Lab A",
            "description": "Monthly calibration of MRI equipment"
        }
        
        created_appointment_id = None
        try:
            response = self.session.post(
                f"{self.base_url}/schedule/appointments",
                json=appointment_data
            )
            if response.status_code == 200:
                appointment = response.json()
                created_appointment_id = appointment.get('id')
                self.log_test("Create appointment", True, f"Created appointment ID: {created_appointment_id}")
            else:
                self.log_test("Create appointment", False, f"Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create appointment", False, f"Exception: {str(e)}")
        
        # Test GET specific appointment
        if created_appointment_id:
            try:
                response = self.session.get(f"{self.base_url}/schedule/appointments/{created_appointment_id}")
                if response.status_code == 200:
                    appointment = response.json()
                    self.log_test("Get specific appointment", True, f"Title: {appointment.get('title')}")
                else:
                    self.log_test("Get specific appointment", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Get specific appointment", False, f"Exception: {str(e)}")
        
        # Test UPDATE appointment
        if created_appointment_id:
            update_data = {
                "title": "Updated Equipment Calibration",
                "status": "scheduled"
            }
            try:
                response = self.session.put(
                    f"{self.base_url}/schedule/appointments/{created_appointment_id}",
                    json=update_data
                )
                if response.status_code == 200:
                    self.log_test("Update appointment", True, "Appointment updated successfully")
                else:
                    self.log_test("Update appointment", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Update appointment", False, f"Exception: {str(e)}")
        
        # Test upcoming appointments
        try:
            response = self.session.get(f"{self.base_url}/schedule/appointments/upcoming?days=7")
            if response.status_code == 200:
                upcoming = response.json()
                self.log_test("Get upcoming appointments", True, f"Found {len(upcoming)} upcoming")
            else:
                self.log_test("Get upcoming appointments", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get upcoming appointments", False, f"Exception: {str(e)}")
        
        # Test DELETE appointment (cleanup)
        if created_appointment_id:
            try:
                response = self.session.delete(f"{self.base_url}/schedule/appointments/{created_appointment_id}")
                if response.status_code == 200:
                    self.log_test("Delete appointment", True, "Appointment deleted successfully")
                else:
                    self.log_test("Delete appointment", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Delete appointment", False, f"Exception: {str(e)}")
    
    def test_maintenance_module(self):
        """Test maintenance module endpoints"""
        print("\n=== Testing Maintenance Module ===")
        
        # Test GET spare parts
        try:
            response = self.session.get(f"{self.base_url}/maintenance/spare-parts")
            if response.status_code == 200:
                parts = response.json()
                self.log_test("Get spare parts", True, f"Found {len(parts)} spare parts")
            else:
                self.log_test("Get spare parts", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get spare parts", False, f"Exception: {str(e)}")
        
        # Test CREATE spare part
        part_data = {
            "name": "MRI Coil Assembly",
            "part_number": "MRI-COIL-001",
            "quantity": 5,
            "location": "Storage Room A",
            "minimum_stock": 2,
            "supplier": "Medical Equipment Corp"
        }
        
        created_part_id = None
        try:
            response = self.session.post(
                f"{self.base_url}/maintenance/spare-parts",
                json=part_data
            )
            if response.status_code == 200:
                part = response.json()
                created_part_id = part.get('id')
                self.log_test("Create spare part", True, f"Created part ID: {created_part_id}")
            else:
                self.log_test("Create spare part", False, f"Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create spare part", False, f"Exception: {str(e)}")
        
        # Test GET specific spare part
        if created_part_id:
            try:
                response = self.session.get(f"{self.base_url}/maintenance/spare-parts/{created_part_id}")
                if response.status_code == 200:
                    part = response.json()
                    self.log_test("Get specific spare part", True, f"Part: {part.get('name')}")
                else:
                    self.log_test("Get specific spare part", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Get specific spare part", False, f"Exception: {str(e)}")
        
        # Test maintenance history
        try:
            response = self.session.get(f"{self.base_url}/maintenance/history")
            if response.status_code == 200:
                history = response.json()
                self.log_test("Get maintenance history", True, f"Found {len(history)} records")
            else:
                self.log_test("Get maintenance history", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get maintenance history", False, f"Exception: {str(e)}")
        
        # Test CREATE maintenance record
        maintenance_data = {
            "equipment_id": "MRI-001",
            "equipment_name": "MRI Scanner Unit 1",
            "maintenance_type": "preventive",
            "description": "Monthly preventive maintenance check",
            "parts_used": [created_part_id] if created_part_id else [],
            "technician": "John Smith",
            "duration_hours": 2.5
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/maintenance/history",
                json=maintenance_data
            )
            if response.status_code == 200:
                record = response.json()
                self.log_test("Create maintenance record", True, f"Created record ID: {record.get('id')}")
            else:
                self.log_test("Create maintenance record", False, f"Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create maintenance record", False, f"Exception: {str(e)}")
        
        # Test analytics endpoints
        analytics_endpoints = [
            ("/maintenance/analytics/low-stock", "Low stock alerts"),
            ("/maintenance/analytics/equipment-status", "Equipment status")
        ]
        
        for endpoint, description in analytics_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(description, True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
    
    def test_quiz_module(self):
        """Test quiz module endpoints"""
        print("\n=== Testing Quiz Module ===")
        
        # Test GET questions
        try:
            response = self.session.get(f"{self.base_url}/quiz/questions")
            if response.status_code == 200:
                questions = response.json()
                self.log_test("Get quiz questions", True, f"Found {len(questions)} questions")
            else:
                self.log_test("Get quiz questions", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get quiz questions", False, f"Exception: {str(e)}")
        
        # Test CREATE question
        question_data = {
            "question_text": "What is the recommended frequency for MRI equipment calibration?",
            "options": ["Daily", "Weekly", "Monthly", "Yearly"],
            "correct_answer": 2,  # Monthly
            "category": "equipment_maintenance",
            "difficulty": "medium"
        }
        
        created_question_id = None
        try:
            response = self.session.post(
                f"{self.base_url}/quiz/questions",
                json=question_data
            )
            if response.status_code == 200:
                question = response.json()
                created_question_id = question.get('id')
                self.log_test("Create quiz question", True, f"Created question ID: {created_question_id}")
            else:
                self.log_test("Create quiz question", False, f"Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create quiz question", False, f"Exception: {str(e)}")
        
        # Test GET specific question
        if created_question_id:
            try:
                response = self.session.get(f"{self.base_url}/quiz/questions/{created_question_id}")
                if response.status_code == 200:
                    question = response.json()
                    self.log_test("Get specific question", True, f"Question: {question.get('question_text')[:50]}...")
                else:
                    self.log_test("Get specific question", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Get specific question", False, f"Exception: {str(e)}")
        
        # Test SUBMIT answer
        if created_question_id:
            submission_data = {
                "user_id": "test_user_001",
                "question_id": created_question_id,
                "selected_answer": 2  # Correct answer
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/quiz/submit-answer",
                    json=submission_data
                )
                if response.status_code == 200:
                    result = response.json()
                    self.log_test("Submit quiz answer", True, f"Correct: {result.get('is_correct')}")
                else:
                    self.log_test("Submit quiz answer", False, f"Status code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_test("Submit quiz answer", False, f"Exception: {str(e)}")
        
        # Test GET user results
        try:
            response = self.session.get(f"{self.base_url}/quiz/results/test_user_001")
            if response.status_code == 200:
                results = response.json()
                self.log_test("Get user quiz results", True, f"Found {len(results)} results")
            else:
                self.log_test("Get user quiz results", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get user quiz results", False, f"Exception: {str(e)}")
        
        # Test analytics and categories
        analytics_endpoints = [
            ("/quiz/analytics/performance/test_user_001", "User performance analytics"),
            ("/quiz/categories", "Quiz categories")
        ]
        
        for endpoint, description in analytics_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(description, True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
    
    def test_request_module(self):
        """Test request module endpoints"""
        print("\n=== Testing Request Module ===")
        
        # Test GET demo requests
        try:
            response = self.session.get(f"{self.base_url}/request/demo-requests")
            if response.status_code == 200:
                requests_data = response.json()
                self.log_test("Get demo requests", True, f"Found {len(requests_data)} requests")
            else:
                self.log_test("Get demo requests", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get demo requests", False, f"Exception: {str(e)}")
        
        # Test CREATE demo request
        request_data = {
            "title": "CT Scanner Demo Request",
            "description": "Need demonstration of new CT scanner features for radiology department",
            "requester": "Dr. Sarah Johnson",
            "requester_email": "sarah.johnson@hospital.com",
            "priority": "high",
            "category": "imaging_equipment",
            "expected_demo_date": (date.today() + timedelta(days=14)).isoformat()
        }
        
        created_request_id = None
        try:
            response = self.session.post(
                f"{self.base_url}/request/demo-requests",
                json=request_data
            )
            if response.status_code == 200:
                demo_request = response.json()
                created_request_id = demo_request.get('id')
                self.log_test("Create demo request", True, f"Created request ID: {created_request_id}")
            else:
                self.log_test("Create demo request", False, f"Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create demo request", False, f"Exception: {str(e)}")
        
        # Test GET specific demo request
        if created_request_id:
            try:
                response = self.session.get(f"{self.base_url}/request/demo-requests/{created_request_id}")
                if response.status_code == 200:
                    demo_request = response.json()
                    self.log_test("Get specific demo request", True, f"Title: {demo_request.get('title')}")
                else:
                    self.log_test("Get specific demo request", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Get specific demo request", False, f"Exception: {str(e)}")
        
        # Test UPDATE demo request
        if created_request_id:
            update_data = {
                "status": "approved",
                "priority": "high"
            }
            try:
                response = self.session.put(
                    f"{self.base_url}/request/demo-requests/{created_request_id}",
                    json=update_data
                )
                if response.status_code == 200:
                    self.log_test("Update demo request", True, "Request updated successfully")
                else:
                    self.log_test("Update demo request", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Update demo request", False, f"Exception: {str(e)}")
        
        # Test analytics endpoints
        analytics_endpoints = [
            ("/request/analytics/status-summary", "Request status summary"),
            ("/request/analytics/pending-requests", "Pending requests"),
            ("/request/categories", "Request categories")
        ]
        
        for endpoint, description in analytics_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(description, True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
        
        # Test DELETE demo request (cleanup)
        if created_request_id:
            try:
                response = self.session.delete(f"{self.base_url}/request/demo-requests/{created_request_id}")
                if response.status_code == 200:
                    self.log_test("Delete demo request", True, "Request deleted successfully")
                else:
                    self.log_test("Delete demo request", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test("Delete demo request", False, f"Exception: {str(e)}")
    
    def test_documents_module(self):
        """Test documents module endpoints (excluding file upload)"""
        print("\n=== Testing Documents Module ===")
        
        # Test GET documents library
        try:
            response = self.session.get(f"{self.base_url}/documents/library")
            if response.status_code == 200:
                documents = response.json()
                self.log_test("Get documents library", True, f"Found {len(documents)} documents")
            else:
                self.log_test("Get documents library", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get documents library", False, f"Exception: {str(e)}")
        
        # Test documents with filters
        filter_tests = [
            ("?category=manual", "Filter by category"),
            ("?file_type=pdf", "Filter by file type"),
            ("?search=equipment", "Search documents"),
            ("?limit=10", "Limit results")
        ]
        
        for filter_param, description in filter_tests:
            try:
                response = self.session.get(f"{self.base_url}/documents/library{filter_param}")
                if response.status_code == 200:
                    documents = response.json()
                    self.log_test(description, True, f"Found {len(documents)} documents")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
        
        # Test analytics endpoints
        analytics_endpoints = [
            ("/documents/analytics/categories", "Document categories analytics"),
            ("/documents/analytics/recent?days=30", "Recent documents"),
        ]
        
        for endpoint, description in analytics_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(description, True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(description, False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
        
        # Test search by tags (will return empty but should not error)
        try:
            response = self.session.get(f"{self.base_url}/documents/search/tags?tags=medical,equipment")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Search documents by tags", True, f"Found {data.get('count', 0)} documents")
            else:
                self.log_test("Search documents by tags", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Search documents by tags", False, f"Exception: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        print("\n=== Testing Error Handling ===")
        
        # Test invalid IDs
        invalid_id_tests = [
            ("/schedule/appointments/invalid-id", "Invalid appointment ID"),
            ("/maintenance/spare-parts/invalid-id", "Invalid spare part ID"),
            ("/quiz/questions/invalid-id", "Invalid question ID"),
            ("/request/demo-requests/invalid-id", "Invalid request ID"),
            ("/documents/invalid-id", "Invalid document ID")
        ]
        
        for endpoint, description in invalid_id_tests:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 404:
                    self.log_test(description, True, "Correctly returned 404")
                else:
                    self.log_test(description, False, f"Expected 404, got {response.status_code}")
            except Exception as e:
                self.log_test(description, False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Starting Clinical Assets Dashboard Backend API Tests")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all test modules
        self.test_basic_api_health()
        self.test_dashboard_module()
        self.test_schedule_module()
        self.test_maintenance_module()
        self.test_quiz_module()
        self.test_request_module()
        self.test_documents_module()
        self.test_error_handling()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        return passed_tests, failed_tests

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()
