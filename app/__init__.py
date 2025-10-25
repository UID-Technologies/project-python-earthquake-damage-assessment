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
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST

    # Response for revoked tokens
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has been revoked"}), 401

    return app

