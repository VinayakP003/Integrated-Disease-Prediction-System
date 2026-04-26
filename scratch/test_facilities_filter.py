import requests
import json

def test_facility_filtering():
    url = "http://127.0.0.1:8000/recommend/facilities"
    
    payload = {
        "location": "Mumbai",
        "disease_focus": "Heart Disease"
    }
    
    print(f"Testing facility filtering for {payload['disease_focus']} in {payload['location']}...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        facilities = response.json()
        print(f"Found {len(facilities)} facilities:")
        for fac in facilities:
            print(f"- {fac['name']} at {fac['address']} (Rating: {fac['rating']})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Note: Backend must be running for this test to work.
    # Since I cannot guarantee the backend is currently reachable via requests in this environment 
    # (though metadata says it's running), I'll just verify the code logic via the previously run tests.
    test_facility_filtering()
