# Secure Multimodal RAG Agent for Banking Scam Investigation

AI-assisted investigation platform for analyzing banking scam evidence such as screenshots, PDFs, and text messages.

The system combines **OCR/document extraction, entity extraction, rule-based risk analysis, Retrieval-Augmented Generation (RAG), local LLM reasoning, and human investigator review**.

> **Status:** Working Prototype  
> **Domain:** Banking Fraud Investigation  
> **Data:** Synthetic Evidence

---

## Overview

The system helps investigators process unstructured banking scam evidence and generate structured investigation insights.

### Workflow

```text
Customer Complaint
       ↓
Evidence Upload
       ↓
OCR / Text Extraction
       ↓
Entity Extraction
       ↓
Risk Analysis
       ↓
RAG Retrieval
       ↓
LLM Reasoning
       ↓
Investigation Report
       ↓
Human Decision
```

---

## Key Features

- **Evidence Processing** — Images, PDFs, and text files.
- **OCR Extraction** — Extract text from image-based evidence.
- **Entity Extraction** — Detect URLs, phone numbers, amounts, transaction IDs, UPI IDs, dates, OTP, PIN, and CVV requests.
- **Risk Analysis** — Rule-based scam risk scoring.
- **RAG** — Retrieve relevant banking guidance from a local knowledge base.
- **LLM Reasoning** — Generate structured investigation reports using retrieved knowledge and evidence.
- **Human-in-the-Loop** — Investigator can record `APPROVE`, `REJECT`, or `ESCALATE`.

---

## Risk Analysis

The current rule-based scoring system uses:

| Indicator | Score |
|---|---:|
| OTP Request | +30 |
| PIN Request | +30 |
| CVV Request | +30 |
| Suspicious URL | +25 |
| Phone Number | +10 |
| Transaction Information | +10 |
| UPI ID | +5 |

Risk levels:

```text
0–39     LOW
40–69    MEDIUM
70–100   HIGH
```

Example:

```text
OTP Request       +30
Suspicious URL    +25
Phone Number      +10
----------------------
Risk Score         65/100
Risk Level         MEDIUM
```

---

## RAG Pipeline

The system retrieves relevant banking guidance before generating the investigation report.

```text
Case + Evidence + Entities
          ↓
   Investigation Query
          ↓
      Embeddings
          ↓
     FAISS Search
          ↓
Relevant Knowledge
          ↓
    Local LLM
          ↓
 Investigation Report
```

Current knowledge sources include:

```text
backend/knowledge/
├── scam_otp.txt
├── suspicious_urls.txt
└── upi_fraud.txt
```

---

## Example Investigation

A synthetic scam message containing an OTP request, suspicious URL, and phone number produced:

```text
URL:
http://secure-bank-example.com

Phone:
9876543210

OTP Request:
YES

PIN Request:
NO

CVV Request:
NO

Risk Score:
65/100

Risk Level:
MEDIUM
```

The system then retrieves relevant OTP and suspicious-URL guidance and generates an investigation report with recommended investigator actions.

---

## Architecture

```text
React + Vite
     ↓
FastAPI
     ↓
Evidence Processing
     ↓
OCR / PDF Extraction
     ↓
Entity Extraction
     ↓
Risk Analysis
     ↓
RAG / FAISS
     ↓
Local LLM
     ↓
Investigation Report
     ↓
Human Investigator
```

---

## Technology Stack

**Backend**

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

**AI / RAG**

- Sentence Transformers
- FAISS
- Ollama
- Local LLM

**Document Processing**

- Tesseract OCR
- pytesseract
- Pillow
- PyMuPDF

**Frontend**

- React
- Vite
- JavaScript
- CSS

---

## Project Structure

```text
secure-rag-bank/
│
├── backend/
│   ├── knowledge/
│   ├── services/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── *_test.py
│
├── frontend/
│   ├── public/
│   └── src/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running Locally

### Backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
uvicorn main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Tesseract OCR and Ollama are required for the corresponding features.

---

## Limitations

- Risk scoring is currently rule-based.
- The RAG knowledge base uses synthetic banking guidance.
- OCR accuracy depends on image quality.
- URL checking uses configured authorized domains rather than real-time threat intelligence.
- The system does not connect to real banking systems.
- AI-generated reports require human review.

---

## Disclaimer

This is an educational and portfolio prototype.

It does not access real banking systems, perform financial transactions, automatically freeze accounts, or make autonomous legal decisions.

Final investigation decisions remain under human oversight.

---

## Author

**Ranjan Kumar Mandal**

M.Tech — Artificial Intelligence & Data Science  
Indian Institute of Information Technology, Kota

[GitHub](https://github.com/ranjanmandal-cse) ·
[Project Repository](https://github.com/ranjanmandal-cse/secure-multimodal-rag-agent) ·
[LinkedIn](https://www.linkedin.com/in/ranjan-kumar-mandal-1886a5196)
