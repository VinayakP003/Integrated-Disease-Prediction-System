# Integrated Disease Prediction System — Complete Project Documentation

---

## 1. Project Overview

**Project Title:** AI-Based Integrated Cardiometabolic & Renal Risk Assessment System  
**Short Name:** Health Navigator / Integrated Disease Prediction System (IDPS)  
**Type:** Capstone Machine Learning + Full-Stack Web Application  

### What the System Does
The system is a clinical decision-support tool that takes a patient's basic health vitals and returns:
1. Individual risk probabilities for four diseases: **Heart Disease, Diabetes, Stroke, Chronic Kidney Disease (CKD)**
2. A single combined score called the **CHRI** (Cardiometabolic Health Risk Index)
3. **Explainability** — which factors drove the risk predictions
4. **Actionable recommendations** — urgency level + what the patient should do next
5. **Specialist doctor recommendations** scraped from the web in real time
6. **Nearby hospital/facility recommendations** using OpenStreetMap

---

## 2. Project Architecture (End-to-End)

```
Raw CSV Datasets
      │
      ▼
[Phase 1] Data Cleaning & EDA  (scripts/clean_data.py, scripts/eda.py)
      │
      ▼
[Phase 2] Baseline Model Training  (scripts/train_baselines.py)
      │   LR, RF, SVM per disease
      ▼
[Phase 3] Hyperparameter Optimization  (scripts/model_optimization.py)
      │   GridSearchCV → best params
      ▼
[Phase 4] Ensemble Modeling  (scripts/ensemble_modeling.py)
      │   Voting (Soft), Stacking → exported as .joblib
      ▼
[Phase 5] CHRI Meta-Model Training  (scripts/week7_upgrade.py)
      │   Logistic Regression on synthetic probability data
      ▼
[Phase 6] FastAPI Backend  (backend/app/)
      │   /predict/heart, /predict/diabetes, /predict/stroke, /predict/ckd
      │   /predict/chri  (calls all 4 + meta-model)
      │   /recommend/action, /recommend/doctors, /recommend/facilities
      ▼
[Phase 7] Frontend Dashboard  (frontend/)
      │   Single-page app — Input Form → Results Dashboard
      │   Bento-grid layout with CHRI gauge, risk bars, action plan
      │   Doctor cards with real-time scraped data
      ▼
User receives personalized health assessment + specialist recommendations
```

---

## 3. Datasets Used

| Disease | File | Records | Features | Target Column |
|---|---|---|---|---|
| Heart Disease | `data/heart_disease.csv` | 303 | 13 | `target` (0/1) |
| Diabetes | `data/diabetes.csv` | 768 | 8 | `Outcome` (0/1) |
| Stroke | `data/stroke.csv` | 5,110 | 10 | `stroke` (0/1) |
| CKD | `data/ckd.csv` | 400 | 24 | `class` (ckd/notckd) |

### Heart Disease Features
`age, sex, cp (chest pain type), trestbps (resting BP), chol (cholesterol), fbs (fasting blood sugar), restecg (ECG result), thalach (max heart rate), exang (exercise angina), oldpeak (ST depression), slope, ca (major vessels), thal`

### Diabetes Features
`Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age`

### Stroke Features
`gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status`

### CKD Features (24 columns)
`age, bp, sg (specific gravity), al (albumin), su (sugar), rbc, pc, pcc, ba, bgr, bu (blood urea), sc (serum creatinine), sod, pot, hemo, pcv, wc, rc, htn, dm, cad, appet, pe, ane`

---

## 4. Phase 1 — Data Cleaning & EDA

**Script:** `scripts/clean_data.py`, `scripts/eda.py`

### Cleaning Steps Per Dataset

**Heart Disease:**
- Named columns manually (CSV had no header)
- Binarized target: values 1–4 → 1 (disease), 0 → 0 (no disease)
- Treated `?` as NaN

**Diabetes:**
- Replaced biologically impossible zeros in `Glucose, BloodPressure, SkinThickness, Insulin, BMI` with NaN
- Zeros in these columns are medically invalid (e.g., glucose cannot be 0)

**Stroke:**
- Dropped the irrelevant `id` column
- Stripped whitespace from all categorical columns
- Retained BMI NaN values for imputation at model stage

