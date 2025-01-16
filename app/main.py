from fastapi import FastAPI, Depends
from app.auth import verify_token
from app.logging_config import setup_logging

app = FastAPI()

setup_logging()

@app.get("/")
def root():
    return {"message": "Zero Trust API Running"}

@app.get("/secure-endpoint")
def secure_endpoint(user: str = Depends(verify_token)):
    return {"message": f"Access granted to {user}"}
