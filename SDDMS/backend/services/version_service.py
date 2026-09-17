from database.database import get_connection


# ==========================================
# CREATE INITIAL VERSION
# ==========================================
def create_initial_version(document_id, uploaded_by):
    connection = get_connection()

    try:
        document = connection.execute(
            """
            SELECT
                stored_filename,
                file_path,
                sha256_hash
            FROM documents
            WHERE id = ?
            """,
            (document_id,)
        ).fetchone()

        if not document:
            return None

        connection.execute(
            """
            INSERT INTO document_versions
            (
                document_id,
                version_number,
                stored_filename,
                file_path,
                sha256_hash,
                uploaded_by
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                document_id,
                1,
                document["stored_filename"],
                document["file_path"],
                document["sha256_hash"],
                uploaded_by
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET DOCUMENT VERSION HISTORY
# ==========================================
def get_document_versions(document_id, user_id, role):

    connection = get_connection()

    try:
        document = connection.execute(
            """
            SELECT
                d.id,
                d.case_id,
                c.investigator_id
            FROM documents d
            JOIN cases c
                ON d.case_id = c.id
            WHERE d.id = ?
            """,
            (document_id,)
        ).fetchone()

        if not document:
            return None, "DOCUMENT_NOT_FOUND"

        # Admin can access all documents.
        # Investigators can access their own cases.
        if (
            role != "admin"
            and document["investigator_id"] != user_id
        ):
            return None, "ACCESS_DENIED"

        versions = connection.execute(
            """
            SELECT
                id,
                document_id,
                version_number,
                stored_filename,
                file_path,
                sha256_hash,
                uploaded_by
            FROM document_versions
            WHERE document_id = ?
            ORDER BY version_number DESC
            """,
            (document_id,)
        ).fetchall()

        return versions, None

    finally:
        connection.close()
# ==========================================
# CREATE NEW DOCUMENT VERSION
# ==========================================
def create_new_version(
    document_id,
    original_filename,
    file_data,
    uploaded_by
):
    import os
    from uuid import uuid4
    from werkzeug.utils import secure_filename

    from services.encryption_service import encrypt_file
    from services.hash_service import calculate_sha256

    storage_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "storage",
        "encrypted"
    )

    os.makedirs(storage_dir, exist_ok=True)

    safe_filename = secure_filename(original_filename)

    if not safe_filename:
        raise ValueError("Invalid filename")

    connection = get_connection()

    try:
        document = connection.execute(
            """
            SELECT
                id,
                current_version,
                case_id
            FROM documents
            WHERE id = ?
            """,
            (document_id,)
        ).fetchone()

        if not document:
            return None, "DOCUMENT_NOT_FOUND"

        next_version = document["current_version"] + 1

        file_hash = calculate_sha256(file_data)

        encrypted_data = encrypt_file(file_data)

        stored_filename = f"{uuid4().hex}.enc"

        file_path = os.path.join(
            storage_dir,
            stored_filename
        )

        with open(file_path, "wb") as file:
            file.write(encrypted_data)

        try:
            connection.execute(
                """
                INSERT INTO document_versions
                (
                    document_id,
                    version_number,
                    stored_filename,
                    file_path,
                    sha256_hash,
                    uploaded_by
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    next_version,
                    stored_filename,
                    file_path,
                    file_hash,
                    uploaded_by
                )
            )

            connection.execute(
                """
                UPDATE documents
                SET
                    filename = ?,
                    original_filename = ?,
                    stored_filename = ?,
                    file_path = ?,
                    sha256_hash = ?,
                    current_version = ?
                WHERE id = ?
                """,
                (
                    safe_filename,
                    safe_filename,
                    stored_filename,
                    file_path,
                    file_hash,
                    next_version,
                    document_id
                )
            )

            connection.commit()

        except Exception:
            connection.rollback()

            if os.path.exists(file_path):
                os.remove(file_path)

            raise

        return {
            "document_id": document_id,
            "version_number": next_version,
            "stored_filename": stored_filename,
            "file_path": file_path,
            "sha256_hash": file_hash,
            "uploaded_by": uploaded_by
        }, None

    finally:
        connection.close()