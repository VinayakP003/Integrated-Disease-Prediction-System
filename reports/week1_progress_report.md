# Week 1 Progress Report: Exploratory Data Analysis & Planning

**Project Title:** AI-Based Integrated Cardiometabolic & Renal Risk Assessment System  
**Focus:** Exploratory Data Analysis (EDA) and Preprocessing Planning  
**Week 1 Goal:** Understand data distributions, identify quality issues, and define the preprocessing strategy.

---

## 1. Project Overview
The objective of this project is to develop a multi-disease prediction system that assesses risk for Heart Disease, Diabetes, Stroke, and Chronic Kidney Disease (CKD), eventually integrating these into a unified health index.

## 2. Dataset Exploration Summary

| Dataset | Shape | Target Variable | Class Imbalance Ratio | Primary Data Types |
| :--- | :--- | :--- | :--- | :--- |
| **Heart Disease** | (303, 14) | `target` (Binarized) | 0.85 | Numerical & Categorical |
| **Diabetes** | (768, 9) | `Outcome` (0/1) | 0.54 | Numerical |
| **Stroke** | (5110, 12) | `stroke` (0/1) | **0.05** (Critical) | Categorical & Numerical |
| **CKD** | (400, 26) | `class` (ckd/notckd) | 0.60 | Highly Mixed |

---

## 3. Deep-Dive Analysis by Disease

### A. Heart Disease (UCI Cleveland)
- **Key Features:** 13 predictors including age, sex, chest pain (`cp`), resting BP, and cholesterol.
- **Findings:** 
  - `thalach` (Maximum heart rate achieved) shows a strong negative correlation with the presence of disease.
  - Chest pain type (`cp`) is the most significant categorical predictor.
  - *Data Quality:* Minimal missing values (`ca` and `thal`).

### B. Diabetes (Pima Indians)
- **Key Features:** 8 predictors (Pregnancies, Glucose, Blood Pressure, BMI, etc.).
- **Findings:** 
  - Significant physiological "0" values discovered in `Glucose`, `BMI`, and `Insulin` which represent missing data.
  - `Glucose` and `BMI` are the most potent risk indicators.

### C. Stroke Prediction (Kaggle)
- **Key Features:** 11 predictors including hypertension, heart disease, glucose levels, and smoking status.
- **Findings:** 
  - **Severe Class Imbalance:** Only 4.8% of patients suffered a stroke.
  - `Age` is the most dominant risk factor, followed by `avg_glucose_level`.
  - *Data Quality:* 201 missing entries in `bmi`.

### D. Chronic Kidney Disease (UCI)
- **Key Features:** 24 predictors including blood pressure, specific gravity, and various blood cell counts.
- **Findings:** 
  - **Extensive Missing Data:** Nearly every feature has missing values (e.g., `rbc` is missing 38% of entries).
  - Medical markers like `hemo` (hemoglobin) and `pcv` (packed cell volume) show near-perfect separation for CKD cases.

---

## 4. Visual Analysis
*Selected EDA Visualizations (available in `reports/figures/`):*

| Heart Disease Distribution | Stroke Risk Factors |
| :---: | :---: |
| ![Heart EDA](file:///c:/Users/No%20one/Desktop/app/Capstone%20Project/reports/figures/heart_disease_eda.png) | ![Stroke EDA](file:///c:/Users/No%20one/Desktop/app/Capstone%20Project/reports/figures/stroke_eda.png) |

| Diabetes Feature Correlation | CKD Feature Separation |
| :---: | :---: |
| ![Diabetes EDA](file:///c:/Users/No%20one/Desktop/app/Capstone%20Project/reports/figures/diabetes_eda.png) | ![CKD EDA](file:///c:/Users/No%20one/Desktop/app/Capstone%20Project/reports/figures/ckd_eda.png) |

---

## 5. Preprocessing Strategy & Planning

### Data Quality & Imputation
1. **Numerical Imputation:** Median imputation for `bmi`, `ca`, and the "0" values in the Diabetes dataset.
2. **Categorical Imputation:** Constant imputation ("Missing") for CKD's categorical features to preserve the information that the data was not recorded.

### Feature Engineering
- **One-Hot Encoding:** To be applied to multinomial features like `smoking_status` and `cp`.
- **Scaling:** 
  - Standard Scaling for normal distributions.
  - **Robust Scaling** for features with high outlier density (e.g., `BMI`, `Glucose`).

### Balancing Strategy
- **SMOTE (Synthetic Minority Over-sampling):** Mandatory for the Stroke dataset to address the 0.05 imbalance before training.

---

## 6. Proposed Baseline Models
The following models will be evaluated in Week 2 to establish baseline performance:
1. **Logistic Regression:** For clinical interpretability.
2. **Random Forest:** For handling non-linear interactions and missing data robustness.
3. **SVM (Support Vector Machines):** Targeted at high-dimensional CKD data.

---

**Next Steps (Week 2):**
- Build automated `Scikit-Learn` pipelines for all 4 diseases.
- Implement SMOTE for the Stroke dataset.
- Train and compare baseline models using metrics: Accuracy, Precision, **Recall**, and F1-Score.
