def build_investigation_query(
    complaint: str,
    extracted_text: str,
    entities: dict
) -> str:

    parts = []

    if complaint:
        parts.append(
            f"Customer complaint: {complaint}"
        )

    if extracted_text:
        parts.append(
            f"Evidence text: {extracted_text}"
        )

    if entities.get("otp_request"):
        parts.append(
            "The evidence contains an OTP request."
        )

    if entities.get("pin_request"):
        parts.append(
            "The evidence contains a PIN request."
        )

    if entities.get("cvv_request"):
        parts.append(
            "The evidence contains a CVV request."
        )

    if entities.get("urls"):
        parts.append(
            "The evidence contains external URLs."
        )

    if entities.get("phone_numbers"):
        parts.append(
            "The evidence contains phone numbers."
        )

    if entities.get("transaction_ids"):
        parts.append(
            "The evidence contains transaction information."
        )

    if entities.get("upi_ids"):
        parts.append(
            "The evidence contains UPI information."
        )

    return "\n".join(parts)