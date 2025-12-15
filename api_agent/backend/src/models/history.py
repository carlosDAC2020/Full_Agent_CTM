from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.database import Base

class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id = Column(String, primary_key=True, index=True) # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # NEW: Link to user
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active") # active, completed, failed
    
    # Relación con los pasos
    steps = relationship("AgentStep", back_populates="session")

class AgentStep(Base):
    __tablename__ = "agent_steps"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("agent_sessions.id"))
    step_type = Column(String) # ingest, proposal_ideas, etc.
    input_data = Column(JSON)  # Lo que envió el usuario
    output_data = Column(JSON) # El resultado del agente (estado)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("AgentSession", back_populates="steps")