from flask import Flask, jsonify
from flask_cors import CORS
from routes.audit_routes import audit_bp
from config import Config
from routes.auth_routes import auth_bp
from routes.case_routes import case_bp
from routes.document_routes import document_bp


def create_app():
    app = Flask(__name__)

    # ==========================================
    # LOAD CONFIGURATION
    # ==========================================
    app.config.from_object(Config)

    # ==========================================
    # CORS
    # ==========================================
    CORS(
        app,
        origins=[app.config["FRONTEND_URL"]]
    )

    # ==========================================
    # REGISTER BLUEPRINTS


    # ==========================================
    app.register_blueprint(auth_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(document_bp)

    # ==========================================
    # HEALTH CHECK
    # ==========================================
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "success",
            "message": "SecureDMS Backend is running"
        }), 200

    return app


# ==========================================
# CREATE APPLICATION
# ==========================================
app = create_app()


# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )