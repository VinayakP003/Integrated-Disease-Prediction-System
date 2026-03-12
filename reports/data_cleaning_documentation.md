# Data Cleaning and Preprocessing Documentation: Disease Prediction System

This document outlines the specific cleaning steps performed on the raw datasets for the **Disease Prediction System**. These steps ensure data quality and consistency before model training.

---

## 1. General Cleaning Steps (Applied to all)
- **Whitespace Removal:** Stripped leading and trailing whitespace from column names and string/categorical values to avoid matching errors.
- **Missing Value Identification:** Standardized missing value placeholders (like `?`) to `NaN` (Not a Number) for consistent handling by imputation algorithms.

---

## 2. Dataset-Specific Cleaning

### A. Heart Disease Dataset
- **Header Assignment:** Added descriptive column names as the raw file was headerless.
- **Target Binarization:** The original dataset had 5 stages of heart disease (0–4). Since our current focus is binary classification (Presence vs. Absence), values 1, 2, 3, and 4 were mapped to `1` (Disease), while 0 remained `0` (No Disease).
- **Missing Data:** Identified `?` values in features like `ca` (number of major vessels) and `thal` and converted them to `NaN`.

### B. Diabetes Dataset (Pima Indians)
- **Zero-Value Treatment:** In this dataset, `0` was used for features like `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, and `BMI`. Since these values are biologically impossible for living patients, they were replaced with `NaN` to indicate missing data. This allows for more accurate median/mean imputation later.

### C. Stroke Prediction Dataset
- **Feature Reduction:** Removed the `id` column as it is a unique identifier with no predictive power and could cause model overfitting.
- **Categorical Normalization:** Ensured all text-based categories (e.g., `gender`, `smoking_status`) were consistently formatted without extra spaces.

### D. Chronic Kidney Disease (CKD) Dataset
- **Target Variable Normalization:** Resolved inconsistencies in the target column (`class`), where some entries were labeled as `ckd` and others as `ckd\t` (due to tab characters). All were unified to `ckd` or `notckd`.
- **Numeric Conversion:** Columns like `pcv` (Packed Cell Volume), `wc` (White Blood Cell Count), and `rc` (Red Blood Cell Count) were stored as objects/strings in the raw data. These were converted to numeric types, and any non-numeric noise was set to `NaN`.
- **Feature Reduction:** Removed the `id` column.

---

## 3. Output
The cleaned versions of these files are stored in the `data/cleaned/` directory:
- `heart_disease_cleaned.csv`
- `diabetes_cleaned.csv`
- `stroke_cleaned.csv`
- `ckd_cleaned.csv`
