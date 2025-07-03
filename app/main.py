from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, complaints
from app.core.config import settings

app = FastAPI(title="Complaint Management System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(users.router)
app.include_router(complaints.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Complaint Management System"}