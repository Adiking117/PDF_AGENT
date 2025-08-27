from fastapi import FastAPI
from app.routers import pdf, health
from app.db import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PDF Workflow API")

# Include routers
app.include_router(pdf.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "PDF Blog Workflow is running 🚀"}
