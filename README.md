# AI-Based Integrated Cardiometabolic & Renal Risk Assessment System

This project is a comprehensive multi-disease prediction system that calculates individual risks for Heart Disease, Diabetes, Stroke, and CKD, along with an integrated Global Risk Score (CHRI). It features a robust FastAPI backend and a clean, interactive professional frontend dashboard that provides explainable feature importance and logic-based risk-to-action healthcare mapping.

## 🚀 How to Run the App

### 1. Prerequisite: Install dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server (FastAPI)
Run the bootstrapper script from the project root:
```bash
python run_backend.py
```
The API server will start at `http://127.0.0.1:8000`.

### 3. Launch the Professional Frontend Dashboard
The project now includes an interactive dashboard that seamlessly integrates with the API backend to calculate risk probabilities, CHRI (Cardiometabolic Health Risk Indicator) scores, and provide automated, actionable healthcare recommendations.

To interact with the UI, simply open the `frontend/index.html` file in any modern web browser. 

### 4. View the Interactive API Docs (Swagger)
For developer testing, after starting the backend server, open your browser and go to:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

From here, you can:
*   Test endpoints directly (e.g., `/predict/heart`, `/recommend`).
*   Click **"Try it out"**.
*   Enter patient data in the JSON box.
*   Click **"Execute"** to see the real-time AI risk assessment.

---

## 📂 Project Structure for Teammates
*   `backend/`: Contains the FastAPI application logic and recommendation endpoints.
*   `frontend/`: Contains the clean, AI-powered healthcare dashboard UI (HTML, CSS, JS).
*   `models/exported/`: Contains the trained `.joblib` machine learning models.
*   `reports/`: Weekly progress reports, terminology guides, and system analysis documentation.
*   `scripts/`: Python scripts for model training and visualizing risk distributions.
*   `test_api.py`: A script to verify API payloads and overall system health.

## 📊 Key Documentation
For presentation preparation and analysis context, please review:
*   `reports/week7_analysis.md` & `reports/week6_progress_report.md`: Recent updates on system development.
*   `reports/terminology_guide.md`: Explains ML terms and model evaluation metrics.
*   `reports/dataset_parameters_guide.md`: Explains clinical features and why we monitor them.
*   `reports/midterm_presentation_outline.md`: The structure for our presentation.
