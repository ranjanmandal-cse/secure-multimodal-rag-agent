# Secure Multimodal RAG Agent for Banking Scam Investigation

AI-assisted investigation platform for analyzing banking scam evidence such as screenshots, PDFs, and text messages.

The system combines OCR/document extraction, entity extraction, rule-based scam analysis, Retrieval-Augmented Generation (RAG), local LLM reasoning, and human investigator review into a single investigation workflow.

> **Project Type:** AI/ML + RAG + Backend + Frontend  
> **Status:** Working prototype  
> **Data:** Synthetic banking evidence for demonstration and testing

---

## Overview

Banking scam investigations often involve unstructured evidence such as:

- SMS screenshots
- PDF documents
- Text messages
- URLs
- Phone numbers
- Transaction information
- Customer complaints

Manually examining this evidence can be time-consuming and inconsistent.

This project provides an AI-assisted investigation workflow that transforms uploaded evidence into structured investigation information.

The system:

1. Creates an investigation case.
2. Accepts evidence uploads.
3. Extracts text from evidence.
4. Extracts investigation-related entities.
5. Performs rule-based scam risk analysis.
6. Retrieves relevant banking guidance using RAG.
7. Generates an evidence-grounded investigation report.
8. Allows a human investigator to record the final decision.

The system is designed as an **investigation-support tool**, not as an autonomous banking decision system.

---

## System Workflow

```text
Customer Complaint
        │
        ▼
   Create Case
        │
        ▼
   Upload Evidence
        │
        ▼
┌─────────────────────────┐
│ OCR / Document Extraction│
└────────────┬────────────┘
             │
             ▼
    Entity Extraction
             │
             ▼
   Scam Risk Analysis
             │
             ▼
   Investigation Query
             │
             ▼
      RAG Retrieval
             │
             ▼
   LLM Investigation
      Reasoning
             │
             ▼
 Investigation Report
             │
             ▼
 Human Investigator
      Decision
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
    APPROVE REJECT ESCALATE
