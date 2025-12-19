from pydantic import BaseModel
from typing import Optional, List

class EmailSettings(BaseModel):
    # Backward- and forward-compatible fields
    sender_email: Optional[str] = None
    favorite_emails: Optional[List[str]] = None
    # Also accept alternative keys some frontends may send
    sender: Optional[str] = None
    favorites: Optional[List[str]] = None

class SendEmailRequest(BaseModel):
    pdf_url: Optional[str] = None
    pdf_path: Optional[str] = None
    sender: str
    recipients: List[str]
    subject: Optional[str] = "Revista de Convocatorias COTECMAR"
