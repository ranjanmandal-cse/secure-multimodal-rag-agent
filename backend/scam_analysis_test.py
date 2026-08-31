from services.scam_analysis import analyze_entities


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


result = analyze_entities(entities)

print("===== SCAM ANALYSIS =====")
print(result)