import re


def extract_urls(text: str) -> list[str]:
    if not text:
        return []

    pattern = r"(?:https?://|www\.)[^\s]+"

    return re.findall(pattern, text, re.IGNORECASE)


def extract_phone_numbers(text: str) -> list[str]:
    if not text:
        return []

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    return re.findall(pattern, text)


def extract_amounts(text: str) -> list[str]:
    if not text:
        return []

    # Normal currency formats
    pattern = r"(?:₹|Rs\.?|INR)\s?[\d,]+(?:\.\d{1,2})?"

    amounts = re.findall(pattern, text, re.IGNORECASE)

    # OCR may misread the ₹ symbol.
    # If an amount appears after "Amount:", capture it as well.
    amount_label_pattern = (
        r"\bamount\s*:\s*[%₹]?\s*"
        r"([\d,]+(?:\.\d{1,2})?)"
    )

    labeled_amounts = re.findall(
        amount_label_pattern,
        text,
        re.IGNORECASE
    )

    for amount in labeled_amounts:
        formatted_amount = f"₹{amount}"

        if formatted_amount not in amounts:
            amounts.append(formatted_amount)

    return amounts

def extract_transaction_ids(text: str) -> list[str]:
    if not text:
        return []

    pattern = r"\b(?:TXN|UTR|REF|RRN)[-_]?[A-Z0-9]{6,}\b"

    return re.findall(pattern, text, re.IGNORECASE)


def extract_entities(text: str) -> dict:
    return {
        "urls": extract_urls(text),
        "phone_numbers": extract_phone_numbers(text),
        "amounts": extract_amounts(text),
        "transaction_ids": extract_transaction_ids(text),
        "upi_ids": extract_upi_ids(text),
        "dates": extract_dates(text),
        "otp_request": contains_otp_request(text),
        "pin_request": contains_pin_request(text),
        "cvv_request": contains_cvv_request(text)
    }


def extract_upi_ids(text: str) -> list[str]:
    if not text:
        return []

    pattern = r"\b[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\b"

    return re.findall(pattern, text)


def extract_dates(text: str) -> list[str]:
    if not text:
        return []

    pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

    return re.findall(pattern, text)


def contains_otp_request(text: str) -> bool:
    if not text:
        return False

    text_lower = re.sub(r"\s+", " ", text.lower()).strip()

    # Explicit warnings / negative statements.
    # These take priority over request patterns.
    warning_patterns = [
        r"\bdo not\b.*\bshare\b.*\botp\b",
        r"\bdon't\b.*\bshare\b.*\botp\b",
        r"\bnever\b.*\bshare\b.*\botp\b",
        r"\bdo not\b.*\bprovide\b.*\botp\b",
        r"\bdon't\b.*\bprovide\b.*\botp\b",
        r"\bnever\b.*\bprovide\b.*\botp\b",
        r"\bwill never\b.*\bask\b.*\bshare\b.*\botp\b",
        r"\bwill never\b.*\bask\b.*\bprovide\b.*\botp\b",
        r"\bwill not\b.*\bask\b.*\bshare\b.*\botp\b",
        r"\bwill not\b.*\bask\b.*\bprovide\b.*\botp\b",
        r"\bnever\b.*\bask\b.*\bshare\b.*\botp\b",
        r"\bnever\b.*\bask\b.*\bprovide\b.*\botp\b",
        r"\bnever request\b.*\botp\b",
    ]

    if any(
        re.search(pattern, text_lower)
        for pattern in warning_patterns
    ):
        return False

    # Explicit requests for OTP.
    request_patterns = [
        r"\bshare\s+(?:your\s+)?otp\b",
        r"\bsend\s+(?:your\s+)?otp\b",
        r"\bprovide\s+(?:your\s+)?otp\b",
        r"\benter\s+(?:your\s+)?otp\b",
        r"\bverify\s+(?:with\s+)?otp\b",
        r"\botp\s+verification\b",
    ]

    return any(
        re.search(pattern, text_lower)
        for pattern in request_patterns
    )


def contains_pin_request(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()

    request_patterns = [
        r"\bshare\s+(?:your\s+)?pin\b",
        r"\bsend\s+(?:your\s+)?pin\b",
        r"\bprovide\s+(?:your\s+)?pin\b",
        r"\benter\s+(?:your\s+)?pin\b",
        r"\bverify\s+(?:with\s+)?pin\b",
    ]

    warning_patterns = [
        r"\bdo not share\b.*\bpin\b",
        r"\bdon't share\b.*\bpin\b",
        r"\bnever share\b.*\bpin\b",
    ]

    if any(re.search(pattern, text_lower) for pattern in warning_patterns):
        return False

    return any(
        re.search(pattern, text_lower)
        for pattern in request_patterns
    )


def contains_cvv_request(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()

    request_patterns = [
        r"\bshare\s+(?:your\s+)?cvv\b",
        r"\bsend\s+(?:your\s+)?cvv\b",
        r"\bprovide\s+(?:your\s+)?cvv\b",
        r"\benter\s+(?:your\s+)?cvv\b",
        r"\bverify\s+(?:with\s+)?cvv\b",
    ]

    warning_patterns = [
        r"\bdo not share\b.*\bcvv\b",
        r"\bdon't share\b.*\bcvv\b",
        r"\bnever share\b.*\bcvv\b",
    ]

    if any(re.search(pattern, text_lower) for pattern in warning_patterns):
        return False

    return any(
        re.search(pattern, text_lower)
        for pattern in request_patterns
    )