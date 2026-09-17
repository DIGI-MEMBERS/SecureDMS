import secrets
from datetime import datetime, timedelta, timezone


OTP_VALIDITY_MINUTES = 5


def generate_otp():
    """
    Generate a secure 6-digit OTP.

    Returns:
        tuple: (otp, expiry_time)
    """

    otp = f"{secrets.randbelow(1_000_000):06d}"

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=OTP_VALIDITY_MINUTES
    )

    return otp, expires_at


def verify_otp(entered_otp, stored_otp, expires_at):
    """
    Verify OTP value and expiration time.
    """

    if not stored_otp or not expires_at:
        return False

    now = datetime.now(timezone.utc)

    if now >= expires_at:
        return False

    return secrets.compare_digest(
        str(entered_otp),
        str(stored_otp)
    )