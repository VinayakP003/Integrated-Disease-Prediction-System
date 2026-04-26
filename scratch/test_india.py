import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.recommendation_service import recommendation_service

def test_indian_recommendation():
    print("Testing recommendation service for India (New Delhi)...")
    doctors = recommendation_service.get_doctors_recommendation("Heart Disease", "New Delhi")
    print(f"Found {len(doctors)} doctors")
    for doc in doctors:
        print(f"- {doc['doctor_name']} ({doc['specialization']}) at {doc['location']}")
        print(f"  Review: {doc.get('patient_review', 'N/A')[:100]}...")

    print("\nTesting fallback with Indian mock data...")
    doctors_mock = recommendation_service.get_doctors_recommendation("Neurologist", "")
    print(f"Found {len(doctors_mock)} doctors")
    for doc in doctors_mock:
        print(f"- {doc['doctor_name']} ({doc['specialization']})")

if __name__ == "__main__":
    test_indian_recommendation()
