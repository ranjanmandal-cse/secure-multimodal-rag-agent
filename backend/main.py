import json
from services.entity_extraction import extract_entities
from services.ocr_service import extract_text
from services.scam_analysis import analyze_entities
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import os
from services.investigation_query import build_investigation_query
from services.retriever import Retriever
from services.investigation_reasoning import (
    generate_investigation_reasoning
)
retriever = Retriever()

from database import SessionLocal
from models import Case, Evidence
from schemas import CaseCreate, CaseResponse, DecisionCreate

app = FastAPI(title="Secure Banking Investigation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Secure Banking Investigation API"}


@app.post("/cases", response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):

    new_case = Case(
        case_id=f"CASE-{uuid.uuid4().hex[:8].upper()}",
        complaint=case.complaint,
        status="CREATED"
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case


@app.get("/cases", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):

    cases = db.query(Case).all()

    result = []

    for case in cases:

        evidence = (
            db.query(Evidence)
            .filter(Evidence.case_id == case.case_id)
            .order_by(Evidence.risk_score.desc())
            .first()
        )

        result.append({
            "case_id": case.case_id,
            "complaint": case.complaint,
            "status": case.status,
            "decision": case.decision,
            "decision_note": case.decision_note,
            "risk_score": evidence.risk_score if evidence else None,
            "risk_level": evidence.risk_level if evidence else None,
        })

    return result



@app.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return case

@app.delete("/cases/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    # Delete all evidence belonging to this case
    db.query(Evidence).filter(
        Evidence.case_id == case_id
    ).delete(synchronize_session=False)

    # Delete the case
    db.delete(case)

    db.commit()

    return {
        "message": "Case deleted successfully",
        "case_id": case_id
    }

@app.post("/cases/{case_id}/evidence")
def upload_evidence(
    case_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(
        Case.case_id == case_id
    ).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    # Create case storage directory
    case_directory = os.path.join(
        "storage",
        case_id
    )

    os.makedirs(
        case_directory,
        exist_ok=True
    )

    # Save uploaded file
    file_path = os.path.join(
        case_directory,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # OCR only for image files
    
    
    extracted_text = None
    extracted_entities = {}

    if (
        file.content_type
        and (
           file.content_type.startswith("image/")
           or file.content_type == "application/pdf"
           or file.content_type == "text/plain"
        )
    ):
        extracted_text = extract_text(
            file_path,
            file.content_type
    )

    if extracted_text:
        extracted_entities = extract_entities(extracted_text)

    
    analysis_result = analyze_entities(extracted_entities)

    investigation_query = build_investigation_query(
    complaint=case.complaint,
    extracted_text=extracted_text or "",
    entities=extracted_entities
    )

    retrieved_knowledge = retriever.retrieve(
    investigation_query,
    top_k=3
    )

    investigation_report = generate_investigation_reasoning(
    complaint=case.complaint,
    extracted_text=extracted_text or "",
    entities=extracted_entities,
    analysis=analysis_result,
    retrieved_knowledge=retrieved_knowledge
    )
    
    

    # Create database evidence record
    evidence = Evidence(
        evidence_id=str(uuid.uuid4()),
        case_id=case_id,
        filename=file.filename,
        file_type=file.content_type,
        file_path=file_path,
        extracted_text=extracted_text,
        extracted_entities=json.dumps(extracted_entities),

        risk_score=analysis_result["risk_score"],
        risk_level=analysis_result["risk_level"],
        risk_indicators=json.dumps(
        analysis_result["indicators"]
        ),
        investigation_report=investigation_report
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return {
        "message": "Evidence uploaded successfully",
        "evidence_id": evidence.evidence_id,
        "filename": evidence.filename,
        "file_type": evidence.file_type,
        "extracted_text": extracted_text,
        "entities": extracted_entities,
        "analysis": analysis_result,
        "investigation_report": investigation_report
        
    }


@app.get("/cases/{case_id}/evidence")
def get_case_evidence(
    case_id: str,
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.case_id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    evidence_list = (
        db.query(Evidence)
        .filter(Evidence.case_id == case_id)
        .all()
    )

    
    return [
    {
        "evidence_id": evidence.evidence_id,
        "filename": evidence.filename,
        "file_type": evidence.file_type,
        "file_path": evidence.file_path,
        "created_at": evidence.created_at,
        "extracted_text": evidence.extracted_text,

        "extracted_entities": (
            json.loads(evidence.extracted_entities)
            if evidence.extracted_entities
            else {}
        ),

        "risk_score": evidence.risk_score,
        "risk_level": evidence.risk_level,

        "risk_indicators": (
            json.loads(evidence.risk_indicators)
            if evidence.risk_indicators
            else []
        ),
        "investigation_report": evidence.investigation_report,
    }
    for evidence in evidence_list
]


@app.post("/cases/{case_id}/decision")
def update_case_decision(
    case_id: str,
    decision_data: DecisionCreate,
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.case_id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    allowed_decisions = {
        "APPROVE",
        "REJECT",
        "ESCALATE"
    }

    decision = decision_data.decision.upper()

    if decision not in allowed_decisions:
        raise HTTPException(
            status_code=400,
            detail="Invalid decision"
        )

    case.decision = decision
    case.decision_note = decision_data.note
    case.status = "REVIEWED"

    db.commit()
    db.refresh(case)

    return {
        "case_id": case.case_id,
        "decision": case.decision,
        "decision_note": case.decision_note,
        "status": case.status
    }