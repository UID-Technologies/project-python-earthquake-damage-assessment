"""
Claims API Routes
Handles claims-specific API operations
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import get_db

claims_api_bp = Blueprint("claims_api", __name__, url_prefix="/api")


@claims_api_bp.route("/insurance_claims_detail", methods=["GET"])
@jwt_required()
def insurance_claims_detail_api():
    """Get insurance codes for the current user to start a new claim"""
    conn = get_db()
    user_identity = get_jwt_identity()

    try:
        with conn.cursor() as cursor:
            # Get user id from username
            sql_user_id = "SELECT id FROM users WHERE username = %s"
            cursor.execute(sql_user_id, (user_identity,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"success": False, "message": "User not found"}), 404
            
            user_id = row['id']

            # Get all insurance codes for this user
            sql_insurance_code_all = "SELECT insurance_code FROM insurance WHERE user_id = %s"
            cursor.execute(sql_insurance_code_all, (user_id,))
            insurance_code_all = cursor.fetchall()
        
        # Return JSON response with user_id and insurance codes
        return jsonify({
            "success": True,
            "user_id": user_id,
            "insurance_codes": insurance_code_all
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@claims_api_bp.route("/get_policy", methods=["GET"])
def get_policy_api():
    """Get policy numbers for a specific insurance code"""
    insurance_code = request.args.get('insurance_code')
    
    if not insurance_code:
        return jsonify({"success": False, "message": "insurance_code parameter required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql_policy = "SELECT policy_number FROM insurance WHERE insurance_code = %s"
            cursor.execute(sql_policy, (insurance_code,))
            policy_number_all = [row['policy_number'] for row in cursor.fetchall()]
        
        return jsonify({
            "success": True,
            "policy_number_all": policy_number_all
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

