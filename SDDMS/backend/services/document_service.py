import os
from hmac import compare_digest
from uuid import uuid4

from werkzeug.utils import secure_filename

from database.database import get_connection
from services.encryption_service import encrypt_file, decrypt_file
from services.hash_service import calculate_sha256


STORAGE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "storage",
    "encrypted"
)


# ==========================================
# SAVE / UPLOAD DOCUMENT
# ==========================================
def save_document(case_id, original_filename, file_data, uploaded_by):

    os.makedirs(STORAGE_DIR, exist_ok=True)

    safe_filename = secure_filename(original_filename)

    if not safe_filename:
        raise ValueError("Invalid filename")

    # Calculate SHA-256 of original file
    file_hash = calculate_sha256(file_data)

    # Encrypt original file using AES-256
    encrypted_data = encrypt_file(file_data)

    # Generate random stored filename
    stored_filename = f"{uuid4().hex}.enc"
    file_path = os.path.join(STORAGE_DIR, stored_filename)

    # Save encrypted file
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO documents
            (
                case_id,
                filename,
                original_filename,
                stored_filename,
                file_path,
                sha256_hash,
                current_version,
                uploaded_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                safe_filename,
                safe_filename,
                stored_filename,
                file_path,
                file_hash,
                1,
                uploaded_by
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise

    finally:
        connection.close()


# ==========================================
# GET DOCUMENT FOR DOWNLOAD
# ==========================================
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
            JOIN cases c
                ON d.case_id = c.id
            WHERE d.id = ?
            """,
            (document_id,)
        ).fetchone()

    finally:
        connection.close()

    # Document doesn't exist
    if not document:
        return None, "DOCUMENT_NOT_FOUND"

    # Check case access
    if (
        role != "admin"
        and document["investigator_id"] != user_id
    ):
        return None, "ACCESS_DENIED"

    file_path = document["file_path"]

    # Encrypted file doesn't exist
    if not os.path.exists(file_path):
        return None, "FILE_NOT_FOUND"

    try:
        # Read encrypted file
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        # Decrypt AES-256 data
        decrypted_data = decrypt_file(encrypted_data)

    except Exception:
        return None, "DECRYPTION_FAILED"

    # Recalculate SHA-256 after decryption
    calculated_hash = calculate_sha256(decrypted_data)

    # Compare with stored database hash
    if not compare_digest(
        calculated_hash,
        document["sha256_hash"]
    ):
        return None, "INTEGRITY_CHECK_FAILED"

    return {
        "filename": document["original_filename"],
        "data": decrypted_data
    }, None