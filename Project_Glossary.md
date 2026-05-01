# Integrated Disease Prediction System — Project Glossary

---

## Section A: Machine Learning Models

### Logistic Regression (LR)
A statistical model that predicts the probability of a binary outcome (0 or 1). Despite the name "regression", it's a **classification** algorithm. It uses a sigmoid function to output probabilities between 0 and 1. Simple, fast, and highly interpretable. Used as a **base learner** in our ensemble.

### Random Forest Classifier (RF)
An ensemble of many **Decision Trees**, each trained on a random subset of data and features. Final prediction is the majority vote (or averaged probability). Handles non-linear data well. Provides **feature importance scores** (Gini importance) which we use for explainability.

### Support Vector Machine (SVM)
Finds the optimal **decision boundary (hyperplane)** that maximally separates classes. With `kernel='rbf'`, it can handle non-linear data by projecting it into a higher dimension. Used with `probability=True` so it can output class probabilities.

### Voting Classifier (Soft Voting)
Combines predictions from multiple models by **averaging their predicted probabilities**. `voting='soft'` is preferred because it uses the confidence of each model, not just which class it voted for. Our production ensemble.

### Stacking Classifier (StackingClassifier)
A two-level ensemble. Base learners (LR, RF, SVM) each make predictions, and those predictions become **features for a meta-learner** (another Logistic Regression) that makes the final decision. Learns optimal combination weights from data.

### CHRI Meta-Model
A Logistic Regression model trained on **synthetic multi-disease probability data** to output a single unified health risk score. Input features: `prob_heart, prob_diabetes, prob_stroke, prob_ckd`. Output: combined risk probability (0–1).

### Decision Tree
A model that makes predictions via a series of if-else splits on feature values. Single trees are interpretable but prone to overfitting. Random Forests combine many trees to fix this.

---

## Section B: ML Techniques & Concepts

### SMOTE (Synthetic Minority Over-sampling Technique)
A technique for handling **class imbalance**. It creates synthetic new samples for the minority class by interpolating between existing minority class samples. Used for the Stroke dataset because only ~5% of patients had strokes.

### Class Imbalance
When one class has far more samples than another. E.g., in Stroke: 95% "no stroke", 5% "stroke". Models trained on imbalanced data tend to predict the majority class always. Solutions: SMOTE, `class_weight='balanced'`, or threshold adjustment.

### `class_weight='balanced'`
A parameter in sklearn classifiers. Makes the model automatically **penalize misclassifying minority class samples more heavily**, proportional to class frequency. Alternative to SMOTE — no new data is generated.

### GridSearchCV
Systematic hyperparameter tuning. You provide a grid of parameter values; GridSearchCV tries every combination using **cross-validation** and picks the best. In our project: 5-fold CV, scored by Recall.

### Cross-Validation (5-Fold)
Splits data into 5 equal folds. For each fold: train on the other 4, test on this 1. Averages the 5 test scores. Gives a more reliable performance estimate than a single train-test split.

### Pipeline (sklearn)
Chains preprocessing steps and a model into one object. Prevents **data leakage** — the scaler only learns from training data, not test data, because it's fit inside the pipeline.

### ColumnTransformer
Applies different transformations to different columns. In our project: `StandardScaler` to numeric columns, `OneHotEncoder` to categorical columns — all in one step.

### SimpleImputer
Fills missing (NaN) values. Strategy `median` replaces NaN with the column's median value. Strategy `most_frequent` uses the most common value.

### StandardScaler
Transforms features to have **mean = 0 and standard deviation = 1**. Essential for LR and SVM which are sensitive to feature scale.

### RobustScaler
Like StandardScaler but uses **median and IQR** instead of mean and std. Less sensitive to outliers. Used for the Stroke dataset which has continuous features with outliers.

### OneHotEncoder
Converts categorical variables into binary (0/1) columns, one per category. E.g., `smoking_status` becomes three columns: `never_smoked`, `formerly_smoked`, `smokes`.

### Feature Importance (Gini/MDI)
A score from Random Forest that measures how much each feature **reduces impurity** (uncertainty) across all trees. Higher = more important. Also called "Mean Decrease in Impurity".

### Permutation Importance
Measures feature importance by randomly **shuffling one feature's values** and measuring how much model performance drops. More reliable than Gini importance for interpreting models.

