import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from backend.app.schemas.prediction import CHRIPredictionInput
from backend.app.services.prediction_service import prediction_service
from backend.app.services.recommendation_service import recommendation_service

# Mock payload
payload = {
    "heart": {
        "age": 65, "sex": 1, "cp": 3, "trestbps": 150, "chol": 240, "fbs": 1, 
        "restecg": 1, "thalach": 140, "exang": 1, "oldpeak": 1.5, "slope": 1, "ca": 1, "thal": 2
    },
    "diabetes": {
        "Pregnancies": 0, "Glucose": 160, "BloodPressure": 150, "SkinThickness": 20,
        "Insulin": 80, "BMI": 33.6, "DiabetesPedigreeFunction": 0.5, "Age": 65
    },
    "stroke": {
        "gender": "Male", "age": 65, "hypertension": 1, "heart_disease": 1, 
        "ever_married": "Yes", "work_type": "Private", "Residence_type": "Urban", 
        "avg_glucose_level": 160, "bmi": 33.6, "smoking_status": "smokes"
    },
    "ckd": {
        "age": 65, "bp": 150, "sg": 1.015, "al": 2, "su": 0, "rbc": "normal", "pc": "abnormal", 
        "pcc": "present", "ba": "notpresent", "bgr": 160, "bu": 40, "sc": 1.5, "sod": 135, 
        "pot": 4.0, "hemo": 11.0, "pcv": 32, "wc": 6000, "rc": 4.0, "htn": "yes", "dm": "yes", 
        "cad": "no", "appet": "poor", "pe": "yes", "ane": "yes"
    }
}

try:
    print("Starting full pipeline test...")
    data = CHRIPredictionInput(**payload)
    
    heart_prob, heart_factors = prediction_service.predict_heart(data.heart)
    diabetes_prob, diag_factors = prediction_service.predict_diabetes(data.diabetes)
    stroke_prob, stroke_factors = prediction_service.predict_stroke(data.stroke)
    ckd_prob, ckd_factors = prediction_service.predict_ckd(data.ckd)
    
    risks = {
        'heart': heart_prob,
        'diabetes': diabetes_prob,
        'stroke': stroke_prob,
        'ckd': ckd_prob
    }
    
    chri_score = prediction_service.calculate_chri(risks)
    
    print("Calling get_action_recommendation...")
    action_recs = recommendation_service.get_action_recommendation({
        'heart_risk': heart_prob,
        'diabetes_risk': diabetes_prob,
        'stroke_risk': stroke_prob,
        'ckd_risk': ckd_prob,
        'chri_score': chri_score
    })
    
    print("Calling get_doctors_recommendation for each specialist...")
    doctors = []
    for spec in action_recs.get("recommended_specialists", []):
        print(f"  Fetching for: {spec}")
        disease = "Heart Disease" if spec == "Cardiologist" else \
                  "Diabetes" if spec == "Endocrinologist" else \
                  "Stroke" if spec == "Neurologist" else \
                  "Chronic Kidney Disease" if spec == "Nephrologist" else \
                  "General Practitioner"
        docs = recommendation_service.get_doctors_recommendation(disease_focus=disease)
        if docs:
            doctors.append(docs[0])
            print(f"    Found: {docs[0]['doctor_name']}")

    result = {
        "heart": round(float(heart_prob), 4),
        "diabetes": round(float(diabetes_prob), 4),
        "stroke": round(float(stroke_prob), 4),
        "ckd": round(float(ckd_prob), 4),
        "chri_score": round(float(chri_score), 4),
        "risk_level": action_recs["risk_level"],
        "recommendations": {
            "urgency_level": action_recs["urgency_level"],
            "suggested_actions": action_recs["suggested_actions"],
            "recommended_doctors": doctors
        }
    }
    print("Full result generated successfully!")
    # print(json.dumps(result, indent=2))

except Exception as e:
    import traceback
    print("CRASH DETECTED!")
    traceback.print_exc()