**CKD:**
- Stripped column name whitespace
- Normalized `class` column: `'ckd\t'` → `'ckd'`
- Converted `pcv`, `wc`, `rc` to numeric (they had string artifacts)
- Dropped `id` column

### EDA Performed
- Dataset shape and feature listing
- Data type summary
- Missing value counts
- Target class distribution + imbalance ratio
- Visualizations saved to `reports/figures/`:
  - Target distribution bar chart
  - Correlation heatmap
  - Age/key feature histogram with KDE
  - Boxplot of key feature vs target

### Key Findings
- **Stroke dataset is severely imbalanced** (only ~4.87% positive cases → imbalance ratio ~0.06) → required SMOTE
- **CKD** had many mixed-type columns requiring explicit coercion
- **Diabetes**: zero-value imputation was critical for model accuracy

---

## 5. Phase 2 — Baseline Model Training

**Script:** `scripts/train_baselines.py`

### Three Baseline Models Trained Per Disease
1. **Logistic Regression** — linear probabilistic model
2. **Random Forest Classifier** — tree ensemble
3. **SVM (Support Vector Machine)** — margin-based classifier (with `probability=True`)

### Pipeline Construction
For each disease, a `sklearn.pipeline.Pipeline` was built:
```
Pipeline([
    ('preprocessor', ColumnTransformer),
    ('classifier', model)
])
```

**Preprocessor for Numeric Features:**
- `SimpleImputer(strategy='median')` → fills NaN with median
- `StandardScaler()` → normalizes to mean=0, std=1
- `RobustScaler()` used for Stroke (less sensitive to outliers)

**Preprocessor for Categorical Features:**
- `SimpleImputer(strategy='most_frequent')` → fills NaN with mode
- `OneHotEncoder(handle_unknown='ignore')` → creates binary columns

**Stroke Exception:** Used `ImbPipeline` (imbalanced-learn) to include `SMOTE` step between preprocessor and classifier.

### Evaluation Metrics
- Accuracy, Precision, Recall, F1 Score, ROC-AUC
- Confusion matrices saved per model per disease
- Results saved to `reports/baseline_results.csv`

---

## 6. Phase 3 — Hyperparameter Optimization

**Script:** `scripts/model_optimization.py`

### Method: GridSearchCV
- 5-fold cross-validation (`cv=5`)
- Scoring metric: **Recall** (prioritized to minimize false negatives in a medical context — missing a sick patient is more dangerous than a false alarm)
- `n_jobs=-1` for parallel processing

### Parameter Grids Searched

| Model | Parameters Tuned |
|---|---|
| Logistic Regression | C: [0.01, 0.1, 1, 10, 100], penalty: [l1, l2] |
| Random Forest | n_estimators: [100, 200], max_depth: [None, 10, 20], min_samples_split: [2, 5], class_weight: [balanced, None] |
| SVM | C: [0.1, 1, 10], kernel: [rbf, linear], gamma: [scale, auto] |

### Best Parameters Found (used in Ensemble phase)

**Heart Disease:**
- LR: C=1, penalty=l1, solver=liblinear
- RF: class_weight=balanced, max_depth=None, n_estimators=100
- SVM: C=10, gamma=scale, kernel=linear

**Diabetes:**
- LR: C=0.01, penalty=l1, solver=liblinear
- RF: class_weight=balanced, max_depth=10, n_estimators=200
- SVM: C=10, gamma=scale, kernel=rbf

**Stroke:**
- LR: C=0.01, penalty=l1, solver=liblinear
- RF: class_weight=balanced, max_depth=10, n_estimators=100
- SVM: C=0.1, gamma=auto, kernel=rbf

**CKD:**
- LR: C=10, penalty=l2, solver=liblinear
- RF: class_weight=balanced, max_depth=None, n_estimators=100
- SVM: C=1, gamma=auto, kernel=rbf

### Additional Analyses
- **Feature Importance:** Random Forest Gini importance + Permutation Importance (5 repeats, scored by Recall)
- **ROC Curves:** Combined ROC for all 3 models per disease
- **Error Analysis:** False Negatives (FN) and False Positives (FP) counted per model
- **Results saved to:** `reports/tuned_model_results.csv`

---

## 7. Phase 4 — Ensemble Modeling

**Script:** `scripts/ensemble_modeling.py`

### Two Ensemble Strategies

