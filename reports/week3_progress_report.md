# Week 3 Progress Report: Disease Prediction System

**Project Title:** Disease Prediction System  
**Focus:** Hyperparameter Tuning, Feature Importance, and Medical Reliability  
**Week 3 Goal:** Improve model performance and analyze medical predictors.

---

## 1. Hyperparameter Tuning Results

We performed extensive tuning using `GridSearchCV` across Logistic Regression, Random Forest, and SVM for all four diseases. The models were optimized primarily for **Recall** to minimize False Negatives (missing a disease).

### Performance Summary (Tuned Models)

| Disease | Best Model | Accuracy | Recall | ROC-AUC | Top Hyperparameters |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Heart Disease** | Random Forest | 88.5% | **92.9%** | 0.94 | `class_weight: balanced`, `n_estimators: 100` |
| **Diabetes** | Random Forest | 77.3% | 70.4% | 0.83 | `max_depth: 10`, `min_samples_split: 5` |
| **Stroke** | Logistic Regression | 72.9% | **82.0%** | 0.84 | `C: 0.01`, `penalty: l1` |
| **CKD** | Random Forest | **100%** | **100%** | 1.00 | Default/Balanced |

---

## 2. Feature Importance Analysis (Medical Insights)

Identifying the primary predictors is crucial for clinical trust. We used both internal Random Forest importance and model-agnostic **Permutation Importance**.

### Most Influential Medical Parameters
1. **Heart Disease:** 
    - `ca` (Number of major vessels), `cp` (Chest pain type), and `thalach` (Max heart rate).
    - *Insight:* Structural heart changes (vessels) and functional response (heart rate) are key.
2. **Diabetes:** 
    - `Glucose`, `BMI`, and `Age`.
    - *Insight:* Metabolic indicators (Glucose) remain the gold standard.
3. **Stroke:** 
    - `Age`, `avg_glucose_level`, and `hypertension`.
    - *Insight:* Age is the dominant non-modifiable risk factor, while glucose management is a critical modifiable one.
4. **CKD:** 
    - `hemo` (Hemoglobin), `pcv` (Packed Cell Volume), and `sg` (Specific Gravity).
    - *Insight:* CKD often leads to anemia (low hemoglobin), making these hematological markers perfect predictors.

---

## 3. CKD Dataset Investigation (Near-Perfect Accuracy)

Since Week 2 reported ~100% accuracy for CKD, we investigated potential data leakage or suspicious features.

**Findings:**
- **Data Leakage Check:** No administrative IDs or proxy labels were found.
- **Correlation Analysis:** The highest correlation with the target was `hemo` (0.73) and `pcv` (0.69). While high, these are not "leakage" but rather clinical diagnostic markers.
- **Why 100%?** The dataset (UCI CKD) has very distinct separation between classes in features like `hemo` and `sc`. In clinical datasets, these features are often used directly for diagnosis, leading to high model performance.
- **Conclusion:** The model is reliable for this specific dataset, though real-world performance may vary with more "borderline" cases.

---

## 4. Error Analysis

We analyzed False Negatives (FN) and False Positives (FP) for the best models.

- **False Negatives (The "Silent Killer"):** 
    - *Stroke:* 9 cases missed. Implications: Patients at risk of stroke might not receive preventative care.
    - *Diabetes:* 16 cases missed. Implications: Delayed diagnosis leads to long-term complications.
- **False Positives (The "False Alarm"):**
    - *Stroke:* 268 cases flagged. Implications: Higher healthcare burden due to unnecessary secondary screening, but safer than missing a stroke.

---

## 5. Observed Improvements & Limitations

### Improvements
- **Recall Increase:** Tuning specifically for recall significantly improved our ability to detect Diabetes and Stroke compared to baseline models.
- **SMOTE Stability:** Using SMOTE for the Stroke dataset allowed the models to learn the "Stroke" class despite it representing only 5% of the data.

### Remaining Limitations
- **Diabetes Complexity:** Despite tuning, Diabetes recall remains around 70%. The overlapping distributions of features like BMI and Insulin make it the hardest to predict.
- **Stroke False Positives:** To achieve 82% recall, we accepted a high number of false positives (low precision). This is a common trade-off in medical screening.

---

## 6. Visualization 
*Plots generated and available in `reports/figures/`:*
- `roc_curves/`: Combined ROC curves showing model comparison.
- `feature_importance/`: Bar charts highlighting medical predictors.
- `confusion_matrices_tuned/`: Visual breakdown of correct vs. incorrect predictions.

---

**Next Steps (Week 4):**
- Explore Ensemble Stacking to push Diabetes recall higher.
- Begin designing the Clinical Dashboard interface (non-functional mockups first).
