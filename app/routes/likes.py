# app/formations.py
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models import Formation
from app.schemas import FormationResponse, VideoFormationCreate, TextFormationCreate
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/formations", tags=["formations"])


# Creer une formation video
@router.post("/video", response_model=FormationResponse)
async def create_formation(formation: VideoFormationCreate, current_user=Depends(get_current_user)):
    new_formation = await Formation.create(**formation.dict())
    await new_formation.save()

    return new_formation

# Creer une formation textuelle
@router.post("/text", response_model=FormationResponse)
async def create_formation(formation: TextFormationCreate, current_user=Depends(get_current_user)):
    new_formation = await Formation.create(**formation.dict())
    await new_formation.save()

    return new_formation


# supprimer une formation
@router.delete("/{formation_id}", dependencies=[Depends(get_current_user)])
async def delete_formation(formation_id: int, current_user=Depends(get_current_user)):
    formation = await Formation.filter(id=formation_id).first()
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    
    await formation.delete()
    return {"msg": "Formation deleted successfully"}

# lister les formations de l'utilisateur connecte
@router.get("/", response_model=list[FormationResponse])
async def get_formations(current_user=Depends(get_current_user)):
    formations = await Formation.filter(user=current_user).order_by('-date')
    return formations
