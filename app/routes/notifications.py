# app/notifications.py
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models import Notification
from app.schemas import NotificationCreate, NotificationResponse
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/notifications", tags=["notifications"])

## Send mail notifications
def send_email_notification(to_email: str, subject: str, message: str):
    try:
        # Valider l'email
        valid = validate_email(to_email)
        to_email = valid.email

        # Configuration de l'email
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = "tsakeuflora@gmail.com"
        msg['To'] = to_email

        # Envoi de l'email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("tsakeuflora@gmail.com", "obij btxo roik jeru")
            server.send_message(msg)

    except EmailNotValidError as e:
        print(f"Invalid email: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")





# Creer une notification
@router.post("/", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate, current_user=Depends(get_current_user)):
    new_notification = await Notification.create(**notification.dict())
    await new_notification.save()

    return new_notification

# read notification
@router.patch("/{notification_id}/read", dependencies=[Depends(get_current_user)])
async def set_as_read(notification_id: int, current_user=Depends(get_current_user)):
    notification = await Notification.filter(id=notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read_at = datetime.now()
    await notification.save()
    return {"msg": "Notification set as read"}


#supprimer une notification
@router.delete("/{notification_id}", dependencies=[Depends(get_current_user)])
async def delete_notification(notification_id: int, current_user=Depends(get_current_user)):
    notification = await Notification.filter(id=notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    await notification.delete()
    return {"msg": "Notification deleted successfully"}

# lister les notifications de l'utilisateur connecte
@router.get("/", response_model=list[NotificationResponse])
async def get_notifications(current_user=Depends(get_current_user)):
    notifications = await Notification.filter(user=current_user).order_by('-date')
    return notifications
