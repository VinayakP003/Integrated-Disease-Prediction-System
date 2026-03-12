# Dataset Parameters Guide: Clinical Features & Significance
**A Deep Dive into the Variables Monitoring Patient Health**

This document provides a detailed breakdown of all clinical parameters used in the project to train our AI models. It explains what each feature represents and why it is critical for disease prediction.

---

## ❤️ Heart Disease (UCI Cleveland Dataset)
*The heart disease model monitors structural and functional health of the cardiovascular system.*

| Parameter | Type | What it Measures | Clinical Significance |
| :--- | :--- | :--- | :--- |
| **age** | Numeric | Patient's age in years. | Risk increases and heart elasticity decreases with age. |
| **sex** | Binary | 1 = Male; 0 = Female. | Men and post-menopausal women have higher baseline risk. |
| **cp** | Categorical | Chest pain type (0-3). | 0 (Asymptomatic), 1 (Typical Angina), 2 (Atypical), 3 (Non-anginal). |
| **trestbps** | Numeric | Resting Blood Pressure (mm Hg). | High pressure strains heart walls and arteries. |
| **chol** | Numeric | Serum Cholesterol (mg/dl). | High LDL levels lead to plaque buildup (atherosclerosis). |
| **fbs** | Binary | Fasting Blood Sugar > 120 mg/dl. | High blood sugar can damage heart blood vessels. |
| **restecg** | Categorical | Resting Electrocardiographic results (0-2). | Detects abnormal heart rhythms or past muscle damage. |
| **thalach** | Numeric | Maximum Heart Rate Achieved. | **Top Predictor.** Measures the heart's peak functional capacity. |
| **exang** | Binary | Exercise Induced Angina (Chest pain). | Indicates blood flow restriction during physical stress. |
| **oldpeak** | Numeric | ST depression induced by exercise. | Measures heart stress response; higher values indicate ischemia. |
| **ca** | Numeric | Number of Major Vessels (0-3). | **Top Predictor.** Directly counts visible arterial blockages. |
| **thal** | Categorical | Thalassemia Type. | Indicates genetic blood disorders affecting oxygen transport. |

---

## 🩸 Diabetes (Pima Indians Dataset)
*The diabetes model focuses on metabolic indicators and physiological markers.*

| Parameter | Type | What it Measures | Clinical Significance |
| :--- | :--- | :--- | :--- |
| **Glucose** | Numeric | Plasma glucose concentration. | **Primary Predictor.** Directly measures blood sugar control. |
| **BloodPressure**| Numeric | Diastolic blood pressure (mm Hg). | Hypertension is a major co-morbidity for diabetics. |
| **SkinThickness**| Numeric | Triceps skin fold thickness (mm). | Indicates subcutaneous fat levels (linked to insulin resistance). |
| **Insulin** | Numeric | 2-Hour serum insulin (mu U/ml). | Measures the body's ability to process sugar. |
| **BMI** | Numeric | Body Mass Index ($kg/m^2$). | **Key Predictor.** Obesity is a leading cause of Type 2 Diabetes. |
| **DiabetesPedigree**| Numeric | Genetic diabetes history score. | Estimates the hereditary risk based on family history. |
| **Age** | Numeric | Patient's age. | Type 2 risk increases significantly with age. |
| **Pregnancies** | Numeric | Number of times pregnant. | Higher numbers are linked to gestational diabetes risk. |

---

## 🧠 Stroke (Kaggle Dataset)
*The stroke model uses demographic data and chronic health history.*

| Parameter | Type | What it Measures | Clinical Significance |
| :--- | :--- | :--- | :--- |
| **gender** | Categorical | Male, Female, Other. | Hormonal differences influence vascular health. |
| **age** | Numeric | Patient's age. | **Top Predictor.** Stroke risk doubles every decade after 55. |
| **hypertension** | Binary | History of high blood pressure (0/1). | **Key Predictor.** Strains brain arteries, causing them to burst. |
| **heart_disease**| Binary | History of cardiac issues. | Heart issues (like AFib) can cause clots that travel to the brain. |
| **avg_glucose** | Numeric | Average blood sugar level. | High glucose damages blood vessels throughout the body. |
| **bmi** | Numeric | Body Mass Index ($kg/m^2$). | High BMI is linked to inflammation and vascular blockage. |
| **smoking_status**| Categorical | Smokes, Formerly, Never, Unknown. | Smoking thickens blood and increases arterial plaque. |
| **Residence_type**| Categorical | Urban or Rural. | Influence of lifestyle, stress, and healthcare accessibility. |
| **work_type** | Categorical | Employment category. | Surrogate for stress levels and physical activity. |

---

## 🧬 Chronic Kidney Disease (UCI CKD Dataset)
*The CKD model monitors blood chemistry and filtration markers.*

| Parameter | Type | What it Measures | Clinical Significance |
| :--- | :--- | :--- | :--- |
| **sg** | Numeric | Specific Gravity (1.005-1.025). | Measures the kidney's ability to concentrate urine. |
| **al** | Numeric | Albumin levels (0-5). | Protein in urine is a key sign of kidney filtration damage. |
| **hemo** | Numeric | Hemoglobin level (g/dl). | **Top Predictor.** Kidneys produce EPO; low hemo indicates failure. |
| **pcv** | Numeric | Packed Cell Volume (%). | **Top Predictor.** Works with hemoglobin to detect renal anemia. |
| **sc** | Numeric | Serum Creatinine (mg/dl). | Direct waste product indicator; high levels = poor filtration. |
| **bgr** | Numeric | Blood Glucose Random. | Diabetes is the #1 cause of Chronic Kidney Disease. |
| **htn** | Binary | Hypertension (yes/no). | High BP damages the tiny filters (nephrons) in the kidneys. |
| **dm** | Binary | Diabetes Mellitus (yes/no). | Confirms the diabetic link to renal failure. |
| **rbc/pc** | Categorical | Red Blood Cells / Pus Cells. | "Abnormal" findings indicate infection or structural damage. |

---

## 🔍 Why These Parameters? (The "Feature Engineering" Logic)
We chose and prioritized these parameters because they represent **clinical gold standards**:
1.  **Diagnostic Power**: Parameters like `ca` (Heart) and `hemo` (CKD) are so accurate they are used for final diagnoses in hospitals.
2.  **Interconnectedness**: Many parameters repeat across diseases (Glucose, BMI, Age). This highlights the **"Cardiometabolic Syndrome"** where one disease often leads to another.
3.  **Predictive Strength**: By analyzing Feature Importance, we found these specific variables have the highest "Information Gain," meaning they help the model distinguish between healthy and at-risk patients most clearly.
