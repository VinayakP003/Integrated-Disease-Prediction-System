# 🚀 Disease Prediction System Backend

This backend service provides production-ready endpoints for predicting cardiometabolic diseases using the ensemble models trained in previous weeks.

## 🏗️ Architecture
- **Framework**: FastAPI (High-performance Async Python)
- **Validation**: Pydantic (Strong type checking for clinical data)
- **Serialization**: Joblib (Pipeline persistence)
- **Ensemble Model**: Soft-Voting Classifier (Logistic Regression + Random Forest + SVM)

## 📡 Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/predict/heart` | Returns Heart Disease risk probability. |
| `POST` | `/predict/diabetes` | Returns Diabetes risk probability. |
| `POST` | `/predict/stroke` | Returns Stroke risk probability. |
| `POST` | `/predict/ckd` | Returns Chronic Kidney Disease risk probability. |
| `POST` | `/predict/chri` | Returns all individual risks + the combined Global Score. |

---

## 🛠️ How to Run

1.  **Ensure Dependencies are Installed**:
    ```bash
    pip install fastapi uvicorn scikit-learn pandas joblib imbalanced-learn
    ```

2.  **Start the Server**:
    From the project root:
    ```bash
    python run_backend.py
    ```

3.  **Access Interactive Docs**:
    Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

---

## 🧪 Example Request (`/predict/heart`)

```json
{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

## 🧪 Example Request (`/predict/chri`)

The `/predict/chri` endpoint expects a combined JSON containing four separate sections (`heart`, `diabetes`, `stroke`, `ckd`). Refer to the `/docs` page for a full example body.
