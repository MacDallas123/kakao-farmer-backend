# app/notifications.py
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.text import MIMEText

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