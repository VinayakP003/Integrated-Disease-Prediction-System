# Project Glossary: AI-Based Integrated Risk Assessment
**A Guide for Team Presentation Preparation**

This document provides clear explanations of the technical terminologies and methodologies used across the Capstone Project (Week 1 to Week 5). It is designed to ensure everyone on the team can confidently explain the "How" and "Why" during the presentation.

---

## 1. Machine Learning Performance Metrics
*These terms describe how we measure the "success" of our models.*

| Term | Simple Explanation | Why We Use It |
| :--- | :--- | :--- |
| **Accuracy** | The percentage of total predictions that were correct. | Good overall snapshot, but can be misleading for imbalanced data (like Stroke). |
| **Recall (Sensitivity)** | The ability of the model to find **all** actual positive cases (e.g., catching everyone who has a disease). | **Critical for Medicine.** It's better to have a "False Alarm" than to tell a sick person they are healthy. |
| **Precision** | Out of everyone the model flagged as "at risk," how many actually had the disease? | Higher precision means fewer "False Alarms." |
| **ROC-AUC** | A score (0 to 1) that measures how well the model distinguishes between "Healthy" and "Sick." | A score of 0.8+ is considered very good for clinical diagnostic models. |
| **False Negative** | When the model says someone is "Healthy" but they are actually "Sick." | We call this the **"Silent Killer"** in our reports because it leads to missed treatment. |

---

## 2. Preprocessing & Data Quality
*These terms describe how we cleaned and prepared the raw medical data.*

*   **Imputation**: The process of "filling in the blanks." We used **Median Imputation** for numbers (filling missing BMI with the middle value) and **Constant Imputation** for categories (labeling missing data as "Unknown").
*   **Scaling (Standard vs. Robust)**: Adjusting data so large numbers (like Glucose) don't overpower small numbers (like Age). We used **RobustScaler** for features with many outliers (extreme values) to prevent them from skewing the model.
*   **One-Hot Encoding**: Converting text categories (e.g., "Smoker", "Never Smoked") into numbers (0s and 1s) so the math models can understand them.
*   **SMOTE (Synthetic Minority Over-sampling)**: A technique to "balance" our data. For example, if only 5% of our data has Stroke, SMOTE creates "synthetic" examples of stroke patients so the model has enough to learn from.

---

## 3. Advanced Modeling Strategies
*These terms describe the sophisticated techniques used to boost performance.*

*   **Hyperparameter Tuning (GridSearchCV)**: Like fine-tuning a radio. We tested thousands of combinations of internal model settings to find the exact configuration that gave us the highest **Recall**.
*   **Ensemble Modeling**: Using a "Team" of models instead of just one.
    *   **Voting Classifier**: Multiple models (RF, SVM, LR) vote on the outcome. The majority or the highest average confidence wins.
    *   **Stacking**: A "Master Model" looks at the predictions of other models and learns which one to trust more in specific scenarios.
*   **Model Pruning**: Removing a model from the ensemble if it is performing poorly or "diluting" the accuracy of the stronger models (e.g., we removed SVM from the Diabetes ensemble in Week 4).

---

## 4. The CHRI Framework (Our Key Innovation)
*This is the heart of the project integration.*

*   **CHRI (Cardiometabolic Health Risk Index)**: A single comprehensive score (0.0 to 1.0) created by combining the risks of Heart Disease, Stroke, Diabetes, and CKD.
*   **Weighted Sum**: We don't just add the risks; we weight them based on medical priority (e.g., Heart and Stroke are weighted higher at 35% and 30% respectively).
*   **Risk Thresholds**: Categorizing the continuous CHRI score into clinical action levels: **Low**, **Moderate**, **High**, and **Critical**.

---

## 5. Backend & Deployment
*These terms describe how we turned the models into a working application.*

*   **FastAPI**: The modern framework used to build our web server. It is extremely fast and automatically generates a "Swagger UI" (interactive documentation).
*   **Pydantic**: A tool that ensures the data entering the system is valid (e.g., making sure a patient's Age is a number and not "Twenty").
*   **Singleton Pattern**: Ensuring the ML models are loaded into the computer's memory only **once** when the server starts, rather than reloading them for every single patient (which would be slow).
*   **REST API**: A standard way for different software (like a website and a server) to talk to each other using JSON "messages."

---

## 6. Medical Indicators (Dataset Context)
*   **CKD (Chronic Kidney Disease)**: Measured using **Hemoglobin** (hemo) and **PCV** (Packed Cell Volume).
*   **Diabetes**: Primary indicators are **Glucose** and **BMI**.
*   **Heart Disease**: Key indicators include **Thalach** (Maximum Heart Rate) and **CA** (Number of major vessels).
