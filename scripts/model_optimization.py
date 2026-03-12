import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split, GridSearchCV, ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc
from sklearn.inspection import permutation_importance

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Create directories for outputs
os.makedirs('reports/figures/optimization', exist_ok=True)
os.makedirs('reports/figures/feature_importance', exist_ok=True)
os.makedirs('reports/figures/roc_curves', exist_ok=True)
os.makedirs('reports/figures/confusion_matrices_tuned', exist_ok=True)

def get_preprocessor(X, numeric_features, categorical_features, scale_type='standard'):
    scaler = StandardScaler() if scale_type == 'standard' else RobustScaler()
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', scaler)
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent' if categorical_features else 'constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    return preprocessor

def load_and_preprocess_heart():
    df = pd.read_csv('data/cleaned/heart_disease_cleaned.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    categorical_features = [c for c in X.columns if c not in numeric_features]
    return X, y, numeric_features, categorical_features

def load_and_preprocess_diabetes():
    df = pd.read_csv('data/cleaned/diabetes_cleaned.csv')
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    numeric_features = X.columns.tolist()
    categorical_features = []
    return X, y, numeric_features, categorical_features

def load_and_preprocess_stroke():
    df = pd.read_csv('data/cleaned/stroke_cleaned.csv')
    # Dropping BMI rows for baseline or imputing? Script says impute.
    X = df.drop('stroke', axis=1)
    y = df['stroke']
    numeric_features = ['age', 'avg_glucose_level', 'bmi']
    categorical_features = [c for c in X.columns if c not in numeric_features]
    return X, y, numeric_features, categorical_features

def load_and_preprocess_ckd():
    df = pd.read_csv('data/cleaned/ckd_cleaned.csv')
    
    # Check for suspected leakage or high correlation
    # We will exclude 'id' (already done in cleaning)
    # Check correlations
    df_temp = df.copy()
    df_temp['class_num'] = df_temp['class'].map({'ckd': 1, 'notckd': 0})
    
    # Suspicious check: features that perfectly separate the data
    # In clinical practice, SC and Hemo are very strong.
    # But let's see if any feature is TOO good.
    
    X = df.drop('class', axis=1)
    y = df['class'].map({'ckd': 1, 'notckd': 0})
    
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    return X, y, numeric_features, categorical_features

def run_optimization(disease_name, X, y, preprocessor, use_smote=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    models_params = {
        'Logistic Regression': {
            'model': LogisticRegression(max_iter=5000, solver='liblinear'),
            'params': {
                'classifier__C': [0.01, 0.1, 1, 10, 100],
                'classifier__penalty': ['l1', 'l2']
            }
        },
        'Random Forest': {
            'model': RandomForestClassifier(random_state=42),
            'params': {
                'classifier__n_estimators': [100, 200],
                'classifier__max_depth': [None, 10, 20],
                'classifier__min_samples_split': [2, 5],
                'classifier__class_weight': ['balanced', None]
            }
        },
        'SVM': {
            'model': SVC(probability=True, random_state=42),
            'params': {
                'classifier__C': [0.1, 1, 10],
                'classifier__kernel': ['rbf', 'linear'],
                'classifier__gamma': ['scale', 'auto']
            }
        }
    }
    
    optimized_results = {}
    
    for model_name, config in models_params.items():
        print(f"  Tuning {model_name} for {disease_name}...")
        
        if use_smote:
            pipeline = ImbPipeline(steps=[
                ('preprocessor', preprocessor),
                ('smote', SMOTE(random_state=42)),
                ('classifier', config['model'])
            ])
        else:
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', config['model'])
            ])
            
        grid = GridSearchCV(pipeline, config['params'], cv=5, scoring='recall', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        best_model = grid.best_estimator_
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1] if hasattr(best_model, "predict_proba") else best_model.decision_function(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'auc': roc_auc_score(y_test, y_prob),
            'best_params': grid.best_params_,
            'model_obj': best_model
        }
        optimized_results[model_name] = metrics
        
        # Save Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens')
        plt.title(f'{disease_name} - {model_name} (Tuned)\nRecall: {metrics["recall"]:.2f}')
        plt.savefig(f'reports/figures/confusion_matrices_tuned/{disease_name.lower()}_{model_name.lower().replace(" ", "_")}_tuned_cm.png')
        plt.close()

    return optimized_results, X_test, y_test

