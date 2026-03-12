# Midterm Presentation Outline: Disease Prediction System
**Updated to Include Week 5 Progress**

## 1. Project Vision
**Objective:** An AI-integrated clinical support tool for forecasting risks of Heart Disease, Stroke, Diabetes, and Chronic Kidney Disease (CKD).

## 2. Methodology & Pipeline (Weeks 1-2)
*   **Data Acquisition:** UCI Repositories & Kaggle (diverse physiological datasets).
*   **Preprocessing Engine:** Automated `ColumnTransformer` for imputation and scaling.
*   **Addressing Imbalance:** Used **SMOTE** to handle the severe stroke class imbalance (5% stroke vs 95% healthy).

## 3. Optimization & Reliability (Week 3)
*   **Metric Shift:** Prioritized **Recall** over Accuracy to minimize clinical "False Negatives."
*   **Tuning:** used `GridSearchCV` to optimize estimators.
*   **Transparency:** Implemented **Permutation Importance** to verify models align with clinical knowledge (e.g., Glucose as primary Diabetes predictor).

## 4. Advanced System Integration (Week 4)
*   **Ensemble Modeling:** Implemented **Voting & Stacking Classifiers** to aggregate model strengths.
    *   *Win:* Increased Diabetes Recall from **70% → 87%** through model pruning and threshold tuning.
*   **The CHRI Global Score:** Introduced the *Cardiometabolic Health Risk Index*.
    *   Formula: $CHRI = \sum (Weight_i \times Probability_i)$
    *   Categorized risks into **Low, Moderate, High, and Critical**.

## 5. Deployment & Backend (Week 5)
*   **Framework:** Built a high-performance **FastAPI** backend.
*   **Features:**
    *   **Auto-documentation:** Swagger UI for easy data entry testing.
    *   **Pydantic Schemas:** Rigid clinical data validation (ensures biologically possible inputs).
    *   **Singleton Loading:** Models kept "warm" in memory for instantaneous prediction.

## 6. Current System Status
| Component | Status | Performance Highlight |
| :--- | :--- | :--- |
| **Heart ML** | Optimized | 93% Recall (Ensemble) |
| **Stroke ML** | Balanced | 78% Recall (Ensemble) |
| **Diabetes ML**| Pruned/Tuned | 87% Recall (Ensemble) |
| **CKD ML** | Verified | 100% Accuracy (Diagnostic Markers) |
| **API Backend** | Production-Ready | Fully validated schemas & docs |

## 7. Roadmap to Finalization
*   **Frontend:** React-based clinical dashboard.
*   **Visualization:** Interactive risk gauges for CHRI.
*   **Documentation:** Final clinical report generation engine.
