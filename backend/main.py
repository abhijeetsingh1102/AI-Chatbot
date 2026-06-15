from fastapi import FastAPI
from backend.llama_api import router as llama_router

app = FastAPI(
    title="Secure Chat Guardian",
    description="FastAPI backend integrated with LLaMA API",
    version="1.0.0"
)

# Include the llama API routes
app.include_router(llama_router)

@app.get("/")
def root():
    return {"message": "Secure Chat Guardian Backend is running with LLaMA API 🚀"}