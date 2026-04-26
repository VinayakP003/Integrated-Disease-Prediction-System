import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

from backend.app.services.recommendation_service import recommendation_service

def test_facilities():
    print("Testing fetch_nearby_facilities_mock...")
    facilities = recommendation_service.fetch_nearby_facilities_mock("New York")
    for fac in facilities:
        print(f"Facility: {fac['name']}, Address: {fac['address']}, Rating: {fac['rating']}")

if __name__ == "__main__":
    test_facilities()
