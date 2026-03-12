import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.metrics import recall_score, roc_auc_score, roc_curve, auc, accuracy_score, precision_score, f1_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Create directories for outputs
os.makedirs('reports/figures/ensemble', exist_ok=True)
os.makedirs('models/exported', exist_ok=True)

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

def load_heart():
    df = pd.read_csv('data/cleaned/heart_disease_cleaned.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    categorical_features = [c for c in X.columns if c not in numeric_features]
    return X, y, numeric_features, categorical_features

def load_diabetes():
    df = pd.read_csv('data/cleaned/diabetes_cleaned.csv')
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    numeric_features = X.columns.tolist()
    categorical_features = []
    return X, y, numeric_features, categorical_features

def load_stroke():
    df = pd.read_csv('data/cleaned/stroke_cleaned.csv')
    X = df.drop('stroke', axis=1)
    y = df['stroke']
    numeric_features = ['age', 'avg_glucose_level', 'bmi']
    categorical_features = [c for c in X.columns if c not in numeric_features]
    return X, y, numeric_features, categorical_features

def load_ckd():
    df = pd.read_csv('data/cleaned/ckd_cleaned.csv')
    X = df.drop('class', axis=1)
    y = df['class'].map({'ckd': 1, 'notckd': 0})
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    return X, y, numeric_features, categorical_features

# Best params extracted from tuned_model_results.csv
BEST_PARAMS = {
    'Heart': {
        'LR': {'C': 1, 'penalty': 'l1', 'solver': 'liblinear', 'max_iter': 5000},
        'RF': {'class_weight': 'balanced', 'max_depth': None, 'min_samples_split': 2, 'n_estimators': 100},
        'SVM': {'C': 10, 'gamma': 'scale', 'kernel': 'linear', 'probability': True}
    },
    'Diabetes': {
        'LR': {'C': 0.01, 'penalty': 'l1', 'solver': 'liblinear', 'max_iter': 5000},
        'RF': {'class_weight': 'balanced', 'max_depth': 10, 'min_samples_split': 5, 'n_estimators': 200},
        'SVM': {'C': 10, 'gamma': 'scale', 'kernel': 'rbf', 'probability': True}
    },
    'Stroke': {
        'LR': {'C': 0.01, 'penalty': 'l1', 'solver': 'liblinear', 'max_iter': 5000},
        'RF': {'class_weight': 'balanced', 'max_depth': 10, 'min_samples_split': 5, 'n_estimators': 100},
        'SVM': {'C': 0.1, 'gamma': 'auto', 'kernel': 'rbf', 'probability': True}
    },
    'CKD': {
        'LR': {'C': 10, 'penalty': 'l2', 'solver': 'liblinear', 'max_iter': 5000},
        'RF': {'class_weight': 'balanced', 'max_depth': None, 'min_samples_split': 2, 'n_estimators': 100},
        'SVM': {'C': 1, 'gamma': 'auto', 'kernel': 'rbf', 'probability': True}
    }
}

def run_ensemble(disease_name, X, y, preprocessor, use_smote=False):
    print(f"\nTraining Ensembles for {disease_name}...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    params = BEST_PARAMS[disease_name]
    
    # Define Base Estimators (without the classifier__ prefix as they will be in a pipeline OR used directly)
    # Actually, we need them to be separate models to pass into Voting/Stacking.
    # But those models usually expect preprocessed data or be part of a pipeline.
    # The most robust way is to include the preprocessor in EACH base learner, 
    # OR pass the preprocessed data to the ensembles.
    # Let's preprocess the data first.
    
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    if use_smote:
        smote = SMOTE(random_state=42)
        X_train_processed, y_train = smote.fit_resample(X_train_processed, y_train)
    
    base_models = [
        ('lr', LogisticRegression(**params['LR'])),
        ('rf', RandomForestClassifier(**params['RF'], random_state=42)),
        ('svm', SVC(**params['SVM'], random_state=42))
    ]
    
    # 1. Voting Classifier
    voting_clf = VotingClassifier(estimators=base_models, voting='soft')
    voting_clf.fit(X_train_processed, y_train)
    
    # 2. Stacking Classifier
    stacking_clf = StackingClassifier(estimators=base_models, final_estimator=LogisticRegression())
    stacking_clf.fit(X_train_processed, y_train)
    
    models = {
        'Voting (Soft)': voting_clf,
        'Stacking': stacking_clf,
        'Base_LR': base_models[0][1].fit(X_train_processed, y_train),
        'Base_RF': base_models[1][1].fit(X_train_processed, y_train),
        'Base_SVM': base_models[2][1].fit(X_train_processed, y_train)
    }

    # Add Optimized version for Diabetes
    if disease_name == 'Diabetes':
        optimized_base = [('lr', LogisticRegression(**params['LR'])), ('rf', RandomForestClassifier(**params['RF'], random_state=42))]
        opt_voting = VotingClassifier(estimators=optimized_base, voting='soft')
        opt_voting.fit(X_train_processed, y_train)
        models['Optimized Voting (LR+RF, Th=0.4)'] = opt_voting
    
    results = []
    plt.figure(figsize=(10, 8))
    
    for name, model in models.items():
        y_prob = model.predict_proba(X_test_processed)[:, 1]
        
        # Apply custom threshold for Optimized Diabetes model
        threshold = 0.4 if 'Optimized' in name else 0.5
        y_pred = (y_prob >= threshold).astype(int)
        
        recall = recall_score(y_test, y_pred)
        auc_val = roc_auc_score(y_test, y_prob)
        acc = accuracy_score(y_test, y_pred)
        
        results.append({
            'Disease': disease_name,
            'Model': name,
            'Recall': recall,
            'AUC': auc_val,
            'Accuracy': acc
        })
        
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.plot(fpr, tpr, label=f'{name} (AUC = {auc_val:.3f})')
        
        # Export logic
        if 'Voting' in name or 'Stacking' in name:
            export_name = name.lower().replace(" (lr+rf, th=0.4)", "_optimized").replace(" (soft)", "").replace(" ", "_")
            full_pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('classifier', model)
            ])
            joblib.dump(full_pipeline, f'models/exported/{disease_name.lower()}_{export_name}.joblib')


    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Ensemble Comparison - {disease_name}')
    plt.legend()
    plt.savefig(f'reports/figures/ensemble/{disease_name.lower()}_ensemble_roc.png')
    plt.close()
    
    return results

def main():
    configs = [
        ('Heart', load_heart, False),
        ('Diabetes', load_diabetes, False),
        ('Stroke', load_stroke, True),
        ('CKD', load_ckd, False)
    ]
    
    all_results = []
    for disease, load_fn, use_smote in configs:
        X, y, num_feats, cat_feats = load_fn()
        preprocessor = get_preprocessor(X, num_feats, cat_feats, scale_type='robust' if disease == 'Stroke' else 'standard')
        res = run_ensemble(disease, X, y, preprocessor, use_smote)
        all_results.extend(res)
    
    results_df = pd.DataFrame(all_results)
    results_df.to_csv('reports/ensemble_model_results.csv', index=False)
    
    # Generate Comparison Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=results_df, x='Disease', y='Recall', hue='Model')
    plt.title('Recall Comparison: Base Models vs Ensembles')
    plt.savefig('reports/figures/ensemble/recall_comparison.png')
    plt.close()

    print("\nEnsemble Modeling complete. Results saved and models exported.")

if __name__ == "__main__":
    main()
