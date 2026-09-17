from functools import wraps

from flask import g, jsonify


def require_roles(*allowed_roles):
    """
    Allow access only when the authenticated user's role
    is included in allowed_roles.
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # Authentication must run first.
            if not hasattr(g, "user") or not g.user:
                return jsonify({
                    "status": "error",
                    "message": "Authentication required"
                }), 401

            user_role = g.user.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "status": "error",
                    "message": "Insufficient permissions"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator