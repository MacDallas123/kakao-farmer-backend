# app/formations.py
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models import Formation
from app.schemas import FormationResponse, VideoFormationCreate, TextFormationCreate
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/likes", tags=["formations"])