**1. Voting Classifier (Soft Voting)**
- Combines predictions from LR + RF + SVM
- `voting='soft'` → averages probability outputs (not just class votes)
- Final probability = average of the three models' probabilities
- More stable and accurate than hard voting

**2. Stacking Classifier**
- Base learners: LR + RF + SVM
- Meta-learner: `LogisticRegression()` trained on out-of-fold predictions of base learners
- More complex — learns optimal combination weights from data
- Can capture patterns that simple averaging misses

### Special Case: Optimized Diabetes Model
- Used LR + RF only (no SVM) with threshold = 0.4 (instead of 0.5)
- Lowering the threshold increases Recall (catches more diabetic patients)

### SMOTE (for Stroke only)
- `SMOTE(random_state=42)` applied after preprocessing on training data
- Synthetically generates minority class (stroke=1) samples
- Prevents model from ignoring the rare positive class

### Exported Models (14 `.joblib` files)
Each saved model is a full pipeline (`preprocessor → classifier`):
- `heart_voting_(soft).joblib`, `heart_stacking.joblib`, `heart_voting.joblib`
- `diabetes_voting_(soft).joblib`, `diabetes_stacking.joblib`, `diabetes_optimized_voting_optimized.joblib`
- `stroke_voting_(soft).joblib`, `stroke_stacking.joblib`, `stroke_voting.joblib`
- `ckd_voting_(soft).joblib`, `ckd_stacking.joblib`, `ckd_voting.joblib`

### Model Selected for Production
`voting_(soft)` for all four diseases — best balance of accuracy and AUC.

---

## 8. Phase 5 — CHRI Meta-Model (Week 7)

**Script:** `scripts/week7_upgrade.py`

### What is CHRI?
**Cardiometabolic Health Risk Index** — a single composite score (0–100%) representing overall multi-disease risk.

### Why a Meta-Model?
Instead of using fixed manual weights (Heart×0.35 + Stroke×0.30 + Diabetes×0.20 + CKD×0.15), a Logistic Regression meta-model was trained to **learn optimal weights** from data.

### Training Approach
Since real "combined disease" data doesn't exist, a **synthetic dataset** of 10,000 patients was generated:
1. Simulated correlated disease probabilities using a **Multivariate Gaussian** with a correlation matrix reflecting known clinical co-occurrence (e.g., heart+stroke are highly correlated)
2. Converted Gaussian samples to probabilities using the **sigmoid function**
3. Defined ground truth: patient is high-risk if `0.4×P(heart) + 0.3×P(diabetes) + 0.2×P(stroke) + 0.1×P(ckd) > 0.4`
4. Trained `LogisticRegression` on features `[prob_heart, prob_diabetes, prob_stroke, prob_ckd]`

### Learned Weights
The meta-model learned its own internal weights through regression. The intercept and coefficients capture the relative clinical importance of each disease for the overall risk.

**Fallback:** If meta-model is unavailable, a manual weighted formula is used:
`CHRI = 0.35×heart + 0.30×stroke + 0.20×diabetes + 0.15×ckd`

### Reliability Analysis
- **Brier Score** calculated on Stroke dataset (measures probability calibration)
- **Baseline comparison:** Ensemble AUC vs. Single LR AUC on Stroke
- Results saved to `reports/week7_analysis.md`

---

## 9. Backend — FastAPI Application

**Directory:** `backend/app/`

### Structure
```
backend/app/
├── main.py                    # App entry point, CORS, router registration
├── routers/
│   ├── prediction.py          # All /predict/* endpoints
│   └── recommendation.py     # All /recommend/* endpoints
├── schemas/
│   ├── prediction.py          # Pydantic input models
│   └── recommendation.py     # Pydantic output models
└── services/
    ├── prediction_service.py  # Model loading, inference, explainability
    └── recommendation_service.py  # Action logic, doctor/facility search
```

### main.py
- Creates FastAPI app with title, description, version
- Adds `CORSMiddleware` with `allow_origins=["*"]` (open for frontend dev)
- Registers prediction and recommendation routers
- Root endpoint returns welcome message + docs link

### Prediction Endpoints (`/predict/`)

| Endpoint | Method | Input Schema | Output |
|---|---|---|---|
| `/predict/heart` | POST | `HeartPredictionInput` | probability, risk_level, top_features |
| `/predict/diabetes` | POST | `DiabetesPredictionInput` | probability, risk_level, top_features |
| `/predict/stroke` | POST | `StrokePredictionInput` | probability, risk_level, top_features |
| `/predict/ckd` | POST | `CKDPredictionInput` | probability, risk_level, top_features |
| `/predict/chri` | POST | `CHRIPredictionInput` | all 4 risks + CHRI score + recommendations + doctors |

