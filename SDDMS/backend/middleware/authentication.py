from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
from datetime import datetime, timedelta, timezone


def generate_token(user_id: int, username: str, role: str) -> str:
    """
    Generate a JWT for an authenticated user.
    """

    expiration_hours = current_app.config.get(
        "JWT_EXPIRATION_HOURS", 1
    )

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=expiration_hours)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def token_required(function):
    """
    Protect an endpoint and require a valid JWT.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Authorization token is required"
            }), 401

        parts = auth_header.split(" ", 1)

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "status": "error",
                "message": "Authorization header must use Bearer token"
            }), 401

        token = parts[1].strip()

        if not token:
            return jsonify({
                "status": "error",
                "message": "Token is missing"
            }), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            # Make authenticated user available to the request
            g.user = {
                "id": int(payload["sub"]),
                "username": payload["username"],
                "role": payload["role"]
            }

        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "error",
                "message": "Token has expired"
            }), 401

        except (jwt.InvalidTokenError, KeyError, ValueError):
            return jsonify({
                "status": "error",
                "message": "Invalid authentication token"
            }), 401

        return function(*args, **kwargs)

    return wrapper