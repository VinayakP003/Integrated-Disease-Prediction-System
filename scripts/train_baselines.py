import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import os

# Create directories
os.makedirs('reports/figures/confusion_matrices', exist_ok=True)

def load_heart_data():
    names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    df = pd.read_csv('data/heart_disease.csv', names=names, na_values='?')
    df = df.dropna(subset=['target'])
    df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0).astype(int)
    X = df.drop('target', axis=1)
    y = df['target']
    
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    return X, y, preprocessor

def load_diabetes_data():
    names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    df = pd.read_csv('data/diabetes.csv', names=names)
    df = df.dropna(subset=['Outcome'])
    df['Outcome'] = df['Outcome'].astype(int)
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    numeric_features = X.columns
    preprocessor = ColumnTransformer(transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features)
    ])
    return X, y, preprocessor

def load_stroke_data():
    df = pd.read_csv('data/stroke.csv')
    df = df.dropna(subset=['stroke'])
    df['stroke'] = df['stroke'].astype(int)
    df = df.drop('id', axis=1)
    X = df.drop('stroke', axis=1)
    y = df['stroke']
    
    numeric_features = ['age', 'avg_glucose_level', 'bmi']
    categorical_features = ['gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    return X, y, preprocessor

def load_ckd_data():
    df = pd.read_csv('data/ckd.csv')
    df.columns = [c.strip() for c in df.columns]
    df['class'] = df['class'].astype(str).str.strip().str.lower()
    df = df[df['class'].isin(['ckd', 'notckd', 'ckd\t'])]
    df['class'] = df['class'].replace({'ckd': 1, 'notckd': 0, 'ckd\t': 1}).astype(int)
    
    for col in ['pcv', 'wc', 'rc']:
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')
    
    X = df.drop(['id', 'class'], axis=1)
    y = df['class']
    
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    return X, y, preprocessor

def evaluate_model(name, model, X_test, y_test, disease_name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X_test)
    
    metrics = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, zero_division=0),
        'Recall': recall_score(y_test, y_pred, zero_division=0),
        'F1': f1_score(y_test, y_pred, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_prob)
    }
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'{disease_name} - {name}\nRecall: {metrics["Recall"]:.2f}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(f'reports/figures/confusion_matrices/{disease_name.lower()}_{name.lower().replace(" ", "_")}_cm.png')
    plt.close()
    
    return metrics

datasets = {'Heart': load_heart_data, 'Diabetes': load_diabetes_data, 'Stroke': load_stroke_data, 'CKD': load_ckd_data}
models = {
    'Logistic Regression': LogisticRegression(max_iter=2000),
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(probability=True, random_state=42)
}

results = []
for disease_name, load_fn in datasets.items():
    print(f"\nProcessing {disease_name}...")
    X, y, preprocessor = load_fn()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    for model_name, model in models.items():
        print(f"  Training {model_name}...")
        if disease_name == 'Stroke':
            pipeline = ImbPipeline(steps=[('preprocessor', preprocessor), ('smote', SMOTE(random_state=42)), ('classifier', model)])
        else:
            pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        
        pipeline.fit(X_train, y_train)
        print(f"  Evaluating {model_name}...")
        metrics = evaluate_model(model_name, pipeline, X_test, y_test, disease_name)
        metrics['Disease'] = disease_name
        metrics['Model'] = model_name
        results.append(metrics)

pd.DataFrame(results).to_csv('reports/baseline_results.csv', index=False)
print("\nDone. Results saved to reports/baseline_results.csv")
