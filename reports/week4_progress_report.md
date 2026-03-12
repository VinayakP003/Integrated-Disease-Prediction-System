# Week 4 Progress Report: System-Level Integration and Advanced Modeling

## Project: Disease Prediction System

### Overview
This week centered on enhancing model reliability through ensemble techniques, defining a global cardiometabolic risk index (CHRI), and designing a clinical dashboard for end-user interaction.

---

## 1. Ensemble Modeling
We implemented **Stacking** and **Voting (Soft)** classifiers to aggregate predictions from our tuned base learners (Logistic Regression, Random Forest, and SVM).

### Results Summary (Key Metrics)
| Disease | Top Ensemble Model | Recall | ROC-AUC | Comparison to Tuned Single Model |
| :--- | :--- | :--- | :--- | :--- |
| **Heart** | Voting Classifier | 0.93 | 0.956 | High reliability across estimators. |
| **Diabetes** | Optimized Voting | 0.87 | 0.826 | Pruned SVM and tuned threshold for clinical safety. |
| **Stroke** | Voting Classifier | 0.78 | 0.838 | Effective at handling SMOTE-augmented data. |
| **CKD** | Stacking/Voting | 1.00 | 1.000 | Maintained clinical accuracy. |

---

## 2. Global Risk Scoring Concept
The **Cardiometabolic Health Risk Index (CHRI)** represents a holistic score that accounts for the interconnected nature of vascular and metabolic diseases.

### Mathematical Framework
We applied a weighted sum of probabilities:
$$CHRI = 0.35 \times P(Heart) + 0.30 \times P(Stroke) + 0.20 \times P(Diabetes) + 0.15 \times P(CKD)$$

### Risk Score Distribution
We simulated the CHRI for a sample population to establish risk thresholds:
- **Low Risk**: < 0.2
- **Moderate Risk**: 0.2 - 0.4
- **High Risk**: 0.4 - 0.7
- **Critical Risk**: > 0.7

*(See `reports/figures/ensemble/global_risk_distribution.png` for visualization)*

---

## 3. Clinical Dashboard Design
We designed a conceptual interface that balances detailed medical data with actionable risk insights.

### Dashboard Key Features:
1. **Interactive Sidebar**: Input for vitals (Age, BMI, BP, Glucose).
2. **Radial Risk Gauges**: Individual disease probabilities.
3. **CHRI Indicator**: A centralized semi-circle gauge for global health index.
4. **Actionable Insights**: Feature attribution (e.g., 'Lowering LDL may reduce risk by 12%').

---

## 4. Deployment & Integration
The system is now prepared for backend integration:
- **Model Storage**: 8 ensemble models (4 Voting, 4 Stacking) exported as `.joblib` files in `models/exported/`.
- **Preprocessing**: Each model includes the full `ColumnTransformer` (Scaling + Encoding), meaning raw JSON inputs from a web form can be processed instantly.
- **Utility Functions**: `scripts/deploy_utils.py` contains the standardization logic for predicting risks and calculating the CHRI.

---

## 5. Post-Ensemble Optimization (Diabetes Case Study)
Upon initial evaluation, the Diabetes ensemble achieved a sub-optimal Recall of 0.63. We conducted a failure analysis and implemented two key optimizations:

1.  **Model Pruning**: Removed the SVM component from the ensemble. SVM was exhibiting low confidence in its predictions, effectively "diluting" the strong signals from Logistic Regression and Random Forest.
2.  **Threshold Tuning**: Lowered the probability threshold for classification from 0.5 to 0.4.

**Result**: Recall increased from **0.63 → 0.87** (+24% improvement), significantly reducing the risk of missing diabetic patients in a screening scenario.

---

## 6. Implementation Summary
- **Week 4 Goal**: Transition from model optimization to integration.
- **Status**: **Complete.** Models are robust, optimized for recall, exported, and the system framework is defined.

---

## Next Steps (Week 5)
- **Model Serving**: Set up a FastAPI server to host the models.
- **Frontend Prototype**: Build the clinical dashboard using React.
- **Documentation**: Create an API specification for clinical data ingestion.
