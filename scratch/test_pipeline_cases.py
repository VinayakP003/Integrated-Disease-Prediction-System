import sys
import os

# Add root project path to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.schemas.prediction import CHRIPredictionInput, HeartPredictionInput, DiabetesPredictionInput, StrokePredictionInput, CKDPredictionInput
from backend.app.services.prediction_service import prediction_service
from backend.app.services.recommendation_service import recommendation_service

# Base "normal" parameters
def get_normal_heart():
    return HeartPredictionInput(age=30, sex=1, cp=0, trestbps=110, chol=150, fbs=0, restecg=0, thalach=180, exang=0, oldpeak=0.0, slope=2, ca=0, thal=2)

def get_normal_diabetes():
    return DiabetesPredictionInput(Pregnancies=0, Glucose=90, BloodPressure=70, SkinThickness=20, Insulin=30, BMI=22.0, DiabetesPedigreeFunction=0.2, Age=30)

def get_normal_stroke():
    return StrokePredictionInput(gender="Male", age=30.0, hypertension=0, heart_disease=0, ever_married="No", work_type="Private", Residence_type="Urban", avg_glucose_level=90.0, bmi=22.0, smoking_status="never smoked")

def get_normal_ckd():
    return CKDPredictionInput(age=30, bp=70, sg=1.020, al=0, su=0, rbc="normal", pc="normal", pcc="notpresent", ba="notpresent", bgr=90, bu=20, sc=0.8, sod=140, pot=4.0, hemo=15.0, pcv=45, wc=8000, rc=5.0, htn="no", dm="no", cad="no", appet="good", pe="no", ane="no")


cases = {
    "1. All Normal": {
        "heart": get_normal_heart(),
        "diabetes": get_normal_diabetes(),
        "stroke": get_normal_stroke(),
        "ckd": get_normal_ckd()
    },
    "2. High Heart Risk": {
        "heart": HeartPredictionInput(age=65, sex=1, cp=3, trestbps=160, chol=280, fbs=1, restecg=1, thalach=110, exang=1, oldpeak=3.0, slope=1, ca=3, thal=3),
        "diabetes": get_normal_diabetes(),
        "stroke": get_normal_stroke(),
        "ckd": get_normal_ckd()
    },
    "3. High Diabetes Risk": {
        "heart": get_normal_heart(),
        "diabetes": DiabetesPredictionInput(Pregnancies=3, Glucose=190, BloodPressure=90, SkinThickness=40, Insulin=150, BMI=35.0, DiabetesPedigreeFunction=0.8, Age=55),
        "stroke": get_normal_stroke(),
        "ckd": get_normal_ckd()
    },
    "4. High Stroke Risk": {
        "heart": get_normal_heart(),
        "diabetes": get_normal_diabetes(),
        "stroke": StrokePredictionInput(gender="Male", age=75.0, hypertension=1, heart_disease=1, ever_married="Yes", work_type="Self-employed", Residence_type="Urban", avg_glucose_level=230.0, bmi=38.0, smoking_status="smokes"),
        "ckd": get_normal_ckd()
    },
    "5. High CKD Risk": {
        "heart": get_normal_heart(),
        "diabetes": get_normal_diabetes(),
        "stroke": get_normal_stroke(),
        "ckd": CKDPredictionInput(age=60, bp=100, sg=1.010, al=4, su=2, rbc="abnormal", pc="abnormal", pcc="present", ba="present", bgr=150, bu=80, sc=4.5, sod=130, pot=6.0, hemo=9.0, pcv=30, wc=12000, rc=3.0, htn="yes", dm="yes", cad="yes", appet="poor", pe="yes", ane="yes")
    },
    "6. Critical (Multiple High Risks)": {
        "heart": HeartPredictionInput(age=65, sex=1, cp=3, trestbps=160, chol=280, fbs=1, restecg=1, thalach=110, exang=1, oldpeak=3.0, slope=1, ca=3, thal=3),
        "diabetes": DiabetesPredictionInput(Pregnancies=3, Glucose=190, BloodPressure=90, SkinThickness=40, Insulin=150, BMI=35.0, DiabetesPedigreeFunction=0.8, Age=55),
        "stroke": StrokePredictionInput(gender="Male", age=75.0, hypertension=1, heart_disease=1, ever_married="Yes", work_type="Self-employed", Residence_type="Urban", avg_glucose_level=230.0, bmi=38.0, smoking_status="smokes"),
        "ckd": CKDPredictionInput(age=60, bp=100, sg=1.010, al=4, su=2, rbc="abnormal", pc="abnormal", pcc="present", ba="present", bgr=150, bu=80, sc=4.5, sod=130, pot=6.0, hemo=9.0, pcv=30, wc=12000, rc=3.0, htn="yes", dm="yes", cad="yes", appet="poor", pe="yes", ane="yes")
    }
}

for case_name, inputs in cases.items():
    print(f"\n{'='*50}\nTesting Case: {case_name}\n{'='*50}")
    chri_input = CHRIPredictionInput(**inputs)
    
    # Run predictions
    heart_prob, _ = prediction_service.predict_heart(chri_input.heart)
    diabetes_prob, _ = prediction_service.predict_diabetes(chri_input.diabetes)
    stroke_prob, _ = prediction_service.predict_stroke(chri_input.stroke)
    ckd_prob, _ = prediction_service.predict_ckd(chri_input.ckd)
    
    risks = {
        'heart': heart_prob,
        'diabetes': diabetes_prob,
        'stroke': stroke_prob,
        'ckd': ckd_prob
    }
    chri_score = prediction_service.calculate_chri(risks)
    
    print(f"Probabilities -> Heart: {heart_prob:.2f}, Diabetes: {diabetes_prob:.2f}, Stroke: {stroke_prob:.2f}, CKD: {ckd_prob:.2f}, CHRI: {chri_score:.2f}")
    
    action_recs = recommendation_service.get_action_recommendation({
        'heart_risk': heart_prob,
        'diabetes_risk': diabetes_prob,
        'stroke_risk': stroke_prob,
        'ckd_risk': ckd_prob,
        'chri_score': chri_score
    })
    
    print(f"Overall Risk Level : {action_recs['risk_level']}")
    print(f"Urgency Level      : {action_recs['urgency_level']}")
    print(f"Primary Specialist : {action_recs['primary_specialist']}")
    print(f"Recommended Specs  : {', '.join(action_recs['recommended_specialists'])}")
    print(f"Suggested Actions  :")
    for action in action_recs['suggested_actions']:
        print(f"  - {action}")
        
    doctors = []
    for spec in action_recs.get("recommended_specialists", []):
        disease = "Heart Disease" if spec == "Cardiologist" else \
                  "Diabetes" if spec == "Endocrinologist" else \
                  "Stroke" if spec == "Neurologist" else \
                  "Chronic Kidney Disease" if spec == "Nephrologist" else \
                  "General Practitioner"
        docs = recommendation_service.get_doctors_recommendation(disease_focus=disease)
        if docs:
            doctors.append((spec, docs[0]['doctor_name']))
    print("Fetched Mock Doctors:")
    for spec, doc in doctors:
        print(f"  - {spec} -> {doc}")
