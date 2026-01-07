import os
import smtplib
import time
import mimetypes
from email.message import EmailMessage
from typing import List, Any, Dict
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader

from backend.app.core.config import settings
from backend.app.utils.files import ensure_outputs

# Setup Jinja2 for emails
# Assuming templates are in /templates/emails
_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "templates")
email_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR))

def send_smtp_email(to_list: List[str], subject: str, html_content: str, sender: str = None, attachments: List[str] = []):
    if not sender:
        sender = settings.DEFAULT_SENDER_EMAIL

    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    user = settings.SMTP_USER
    password = settings.SMTP_PASS
    use_tls = settings.SMTP_TLS
    demo_mode = settings.DEMO_MODE

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg.set_content(html_content, subtype="html")

    for path in attachments:
        if not os.path.exists(path):
            continue
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))

    if demo_mode:
        # Simular envío guardando el .eml
        ensure_outputs(os.path.join(settings.OUTPUTS_DIR, "sent_emails"))
        out_dir = os.path.join(settings.OUTPUTS_DIR, "sent_emails")
        fname = os.path.join(out_dir, f"email_{int(time.time())}.eml")
        
        # Save explicit html debug file too
        with open(fname + ".html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        with open(fname, "wb") as f:
            f.write(bytes(msg))
        print(f"DEMO MODE: Email saved to {fname}")
        return

    if not host:
        print("SMTP_HOST not set, skipping email.")
        return

    try:
        with smtplib.SMTP(host, port) as server:
            if use_tls:
                server.starttls()
            if user and password:
                server.login(user, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        # Don't crash the app for email errors, but log it
        pass

def send_template_email(to_email: str, subject: str, template_name: str, context: Dict[str, Any]):
    try:
        template = email_env.get_template(template_name)
        html_content = template.render(**context)
        send_smtp_email([to_email], subject, html_content)
    except Exception as e:
        print(f"Template rendering error: {e}")

def send_reset_password_email(to_email: str, token: str):
    subject = f"{settings.PROJECT_NAME} - Recuperación de contraseña"
    link = f"{settings.API_INTERNAL_URL}/reset-password?token={token}"
    context = {
        "project_name": settings.PROJECT_NAME,
        "valid_hours": 24,
        "reset_link": link,
        "email": to_email
    }
    send_template_email(to_email, subject, "emails/reset_password.html", context)
