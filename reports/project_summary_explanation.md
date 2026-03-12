# Project Overview & Progress Report: Disease Prediction System

## 1. Project Introduction
**Title:** Disease Prediction System  
**Objective:** To develop a robust machine learning system capable of predicting the risk of four interconnected chronic conditions: **Heart Disease, Diabetes, Stroke, and Chronic Kidney Disease (CKD)**. 

The system aims to serve as a clinical decision-support tool, helping healthcare providers identify high-risk patients early using standard medical parameters.

---

## 2. Phase 1: Data Exploration & Preprocessing (Weeks 1 & 2)
In the initial phase, we focused on understanding the "health" of our data across four distinct datasets:

- **Data Cleaning:** 
    - Resolved inconsistencies like the "ckd\t" label in the CKD dataset.
    - Handled hidden missing values, such as "0" values in Diabetes (BMI/Glucose) that were biologically impossible.
    - Standardized placeholders (e.g., converting '?' to NaN).
- **Exploratory Data Analysis (EDA):**
    - Identified significant **Class Imbalance** in the Stroke dataset (only 5% of patients had strokes).
    - Discovered that the Heart Disease dataset required **Binarization** (converting stages 1-4 into a single "Disease" class).
- **Pipeline Architecture:**
    - Developed an automated preprocessing pipeline using `ColumnTransformer` to handle numerical (scaling) and categorical (One-Hot Encoding) data simultaneously.

---

## 3. Phase 2: Baseline Modeling (Week 2)
We established a performance floor by training simple versions of **Logistic Regression, Random Forest, and SVM**.
- **Initial Metrics:** Most models showed decent accuracy, but the Stroke model struggled heavily with the minority class, often ignoring stroke cases entirely.
- **The "Perfect" Model Case:** The CKD dataset showed ~100% accuracy, which triggered a deep-dive investigation in Phase 3 to ensure no data leakage was occurring.

---

## 4. Phase 3: Optimization & Medical Reliability (Current Phase)
The focus shifted from "general accuracy" to **"clinical utility"**. In medicine, a False Negative (missing a sick person) is far more costly than a False Positive.

- **Hyperparameter Tuning:** 
    - Used `GridSearchCV` to find the best settings for each model.
    - Optimized specifically for **Recall**, ensuring the system is sensitive enough to catch early-stage disease.
- **Handling Imbalance:** 
    - Implemented **SMOTE** (Synthetic Minority Over-sampling Technique) for Stroke, which successfully taught the model to recognize the rare "Stroke" class.
- **Feature Importance (The "Why"):**
    - We moved beyond just "predictions" to "explanations." 
    - Using **Permutation Importance**, we identified that the models rely on medically sound markers: **Glucose** for Diabetes, **Number of Major Vessels** for Heart Disease, and **Hemoglobin** for CKD.
- **CKD Verification:** 
    - Confirmed that the 100% accuracy in CKD is legitimate. The combination of **Specific Gravity, Albumin, and Hemoglobin** provides a near-perfect diagnostic fingerprint for kidney failure in this specific population.

---

## 5. Current Performance Summary

| Disease | Best Model | Recall (Sensitivity) | Clinical Interpretation |
| :--- | :--- | :--- | :--- |
| **Heart Disease** | Random Forest | **92.9%** | Highly reliable; relies on structural heart data. |
| **Stroke** | Logistic Regression | **82.0%** | Successfully balanced; prioritizes patient safety. |
| **Diabetes** | Random Forest | **70.4%** | Challenging; features (BMI/Age) overlap significantly. |
| **CKD** | Random Forest | **100%** | Exceptionally strong diagnostic markers present. |

---

## 6. Conclusion & Roadmap
**Where we stand:** We have moved from raw, messy data to tuned, medically-interpretable models. We have successfully mitigated class imbalances and verified the reliability of our "perfect" predictors.

**Next Steps:**
1. **Ensemble Stacking:** Combining multiple models to boost the harder-to-predict diseases (Diabetes).
2. **Integrated Risk Scoring:** Developing a unified logic to calculate multiple risks from a single patient input.
3. **Clinical Interface:** Designing the user interface for practitioners to input data and receive risk assessments.
