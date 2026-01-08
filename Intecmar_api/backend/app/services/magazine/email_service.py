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

def send_smtp_email(to_list: List[str], subject: str, html_content: str, sender: str = None, attachments: List[str] = [], inline_attachments: List[tuple] = []):
    """
    inline_attachments: List of (file_path, content_id) tuples.
    """
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
    
    # Use make_related() or set_content then add_related
    # Simplest for HTML with inline images:
    msg.set_content(html_content, subtype="html")

    # Add inline attachments (images referenced by cid:xxxx)
    for path, cid in inline_attachments:
        if not os.path.exists(path):
            print(f"Inline attachment not found: {path}")
            continue
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
        
        with open(path, "rb") as f:
            file_data = f.read()
            msg.add_related(file_data, maintype=maintype, subtype=subtype, cid=f"<{cid}>", filename=os.path.basename(path))

    # Add regular attachments
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
        pass

def send_template_email(to_email: str, subject: str, template_name: str, context: Dict[str, Any], inline_attachments: List[tuple] = []):
    try:
        template = email_env.get_template(template_name)
        html_content = template.render(**context)
        send_smtp_email([to_email], subject, html_content, inline_attachments=inline_attachments)
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
    
    # Locate Logo
    # _TEMPLATE_DIR is .../templates
    # We need .../static/images/CotecmarLogo_white.png
    root_dir = os.path.dirname(_TEMPLATE_DIR) # Intecmar_api
    logo_path = os.path.join(root_dir, "static", "images", "CotecmarLogo_white.png")
    
    inline = []
    if os.path.exists(logo_path):
        inline = [(logo_path, "logo_cotecmar")]
    else:
        print("Warning: Logo file not found for email embedding.")

    send_template_email(to_email, subject, "emails/reset_password.html", context, inline_attachments=inline)

def send_notification_email(to_email: str, subject: str, title: str, body: str, cta_link: str = None, cta_text: str = None, attachments: List[str] = []):
    """
    Envía un correo de notificación genérico con el branding de Intecmar AI.
    """
    context = {
        "project_name": settings.PROJECT_NAME,
        "title": title,
        "body": body,
        "cta_link": cta_link,
        "cta_text": cta_text
    }
    
    # Locate Logo
    root_dir = os.path.dirname(_TEMPLATE_DIR)
    logo_path = os.path.join(root_dir, "static", "images", "CotecmarLogo_white.png")
    
    inline = []
    if os.path.exists(logo_path):
        inline = [(logo_path, "logo_cotecmar")]
        
    # Render template manually to include regular attachments in the final send_smtp call
    # Or better, reuse send_template_email but we need to support regular attachments there too.
    # Let's fix send_template_email first to support attachments.
    
    try:
        template = email_env.get_template("emails/notification.html")
        html_content = template.render(**context)
        send_smtp_email(
            [to_email], 
            subject, 
            html_content, 
            attachments=attachments, 
            inline_attachments=inline
        )
    except Exception as e:
        print(f"Notification email error: {e}")
