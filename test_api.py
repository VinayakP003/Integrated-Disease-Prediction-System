import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_heart():
    print("Testing Heart Prediction...")
    payload = {
        "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, 
        "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
    }
    response = requests.post(f"{BASE_URL}/predict/heart", json=payload)
    print(response.json())

def test_diabetes():
    print("\nTesting Diabetes Prediction...")
    payload = {
        "Pregnancies": 6, "Glucose": 148, "BloodPressure": 72, "SkinThickness": 35,
        "Insulin": 0, "BMI": 33.6, "DiabetesPedigreeFunction": 0.627, "Age": 50
    }
    response = requests.post(f"{BASE_URL}/predict/diabetes", json=payload)
    print(response.json())

if __name__ == "__main__":
    # Start the server independently, then run this
    try:
        test_heart()
        test_diabetes()
    except Exception as e:
        print(f"Could not connect to server. Ensure it's running. Error: {e}")
