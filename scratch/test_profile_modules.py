import sys
import unittest
from pathlib import Path
from database.database import (
    init_db,
    execute_query,
    get_user_projects,
    get_user_certificates
)
from services.project_service import create_project, edit_project, remove_project, fetch_user_projects
from services.certificate_service import create_certificate, edit_certificate, remove_certificate, fetch_user_certificates
from services.profile_service import get_full_user_profile, calculate_profile_completion_details
from services.resume_service import get_user_active_resume, delete_user_resume

class TestProfileModuleExpansion(unittest.TestCase):
    
    def setUp(self):
        init_db()
        self.user_id = 999  # Test user
        # Clean test user records
        execute_query("DELETE FROM projects WHERE user_id = %s", (self.user_id,), commit=True)
        execute_query("DELETE FROM certificates WHERE user_id = %s", (self.user_id,), commit=True)
        execute_query("DELETE FROM resumes WHERE user_id = %s", (self.user_id,), commit=True)

    def test_project_crud(self):
        # 1. Validation error on missing name
        ok, msg, _ = create_project(self.user_id, {"project_name": "", "description": "Desc"})
        self.assertFalse(ok)

        # 2. Add Project 1
        ok1, msg1, pid1 = create_project(self.user_id, {
            "project_name": "AI Resume Screening System",
            "description": "Streamlit & Python platform",
            "technologies": "Python, Streamlit, MySQL",
            "project_role": "Lead Engineer",
            "project_type": "AI / ML System"
        })
        self.assertTrue(ok1)
        self.assertGreater(pid1, 0)

        # 3. Add Project 2 (Multiple projects)
        ok2, msg2, pid2 = create_project(self.user_id, {
            "project_name": "Financial Fraud Detection",
            "description": "ML Fraud Detection Model",
            "technologies": "Python, ML, Streamlit",
            "project_role": "Data Scientist",
            "project_type": "Personal Project"
        })
        self.assertTrue(ok2)

        # Verify multiple projects stored
        projs = fetch_user_projects(self.user_id)
        self.assertEqual(len(projs), 2)

        # 4. Edit Project 1
        e_ok, e_msg = edit_project(pid1, self.user_id, {
            "project_name": "AI Resume Screening System v2",
            "description": "Updated Streamlit & Python platform",
            "technologies": "Python, Streamlit, MySQL, PyTorch"
        })
        self.assertTrue(e_ok)

        # 5. Delete Project 2
        d_ok, d_msg = remove_project(self.user_id, pid2)
        self.assertTrue(d_ok)

        projs_after = fetch_user_projects(self.user_id)
        self.assertEqual(len(projs_after), 1)
        self.assertEqual(projs_after[0]["project_name"], "AI Resume Screening System v2")

    def test_certificate_crud(self):
        # 1. Add Certificate 1
        ok1, msg1, cid1 = create_certificate(self.user_id, {
            "certificate_name": "Python for Data Science",
            "issuing_organization": "Google",
            "issue_date": "2026-08-01"
        })
        self.assertTrue(ok1)

        # 2. Add Certificate 2
        ok2, msg2, cid2 = create_certificate(self.user_id, {
            "certificate_name": "Machine Learning Certificate",
            "issuing_organization": "Infosys",
            "issue_date": "2026-07-15"
        })
        self.assertTrue(ok2)

        certs = fetch_user_certificates(self.user_id)
        self.assertEqual(len(certs), 2)

        # 3. Delete Certificate 1
        d_ok, d_msg = remove_certificate(self.user_id, cid1)
        self.assertTrue(d_ok)

        certs_after = fetch_user_certificates(self.user_id)
        self.assertEqual(len(certs_after), 1)

    def test_profile_completion_details(self):
        # Add project & cert
        create_project(self.user_id, {"project_name": "P1", "description": "D1"})
        create_certificate(self.user_id, {"certificate_name": "C1", "issuing_organization": "O1"})

        details = calculate_profile_completion_details(self.user_id)
        self.assertIn("percentage", details)
        self.assertTrue(details["checklist"]["Projects"]["status"])
        self.assertEqual(details["checklist"]["Projects"]["count"], 1)

if __name__ == "__main__":
    unittest.main()
