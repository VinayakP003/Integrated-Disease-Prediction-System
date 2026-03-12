from pydantic import BaseModel, Field
from typing import Optional

class HeartPredictionInput(BaseModel):
    age: float
    sex: int # 1 = male, 0 = female
    cp: int # chest pain type (0-3)
    trestbps: float # resting blood pressure
    chol: float # serum cholesterol
    fbs: int # fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
    restecg: int # resting electrocardiographic results (0-2)
    thalach: float # maximum heart rate achieved
    exang: int # exercise induced angina (1 = yes; 0 = no)
    oldpeak: float # ST depression induced by exercise relative to rest
    slope: int # the slope of the peak exercise ST segment (0-2)
    ca: int # number of major vessels (0-3)
    thal: int # 3 = normal; 6 = fixed defect; 7 = reversible defect (mapped as 1,2,3 in many cleaned versions)

    class Config:
        json_schema_extra = {
            "example": {
                "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, 
                "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
            }
        }

class DiabetesPredictionInput(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

    class Config:
        json_schema_extra = {
            "example": {
                "Pregnancies": 6, "Glucose": 148, "BloodPressure": 72, "SkinThickness": 35,
                "Insulin": 0, "BMI": 33.6, "DiabetesPedigreeFunction": 0.627, "Age": 50
            }
        }

class StrokePredictionInput(BaseModel):
    gender: str # 'Male', 'Female', 'Other'
    age: float
    hypertension: int # 0 or 1
    heart_disease: int # 0 or 1
    ever_married: str # 'Yes' or 'No'
    work_type: str # 'Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'
    Residence_type: str # 'Urban' or 'Rural'
    avg_glucose_level: float
    bmi: float
    smoking_status: str # 'formerly smoked', 'never smoked', 'smokes', 'Unknown'

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male", "age": 67.0, "hypertension": 0, "heart_disease": 1, "ever_married": "Yes",
                "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 228.69, "bmi": 36.6, 
                "smoking_status": "formerly smoked"
            }
        }

class CKDPredictionInput(BaseModel):
    age: Optional[float] = None
    bp: Optional[float] = None
    sg: Optional[float] = None # 1.005, 1.010, 1.015, 1.020, 1.025
    al: Optional[float] = None # 0, 1, 2, 3, 4, 5
    su: Optional[float] = None # 0, 1, 2, 3, 4, 5
    rbc: Optional[str] = "normal" # 'normal', 'abnormal'
    pc: Optional[str] = "normal" # 'normal', 'abnormal'
    pcc: Optional[str] = "notpresent" # 'present', 'notpresent'
    ba: Optional[str] = "notpresent" # 'present', 'notpresent'
    bgr: Optional[float] = None
    bu: Optional[float] = None
    sc: Optional[float] = None
    sod: Optional[float] = None
    pot: Optional[float] = None
    hemo: Optional[float] = None
    pcv: Optional[float] = None
    wc: Optional[float] = None
    rc: Optional[float] = None
    htn: Optional[str] = "no" # 'yes', 'no'
    dm: Optional[str] = "no" # 'yes', 'no'
    cad: Optional[str] = "no" # 'yes', 'no'
    appet: Optional[str] = "good" # 'good', 'poor'
    pe: Optional[str] = "no" # 'yes', 'no'
    ane: Optional[str] = "no" # 'yes', 'no'

    class Config:
        json_schema_extra = {
            "example": {
                "age": 48, "bp": 80, "sg": 1.02, "al": 1, "su": 0, "rbc": "normal", "pc": "normal",
                "pcc": "notpresent", "ba": "notpresent", "bgr": 121, "bu": 36, "sc": 1.2, "sod": 135,
                "pot": 4.5, "hemo": 15.4, "pcv": 44, "wc": 7800, "rc": 5.2, "htn": "yes", "dm": "yes",
                "cad": "no", "appet": "good", "pe": "no", "ane": "no"
            }
        }

class CHRIPredictionInput(BaseModel):
    # This combines all features or uses common ones
    # For Week 5, specifically for calculated risk, we need everything.
    # However, to be practical, a user could provide a combined dictionary.
    heart: HeartPredictionInput
    diabetes: DiabetesPredictionInput
    stroke: StrokePredictionInput
    ckd: CKDPredictionInput
