import base64
import os

from hmac import compare_digest

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_encryption_key():
    key = os.getenv("AES_ENCRYPTION_KEY")

    if not key:
        raise RuntimeError("AES_ENCRYPTION_KEY is not configured")

    try:
        decoded_key = base64.urlsafe_b64decode(key)
    except Exception as error:
        raise RuntimeError("Invalid AES_ENCRYPTION_KEY") from error

    if len(decoded_key) != 32:
        raise RuntimeError("AES_ENCRYPTION_KEY must decode to 32 bytes")

    return decoded_key


def encrypt_file(file_data: bytes):
    key = get_encryption_key()

    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted_data = aes.encrypt(
        nonce,
        file_data,
        None
    )

    return nonce + encrypted_data


def decrypt_file(encrypted_data: bytes):
    key = get_encryption_key()

    aes = AESGCM(key)

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    return aes.decrypt(
        nonce,
        ciphertext,
        None
    )
from hmac import compare_digest

from services.encryption_service import encrypt_file, decrypt_file


def get_document_for_download(document_id, user_id, role):
    connection = get_connection()

    try:
        document = connection.execute(
            """
            SELECT
                d.id,
                d.case_id,
                d.original_filename,
                d.file_path,
                d.sha256_hash,
                c.investigator_id
            FROM documents d
            JOIN cases c ON d.case_id = c.id
            WHERE d.id = ?
            """,
            (document_id,)
        ).fetchone()
    finally:
        connection.close()

    if not document:
        return None, "DOCUMENT_NOT_FOUND"

    # Admin can access all documents.
    # Investigators can access documents belonging to their cases.
    if role != "admin" and document["investigator_id"] != user_id:
        return None, "ACCESS_DENIED"

    file_path = document["file_path"]

    if not os.path.exists(file_path):
        return None, "FILE_NOT_FOUND"

    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = decrypt_file(encrypted_data)

    except Exception:
        return None, "DECRYPTION_FAILED"

    calculated_hash = calculate_sha256(decrypted_data)

    if not compare_digest(
        calculated_hash,
        document["sha256_hash"]
    ):
        return None, "INTEGRITY_CHECK_FAILED"

    return {
        "filename": document["original_filename"],
        "data": decrypted_data
    }, None
    