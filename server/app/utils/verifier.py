import hmac
import hashlib


def verify_signature(payload: bytes, signature: str, secret: str):
    if not signature:
        return False

    expected_signature = (
        "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    )

    return hmac.compare_digest(expected_signature, signature)
