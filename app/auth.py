import hashlib, hmac, base64, json, time
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def hash_password(password: str) -> str:
    """ Hashage du mot de passe avec SHA-256 """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    """ Vérifie si le mot de passe correspond au hash """
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Génération d'un token JWT """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=60 * 24))
    to_encode.update({"exp": int(expire.timestamp())})

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip("=")

    signature = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_access_token(token: str):
    """ Décodage et vérification d'un token JWT """
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")

        expected_signature = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip("=")

        if not hmac.compare_digest(signature_b64, expected_signature_b64):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token r")

        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
        
        if payload["exp"] < int(time.time()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token expired {payload} - {int(time.time())}")

        return payload
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token p {str(e)}")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    
    user = await User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token " + token)
    
    return user

async def get_current_seller(current_user: User = Depends(get_current_user)):
    if current_user.status != "farmer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource.")
    return current_user


async def is_admin(current_user=Depends(get_current_user)):
    if current_user.status != 'admin':  # Vérifiez si le statut est 'admin'
        raise HTTPException(status_code=403, detail="Not enough permissions")