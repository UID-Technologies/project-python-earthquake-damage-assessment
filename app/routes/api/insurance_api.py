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
                    c.time_of_loss as incident_date,
                    c.claim_details as description,
                    c.situation_of_loss,
                    c.cause_of_loss,
                    c.status as claim_status,
                    c.created_at as claim_date,
                    i.insured,
                    i.insurance_type,
                    i.insurance_code,
                    COALESCE(cv.claim_recommended, 0) as total_claim_value,
                    CASE 
                        WHEN cv.claim_recommended > 0 THEN 'yes'
                        WHEN cv.claim_recommended = 0 THEN 'no'
                        ELSE NULL
                    END as claim_recommended
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
        import traceback
        traceback.print_exc()
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


@insurance_api_bp.route("/claims/submit-final", methods=["POST"])
@jwt_required()
def submit_final_claim():
    """Submit final claim with property details, images, and analysis results"""
    from werkzeug.utils import secure_filename
    import os
    import time
    
    conn = get_db()
    user_identity = get_jwt_identity()
    
    try:
        # Get form data
        data = request.form
        claims_code = data.get('claims_code')
        property_type = data.get('property_type')
        wall_type = data.get('wall_type')
        damage_area = float(data.get('damage_area', 0))
        damage_length = float(data.get('damage_length', 0))
        damage_breadth = float(data.get('damage_breadth', 0))
        damage_height = float(data.get('damage_height', 1))
        rate_per_sqft = float(data.get('rate_per_sqft', 350))
        
        # Get images
        images = request.files.getlist('images')
        
        if not claims_code:
            return jsonify({"success": False, "error": "Claims code is required"}), 400
        
        with conn.cursor() as cursor:
            # Get claims_id
            cursor.execute("SELECT id, user_id FROM claims WHERE claims_code = %s", (claims_code,))
            claim_row = cursor.fetchone()
            
            if not claim_row:
                return jsonify({"success": False, "error": "Claim not found"}), 404
            
            claims_id = claim_row['id']
            claim_user_id = claim_row['user_id']
            
            # Verify ownership
            cursor.execute("SELECT id FROM users WHERE username = %s", (user_identity,))
            user_row = cursor.fetchone()
            if not user_row or user_row['id'] != claim_user_id:
                return jsonify({"success": False, "error": "Unauthorized"}), 403
            
            # Insert into claim_property_details
            sql_property = """
                INSERT INTO claim_property_details
                (claims_id, property_type, wall_type, damage_area, damage_length, 
                 damage_breadth, damage_height, rate_per_sqft, is_active, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, 'active')
            """
            cursor.execute(sql_property, (
                claims_id, property_type, wall_type, damage_area,
                damage_length, damage_breadth, damage_height, rate_per_sqft
            ))
            claim_property_details_id = cursor.lastrowid
            
            # Process images
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/upload_image')
            os.makedirs(upload_folder, exist_ok=True)
            
            total_crack_area = 0
            analysis_count = 0
            total_confidence = 0
            
            for image_file in images:
                if image_file and image_file.filename:
                    # Save image
                    filename = secure_filename(image_file.filename)
                    timestamp = int(time.time())
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(upload_folder, unique_filename)
                    image_file.save(filepath)
                    
                    # Run AI analysis
                    try:
                        from app.routes.earthquake_detection import e_detect_earthquake
                        from app.routes.image_area_calculater import calculate_crack_area
                        
                        # AI Detection
                        with open(filepath, 'rb') as img_file:
                            response, status_code = e_detect_earthquake(img_file)
                            detection_data = response.json
                            confidence = detection_data.get("confidence", 0)
                            crack_percent = detection_data.get("probabilities", {}).get("Positive (Crack Detected)", 0)
                            non_crack_percent = detection_data.get("probabilities", {}).get("Negative (No Crack)", 0)
                            ai_decision = detection_data.get("predicted_class", "Unknown")
                        
                        # Crack area calculation
                        image_response = calculate_crack_area(filepath)
                        crack_area = image_response.get('crack_area', 0)
                        crack_length = image_response.get('length_ft', 0)
                        crack_width = image_response.get('width_ft', 0)
                        
                        total_crack_area += crack_area
                        total_confidence += confidence
                        analysis_count += 1
                        
                        # Save image record
                        sql_image = """
                            INSERT INTO claim_property_image
                            (claim_property_details_id, file_name, file_format, file_desc)
                            VALUES (%s, %s, %s, %s)
                        """
                        file_ext = os.path.splitext(filename)[1]
                        cursor.execute(sql_image, (
                            claim_property_details_id, unique_filename, file_ext, f"Uploaded: {filename}"
                        ))
                        
                    except Exception as e:
                        current_app.logger.error(f"Error processing image {filename}: {e}")
                        # Continue with other images
                        continue
            
            # Save assessment (average of all images)
            if analysis_count > 0:
                avg_confidence = total_confidence / analysis_count
                sql_assessment = """
                    INSERT INTO claim_property_assessment
                    (claims_id, confidence, crack_percent, non_crack_percent, ai_decision)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_assessment, (
                    claims_id, avg_confidence, crack_percent, non_crack_percent, ai_decision
                ))
            
            # Calculate claim value
            claim_recommended = damage_area * rate_per_sqft
            
            # Save to claims_value
            sql_value = """
                INSERT INTO claims_value
                (claims_id, claims_code, claim_recommended)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql_value, (claims_id, claims_code, claim_recommended))
            
            # Update claim status to active
            cursor.execute(
                "UPDATE claims SET status = 'active' WHERE id = %s",
                (claims_id,)
            )
            
            conn.commit()
        
        return jsonify({
            "success": True,
            "message": "Claim submitted successfully",
            "claims_id": claims_id,
            "claims_code": claims_code,
            "claim_property_details_id": claim_property_details_id,
            "total_claim_value": claim_recommended,
            "images_processed": len(images)
        }), 201
        
    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@insurance_api_bp.route("/claims/save-manual-override", methods=["POST"])
