import os
import smtplib
import time
import mimetypes
from email.message import EmailMessage
from typing import List
from fastapi import HTTPException
from backend.app.core.config import settings
from backend.app.utils.files import ensure_outputs

def send_smtp_email(sender: str, to_list: List[str], subject: str, body: str, attachments: List[str]):
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    user = settings.SMTP_USER
    password = settings.SMTP_PASS
    use_tls = settings.SMTP_TLS
    demo_mode = settings.DEMO_MODE

    if demo_mode:
        # Simular envío guardando el .eml
        ensure_outputs(os.path.join(settings.OUTPUTS_DIR, "sent_emails"))
        out_dir = os.path.join(settings.OUTPUTS_DIR, "sent_emails")
        
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = subject
        msg.set_content(body)
        for path in attachments:
            if not os.path.exists(path):
                continue
            ctype, _ = mimetypes.guess_type(path)
            maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
            with open(path, "rb") as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))
        fname = os.path.join(out_dir, f"email_{int(time.time())}.eml")
        with open(fname, "wb") as f:
            f.write(bytes(msg))
        return

    if not host:
        raise HTTPException(status_code=500, detail="SMTP_HOST no configurado. Define variables SMTP_* o activa DEMO_MODE=true")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments:
        if not os.path.exists(path):
             continue
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))

    with smtplib.SMTP(host, port) as server:
        if use_tls:
            server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)