### ROC Curve (Receiver Operating Characteristic)
A plot of True Positive Rate (Recall) vs. False Positive Rate at different decision thresholds. Shows the trade-off between sensitivity and specificity.

### AUC (Area Under the ROC Curve)
A single number (0.5–1.0) summarizing the ROC curve. AUC = 1.0 is a perfect model. AUC = 0.5 is random guessing. We target AUC > 0.85 in our models.

### Brier Score
Measures how well **calibrated** a model's probabilities are. The average squared difference between predicted probability and actual outcome. Range: 0 (perfect) to 1 (worst). Values < 0.10 are considered very good.

### Confusion Matrix
A 2×2 table showing True Positives (TP), True Negatives (TN), False Positives (FP), False Negatives (FN).
- **TP:** Predicted sick, actually sick ✓
- **TN:** Predicted healthy, actually healthy ✓
- **FP:** Predicted sick, actually healthy ✗ (false alarm)
- **FN:** Predicted healthy, actually sick ✗ (dangerous miss)

### Recall (Sensitivity)
`Recall = TP / (TP + FN)` — Of all actually sick patients, how many did we correctly identify? We **optimize for Recall** because FN (missing a sick patient) is more dangerous in medical contexts.

### Precision
`Precision = TP / (TP + FP)` — Of all patients we flagged as sick, how many actually were? High precision = fewer false alarms.

### F1 Score
Harmonic mean of Precision and Recall: `F1 = 2×(P×R)/(P+R)`. Useful when you want a balance of both.

### Sigmoid Function
`σ(x) = 1 / (1 + e^(-x))` — Maps any real number to the range (0, 1). Used in Logistic Regression to convert a linear score into a probability.

### Gaussian Copula / Multivariate Normal
A statistical model for generating **correlated random variables**. Used in Week 7 to synthesize 10,000 realistic patients whose 4 disease probabilities are positively correlated (as they are in real life).

### Decision Threshold
The cutoff probability above which a prediction is classified as positive. Default is 0.5. Lowering to 0.4 (as done for the Optimized Diabetes model) increases Recall at the cost of more False Positives.

### Error Analysis
Studying the types of errors a model makes — specifically False Negatives and False Positives — to understand where the model fails and how to improve it.

### Stratified Train-Test Split
When splitting data into train/test, stratification ensures the **class proportion is preserved** in both sets. Prevents by-chance skewed splits.

---

## Section C: Clinical / Medical Terms

### CHRI (Cardiometabolic Health Risk Index)
Our custom composite score (0–100%). Combines individual disease probabilities into one number representing overall multi-disease health risk.

### Hypertension
High blood pressure (systolic ≥ 130 mmHg). A major risk factor for Heart Disease, Stroke, and CKD.

### Serum Creatinine (sc)
A waste product in blood filtered by kidneys. Elevated levels indicate **kidney dysfunction**. Key feature in CKD prediction.

### Hemoglobin (hemo)
Protein in red blood cells carrying oxygen. Low hemoglobin = **anemia**, a complication and indicator of CKD.

### ST Depression (oldpeak)
A measure from an ECG (electrocardiogram). Higher values indicate **myocardial ischemia** (reduced blood flow to heart).

### Thalach (Maximum Heart Rate)
The maximum heart rate achieved during a stress test. Lower max HR in older patients can indicate heart problems.

### DiabetesPedigreeFunction
A score representing **genetic diabetes risk** based on family history. A higher value means a stronger hereditary diabetes component.

### Specific Gravity (sg)
A measure of urine concentration. Very low values indicate kidneys can't concentrate urine — a CKD marker.

### BMI (Body Mass Index)
`BMI = weight (kg) / height² (m²)`. Categorizes body weight: <18.5 underweight, 18.5–24.9 normal, 25–29.9 overweight, ≥30 obese. Obesity elevates risk for all four diseases.

### Cardiologist
Heart specialist. Recommended when Heart Disease risk is elevated.

### Endocrinologist
Hormone and metabolism specialist. Recommended when Diabetes risk is elevated.

### Neurologist
Brain and nervous system specialist. Recommended when Stroke risk is elevated.

### Nephrologist
Kidney specialist. Recommended when CKD risk is elevated.

---

## Section D: Backend Tech Stack

