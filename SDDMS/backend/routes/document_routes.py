from flask import Blueprint, request, jsonify, g, send_file
import io

from middleware.authentication import token_required
from middleware.rbac import require_roles
from database.database import get_connection
from services.version_service import (
    get_document_versions,
    create_new_version
)
from services.document_service import (
    save_document,
    get_document_for_download
)
from services.audit_service import log_action


document_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/api/documents"
)


# ==========================================
# UPLOAD DOCUMENT
# ==========================================
@document_bp.route("/upload", methods=["POST"])
@token_required
@require_roles("admin", "investigator")
def upload_document():

    case_id = request.form.get("case_id")
    uploaded_file = request.files.get("file")

    if not case_id:
        return jsonify({
            "status": "error",
            "message": "case_id is required"
        }), 400

    if not uploaded_file:
        return jsonify({
            "status": "error",
            "message": "File is required"
        }), 400

    if not uploaded_file.filename:
        return jsonify({
            "status": "error",
            "message": "Filename is required"
        }), 400

    try:
        case_id = int(case_id)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "case_id must be an integer"
        }), 400

    connection = get_connection()

    try:
        case = connection.execute(
            """
            SELECT id, investigator_id
            FROM cases
            WHERE id = ?
            """,
            (case_id,)
        ).fetchone()

    finally:
        connection.close()

    if not case:
        return jsonify({
            "status": "error",
            "message": "Case not found"
        }), 404

    if (
        g.user["role"] != "admin"
        and case["investigator_id"] != g.user["id"]
    ):
        return jsonify({
            "status": "error",
            "message": "You do not have access to this case"
        }), 403

    file_data = uploaded_file.read()

    if not file_data:
        return jsonify({
            "status": "error",
            "message": "Uploaded file is empty"
        }), 400

    try:
        document_id = save_document(
            case_id=case_id,
            original_filename=uploaded_file.filename,
            file_data=file_data,
            uploaded_by=g.user["id"]
        )

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        return jsonify({
            "status": "error",
            "message": "Failed to upload document"
        }), 500

    # ==========================================
    # AUDIT LOG - DOCUMENT UPLOAD
    # ==========================================
    log_action(
        user_id=g.user["id"],
        action="UPLOAD",
        resource_type="DOCUMENT",
        resource_id=document_id,
        description=(
            f"Document {uploaded_file.filename} "
            f"uploaded to case {case_id}"
        ),
        ip_address=request.remote_addr
    )

    return jsonify({
        "status": "success",
        "message": "Document uploaded successfully",
        "document": {
            "id": document_id,
            "case_id": case_id,
            "filename": uploaded_file.filename,
            "uploaded_by": g.user["id"]
        }
    }), 201


# ==========================================
# DOWNLOAD DOCUMENT
# ==========================================
@document_bp.route(
    "/<int:document_id>/download",
    methods=["GET"]
)
@token_required
@require_roles("admin", "investigator", "viewer")
def download_document(document_id):

    document, error = get_document_for_download(
        document_id=document_id,
        user_id=g.user["id"],
        role=g.user["role"]
    )

    if error == "DOCUMENT_NOT_FOUND":
        return jsonify({
            "status": "error",
            "message": "Document not found"
        }), 404

    if error == "ACCESS_DENIED":
        return jsonify({
            "status": "error",
            "message": "You do not have access to this document"
        }), 403

    if error == "FILE_NOT_FOUND":
        return jsonify({
            "status": "error",
            "message": "Stored file not found"
        }), 404

    if error == "DECRYPTION_FAILED":
        return jsonify({
            "status": "error",
            "message": "Failed to decrypt document"
        }), 500

    if error == "INTEGRITY_CHECK_FAILED":
        return jsonify({
            "status": "error",
            "message": "Document integrity check failed"
        }), 500

    # ==========================================
    # AUDIT LOG - DOCUMENT DOWNLOAD
    # ==========================================
    log_action(
        user_id=g.user["id"],
        action="DOWNLOAD",
        resource_type="DOCUMENT",
        resource_id=document_id,
        description=(
            f"Document {document['filename']} downloaded"
        ),
        ip_address=request.remote_addr
    )

    return send_file(
        io.BytesIO(document["data"]),
        as_attachment=True,
        download_name=document["filename"]
    )
# ==========================================
# GET DOCUMENT VERSION HISTORY
# ==========================================
@document_bp.route(
    "/<int:document_id>/versions",
    methods=["GET"]
)
@token_required
@require_roles("admin", "investigator", "viewer")
def document_versions(document_id):

    versions, error = get_document_versions(
        document_id=document_id,
        user_id=g.user["id"],
        role=g.user["role"]
    )

    if error == "DOCUMENT_NOT_FOUND":
        return jsonify({
            "status": "error",
            "message": "Document not found"
        }), 404

    if error == "ACCESS_DENIED":
        return jsonify({
            "status": "error",
            "message": "You do not have access to this document"
        }), 403

    version_list = []

    for version in versions:
        version_list.append({
            "id": version["id"],
            "document_id": version["document_id"],
            "version_number": version["version_number"],
            "stored_filename": version["stored_filename"],
            "sha256_hash": version["sha256_hash"],
            "uploaded_by": version["uploaded_by"]
        })

    return jsonify({
        "status": "success",
        "versions": version_list
    }), 200
# ==========================================
# CREATE NEW DOCUMENT VERSION
# ==========================================
@document_bp.route(
    "/<int:document_id>/versions",
    methods=["POST"]
)
@token_required
@require_roles("admin", "investigator")
def create_document_version(document_id):

    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({
            "status": "error",
            "message": "File is required"
        }), 400

    if not uploaded_file.filename:
        return jsonify({
            "status": "error",
            "message": "Filename is required"
        }), 400

    # Check document and case access
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
    finally:
        connection.close()

    if not document:
        return jsonify({
            "status": "error",
            "message": "Document not found"
        }), 404

    if (
        g.user["role"] != "admin"
        and document["investigator_id"] != g.user["id"]
    ):
        return jsonify({
            "status": "error",
            "message": "You do not have access to this document"
        }), 403

    file_data = uploaded_file.read()

    if not file_data:
        return jsonify({
            "status": "error",
            "message": "Uploaded file is empty"
        }), 400

    try:
        version, error = create_new_version(
            document_id=document_id,
            original_filename=uploaded_file.filename,
            file_data=file_data,
            uploaded_by=g.user["id"]
        )

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        return jsonify({
            "status": "error",
            "message": "Failed to create document version"
        }), 500

    if error == "DOCUMENT_NOT_FOUND":
        return jsonify({
            "status": "error",
            "message": "Document not found"
        }), 404

    log_action(
        user_id=g.user["id"],
        action="VERSION_UPLOAD",
        resource_type="DOCUMENT",
        resource_id=document_id,
        description=(
            f"Version {version['version_number']} "
            f"uploaded for document {document_id}"
        ),
        ip_address=request.remote_addr
    )

    return jsonify({
        "status": "success",
        "message": "Document version created successfully",
        "version": {
            "document_id": version["document_id"],
            "version_number": version["version_number"],
            "stored_filename": version["stored_filename"],
            "sha256_hash": version["sha256_hash"],
            "uploaded_by": version["uploaded_by"]
        }
    }), 201