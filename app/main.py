from fastapi import FastAPI, HTTPException, Depends
from app.auth import create_token, verify_token, generate_mfa_secret, verify_mfa
import pyotp

# Creación única de la API
app = FastAPI()

# Base de datos simulada de usuarios
users_db = {
    "admin": {"password": "admin123", "mfa_secret": generate_mfa_secret()}
}

# ✅ Ruta raíz para verificar que la API está corriendo
@app.get("/")
def root():
    return {"message": "Zero Trust API Running"}

# ✅ Endpoint de login con MFA
@app.post("/auth/login")
def login(username: str, password: str, mfa_code: str):
    if username not in users_db or users_db[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verificar el código MFA
    if not verify_mfa(users_db[username]["mfa_secret"], mfa_code):
        raise HTTPException(status_code=401, detail="Invalid MFA Code")

    token = create_token(username)
    return {"token": token}

# ✅ Endpoint para configurar MFA
@app.get("/auth/mfa-setup")
def mfa_setup(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    secret = users_db[username]["mfa_secret"]
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name="ZeroTrustApp")

    return {"mfa_secret": secret, "qr_code": otp_uri}
