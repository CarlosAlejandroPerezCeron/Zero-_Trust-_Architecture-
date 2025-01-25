from fastapi import FastAPI, HTTPException, Request
from app.auth import create_token, verify_token, generate_mfa_secret, verify_mfa
from app.logging_config import log_security_event
import pyotp

app = FastAPI()

# Base de datos simulada con usuario ficticio
users_db = {
    "ceron8402@gmail.com": {"password": "alejo12345", "mfa_secret": generate_mfa_secret(), "failed_attempts": 0}
}

@app.get("/")
def root():
    return {"message": "Zero Trust API Running"}

@app.post("/auth/login")
def login(request: Request, username: str, password: str, mfa_code: str):
    if username not in users_db:
        log_security_event("LOGIN_FAIL", username, request.client.host, "FAILED", "Usuario no registrado")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = users_db[username]

    if user["password"] != password:
        user["failed_attempts"] += 1
        log_security_event("LOGIN_FAIL", username, request.client.host, "FAILED", "Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_mfa(user["mfa_secret"], mfa_code):
        log_security_event("MFA_FAIL", username, request.client.host, "FAILED", "Código MFA incorrecto")
        raise HTTPException(status_code=401, detail="Invalid MFA Code")

    user["failed_attempts"] = 0
    log_security_event("LOGIN_SUCCESS", username, request.client.host, "SUCCESS", "Inicio de sesión exitoso")
    token = create_token(username)
    return {"token": token}
