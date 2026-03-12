from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction import (
    HeartPredictionInput,
    DiabetesPredictionInput,
    StrokePredictionInput,
    CKDPredictionInput,
    CHRIPredictionInput
)
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/predict/heart")
async def predict_heart(data: HeartPredictionInput):
    try:
        prob = prediction_service.predict_heart(data)
        return {
            "disease": "Heart Disease",
            "risk_probability": round(float(prob), 4),
            "risk_level": prediction_service.get_risk_level(prob)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesPredictionInput):
    try:
        prob = prediction_service.predict_diabetes(data)
        return {
            "disease": "Diabetes",
            "risk_probability": round(float(prob), 4),
            "risk_level": prediction_service.get_risk_level(prob)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/stroke")
async def predict_stroke(data: StrokePredictionInput):
    try:
        prob = prediction_service.predict_stroke(data)
        return {
            "disease": "Stroke",
            "risk_probability": round(float(prob), 4),
            "risk_level": prediction_service.get_risk_level(prob)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/ckd")
async def predict_ckd(data: CKDPredictionInput):
    try:
        prob = prediction_service.predict_ckd(data)
        return {
            "disease": "Chronic Kidney Disease",
            "risk_probability": round(float(prob), 4),
            "risk_level": prediction_service.get_risk_level(prob)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/chri")
async def predict_chri(data: CHRIPredictionInput):
    try:
        heart_prob = prediction_service.predict_heart(data.heart)
        diabetes_prob = prediction_service.predict_diabetes(data.diabetes)
        stroke_prob = prediction_service.predict_stroke(data.stroke)
        ckd_prob = prediction_service.predict_ckd(data.ckd)
        
        risks = {
            'heart': heart_prob,
            'diabetes': diabetes_prob,
            'stroke': stroke_prob,
            'ckd': ckd_prob
        }
        
        chri_score = prediction_service.calculate_chri(risks)
        
        return {
            "heart": round(float(heart_prob), 4),
            "diabetes": round(float(diabetes_prob), 4),
            "stroke": round(float(stroke_prob), 4),
            "ckd": round(float(ckd_prob), 4),
            "chri_score": round(float(chri_score), 4),
            "risk_level": prediction_service.get_risk_level(chri_score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
