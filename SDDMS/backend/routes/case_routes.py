from flask import Blueprint, request, jsonify, g

from middleware.authentication import token_required
from middleware.rbac import require_roles
from services.case_service import create_case, get_cases
from services.audit_service import log_action


case_bp = Blueprint(
    "cases",
    __name__,
    url_prefix="/api/cases"
)


@case_bp.route("", methods=["POST"])
@token_required
@require_roles("admin", "investigator")
def create_case_route():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    case_number = data.get("case_number")
    title = data.get("title")
    description = data.get("description")

    if not case_number or not title:
        return jsonify({
            "status": "error",
            "message": "case_number and title are required"
        }), 400

    investigator_id = g.user["id"]

    try:
        case = create_case(
            case_number=case_number,
            title=title,
            description=description,
            investigator_id=investigator_id
        )

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):
            return jsonify({
                "status": "error",
                "message": "Case number already exists"
            }), 409

        return jsonify({
            "status": "error",
            "message": "Failed to create case"
        }), 500
    log_action(
        user_id=g.user["id"],
        action="CREATE",
        resource_type="CASE",
        resource_id=case["id"],
        description=f"Case {case['case_number']} created",
        ip_address=request.remote_addr
)    

    return jsonify({
        "status": "success",
        "message": "Case created successfully",
        "case": {
            "id": case["id"],
            "case_number": case["case_number"],
            "title": case["title"],
            "description": case["description"],
            "investigator_id": case["investigator_id"],
            "status": case["status"],
            "created_at": case["created_at"],
            "updated_at": case["updated_at"]
        }
    }), 201


@case_bp.route("", methods=["GET"])
@token_required
@require_roles("admin", "investigator", "viewer")
def get_cases_route():

    cases = get_cases(
        user_id=g.user["id"],
        role=g.user["role"]
    )

    case_list = []

    for case in cases:
        case_list.append({
            "id": case["id"],
            "case_number": case["case_number"],
            "title": case["title"],
            "description": case["description"],
            "investigator_id": case["investigator_id"],
            "status": case["status"],
            "created_at": case["created_at"],
            "updated_at": case["updated_at"]
        })

    return jsonify({
        "status": "success",
        "cases": case_list
    }), 200