### FastAPI
A modern Python web framework for building APIs. Key features: automatic **OpenAPI (Swagger) documentation**, async support, very high performance (comparable to NodeJS). Built on top of Starlette and Pydantic.

### Uvicorn
ASGI (Asynchronous Server Gateway Interface) server that **runs the FastAPI application**. Invoked with `uvicorn backend.app.main:app`.

### Pydantic
Data validation library used by FastAPI. **Schemas define the shape of API inputs and outputs**. Automatically validates types, raises clear errors on bad input. E.g., `HeartPredictionInput` ensures all fields are present and correctly typed.

### BaseModel (Pydantic)
The base class all our schemas inherit from. Provides automatic parsing, validation, and JSON serialization of request/response data.

### APIRouter
FastAPI's way of **grouping related endpoints**. We have two routers: `prediction_router` and `recommendation_router`. They're registered in `main.py`.

### CORS (Cross-Origin Resource Sharing)
Browser security policy that blocks JavaScript from calling APIs on different domains/ports. `CORSMiddleware(allow_origins=["*"])` disables these restrictions so our frontend (file://) can call the backend (localhost:8000).

### joblib
A Python library for **saving and loading Python objects to/from disk**. Used to serialize trained scikit-learn pipeline objects (`.joblib` files). Faster than `pickle` for large numpy arrays.

### pandas
Python library for data manipulation. We use `pd.DataFrame([data.model_dump()])` to convert Pydantic input into a DataFrame, which sklearn models expect.

### DuckDuckGo HTML Scraping
Uses `urllib.request` to fetch the HTML version of DuckDuckGo search results (`html.duckduckgo.com/html/?q=...`). A custom `HTMLParser` subclass (`DDGParser`, `DoctorNameParser`) extracts text snippets and search result titles. No API key needed.

### OpenStreetMap Nominatim API
A free geocoding and place search API. We query it with `https://nominatim.openstreetmap.org/search?q={hospital in location}&format=json` to find real hospital names and addresses. No API key needed.

### Singleton Pattern
`prediction_service = PredictionService()` is called once at module load time and reused across all requests. Prevents reloading large `.joblib` files on every API call.

### HTTPException
FastAPI's way of returning HTTP error responses. We wrap all endpoint logic in `try/except` and raise `HTTPException(status_code=500, detail=str(e))` on failures.

---

## Section E: Frontend Tech Stack

### Vanilla JavaScript (ES6+)
Plain JavaScript without any framework. Uses `async/await` for API calls, `fetch()` for HTTP requests, and DOM manipulation (`innerHTML`, `getElementById`).

### fetch() API
Browser-native function for making HTTP requests. Returns a Promise. We `await` the response and parse it as JSON.

### async/await
JavaScript syntax for writing asynchronous code that looks synchronous. `async function f() { const data = await fetch(...); }` — the function pauses at `await` until the network call completes.

### Vanilla CSS
Plain CSS without frameworks like Tailwind or Bootstrap. We use CSS custom properties (`--health-good`, `--accent-primary`), CSS Grid (bento layout), Flexbox, and conic-gradient for the CHRI circle.

### CSS Custom Properties (Variables)
`--health-good: #22c55e` etc. Defined in `:root {}`. Makes theming consistent across the whole stylesheet.

### Glassmorphism
A UI design trend using **frosted glass effect**: semi-transparent background, `backdrop-filter: blur()`, subtle border. All `.glass-panel` elements use this.

### Bento Grid
A CSS Grid layout inspired by Apple's marketing pages. Cards of different sizes arranged in a grid. We use `col-span-4`, `col-span-6`, `col-span-8`, `col-span-12` utility classes.

### Conic Gradient (CHRI Gauge)
`conic-gradient(color 60%, transparent 60%)` creates a pie/gauge effect. Used for the circular CHRI score display.

### FontAwesome
Icon library (CDN link). We use icon classes like `fa-solid fa-heart-pulse` for UI icons.

### Google Fonts
We load `Inter` (body text) and `Outfit` (headings) via CDN for modern typography.

### SPA (Single Page Application)
The entire UI lives in one HTML file. Switching between the Input Form and Results Dashboard is done by toggling CSS classes (`active-view`) — no page reload.

### Payload Mapping
The `buildPayload()` function translates 7 user inputs into the complex 4-schema JSON object that `/predict/chri` expects. This abstraction hides ML complexity from users.
