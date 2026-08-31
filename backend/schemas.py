from pydantic import BaseModel


class CaseCreate(BaseModel):
    complaint: str

class DecisionCreate(BaseModel):
    decision: str
    note: str | None = None

class CaseResponse(BaseModel):
    case_id: str
    complaint: str | None
    status: str
    decision: str | None = None
    decision_note: str | None = None
    risk_score: int | None = None
    risk_level: str | None = None

    class Config:
        from_attributes = True