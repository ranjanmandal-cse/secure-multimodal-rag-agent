from services.investigation_query import (
    build_investigation_query
)

from services.retriever import Retriever

from services.scam_analysis import (
    analyze_entities
)

from services.investigation_reasoning import (
    generate_investigation_reasoning
)


complaint = """
Customer received a suspicious message asking for OTP verification.
"""


extracted_text = """
Transaction successful.

Amount: ₹4,500

Transaction ID: TXN123456789

UPI ID: merchant@upi

Date: 21/08/2026

Please share your OTP to verify the transaction.

Visit https://secure-bank-login.com

Call +919876543210
"""


entities = {
    "urls": [
        "https://secure-bank-login.com"
    ],
    "phone_numbers": [
        "+919876543210"
    ],
    "amounts": [
        "₹4,500"
    ],
    "transaction_ids": [
        "TXN123456789"
    ],
    "upi_ids": [
        "merchant@upi"
    ],
    "dates": [
        "21/08/2026"
    ],
    "otp_request": True,
    "pin_request": False,
    "cvv_request": False
}


# --------------------------------
# 1. Rule-based analysis
# --------------------------------

analysis = analyze_entities(entities)


# --------------------------------
# 2. Build investigation query
# --------------------------------

query = build_investigation_query(
    complaint,
    extracted_text,
    entities
)


# --------------------------------
# 3. Retrieve knowledge
# --------------------------------

retriever = Retriever()

retrieved_knowledge = retriever.retrieve(
    query,
    top_k=3
)


print("===== RETRIEVED KNOWLEDGE =====")

for result in retrieved_knowledge:

    print()
    print(
        "SOURCE:",
        result["document"]["filename"]
    )

    print(
        "DISTANCE:",
        result["distance"]
    )


# --------------------------------
# 4. LLM investigation reasoning
# --------------------------------

report = generate_investigation_reasoning(
    complaint,
    extracted_text,
    entities,
    analysis,
    retrieved_knowledge
)


print()
print("================================")
print("===== INVESTIGATION REPORT =====")
print("================================")
print()

print(report)