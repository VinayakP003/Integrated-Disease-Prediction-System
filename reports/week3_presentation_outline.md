# Week 3 Presentation: Disease Prediction System

## 🎯 Target Goal
Maximize the clinical utility of our disease prediction models by optimizing **Recall** and ensuring **Medical Reliability**.

---

## 1. Project Progress Overview
- **Week 1:** Data Exploration & Preprocessing Planning.
- **Week 2:** Baseline pipelines & initial model comparisons.
- **Week 3 (Now):** Optimization, Hyperparameter Tuning, and Medical Interpretability.

---

## 2. Optimization Strategy
We shifted focus from general Accuracy to **Recall (Sensitivity)**.
- **Why?** In medical diagnosis, missing a sick patient (False Negative) is much more dangerous than a false alarm (False Positive).
- **Techniques Used:**
    - `GridSearchCV` for optimal hyperparameters.
    - `SMOTE` (Synthetic Minority Over-sampling Technique) for imbalanced datasets like Stroke.
    - `RobustScaler` for data with significant outliers.

---

## 3. Key Findings per Disease

### ❤️ Heart Disease
- **Performance:** **92.9% Recall** (Tuned Random Forest).
- **Top Predictor:** `ca` (Number of major vessels) and `cp` (Chest pain).
- **Impact:** The model effectively captures structural heart changes.

### 🩸 Diabetes
- **Performance:** **70.4% Recall** (Tuned Random Forest).
- **Top Predictor:** `Glucose` and `BMI`.
- **Challenge:** Diabetes remains difficult due to overlapping feature distributions; further ensemble methods may be needed.

### 🧠 Stroke
- **Performance:** **82.0% Recall** (Tuned Logistic Regression).
- **Top Predictor:** `Age` and `Glucose Level`.
- **Solution:** Balanced the 5% minority class using SMOTE to prevent the model from ignoring stroke cases.

### 🧬 Chronic Kidney Disease (CKD)
- **Performance:** **100% Accuracy/Recall** (Random Forest).
- **Medical Validity:** Confirmed top predictors are `hemo` (Hemoglobin) and `pcv`.
- **Finding:** Near-perfect results are due to the strong diagnostic power of these specific clinical markers.

---

## 4. Feature Importance (Medical Insight)
We verified our models against known medical knowledge using **Permutation Importance**:
- **Consistency:** The features the models rely on (like Glucose for Diabetes and Hemoglobin for CKD) match exactly what a clinician would look for.
- **Reliability:** This builds trust in the "Black Box" of Machine Learning.

---

## 5. Next Steps for Week 4
- **Ensemble Stacking:** Combining models to push Diabetes performance higher.
- **System Integration:** Beginning the architecture for the "Integrated Assessment" where multiple risks are calculated simultaneously.
- **Mentor Feedback:** Reviewing these findings for clinical approval.
