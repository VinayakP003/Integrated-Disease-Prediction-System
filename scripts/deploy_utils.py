import joblib
import pandas as pd
import numpy as np
import os

MODEL_DIR = 'models/exported'
DISEASES = ['heart', 'diabetes', 'stroke', 'ckd']
ENSEMLE_TYPES = ['voting_soft', 'stacking']

def load_all_models(ensemble_type='voting_soft'):
    """
    Loads one ensemble model for each disease.
    """
    models = {}
    for disease in DISEASES:
        # Check for optimized versions first
        opt_path = os.path.join(MODEL_DIR, f'{disease}_optimized_voting_optimized.joblib')
        path = os.path.join(MODEL_DIR, f'{disease}_{ensemble_type}.joblib')
        
        if os.path.exists(opt_path):
            models[disease] = joblib.load(opt_path)
            print(f"Loaded Optimized model for {disease}")
        elif os.path.exists(path):
            models[disease] = joblib.load(path)
        else:
            print(f"Warning: Model not found at {path}")

    return models

def predict_single_patient(models, patient_data_dict):
    """
    Takes a dictionary of feature data and returns probabilities for each disease.
    The dictionary should be formatted to be compatible with each disease preprocessor.
    """
    results = {}
    
    # Create a DataFrame from the dict for compatibility
    df = pd.DataFrame([patient_data_dict])
    
    for disease, model in models.items():
        try:
            # The model is a Pipeline (preprocessor -> classifier)
            prob = model.predict_proba(df)[0][1] # Probability of target=1
            results[disease] = prob
        except Exception as e:
            print(f"Error predicting {disease}: {e}")
            results[disease] = None
            
    return results

def calculate_global_risk_score(risks):
    """
    Combines disease probabilities into a single risk score.
    Weights are heuristic based on relative clinical severity and prevalence.
    """
    # Weights sum to 1.0
    weights = {
        'heart': 0.35,
        'stroke': 0.30,
        'diabetes': 0.20,
        'ckd': 0.15
    }
    
    score = 0
    total_weight = 0
    for disease, prob in risks.items():
        if prob is not None:
            score += prob * weights[disease]
            total_weight += weights[disease]
            
    if total_weight == 0:
        return 0
    
    # Re-normalize if some models failed
    return score / total_weight

def get_risk_label(score):
    if score < 0.2:
        return 'Low'
    elif score < 0.4:
        return 'Moderate'
    elif score < 0.7:
        return 'High'
    else:
        return 'Critical'

if __name__ == "__main__":
    # Example usage (Dummy data)
    print("Loading models...")
    models = load_all_models('voting_soft')
    
    # Heart features: ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
    # Diabetes: ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    # Stroke: ['age', 'avg_glucose_level', 'bmi', 'gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
    # CKD: many...
    
    # For a real prediction, we'd need a full set of columns. 
    # This script is primarily for the framework definition.
    print("Models Loaded. Framework Ready.")
