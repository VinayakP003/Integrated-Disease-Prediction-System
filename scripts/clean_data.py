import pandas as pd
import numpy as np
import os

# Ensure output directory exists
output_dir = 'data/cleaned'
os.makedirs(output_dir, exist_ok=True)

def clean_heart_disease():
    print("Cleaning Heart Disease dataset...")
    names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    df = pd.read_csv('data/heart_disease.csv', names=names, na_values='?')
    
    # Binarize target (0 = no disease, 1-4 = disease)
    df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)
    
    df.to_csv(os.path.join(output_dir, 'heart_disease_cleaned.csv'), index=False)
    print("  Saved to data/cleaned/heart_disease_cleaned.csv")

def clean_diabetes():
    print("Cleaning Diabetes dataset...")
    names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    df = pd.read_csv('data/diabetes.csv', names=names)
    
    # Replace zeros with NaN for features where zero is invalid
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)
    
    df.to_csv(os.path.join(output_dir, 'diabetes_cleaned.csv'), index=False)
    print("  Saved to data/cleaned/diabetes_cleaned.csv")

def clean_stroke():
    print("Cleaning Stroke dataset...")
    df = pd.read_csv('data/stroke.csv')
    
    # Drop irrelevant ID column
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Strip whitespace from categorical columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip()
        
    df.to_csv(os.path.join(output_dir, 'stroke_cleaned.csv'), index=False)
    print("  Saved to data/cleaned/stroke_cleaned.csv")

def clean_ckd():
    print("Cleaning CKD dataset...")
    df = pd.read_csv('data/ckd.csv')
    
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]
    
    # Normalize 'class' column
    df['class'] = df['class'].astype(str).str.strip().str.lower()
    df['class'] = df['class'].replace({'ckd\t': 'ckd', 'notckd': 'notckd'})
    
    # Drop ID column
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
        
    # Clean numeric columns that might contain strings/whitespace
    for col in ['pcv', 'wc', 'rc']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')
            
    # Strip whitespace from all other object columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip()
        
    df.to_csv(os.path.join(output_dir, 'ckd_cleaned.csv'), index=False)
    print("  Saved to data/cleaned/ckd_cleaned.csv")

if __name__ == "__main__":
    clean_heart_disease()
    clean_diabetes()
    clean_stroke()
    clean_ckd()
    print("\nAll datasets cleaned and saved successfully.")
