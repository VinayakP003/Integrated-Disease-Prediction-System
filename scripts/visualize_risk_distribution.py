import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

def load_data():
    # Load test sets (re-split for consistency or just load full if small)
    heart = pd.read_csv('data/cleaned/heart_disease_cleaned.csv')
    diabetes = pd.read_csv('data/cleaned/diabetes_cleaned.csv')
    stroke = pd.read_csv('data/cleaned/stroke_cleaned.csv')
    ckd = pd.read_csv('data/cleaned/ckd_cleaned.csv')
    return heart, diabetes, stroke, ckd

def generate_risk_distribution():
    print("Generating Risk Distribution...")
    
    # Load Models
    models = {
        'heart': joblib.load('models/exported/heart_voting_(soft).joblib'),
        'diabetes': joblib.load('models/exported/diabetes_voting_(soft).joblib'),
        'stroke': joblib.load('models/exported/stroke_voting_(soft).joblib'),
        'ckd': joblib.load('models/exported/ckd_voting_(soft).joblib')
    }
    
    heart_df, diabetes_df, stroke_df, ckd_df = load_data()
    
    # Create a synthetic population of 200 patients by randomly sampling from each dataset
    # (Simplified approach since we don't have a single multi-target dataset)
    n_samples = 200
    
    weights = {'heart': 0.35, 'stroke': 0.30, 'diabetes': 0.20, 'ckd': 0.15}
    global_scores = []
    
    # Drop target columns for prediction
    heart_df = heart_df.drop('target', axis=1)
    diabetes_df = diabetes_df.drop('Outcome', axis=1)
    stroke_df = stroke_df.drop('stroke', axis=1)
    ckd_df = ckd_df.drop('class', axis=1)
    
    for _ in range(n_samples):
        # Sample one random row from each dataset
        p_heart = models['heart'].predict_proba(heart_df.sample(1))[0][1]
        p_diabetes = models['diabetes'].predict_proba(diabetes_df.sample(1))[0][1]
        p_stroke = models['stroke'].predict_proba(stroke_df.sample(1))[0][1]
        p_ckd = models['ckd'].predict_proba(ckd_df.sample(1))[0][1]
        
        g_score = (p_heart * weights['heart'] + 
                   p_diabetes * weights['diabetes'] + 
                   p_stroke * weights['stroke'] + 
                   p_ckd * weights['ckd'])
        global_scores.append(g_score)
        
    global_scores = np.array(global_scores)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.histplot(global_scores, bins=20, kde=True, color='teal')
    
    # Add vertical lines for risk levels
    plt.axvline(x=0.2, color='green', linestyle='--', label='Low ( <0.2 )')
    plt.axvline(x=0.4, color='orange', linestyle='--', label='Moderate ( 0.2-0.4 )')
    plt.axvline(x=0.7, color='red', linestyle='--', label='High ( 0.4-0.7 )')
    
    plt.title('Distribution of Cardiometabolic Health Risk Index (CHRI) in Synthetic Population')
    plt.xlabel('Global Risk Score')
    plt.ylabel('Patient Count')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.savefig('reports/figures/ensemble/global_risk_distribution.png')
    plt.close()
    
    print("Risk distribution plot saved.")

if __name__ == "__main__":
    generate_risk_distribution()