The `/predict/chri` endpoint is the **primary endpoint** used by the frontend. It orchestrates all four predictions, computes CHRI, generates action recommendations, and fetches one recommended doctor per specialist.

### Recommendation Endpoints (`/recommend/`)

| Endpoint | Method | Input | Output |
|---|---|---|---|
| `/recommend/action` | POST | `RiskInput` (all 4 risks + CHRI) | urgency, actions, specialists list |
| `/recommend/doctors` | POST | `DoctorInput` (disease_focus, location) | list of doctor profiles |
| `/recommend/facilities` | POST | `LocationFacilitiesInput` (location, disease) | list of hospital names + addresses |

### Prediction Service (`prediction_service.py`)

**Model Loading:**
- Loads all 4 `voting_(soft)` pipelines using `joblib.load()`
- Loads the `chri_meta_model.joblib`
- Singleton pattern: `prediction_service = PredictionService()`

**Inference:**
- Converts Pydantic input to `pandas.DataFrame`
- Calls `.predict_proba(df)[0][1]` to get probability of positive class

**Explainability (`_explain_prediction`):**
- Extracts `RandomForestClassifier` from inside the `VotingClassifier`
- Uses the RF's `.feature_importances_` (Gini importance) as a proxy for feature impact
- Gets feature names from preprocessor's `get_feature_names_out()`
- Returns top 3 features with `importance` = "high" (top 2) or "medium" (rank 3)

**Risk Level Thresholds:**
```
< 0.20  → Low
< 0.40  → Moderate
< 0.70  → High
≥ 0.70  → Critical
```

**CHRI Calculation:**
- If meta-model exists: passes 4 probabilities as `[prob_heart, prob_diabetes, prob_stroke, prob_ckd]` to meta-model
- Fallback: weighted formula

### Recommendation Service (`recommendation_service.py`)

**Action Recommendation Logic (`get_action_recommendation`):**
Priority-based rule engine:
1. Evaluate CHRI score → set base urgency and CHRI action message
2. Check each disease individually:
   - ≥ 0.70 → "High Priority", add specialist
   - ≥ 0.50 → "Moderate", add lifestyle advice
3. Determine `primary_specialist` by finding the **highest individual risk value** ≥ 0.40
4. Specialist priority order: Stroke → Cardiologist → Nephrologist → Endocrinologist
5. Returns: `risk_level, urgency_level, recommended_specialists[], primary_specialist, suggested_actions[]`

**Urgency Levels:** Routine → Moderate → High Priority → Urgent

**Doctor Recommendation (`get_doctors_recommendation`):**
1. Maps disease name → specialist type (`Heart Disease → Cardiologist`, etc.)
2. If location provided: scrapes **DuckDuckGo HTML** (`html.duckduckgo.com/html/?q=...`) for real doctor names
3. Applies strict name filtering: must start with "Dr.", 2–4 words, no blacklisted words
4. Assigns random rating (4.5–5.0) and availability
5. Scrapes **real patient reviews** per doctor from DuckDuckGo (using `DDGParser`)
6. Adds Google Maps search URL for each doctor
7. Fallback: returns from static `doctors_db` (10 pre-loaded Indian doctors)

**Facility Recommendation (`fetch_nearby_facilities_mock`):**
1. Builds disease-specific query (e.g., "cardiac hospital in Mumbai")
2. Queries **OpenStreetMap Nominatim API** (`nominatim.openstreetmap.org/search`)
3. Filters out irrelevant results (dental, veterinary, aesthetic)
4. Fallback: returns from a list of well-known Indian hospital names with randomized areas

**No API Keys Required** — uses only standard library (`urllib`, `html.parser`) and free public APIs.

---

## 10. Frontend Dashboard

**Directory:** `frontend/`  
**Files:** `index.html`, `styles.css`, `app.js`

### Tech Stack
- Pure HTML5 + Vanilla CSS + Vanilla JavaScript (no framework)
- Google Fonts: Inter (body) + Outfit (headings)
- FontAwesome 6.4 (icons)
- API calls via `fetch()` (async/await)

