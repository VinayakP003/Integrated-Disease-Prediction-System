# Week 2 Progress Report: Pipeline Implementation and Baseline Model Training

**Project Title:** AI-Based Integrated Cardiometabolic & Renal Risk Assessment System  
**Week 2 Focus:** Preprocessing Pipelines, SMOTE, and Baseline ML Performance  

---

## 1. Implemented Preprocessing Pipeline

A unified `Scikit-Learn` pipeline architecture was implemented for each disease, ensuring a reproducible path from raw data to model input.

### Pipeline Components:
*   **Heart Disease:**
    *   Target: Binarized (0: No Disease, 1: Presence of Disease).
    *   Numeric Features: Median Imputation + Standard Scaling.
    *   Categorical Features: Mode Imputation + One-Hot Encoding.
*   **Diabetes:**
    *   Key Step: Replaced "0" values in Glucose, BP, BMI, etc., with `NaN` before median imputation.
    *   Scaling: Standard Scaling.
*   **Stroke:**
    *   Scaling: **RobustScaler** used for BMI and Glucose to mitigate outlier impact.
    *   Balancing: **SMOTE** (Synthetic Minority Over-sampling) applied only to the training set.
*   **CKD:**
    *   Numeric: Median Imputation + Standard Scaling.
    *   Categorical: Constant Imputation ("missing") + One-Hot Encoding.

---

## 2. Baseline Training Results & Comparison

Models used: **Logistic Regression (LR)**, **Random Forest (RF)**, and **Support Vector Machine (SVM)**.

### Disease Class Comparison Tables

#### Heart Disease (Cleveland UCI)
| Model | Accuracy | Precision | **Recall** | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.885 | 0.838 | **0.928** | 0.881 | 0.966 |
| Random Forest | 0.869 | 0.812 | 0.928 | 0.867 | 0.943 |
| SVM (RBF) | 0.885 | 0.838 | **0.928** | 0.881 | 0.964 |

#### Diabetes (Pima Indians)
| Model | Accuracy | Precision | **Recall** | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.707 | 0.600 | 0.500 | 0.545 | 0.813 |
| **Random Forest** | 0.772 | 0.702 | **0.611** | 0.653 | 0.818 |
| SVM (RBF) | 0.740 | 0.652 | 0.555 | 0.600 | 0.796 |

#### Stroke Prediction (Kaggle)
| Model | Accuracy | Precision | **Recall** | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.751 | 0.141 | **0.800** | 0.240 | 0.843 |
| Random Forest | 0.928 | 0.171 | 0.120 | 0.141 | 0.773 |
| SVM (RBF) | 0.808 | 0.120 | 0.460 | 0.190 | 0.773 |

#### Chronic Kidney Disease (UCI)
| Model | Accuracy | Precision | **Recall** | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.987 | 1.000 | 0.980 | 0.990 | 1.000 |
| **Random Forest** | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 |
| SVM (RBF) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

---

## 3. Medical Analysis & Observations

### Focus on Recall
In medical screening, **False Negatives (Type II Errors)** are more dangerous than False Positives. A low recall means patients with the disease are being told they are healthy.

*   **Stroke:** Logistic Regression achieved the highest Recall (**0.80**) thanks to SMOTE. While precision is low (high false alarm rate), it is the most effective baseline for catching actual stroke risks. Random Forest failed significantly here (Recall 0.12), highlighting that without careful tuning, complex models can ignore the minority class despite SMOTE.
*   **Heart Disease:** Excellent performance across the board. Recall of 0.93 indicates only 7% of high-risk cases were missed.
*   **Diabetes:** Performance is average. Recall (0.61) is insufficient for a screening tool. This suggests missing data (imputed zeros) might be affecting feature quality.
*   **CKD:** Perfect scores across all models suggest a likely "data leak" or a feature that strongly correlates with the target (e.g., Specific Gravity). This will be audited in Week 3.

### Best Baseline Models
1.  **Heart Disease:** Logistic Regression / SVM
2.  **Diabetes:** Random Forest
3.  **Stroke:** Logistic Regression (with SMOTE)
4.  **CKD:** Random Forest

---

## 4. Next Steps
*   **Hyperparameter Tuning:** Use GridSearch/RandomSearch to optimize Recall for Stroke and Diabetes.
*   **Feature Engineering:** Address the CKD dataset's perfect scores by inspecting feature importance.
*   **Integrated Risk Score:** Begin designing a mathematical framework to combine these 4 individual risks into a "Global Cardiometabolic-Renal Index".
