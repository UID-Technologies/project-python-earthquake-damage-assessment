from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app.config import Config
from app.blocklist import BLOCKLIST

# Import API blueprints
from app.routes.api.auth_api import auth_api_bp
from app.routes.api.dashboard_api import dashboard_api_bp
from app.routes.api.detection_api import detection_api_bp
from app.routes.api.insurance_api import insurance_api_bp
from app.routes.api.claims_api import claims_api_bp

# Import Page blueprints
from app.routes.pages.auth_pages import auth_pages_bp
from app.routes.pages.dashboard_pages import dashboard_pages_bp
from app.routes.pages.insurance_pages import insurance_pages_bp

# Initialize extensions (without app context)
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app context
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register API Blueprints
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(dashboard_api_bp)
    app.register_blueprint(detection_api_bp)
    app.register_blueprint(insurance_api_bp)
    app.register_blueprint(claims_api_bp)
    
    # Register Page Blueprints
    app.register_blueprint(auth_pages_bp)
    app.register_blueprint(dashboard_pages_bp)
    app.register_blueprint(insurance_pages_bp) 
    # Check if token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        if not jti:
            return False
        return jti in BLOCKLIST

    # Response for revoked tokens
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has been revoked"}), 401

    # Response for expired tokens
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has expired"}), 401

    # Response for invalid tokens
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"success": False, "message": f"Invalid token: {str(error)}"}), 401

    # Response for missing tokens
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"success": False, "message": "Authorization token is missing"}), 401

    # Response for tokens that failed to decode
    @jwt.decode_error_loader
    def decode_error_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token decoding failed"}), 401

    return app

