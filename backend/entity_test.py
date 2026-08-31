from services.entity_extraction import extract_entities


text = """
Transaction successful.

Amount: %4,500

Transaction ID: TXN123456789

UPI ID: merchant@upi

Date: 21/08/2026

Please share your OTP to verify the transaction.

Visit https://secure-bank-login.com

Call +919876543210
"""


entities = extract_entities(text)

print("===== EXTRACTED ENTITIES =====")
print(entities)