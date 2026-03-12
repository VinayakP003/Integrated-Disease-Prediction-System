# Week 5 Progress Report: Deployable Backend Service

## Project: Disease Prediction System

### Overview
This week, we transformed our validated ensemble models into a production-ready **Backend API** built on **FastAPI**. This allows real-time risk assessments for Heart Disease, Stroke, Diabetes, and CKD, along with the integrated CHRI score.

---

## 1. Backend Architecture
We implemented a modular **Service-Router** pattern to ensure scalability and clean separation of concerns. This structure allows the AI models to run in a dedicated "Service" layer while the "Routers" handle incoming web requests.

```text
backend/
├── app/
│   ├── main.py (App initialization)
│   ├── routers/ (API endpoint handlers)
│   ├── services/ (Prediction logic & model management)
│   ├── schemas/ (Data validation via Pydantic models)
│   ├── models/ (Placeholder for specialized ML data models)
│   └── utils/ (Helper functions)
├── README.md (Usage instructions)
└── run_backend.py (Entry point for starting the server)
```

---

## 2. API Endpoints
The following endpoints are now active and support **Auto-documentation (Swagger UI)**:

| Endpoint | Method | Response Example |
| :--- | :--- | :--- |
| `/predict/heart` | `POST` | `{"risk_probability": 0.72, "risk_level": "High"}` |
| `/predict/diabetes`| `POST` | `{"risk_probability": 0.41, "risk_level": "Moderate"}` |
| `/predict/chri` | `POST` | `{"heart": 0.72, "chri_score": 0.39, "risk_level": "Moderate"}` |

> [!IMPORTANT]
> **Model Optimization**: Models are loaded into memory **once** on server startup (Singleton pattern). This ensures sub-millisecond prediction times once the server is "warm."

---

## 3. Data Validation & Clinical Typing
We used **Pydantic Schemas** to enforce strict data types and valid biological ranges. This prevents the system from processing invalid data (like negative ages or non-numeric patient data).

```python
# From /backend/app/schemas/prediction.py
class StrokePredictionInput(BaseModel):
    gender: str          # 'Male', 'Female', 'Other'
    age: float           # Age range 0.0 - 120.0
    bmi: float           # Valid BMI range
    smoking_status: str  # Clinical categories ('smokes', 'never smoked', etc.)
```

---

## 4. Deployment Readiness
The system is now "Export Ready." We created a standardized prediction pipeline where raw JSON data enters the system and a fully processed risk score is returned instantly.

**Key Features:**
- **Auto-Imputation**: The backend handles missing fields automatically.
- **Auto-Scaling**: Raw numbers are correctly normalized before reaching the model.
- **Consensus Prediction**: Uses our Soft-Voting ensembles for maximum clinical reliability.

---

## 5. How to Run & Verify

1.  **Start the Server**:
    From the project root: `python run_backend.py`
2.  **Interactive Documentation**:
    Browse to `http://127.0.0.1:8000/docs` to test the API.
3.  **Automated Verification**:
    Run `python test_api.py` to see the backend correctly predict mock clinical cases.

---

## Next Steps (Week 6)
- **Frontend Development**: Build the React-based Clinical Dashboard.
- **Dashboard Integration**: Connect the frontend forms to the Backend API.
- **Reporting Engine**: Generate PDF health reports for patients based on API outputs.
