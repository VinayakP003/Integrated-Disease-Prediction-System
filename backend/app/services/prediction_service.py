import joblib
import pandas as pd
import os
from pathlib import Path
from backend.app.schemas.prediction import (
    HeartPredictionInput, 
    DiabetesPredictionInput, 
    StrokePredictionInput, 
    CKDPredictionInput
)

class PredictionService:
    def __init__(self):
        # Base path relative to where the server runs (project root)
        self.model_dir = Path("models/exported")
        self.models = {}
        self.load_models()

    def load_models(self):
        # We will use the Voting (Soft) ensemble as our primary one for the backend
        model_files = {
            'heart': 'heart_voting_(soft).joblib',
            'diabetes': 'diabetes_voting_(soft).joblib',
            'stroke': 'stroke_voting_(soft).joblib',
            'ckd': 'ckd_voting_(soft).joblib'
        }
        
        for disease, filename in model_files.items():
            path = self.model_dir / filename
            if path.exists():
                print(f"Loading {disease} model from {path}...")
                self.models[disease] = joblib.load(path)
            else:
                print(f"Warning: Model not found at {path}")

    def predict_heart(self, data: HeartPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['heart'].predict_proba(df)[0][1]
        return prob

    def predict_diabetes(self, data: DiabetesPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['diabetes'].predict_proba(df)[0][1]
        return prob

    def predict_stroke(self, data: StrokePredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['stroke'].predict_proba(df)[0][1]
        return prob

    def predict_ckd(self, data: CKDPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['ckd'].predict_proba(df)[0][1]
        return prob

    def get_risk_level(self, prob: float):
        if prob < 0.2:
            return "Low"
        elif prob < 0.4:
            return "Moderate"
        elif prob < 0.7:
            return "High"
        else:
            return "Critical"

    def calculate_chri(self, risks: dict):
        weights = {
            'heart': 0.35,
            'stroke': 0.30,
            'diabetes': 0.20,
            'ckd': 0.15
        }
        chri = sum(risks[d] * weights[d] for d in weights if risks[d] is not None)
        return chri

# Singleton instance
prediction_service = PredictionService()
