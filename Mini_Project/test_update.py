#!/usr/bin/env python
"""
Quick Test Script to Verify Patient Update Functionality
Run this after starting the Flask app to test if updates work
"""

import requests
import json
from time import sleep

BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

def test_login():
    """Test login"""
    print("\n🔐 Testing Login...")
    data = {
        "email": "kesavan@example.com",  # Change to your test user
        "password": "test123"  # Change to your test password
    }
    response = SESSION.post(f"{BASE_URL}/login", data=data)
    print(f"✅ Login status: {response.status_code}")
    return response.status_code == 200

def test_fetch_patients():
    """Fetch all patients"""
    print("\n📋 Fetching Patients...")
    response = SESSION.get(f"{BASE_URL}/api/patients")
    if response.status_code == 200:
        patients = response.json().get('patients', [])
        print(f"✅ Found {len(patients)} patients")
        if patients:
            return patients[0]['id']
    return None

def test_update_patient(patient_id):
    """Test updating a patient"""
    print(f"\n✏️ Testing Update for Patient ID: {patient_id}")
    
    update_data = {
        "first_name": "Updated",
        "last_name": "TestPatient",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "contact_number": "9876543210",
        "email": "updated@test.com",
        "primary_diagnosis": "Updated Diagnosis",
        "attending_physician": "Dr. Updated",
        "admission_date": "2025-10-24",
        "status": "discharged",
        "notes": "This is an updated test note"
    }
    
    response = SESSION.put(
        f"{BASE_URL}/api/patient/{patient_id}",
        headers={"Content-Type": "application/json"},
        json=update_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Patient Updated Successfully!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def main():
    print("=" * 60)
    print("🏥 MedCare Patient Update Test Script")
    print("=" * 60)
    
    # Note: Adjust credentials as needed
    if test_login():
        patient_id = test_fetch_patients()
        if patient_id:
            if test_update_patient(patient_id):
                print("\n✅ ALL TESTS PASSED! Update functionality is working!")
            else:
                print("\n❌ Update test failed")
        else:
            print("\n❌ No patients found")
    else:
        print("\n❌ Login failed - Check credentials")

if __name__ == "__main__":
    main()
