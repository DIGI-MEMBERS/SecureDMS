import hashlib


def calculate_sha256(file_data: bytes) -> str:
    return hashlib.sha256(file_data).hexdigest()