### Two-View Single Page Application
**View 1: Input Form**
- 7 input fields: Age, BMI, Glucose, Blood Pressure, Hypertension (dropdown), Smoking Status (dropdown), City
- "Load Sample Patient" button fills mock data (age=68, BMI=32.1, glucose=175, etc.)
- "Get Health Assessment" submits → shows loading spinner

**View 2: Results Dashboard (Bento Grid)**
The dashboard is organized in a CSS grid with named sections:

| Section | Description |
|---|---|
| **Clinical Summary** | Auto-generated narrative (e.g., "You have HIGH risk primarily for Stroke, influenced by blood pressure…") |
| **CHRI Score** | Circular gauge showing 0–100 score with color-coded risk legend (green/yellow/orange/red) |
| **Action Plan** | Urgency badge + bullet list of what to do (consult specialist, monitor BP, etc.) |
| **Specific Risk Breakdown** | 4 progress bars for Heart/Diabetes/Stroke/CKD with color-coded percentages |
| **Risk Drivers ("Why?")** | Top 2–3 features that drove the prediction (e.g., Blood Pressure - High Impact) |
| **Find a Specialist** | Doctor cards with name, specialty, location, rating, reviews, Maps link |
| **Nearby Facilities** | Hospital cards with name, address, rating, Get Directions link |
| **Confidence & Disclaimer** | AI confidence level + medical disclaimer |

### Payload Construction (`buildPayload()`)
The frontend takes 7 simple user inputs and **maps them to all 4 disease-specific input schemas**:
- Heart: uses age, bp, glucose (as fbs flag), defaults for ECG/thal/etc.
- Diabetes: uses glucose, bp, bmi, age; defaults for pregnancies/insulin/skin thickness
- Stroke: uses age, hypertension, glucose, bmi, smoking status
- CKD: uses age, bp, glucose; safe defaults for all CKD-specific fields

This allows a simple 7-field form to power 4 complex models simultaneously.

### Risk Color Scale
```
< 20%  → Green  (Low)
20-40% → Yellow (Moderate)
40-70% → Orange (High)
≥ 70%  → Red    (Critical)
```

### Feature Humanization
A `featureDict` maps raw model feature names to readable phrases:
- `avg_glucose_level` → "blood sugar levels"
- `trestbps` → "blood pressure"
- `smoking_status` → "smoking habits"
- `hemo` → "hemoglobin levels"
- etc.

### API Call Flow
1. `POST /predict/chri` → Gets all risks, CHRI, action plan, initial doctors
2. `POST /recommend/doctors` → Fetches real-time specialist recommendations for location
3. `POST /recommend/facilities` → Fetches real-time nearby hospitals for location

---

## 11. Project Timeline (Week-by-Week)

| Week | Milestone |
|---|---|
| Week 1-2 | Dataset collection, EDA, data cleaning |
| Week 3 | Baseline model training (LR, RF, SVM) |
| Week 4 | Hyperparameter optimization (GridSearchCV), feature importance analysis |
| Week 5 | Ensemble modeling (Voting, Stacking), CHRI initial calculation |
| Week 6 | FastAPI backend development, endpoint design, Pydantic schemas |
| Week 7 | CHRI meta-model, explainability layer, error analysis, Brier score |
| Week 8+ | Frontend dashboard, recommendation pipeline, DuckDuckGo + OSM integration, UI polish |

---

## 12. Key Design Decisions

1. **Recall over Accuracy as optimization metric** — In medical screening, missing a sick patient (False Negative) is far more dangerous than falsely flagging a healthy one (False Positive).

2. **Soft Voting Ensemble selected for production** — Better calibrated probabilities vs. hard voting; simpler interpretation vs. stacking.

3. **SMOTE only for Stroke** — Stroke is severely imbalanced (~5% positive). Other datasets are relatively balanced enough for `class_weight='balanced'`.

4. **No external API keys** — All web data (doctors, reviews, facilities) sourced from DuckDuckGo HTML scraping and OpenStreetMap Nominatim to eliminate dependency on paid APIs.

5. **7-field simplified form** — Complex model inputs abstracted behind a simple user experience; sensible defaults used for non-critical features.

6. **Primary specialist alignment** — Both the Action Plan and Doctor Recommendations sections are driven by the same `primary_specialist` value from the backend, ensuring they always show the same specialist type.
