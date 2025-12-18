from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, JSON, Text, Boolean
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
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_items")


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


class Convocatoria(Base):
    __tablename__ = "convocatorias"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)
    source = Column(String(1024), nullable=True)
    type = Column(String(128), nullable=True)
    url = Column(String(1024), nullable=True, index=True)
    created_at = Column(DateTime, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    deadline = Column(DateTime, nullable=True)
    fecha_cierre = Column(Date, nullable=True)
    type_financy = Column(String(512), nullable=True)
    monto = Column(String(512), nullable=True)
    requisitos = Column(JSON, nullable=True)
    beneficios = Column(JSON, nullable=True)
    lugar = Column(String(512), nullable=True)
    created_db_at = Column(DateTime, default=datetime.utcnow)


class EmailConfig(Base):
    __tablename__ = "email_config"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    sender_email = Column(String(255), nullable=False)
    favorite_emails = Column(JSON, nullable=False, default=list)


class Source(Base):
    __tablename__ = "sources"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False, default="")
    url = Column(Text, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
