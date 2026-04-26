import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

from backend.app.services.recommendation_service import scrape_real_review, recommendation_service

def test_scrape():
    print("Testing scrape_real_review...")
    review = scrape_real_review("Dr. Rakesh Gupta", "New York")
    print(f"Scraped review: {review}")

def test_recommendation():
    print("\nTesting get_doctors_recommendation...")
    doctors = recommendation_service.get_doctors_recommendation("Heart Disease", "New York")
    for doc in doctors:
        print(f"Doctor: {doc['doctor_name']}, Rating: {doc['rating']}")
        # Profile URL removed
        print(f"  Review: {doc.get('patient_review')}")

if __name__ == "__main__":
    test_scrape()
    test_recommendation()