@jwt_required()
def save_manual_override():
    """Save manual override for AI analysis results"""
    conn = get_db()
    user_identity = get_jwt_identity()
    
    try:
        data = request.get_json()
        
        # Extract data
        claims_code = data.get('claims_code')
        image_index = data.get('image_index')
        image_filename = data.get('image_filename')
        ai_decision = data.get('ai_decision')
        confidence = float(data.get('confidence', 0))
        length_ft = float(data.get('length_ft', 0))
        width_ft = float(data.get('width_ft', 0))
        area_sqft = float(data.get('area_sqft', 0))
        claim_recommended = float(data.get('claim_recommended', 0))
        crack_detected = data.get('crack_detected', False)
        
        if not claims_code:
            return jsonify({"success": False, "error": "Claims code is required"}), 400
        
        with conn.cursor() as cursor:
            # Verify claim exists and user owns it
            cursor.execute(
                """
                SELECT c.id, c.user_id 
                FROM claims c
                JOIN users u ON c.user_id = u.id
                WHERE c.claims_code = %s AND u.username = %s
                """,
                (claims_code, user_identity)
            )
            claim_row = cursor.fetchone()
            
            if not claim_row:
                return jsonify({"success": False, "error": "Claim not found or unauthorized"}), 404
            
            claims_id = claim_row['id']
            
            # Check if claim_property_image_override table exists, if not create it
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS claim_property_image_override (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    claims_id INT NOT NULL,
                    image_index INT NOT NULL,
                    image_filename VARCHAR(255),
                    ai_decision VARCHAR(100),
                    confidence DECIMAL(10, 2),
                    length_ft DECIMAL(10, 2),
                    width_ft DECIMAL(10, 2),
                    area_sqft DECIMAL(10, 2),
                    claim_recommended DECIMAL(15, 2),
                    crack_detected BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_claim_image (claims_id, image_index),
                    FOREIGN KEY (claims_id) REFERENCES claims(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            
            # Insert or update override data
            sql = """
                INSERT INTO claim_property_image_override 
                (claims_id, image_index, image_filename, ai_decision, confidence, 
                 length_ft, width_ft, area_sqft, claim_recommended, crack_detected)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    image_filename = VALUES(image_filename),
                    ai_decision = VALUES(ai_decision),
                    confidence = VALUES(confidence),
                    length_ft = VALUES(length_ft),
                    width_ft = VALUES(width_ft),
                    area_sqft = VALUES(area_sqft),
                    claim_recommended = VALUES(claim_recommended),
                    crack_detected = VALUES(crack_detected),
                    updated_at = CURRENT_TIMESTAMP
            """
            
            cursor.execute(sql, (
                claims_id, image_index, image_filename, ai_decision, confidence,
                length_ft, width_ft, area_sqft, claim_recommended, crack_detected
            ))
            
            conn.commit()
            
            override_id = cursor.lastrowid if cursor.lastrowid else None
            
        return jsonify({
            "success": True,
            "message": "Manual override saved successfully",
            "override_id": override_id,
            "claims_id": claims_id
        }), 200
        
    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
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

