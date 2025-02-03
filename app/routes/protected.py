from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth import decode_access_token
from app.models import User

router = APIRouter(prefix="/protected", tags=["Protected"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.get("/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")

    user = await User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return {"msg": f"Hello, {username}! You have accessed a protected route."}
