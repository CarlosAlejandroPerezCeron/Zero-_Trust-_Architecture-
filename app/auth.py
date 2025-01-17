import jwt
import datetime
import pyotp
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET_KEY = "supersecret"

security = HTTPBearer()

# Modelo de usuario con MFA
class UserMFA(BaseModel):
    username: str
    password: str
    mfa_code: str

# Generar código MFA para el usuario
def generate_mfa_secret():
    return pyotp.random_base32()

# Crear un token JWT
def create_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verificar Token
def verify_token(credentials: Security = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Verificar Código MFA
def verify_mfa(user_secret, mfa_code):
    totp = pyotp.TOTP(user_secret)
    return totp.verify(mfa_code)
