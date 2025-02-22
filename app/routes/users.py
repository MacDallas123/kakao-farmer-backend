from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, Token, UserLogin, UserResponse
from app.auth import hash_password, verify_password, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from tortoise.expressions import Q
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register")
async def register(user: UserCreate):
    existing_user = await User.filter(username=user.username).first()
    existing_email = await User.filter(email=user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_password = hash_password(user.password)
    
    new_user = await User.create(
        name=user.name,
        username=user.username,
        email=user.email,
        password=hashed_password,
        status=user.status
    )

    return {"msg": "Utilisateur créé avec succès", "id": new_user.id}

"""@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.filter(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}"""

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    existing_user = await User.filter(Q(username=user.identifier) | Q(email=user.identifier)).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")

    access_token = create_access_token({"sub": existing_user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    user_id = existing_user.id
    user_status = existing_user.status
    return {"user_id": user_id, "user_status": user_status,"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=list[UserResponse])
async def get_users(current_user = Depends(get_current_user)):
    users = await User.all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_users(user_id : int, current_user = Depends(get_current_user)):
    user = await User.filter(id = user_id).first()
    return user
