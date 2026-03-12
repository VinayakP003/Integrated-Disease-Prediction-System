from fastapi import FastAPI
from backend.app.routers.prediction import router as prediction_router

app = FastAPI(
    title="Disease Prediction System API",
    description="A multi-model API for predicting cardiometabolic risk factors (Heart, Stroke, Diabetes, CKD) and a combined CHRI score.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Disease Prediction System API",
        "docs": "/docs"
    }

# Include prediction routes
app.include_router(prediction_router, tags=["Predictions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