def analyze_feature_importance(disease_name, model_name, model, X_test, y_test):
    print(f"  Analyzing feature importance for {disease_name} - {model_name}...")
    
    # Get feature names after preprocessing
    preprocessor = model.named_steps['preprocessor']
    
    # Extract numerical feature names
    num_features = preprocessor.transformers_[0][2]
    
    # Extract categorical feature names if they exist and transformer is fitted
    cat_features_transformed = []
    try:
        cat_transformer = preprocessor.named_transformers_.get('cat')
        if cat_transformer and len(preprocessor.transformers_[1][2]) > 0:
            ohe = cat_transformer.named_steps['onehot']
            if hasattr(ohe, 'get_feature_names_out'):
                cat_features_transformed = ohe.get_feature_names_out().tolist()
    except (KeyError, AttributeError, ValueError):
        pass
    
    all_feature_names = list(num_features) + cat_features_transformed
    
    # 1. Random Forest Internal Importance
    if 'Random Forest' in model_name:
        clf = model.named_steps['classifier']
        importances = clf.feature_importances_
        # Ensure name match length (sometimes SMOTE or other steps modify things)
        if len(all_feature_names) == len(importances):
            feat_df = pd.DataFrame({'feature': all_feature_names, 'importance': importances})
            feat_df = feat_df.sort_values(by='importance', ascending=False).head(10)
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=feat_df, x='importance', y='feature', palette='magma')
            plt.title(f'{disease_name} - {model_name} Top 10 Features')
            plt.tight_layout()
            plt.savefig(f'reports/figures/feature_importance/{disease_name.lower()}_rf_importance.png')
            plt.close()

    # 2. Permutation Importance (for medical reliability check)
    r = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42, scoring='recall')
    
    perm_df = pd.DataFrame({'feature': X_test.columns, 'importance': r.importances_mean})
    perm_df = perm_df.sort_values(by='importance', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=perm_df, x='importance', y='feature', palette='viridis')
    plt.title(f'{disease_name} - {model_name} Permutation Importance (Recall)')
    plt.tight_layout()
    plt.savefig(f'reports/figures/feature_importance/{disease_name.lower()}_{model_name.lower().replace(" ", "_")}_perm_importance.png')
    plt.close()
    
    return perm_df

def plot_combined_roc(disease_name, results, X_test, y_test):
    plt.figure(figsize=(8, 6))
    for model_name, res in results.items():
        model = res['model_obj']
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')
        
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curves for {disease_name}')
    plt.legend(loc="lower right")
    plt.savefig(f'reports/figures/roc_curves/{disease_name.lower()}_combined_roc.png')
    plt.close()

def error_analysis(disease_name, model_name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    errors = X_test[y_test != y_pred].copy()
    errors['Actual'] = y_test[y_test != y_pred]
    errors['Predicted'] = y_pred[y_test != y_pred]
    
    fn = errors[errors['Actual'] == 1].shape[0]
    fp = errors[errors['Actual'] == 0].shape[0]
    
    return fn, fp

# --- Main Execution ---

all_disease_results = []

# Disease Configs
configs = [
    ('Heart', load_and_preprocess_heart, False),
    ('Diabetes', load_and_preprocess_diabetes, False),
    ('Stroke', load_and_preprocess_stroke, True),
    ('CKD', load_and_preprocess_ckd, False)
]

print("Starting Week 3 Optimization and Analysis...")

summary_report = []

for disease, load_fn, use_smote in configs:
    print(f"\nProcessing {disease}...")
    X, y, num_feats, cat_feats = load_fn()
    
    # Special Check for CKD Leakage
    if disease == 'CKD':
        corr_matrix = pd.concat([X, y.rename('target')], axis=1).corr(numeric_only=True)
        high_corr = corr_matrix['target'].abs().sort_values(ascending=False)
        print(f"  CKD Correlations with target:\n{high_corr.head(6)}")
        # If any feature is > 0.9, we might consider it leakage, but Hemo and PCV are expected to be high.
        # Let's check for things like 'id' or others.
    
    preprocessor = get_preprocessor(X, num_feats, cat_feats, scale_type='robust' if disease == 'Stroke' else 'standard')
    
    tuned_results, X_test, y_test = run_optimization(disease, X, y, preprocessor, use_smote)
    
    plot_combined_roc(disease, tuned_results, X_test, y_test)
    
    for model_name, res in tuned_results.items():
        importance = analyze_feature_importance(disease, model_name, res['model_obj'], X_test, y_test)
        fn, fp = error_analysis(disease, model_name, res['model_obj'], X_test, y_test)
        
        res['fn'] = fn
        res['fp'] = fp
        res['disease'] = disease
        res['model_name'] = model_name
        all_disease_results.append(res)

# Final Reporting
results_df = pd.DataFrame(all_disease_results)
results_df.to_csv('reports/tuned_model_results.csv', index=False)
print("\nOptimization Complete. Results saved to reports/tuned_model_results.csv")
