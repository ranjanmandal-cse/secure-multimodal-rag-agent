from services.investigation_query import (
    build_investigation_query
)

from services.retriever import Retriever


complaint = """
Customer received a suspicious message
asking for OTP verification.
"""


extracted_text = """
Transaction successful.

Amount: ₹4,500

Transaction ID: TXN123456789

UPI ID: merchant@upi

Please share your OTP to verify the transaction.

Visit https://secure-bank-login.com
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


query = build_investigation_query(
    complaint,
    extracted_text,
    entities
)


print("===== INVESTIGATION QUERY =====")
print(query)


retriever = Retriever()

results = retriever.retrieve(
    query,
    top_k=3
)


print()
print("===== RELEVANT KNOWLEDGE =====")

for result in results:

    print()
    print("FILE:", result["document"]["filename"])
    print("DISTANCE:", result["distance"])
    print(result["document"]["text"])