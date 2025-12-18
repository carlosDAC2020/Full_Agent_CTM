from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, JSON
from src.core.database import Base

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
