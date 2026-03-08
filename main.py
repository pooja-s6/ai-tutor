from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.usage import router as usage_router

app = FastAPI(title="AI Tutor Backend")

# Include routers
app.include_router(chat_router, prefix="/api/v1")
app.include_router(usage_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "AI Tutor Backend Running"}

@app.get("/health")
def health():
    return {"status": "Backend healthy"}
