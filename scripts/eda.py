import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for figures
os.makedirs('reports/figures', exist_ok=True)

datasets = {
    'Heart Disease': {
        'path': 'data/heart_disease.csv',
        'names': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'],
        'has_header': None
    },
    'Diabetes': {
        'path': 'data/diabetes.csv',
        'names': ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'],
        'has_header': None
    },
    'Stroke': {
        'path': 'data/stroke.csv',
        'names': None,
        'has_header': 0
    },
    'CKD': {
        'path': 'data/ckd.csv',
        'names': None,
        'has_header': 0
    }
}

def analyze_dataset(name, info):
    print(f"\n{'='*20} Analyzing {name} {'='*20}")
    
    if info['has_header'] is None:
        df = pd.read_csv(info['path'], names=info['names'], na_values='?')
    else:
        df = pd.read_csv(info['path'], na_values='?')
    
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]
    
    # Strip whitespace from object columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip()
    
    # Dataset Shape
    print(f"Dataset Shape: {df.shape}")
    
    # Feature List
    print(f"Features: {list(df.columns)}")
    
    # Data Type Summary
    print("\nData Types:")
    print(df.dtypes)
    
    # Missing Value Analysis
    missing = df.isnull().sum()
    print("\nMissing Values:")
    print(missing[missing > 0] if missing.sum() > 0 else "None")
    
    # Target Variable Analysis
    target_col = df.columns[-1] # Usually the last column
    if name == 'Stroke': target_col = 'stroke'
    if name == 'CKD': 
        target_col = 'class'
    if name == 'Heart Disease': target_col = 'target'
    if name == 'Diabetes': target_col = 'Outcome'
    
    print(f"\nTarget Variable: {target_col}")
    class_counts = df[target_col].value_counts()
    print("Class Distribution:")
    print(class_counts)
    
    imbalance_ratio = class_counts.min() / class_counts.max()
    print(f"Class Imbalance Ratio: {imbalance_ratio:.2f}")

    # Visualizations
    plt.figure(figsize=(12, 10))
    
    # 1. Target Distribution
    plt.subplot(2, 2, 1)
    sns.countplot(data=df, x=target_col, palette='viridis')
    plt.title(f'{name} Target Distribution')
    
    # 2. Correlation Heatmap (numerical features only)
    numerical_df = df.select_dtypes(include=[np.number])
    plt.subplot(2, 2, 2)
    sns.heatmap(numerical_df.corr(), annot=False, cmap='coolwarm', fmt=".2f")
    plt.title(f'{name} Correlation Heatmap')
    
    # 3. Distribution of a key numerical feature (e.g. Age or Glucose)
    key_feat = 'age' if 'age' in df.columns else df.columns[0]
    plt.subplot(2, 2, 3)
    sns.histplot(df[key_feat].dropna(), kde=True, color='blue')
    plt.title(f'{name} {key_feat} Distribution')
    
    # 4. Boxplot of key feature by target
    plt.subplot(2, 2, 4)
    sns.boxplot(data=df, x=target_col, y=key_feat, palette='Set2')
    plt.title(f'{name} {key_feat} vs Target')
    
    plt.tight_layout()
    plt.savefig(f'reports/figures/{name.lower().replace(" ", "_")}_eda.png')
    plt.close()
    
    return df

for name, info in datasets.items():
    try:
        analyze_dataset(name, info)
    except Exception as e:
        print(f"Error analyzing {name}: {e}")
