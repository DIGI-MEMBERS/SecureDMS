from flask import Blueprint, jsonify, g

from middleware.authentication import token_required
from middleware.rbac import require_roles
from services.audit_service import get_audit_logs


audit_bp = Blueprint(
    "audit",
    __name__,
    url_prefix="/api/audit"
)


# ==========================================
# GET AUDIT LOGS
# ==========================================
@audit_bp.route("/logs", methods=["GET"])
@token_required
@require_roles("admin", "investigator")
def audit_logs():

    logs = get_audit_logs(
        user_id=g.user["id"],
        role=g.user["role"]
    )

    log_list = []

    for log in logs:
        log_list.append({
            "id": log["id"],
            "user_id": log["user_id"],
            "username": log["username"],
            "action": log["action"],
            "resource_type": log["resource_type"],
            "resource_id": log["resource_id"],
            "description": log["description"],
            "ip_address": log["ip_address"],
            "created_at": log["created_at"]
        })

    return jsonify({
        "status": "success",
        "logs": log_list
    }), 200