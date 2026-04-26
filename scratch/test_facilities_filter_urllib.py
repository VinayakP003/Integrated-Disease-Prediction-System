import urllib.request
import urllib.parse
import json

def test_facility_filtering():
    url = "http://127.0.0.1:8000/recommend/facilities"
    
    payload = {
        "location": "Mumbai",
        "disease_focus": "Heart Disease"
    }
    
    print(f"Testing facility filtering for {payload['disease_focus']} in {payload['location']}...")
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            facilities = json.loads(response.read().decode())
            print(f"Found {len(facilities)} facilities:")
            for fac in facilities:
                print(f"- {fac['name']} at {fac['address']} (Rating: {fac['rating']})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_facility_filtering()
