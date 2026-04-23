# CAPSTONE PROJECT REPORT: INTEGRATED DISEASE PREDICTION SYSTEM

## ABSTRACT
The **Integrated Disease Prediction System** is a sophisticated clinical decision-support platform designed to bridge the gap between complex machine learning diagnostics and patient-centric healthcare. By utilizing a "Soft Voting" ensemble of optimized classifiers (Random Forest, SVM, and Logistic Regression), the system predicts risks for four major chronic conditions: Heart Disease, Stroke, Diabetes, and Chronic Kidney Disease. These risks are aggregated into a novel **Cardiometabolic Health Risk Index (CHRI)**, providing a holistic 0–100 score of a patient's metabolic status. Key innovations include a user-filtered Explainable AI (XAI) engine that translates model weights into actionable vitals and a localized recommendation engine that discovers real-world Indian specialists and facilities. This project demonstrates a scalable, transparent, and authoritative approach to preventative AI healthcare.

---

## CHAPTER 1: INTRODUCTION
### 1.1 BACKGROUND
Modern healthcare is shifting from reactive treatment to preventative management. With the rise of lifestyle-related chronic diseases in India, there is an urgent need for tools that can synthesize multiple health markers into a single, actionable assessment.

### 1.2 OBJECTIVES
- To develop an ensemble-based prediction engine for multi-disease risk assessment.
- To implement the **CHRI (Cardiometabolic Health Risk Index)** meta-model.
- To create a transparent explainability layer for patient trust.
- To build a localized recommendation system for Indian healthcare providers.

---

## CHAPTER 2: LITERATURE SURVEY
Existing diagnostic systems often focus on a single disease in isolation, failing to account for the metabolic intersections between conditions like Diabetes and Kidney Disease. Furthermore, many AI models act as "black boxes," providing probabilities without explaining the underlying risk drivers. This project addresses these gaps by implementing ensemble learning and XAI.

---

## CHAPTER 3: SYSTEM DESIGN & METHODOLOGY
### 3.1 SYSTEM ARCHITECTURE
The system follows a modern decoupled architecture:
- **Backend**: FastAPI (Python) managing the clinical pipelines and scraper services.
- **Frontend**: A premium JavaScript-driven dashboard with a Glassmorphism design language.
- **Data Layer**: Optimized joblib models trained on verified medical datasets.

### 3.2 THE CHRI META-MODEL
The **Cardiometabolic Health Risk Index (CHRI)** is calculated using a meta-model that weights individual disease probabilities based on their clinical correlation:
- **Heart & Stroke**: High metabolic weight (35% & 30%).
- **Diabetes & CKD**: Secondary metabolic weights (20% & 15%).
- **Formula (Fallback)**: $CHRI = \sum (Risk_i \times Weight_i)$

### 3.3 EXPLAINABLE AI (XAI) ENGINE
The system utilizes Random Forest feature importance to identify top risk drivers. To ensure honesty, the dashboard filters these results to only show factors the user explicitly entered, hiding internal clinical assumptions.

---

## CHAPTER 4: IMPLEMENTATION
### 4.1 RECOMMENDATION ENGINE
The engine uses a two-stage discovery process:
1. **Live Scraping**: Using DuckDuckGo and Google Maps queries to find verified specialists (e.g., Cardiologists) in the user's city.
2. **Facility Discovery**: Leveraging the Nominatim OpenStreetMap API to locate hospitals, with a high-fidelity fallback to major Indian chains (Apollo, Fortis, Max).

### 4.2 USER INTERFACE (UX)
The dashboard features:
- **Animated Progress Indicators**: Color-coded risk bars synchronized with clinical thresholds.
- **Risk Benchmark Legend**: A 0–100 scale for immediate score interpretation.
- **Interactive Provider Assessments**: Hover-triggered overlays for doctor profiles and patient reviews.

---

## CHAPTER 5: SUMMARY AND CONCLUSIONS
The Integrated Disease Prediction System successfully demonstrates that AI can be both technically robust and patient-friendly. By combining high-accuracy ensemble models with localized, actionable recommendations, the system provides a comprehensive "Health Navigator" that empowers users to take control of their metabolic health.

---

## CHAPTER 6: SCOPE FOR FUTURE WORK
Future iterations will focus on:
- **IoT Integration**: Syncing real-time vitals from wearable devices.
- **Appointment Booking**: Direct API integration with hospital management systems.
- **Expanded Models**: Adding support for respiratory and oncology risk assessments.
