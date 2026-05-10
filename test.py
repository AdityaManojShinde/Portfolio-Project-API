import unittest
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

class TestPortfolioAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class: login and store the authentication token."""
        cls.username = os.getenv("USERNAME", "admin")
        cls.password = os.getenv("PASSWORD", "admin")
        
        # Test login
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": cls.username, "password": cls.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to login and get token. Status: {response.status_code}, Response: {response.text}")
        
        token = response.json().get("access_token")
        cls.headers = {"Authorization": f"Bearer {token}"}
        
        # Storage for IDs created during tests
        cls.project_id = None
        cls.education_id = None
        cls.certification_id = None

    def test_01_auth_me(self):
        """Test GET /auth/me"""
        response = requests.get(f"{BASE_URL}/auth/me", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("username"), self.username)

    def test_02_projects_crud(self):
        """Test Project CRUD operations"""
        # Create Project
        project_data = {
            "title": "Test Project",
            "description": "A project created by unit tests",
            "tech_stack": ["Python", "FastAPI"],
            "github_link": "https://github.com/test/test"
        }
        response = requests.post(f"{BASE_URL}/project/", json=project_data, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Failed to create project: {response.text}")
        project = response.json()
        self.__class__.project_id = project.get("id")
        self.assertIsNotNone(self.project_id)
        
        # Read Project
        response = requests.get(f"{BASE_URL}/project/{self.project_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Test Project")
        
        # Update Project
        update_data = {"title": "Updated Test Project"}
        response = requests.patch(f"{BASE_URL}/project/{self.project_id}", json=update_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Updated Test Project")
        
        # List Projects
        response = requests.get(f"{BASE_URL}/project/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(p["id"] == self.project_id for p in response.json()))
        
        # Delete Project
        response = requests.delete(f"{BASE_URL}/project/{self.project_id}", headers=self.headers)
        self.assertEqual(response.status_code, 204)

    def test_03_user_info_crud(self):
        """Test User Info CRUD operations"""
        # Create or update User Info
        user_info_data = {"name": "Test User", "bio": "Test Bio"}
        response = requests.post(f"{BASE_URL}/user-info/", json=user_info_data, headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to create user info: {response.text}")
        self.assertEqual(response.json().get("name"), "Test User")
        
        # Read User Info
        response = requests.get(f"{BASE_URL}/user-info/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), "Test User")
        
        # Update User Info
        update_data = {"name": "Updated Test User"}
        response = requests.patch(f"{BASE_URL}/user-info/", json=update_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), "Updated Test User")
        
        # Delete User Info
        response = requests.delete(f"{BASE_URL}/user-info/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_04_contact_crud(self):
        """Test Contact CRUD operations"""
        # Create or update Contact
        contact_data = {"email": "test@example.com"}
        response = requests.post(f"{BASE_URL}/contact/", json=contact_data, headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to create contact: {response.text}")
        self.assertEqual(response.json().get("email"), "test@example.com")
        
        # Read Contact
        response = requests.get(f"{BASE_URL}/contact/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("email"), "test@example.com")
        
        # Update Contact
        update_data = {"email": "updated@example.com"}
        response = requests.patch(f"{BASE_URL}/contact/", json=update_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("email"), "updated@example.com")
        
        # Delete Contact
        response = requests.delete(f"{BASE_URL}/contact/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_05_education_crud(self):
        """Test Education CRUD operations"""
        # Create Education
        education_data = {
            "institution_name": "Test University",
            "degree": "B.Sc. Test"
        }
        response = requests.post(f"{BASE_URL}/education/", json=education_data, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Failed to create education: {response.text}")
        education = response.json()
        self.__class__.education_id = education.get("id")
        self.assertIsNotNone(self.education_id)
        
        # Read Education
        response = requests.get(f"{BASE_URL}/education/{self.education_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("institution_name"), "Test University")
        
        # Update Education
        update_data = {"institution_name": "Updated University"}
        response = requests.patch(f"{BASE_URL}/education/{self.education_id}", json=update_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("institution_name"), "Updated University")
        
        # List Education
        response = requests.get(f"{BASE_URL}/education/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(e["id"] == self.education_id for e in response.json()))
        
        # Delete Education
        response = requests.delete(f"{BASE_URL}/education/{self.education_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_06_certification_crud(self):
        """Test Certification CRUD operations"""
        # Create Certification
        cert_data = {
            "name": "Test Certificate",
            "issuing_organization": "Test Org"
        }
        response = requests.post(f"{BASE_URL}/certification/", json=cert_data, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Failed to create certification: {response.text}")
        cert = response.json()
        self.__class__.certification_id = cert.get("id")
        self.assertIsNotNone(self.certification_id)
        
        # Read Certification
        response = requests.get(f"{BASE_URL}/certification/{self.certification_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), "Test Certificate")
        
        # Update Certification
        update_data = {"name": "Updated Certificate"}
        response = requests.patch(f"{BASE_URL}/certification/{self.certification_id}", json=update_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), "Updated Certificate")
        
        # List Certifications
        response = requests.get(f"{BASE_URL}/certification/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(c["id"] == self.certification_id for c in response.json()))
        
        # Delete Certification
        response = requests.delete(f"{BASE_URL}/certification/{self.certification_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main(verbosity=2)
