"""
Insurance & Claims API Routes
Handles all insurance and claims data operations
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.db import get_db
import os
import traceback

insurance_api_bp = Blueprint("insurance_api", __name__, url_prefix="/api/insurance")


@insurance_api_bp.route("/policies", methods=["GET"])
@jwt_required()
def get_user_insurance_policies():
    """Get all insurance policies for the current user with full details"""
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

            # Get all insurance policies with full details for this user
            sql_insurance = """
                SELECT 
                    id,
                    insurance_code, 
                    policy_number,
                    insurance_from,
                    insurance_to,
                    insurance_type,
                    insured,
                    occupation,
                    status,
                    created_at
                FROM insurance 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """
            cursor.execute(sql_insurance, (user_id,))
            insurance_policies = cursor.fetchall()
            
        return jsonify({
            "success": True,
            "user_id": user_id,
            "insurance_policies": insurance_policies
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/policy-numbers", methods=["GET"])
def get_policy_numbers():
    """Get policy numbers for a specific insurance code"""
    insurance_code = request.args.get('insurance_code')
    
    if not insurance_code:
        return jsonify({"success": False, "message": "insurance_code parameter required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql_policy = "SELECT policy_number FROM insurance WHERE insurance_code = %s"
            cursor.execute(sql_policy, (insurance_code,))
            policy_numbers = [row['policy_number'] for row in cursor.fetchall()]
        
        return jsonify({
            "success": True,
            "policy_numbers": policy_numbers
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/claims/all", methods=["GET"])
@jwt_required()
def get_all_user_claims():
    """Get all claims for the current user with full details"""
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

            # Get all claims with full details for this user
            sql_claims = """
                SELECT 
                    c.id,
                    c.claims_code,
                    c.policy_number,
                    c.insurance_id,
                    c.time_of_loss,
                    c.claim_details,
                    c.situation_of_loss,
                    c.cause_of_loss,
                    c.status,
                    c.created_at,
                    i.insured,
                    i.insurance_type,
                    i.insurance_code,
                    cv.claim_recommended
                FROM claims c
                LEFT JOIN insurance i ON c.insurance_id = i.insurance_code
                LEFT JOIN claims_value cv ON c.claims_code = cv.claims_code
                WHERE c.user_id = %s 
                ORDER BY c.created_at DESC
            """
            cursor.execute(sql_claims, (user_id,))
            claims = cursor.fetchall()
            
        return jsonify({
            "success": True,
            "user_id": user_id,
            "claims": claims
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/claims", methods=["GET"])
def get_claims_by_policy():
    """Get claims codes for a specific policy number"""
    policy_number = request.args.get('policy_number')
    
    if not policy_number:
        return jsonify({"success": False, "message": "policy_number parameter required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT claims_code FROM claims WHERE policy_number = %s", 
                (policy_number,)
            )
            claims_codes = [c['claims_code'] for c in cursor.fetchall()]
        
        return jsonify({
            "success": True,
            "claims_codes": claims_codes
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/assessment", methods=["GET"])
def get_assessment_data():
    """Get assessment data for a specific claims code"""
    claims_code = request.args.get('claims_code')
    
    if not claims_code:
        return jsonify({"success": False, "message": "claims_code parameter required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT 
                    cpi.file_name,
                    cpa.ai_decision,
                    cpa.confidence,
                    cpa.crack_percent,
                    cv.claim_recommended,
                    cpd.damage_area,
                    cpd.damage_length,
                    cpd.damage_breadth,
                    cpa.id as cpa_id
                FROM claims as c 
                LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
                LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
                LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
                LEFT JOIN claims_value cv ON cv.claims_id = c.id
                WHERE c.claims_code = %s
            """
            cursor.execute(sql, (claims_code,))
            assessment_data = cursor.fetchone()
        
        return jsonify({
            "success": True,
            "data": assessment_data if assessment_data else {}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_insurance_reports():
    """Get all insurance reports for the current user"""
    conn = get_db()
    
    try:
        user_identity = get_jwt_identity()

        with conn.cursor() as cursor:
            sql_user_id = "SELECT id FROM users WHERE username = %s"
            cursor.execute(sql_user_id, (user_identity,))
            user_row = cursor.fetchone()
            
            if not user_row:
                return jsonify({"success": True, "reports": []}), 200
            
            user_id = user_row['id']

        with conn.cursor() as cursor:
            sql_data = """
                SELECT 
                    u.name,
                    u.email,
                    i.insurance_code,
                    i.insurance_type,
                    c.policy_number,
                    c.claims_code,
                    cpd.property_type,
                    cpd.wall_type,
                    cpd.damage_area,
                    cpd.rate_per_sqft,
                    cpa.confidence,
                    cpa.crack_percent,
                    cpa.non_crack_percent,
                    cpa.ai_decision,
                    cpi.file_name
                FROM users AS u
                INNER JOIN insurance AS i ON i.user_id = u.id
                INNER JOIN claims AS c ON c.insurance_id = i.insurance_code
                INNER JOIN claim_property_details AS cpd ON cpd.claims_id = c.id
                INNER JOIN claim_property_assessment AS cpa ON cpa.claims_id = cpd.claims_id
                INNER JOIN claim_property_image AS cpi ON cpi.claim_property_details_id = cpd.id
                WHERE u.id = %s
            """
            cursor.execute(sql_data, (user_id,))
            records = cursor.fetchall()

        return jsonify({
            "success": True,
            "reports": records if records else []
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/damage-calculation", methods=["GET"])
def get_damage_calculation():
    """Get damage calculation details for a claim"""
    claims_id = request.args.get('claims_id')
    
    if not claims_id:
        return jsonify({"success": False, "message": "claims_id parameter required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql_user_id = "SELECT user_id FROM claims WHERE id=%s"
            cursor.execute(sql_user_id, (claims_id,))
            result = cursor.fetchone()
            
            if not result:
                return jsonify({"success": False, "message": "Claim not found"}), 404
            
            user_id = result.get('user_id')
            
            sql = """
                SELECT 
                    u.name,
                    c.insurance_id AS insurance_id,
                    c.policy_number AS policy_number,
                    c.claims_code AS claim_id,
                    cpi.file_name,
                    cpa.ai_decision,
                    cpa.confidence,
                    cpa.crack_percent,
                    cpa.non_crack_percent,
                    cv.claim_recommended
                FROM users as u
                INNER JOIN claims as c ON c.user_id = u.id
                LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
                LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
                LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
                LEFT JOIN claims_value cv ON cv.claims_id = c.id
                WHERE u.id = %s
            """
            cursor.execute(sql, (user_id,))
            records = cursor.fetchall()
        
        return jsonify({
            "success": True,
            "calculations": records
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

