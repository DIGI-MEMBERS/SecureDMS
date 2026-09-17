from flask import Blueprint, request, jsonify, current_app

from database.database import get_connection
from services.auth_service import verify_password
from services.otp_service import generate_otp, verify_otp
from middleware.authentication import generate_token


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# ============================================================
# TEMPORARY OTP STORAGE
# Prototype only.
# In production, use a proper server-side/session-backed store.
# ============================================================

pending_otps = {}


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Step 1 of authentication:
    Validate username and password, then issue an OTP.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Username and password are required"
        }), 400

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT id, username, password_hash, role, is_active
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

    finally:
        connection.close()

    # User not found
    if user is None:
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    # Account disabled
    if user["is_active"] != 1:
        return jsonify({
            "status": "error",
            "message": "Account is inactive"
        }), 403

    # Verify password
    if not verify_password(
        password,
        user["password_hash"]
    ):
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    # ========================================================
    # Password is correct → generate OTP
    # ========================================================

    otp, expires_at = generate_otp()

    pending_otps[user["id"]] = {
        "otp": otp,
        "expires_at": expires_at,
        "username": user["username"],
        "role": user["role"]
    }

    # ========================================================
    # LOGIN RESPONSE
    # ========================================================

    response = {
        "status": "success",
        "message": "Password verified. OTP verification required.",
        "otp_required": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }

    # Development only.
    # Set EXPOSE_DEV_OTP=true in .env for local testing.
    if current_app.config.get("EXPOSE_DEV_OTP", False):
        response["dev_otp"] = otp

    return jsonify(response), 200


# ============================================================
# VERIFY OTP
# ============================================================

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    """
    Step 2 of authentication:
    Verify the OTP and issue the final JWT.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    username = data.get("username")
    otp = data.get("otp")

    if not username or not otp:
        return jsonify({
            "status": "error",
            "message": "Username and OTP are required"
        }), 400

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

    finally:
        connection.close()

    if user is None:
        return jsonify({
            "status": "error",
            "message": "Invalid authentication request"
        }), 401

    if user["is_active"] != 1:
        return jsonify({
            "status": "error",
            "message": "Account is inactive"
        }), 403

    # Get pending OTP
    pending = pending_otps.get(user["id"])

    if pending is None:
        return jsonify({
            "status": "error",
            "message": "No active OTP found. Please login again."
        }), 401

    # Verify OTP
    valid = verify_otp(
        otp,
        pending["otp"],
        pending["expires_at"]
    )

    if not valid:
        return jsonify({
            "status": "error",
            "message": "Invalid or expired OTP"
        }), 401

    # ========================================================
    # OTP verified → generate final JWT
    # ========================================================

    token = generate_token(
        user_id=user["id"],
        username=user["username"],
        role=user["role"]
    )

    # OTP can only be used once
    del pending_otps[user["id"]]

    return jsonify({
        "status": "success",
        "message": "OTP verified. Login successful.",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }), 200