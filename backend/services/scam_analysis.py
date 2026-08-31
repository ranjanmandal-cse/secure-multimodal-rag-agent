from urllib.parse import urlparse


# Synthetic authorized domains for the project.
# In a real banking deployment, these would come from
# an authorized configuration maintained by the bank.
AUTHORIZED_DOMAINS = {
    "mybank.com",
}


def is_authorized_url(url: str) -> bool:
    """
    Check whether a URL belongs to an authorized bank domain.

    This is an exact-domain check and does not attempt to
    prove that a website is safe or legitimate beyond
    matching the configured authorized domain.
    """

    if not url:
        return False

    normalized_url = url.strip()

    # urlparse needs a scheme to reliably populate netloc.
    if not normalized_url.lower().startswith(
        ("http://", "https://")
    ):
        normalized_url = "https://" + normalized_url

    try:
        parsed = urlparse(normalized_url)
        hostname = parsed.hostname

        if not hostname:
            return False

        hostname = hostname.lower().rstrip(".")

        # Exact domain or legitimate subdomain.
        return (
            hostname in AUTHORIZED_DOMAINS
            or any(
                hostname.endswith("." + domain)
                for domain in AUTHORIZED_DOMAINS
            )
        )

    except Exception:
        return False


def analyze_entities(entities: dict) -> dict:
    score = 0
    indicators = []

    # OTP request
    if entities.get("otp_request"):
        score += 30

        indicators.append({
            "type": "OTP_REQUEST",
            "severity": "HIGH",
            "score": 30,
            "reason": "The evidence requests an OTP from the customer."
        })

    # PIN request
    if entities.get("pin_request"):
        score += 30

        indicators.append({
            "type": "PIN_REQUEST",
            "severity": "HIGH",
            "score": 30,
            "reason": "The evidence requests the customer's PIN."
        })

    # CVV request
    if entities.get("cvv_request"):
        score += 30

        indicators.append({
            "type": "CVV_REQUEST",
            "severity": "HIGH",
            "score": 30,
            "reason": "The evidence requests the customer's CVV."
        })

    # URL analysis
    urls = entities.get("urls", [])

    for url in urls:

        if is_authorized_url(url):

            indicators.append({
                "type": "AUTHORIZED_URL",
                "severity": "INFO",
                "score": 0,
                "reason": "The URL matches a configured authorized bank domain."
            })

        else:

            score += 25

            indicators.append({
                "type": "SUSPICIOUS_URL",
                "severity": "MEDIUM",
                "score": 25,
                "reason": "The URL does not match a configured authorized bank domain."
            })

    # Phone number
    phone_numbers = entities.get("phone_numbers", [])

    if phone_numbers:
        score += 10

        indicators.append({
            "type": "PHONE_DETECTED",
            "severity": "LOW",
            "score": 10,
            "reason": "A phone number is present in the evidence."
        })

    # Transaction information
    transaction_ids = entities.get("transaction_ids", [])

    if transaction_ids:
        score += 10

        indicators.append({
            "type": "TRANSACTION_DETECTED",
            "severity": "LOW",
            "score": 10,
            "reason": "Transaction information is present in the evidence."
        })

    # UPI ID
    upi_ids = entities.get("upi_ids", [])

    if upi_ids:
        score += 5

        indicators.append({
            "type": "UPI_DETECTED",
            "severity": "LOW",
            "score": 5,
            "reason": "A UPI ID is present in the evidence."
        })

    # Cap score at 100
    score = min(score, 100)

    # Determine risk level
    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "indicators": indicators
    }