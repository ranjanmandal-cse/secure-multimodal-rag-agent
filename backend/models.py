from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True, nullable=False)
    complaint = Column(Text, nullable=True)
    status = Column(String, default="CREATED")
    decision = Column(String, nullable=True)
    decision_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String, unique=True, index=True, nullable=False)
    case_id = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    extracted_text = Column(Text, nullable=True)
    extracted_entities = Column(Text, nullable=True)

    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String, nullable=True)
    risk_indicators = Column(Text, nullable=True)
    investigation_report = Column(Text, nullable=True)