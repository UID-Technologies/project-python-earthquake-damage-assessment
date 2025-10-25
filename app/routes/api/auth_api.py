"""
Authentication API Routes
Handles login, signup, logout, and token verification endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
import pymysql
import datetime
from app.blocklist import BLOCKLIST

auth_api_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")
bcrypt = Bcrypt()


@auth_api_bp.route("/login", methods=["POST"])
def login():
    """
    User login endpoint
    Returns JWT token on successful authentication
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    conn = pymysql.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        db=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"]
    )
    
    try:
        with conn.cursor() as cursor:
            sql = "SELECT password, status FROM users WHERE username=%s"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()

            if row is None:
                return jsonify({"success": False, "message": "User not found"}), 404

            stored_hash, status = row

            if not bcrypt.check_password_hash(stored_hash, password):
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

            if status.lower() != "active":
                return jsonify({
                    "success": False,
                    "message": "Your account is currently inactive. Please contact the system administrator to activate your account or for further assistance."
                }), 403

            expires = datetime.timedelta(minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"])
            token = create_access_token(identity=username, expires_delta=expires)
            return jsonify({"success": True, "token": token})
    finally:
        conn.close()


@auth_api_bp.route("/signup", methods=["POST"])
def signup():
    """
    User registration endpoint
    New users are created with 'active' status and can login immediately
    """
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    mobile = data.get("mobile")
    address = data.get("address")
    username = data.get("username")
    password = data.get("password")
    role = "user"
    organization_id = 1
    status = "active"

    if not all([name, email, username, password]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Hash password using Flask-Bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = pymysql.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        db=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"],
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
            existing = cursor.fetchone()
            if existing:
                return jsonify({"success": False, "message": "Username or email already exists"}), 409

            sql = """
            INSERT INTO users (name, email, mobile, address, role, organization_id, username, password, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            cursor.execute(sql, (
                name, email, mobile, address, role, organization_id, username, hashed_password, status
            ))
            conn.commit()

            return jsonify({"success": True, "message": "User registered successfully"})
    finally:
        conn.close()


@auth_api_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    User logout endpoint
    Adds JWT token to blocklist
    """
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"success": True, "message": "Successfully logged out"}), 200


@auth_api_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify_token():
    """
    Token verification endpoint
    Returns current user identity if token is valid
    """
    current_user = get_jwt_identity()
    return jsonify({"success": True, "logged_in_as": current_user}), 200


@auth_api_bp.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Get current user information including name, email, and username
    """
    from app.db import get_db
    
    username = get_jwt_identity()
    conn = get_db()
    
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, email, mobile, address FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404
            
            return jsonify({
                "success": True,
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "name": user.get('name', username),  # Fallback to username if name is empty
                    "email": user.get('email', ''),
                    "mobile": user.get('mobile', ''),
                    "address": user.get('address', '')
                }
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

