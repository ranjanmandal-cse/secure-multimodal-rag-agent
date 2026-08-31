# Secure Multimodal RAG Agent for Banking Scam Investigation

AI-assisted investigation platform for analyzing banking scam evidence such as screenshots, PDFs, and text messages.

## Overview

Banking scam investigations often involve unstructured evidence such as SMS screenshots, payment messages, scanned documents, URLs, phone numbers, and customer complaints.

This project provides an AI-assisted investigation workflow that combines:

- OCR and document text extraction
- Entity extraction
- Rule-based scam analysis
- Retrieval-Augmented Generation (RAG)
- Local LLM-based investigation reasoning
- Structured investigation reports
- Human investigator decisions

The system is designed as an investigation-support tool. It does not automatically freeze accounts, reject transactions, or make final legal decisions.

---

## Key Features

### 1. Multimodal Evidence Processing

The system accepts different evidence formats including:

- Images
- PDFs
- Text files

Image evidence is processed using OCR, while text-based documents can be extracted directly.

### 2. Evidence Extraction

The system extracts useful investigation entities such as:

- URLs
- Phone numbers
- Amounts
- Transaction IDs
- UPI IDs
- Dates
- OTP requests
- PIN requests
- CVV requests

### 3. Scam Risk Analysis

Evidence is analyzed using rule-based indicators.

Current indicators include:

- OTP request
- PIN request
- CVV request
- Suspicious URL
- Phone number
- Transaction information
- UPI ID

The system generates a risk score and risk level.

### 4. Context-Aware Detection

The system distinguishes between an actual request for sensitive information and a security warning.

For example:

> "Provide your OTP"

is treated differently from:

> "The bank will never ask you to share your OTP."

### 5. Authorized URL Checking

URLs are compared against configured authorized banking domains.

For the synthetic test environment:

```text
mybank.com