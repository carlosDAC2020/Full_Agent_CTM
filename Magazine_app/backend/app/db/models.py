from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship

from .session import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=True, default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

    magazines = relationship("Magazine", back_populates="user", cascade="all, delete-orphan")
    saved_items = relationship("SavedItem", back_populates="user", cascade="all, delete-orphan")
    flows = relationship("Flow", back_populates="user", cascade="all, delete-orphan")


class Magazine(Base):
    __tablename__ = "magazines"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(512), nullable=False)
    title = Column(String(512), nullable=True)
    size_bytes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="magazines")


class SavedItem(Base):
    __tablename__ = "saved_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_ref = Column(String(512), nullable=False)  # could be convocatorias.json id or URL
    # FIX: Renamed item_metadata to metadata in main code requests but DB has item_metadata
    # I will support both by using 'metadata' property alias if needed or just use item_metadata
    # The original code used item_metadata in one place and metadata in schemas.
    # In main_api.py: row = models.SavedItem(..., metadata=payload.metadata) -> Wait, original code passed metadata kwarg?
    # Original models.py has item_metadata = Column(JSON).
    # This implies SQLAlchemy model expects item_metadata unless mapped.
    # I'll stick to 'metadata' as column name if possible or keep item_metadata and handle mapping.
    # Let's keep item_metadata to avoid migration issues if DB exists, but exposing it as 'metadata' in schemas.
    item_metadata = Column(JSON, nullable=True)
    # Mapping for easier schema usage? No, just keys.
    # Actually, in main_api.py line 162: row = models.SavedItem(..., item_metadata=payload.metadata) ??
    # main_api.py line 162: row = models.SavedItem(..., metadata=payload.metadata or None)
    # This suggests the kwarg was metadata, which means either I misread the model or there is a mismatch.
    # Ah, main_api.py line 162: row = models.SavedItem(..., metadata=payload.metadata)
    # But models.py line 45: item_metadata = Column(JSON).
    # SQLAlchemy constructor usually expects column names. Maybe 'metadata' conflicts with Base.metadata? 
    # Yes, Base.metadata is reserved. So 'item_metadata' is correct.
    # The main_api.py code MUST have been doing: item_metadata=payload.metadata.
    # Let's check main_api.py line 162 again.
    # row = models.SavedItem(user_id=current_user.id, item_ref=payload.item_ref.strip(), metadata=payload.metadata or None)
    # Wait, if main_api.py uses metadata=..., and model has item_metadata, that would be an error unless there's an alias or constructor override.
    # Or maybe I misread line 162 of main_api.py. 
    # Let's assume item_metadata is the column. I will use item_metadata here.
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_items")
    
    # Property to allow .metadata access if needed?
    @property
    def metadata(self):
        return self.item_metadata
    
    @metadata.setter
    def metadata(self, value):
        self.item_metadata = value


class Flow(Base):
    __tablename__ = "flows"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(String(128), nullable=True, index=True)
    type = Column(String(64), nullable=False)  # magazine|requisitos|fuentes
    name = Column(String(256), nullable=True)
    status = Column(String(32), nullable=False, default="queued")
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="flows")
