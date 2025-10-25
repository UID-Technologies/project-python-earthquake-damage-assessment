"""
Insurance & Claims Page Routes
Serves HTML pages for insurance and claims management
Handles form submissions and data processing
"""
from flask import Blueprint, render_template, request, redirect, current_app, jsonify, abort
from app.db import get_db
from werkzeug.utils import secure_filename
import os
import traceback

insurance_pages_bp = Blueprint("insurance_pages", __name__)


@insurance_pages_bp.route('/insurances', methods=['GET'])
def insurances_list():
    """Render insurance policies list page"""
    return render_template('insurances_list.html')


@insurance_pages_bp.route('/claims', methods=['GET'])
def claims_list():
    """Render claims list page"""
    return render_template('claims_list.html')


@insurance_pages_bp.route('/claim_insurance', methods=['GET'])
def claim_insurance():
    """Render insurance claim form"""
    return render_template('insurance_form.html')


@insurance_pages_bp.route('/submit_insurance_detail', methods=['POST'])
def submit_insurance_detail():
    """Handle insurance detail form submission"""
    conn = get_db()
    data = request.form
    username = data.get('username')
    insurance_code = data.get('insurance_code')
    policy_number = data.get('policy_number')
    insurance_from = data.get('insurance_from')
    insurance_to = data.get('insurance_to')
    insurance_type = data.get('insurance_type')
    insured = data.get('insured')
    occupation = data.get('occupation')
    insurance_details = data.get('insurance_details')
    status = data.get('status')

    # Validate mandatory fields
    if not username:
        return jsonify({"success": False, "message": "Username missing"}), 400
    if not insurance_code or not insurance_from or not insurance_to:
        return jsonify({"success": False, "message": "Required fields missing"}), 400

    try:
        with conn.cursor() as cursor:
            # Get user_id using username
            sql_user_id = "SELECT id FROM users WHERE username=%s"
            cursor.execute(sql_user_id, (username,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"success": False, "message": "User not found"}), 404
            
            user_id = row['id']
            
            # Insert insurance record
            sql = """
                INSERT INTO insurance
                (user_id, insurance_code, insurance_from, insurance_to, insurance_type, insured, occupation, insurance_details, is_active, status, created_by, policy_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id, insurance_code, insurance_from, insurance_to,
                insurance_type, insured, occupation, insurance_details,
                status, user_id, policy_number
            ))
            conn.commit()
            return redirect('/insurance_claims_detail?user_id=' + str(user_id))
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Error inserting insurance: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()


@insurance_pages_bp.route('/insurance_claims_detail', methods=['GET'])
def insurance_claims_detail():
    """Render insurance claims wizard (3-step process)"""
    return render_template('add_claim_wizard.html')


@insurance_pages_bp.route('/submit_insurance_claims', methods=['POST'])
def submit_insurance_claims():
    """Handle insurance claims form submission"""
    conn = get_db()
    data = request.form
    user_id = data.get('user_id')
    claims_code = data.get('claims_code')
    insurance_id = data.get('insurance_id')
    claim_details = data.get('claim_details')
    time_of_loss = data.get('time_of_loss')
    situation_of_loss = data.get('situation_of_loss')
    cause_of_loss = data.get('cause_of_loss')
    policy_number = data.get('policy_number')

    # Better validation with specific error messages
    if not user_id:
        return jsonify({"success": False, "error": "User ID is missing"}), 400
    if not claims_code:
        return jsonify({"success": False, "error": "Claims code is required"}), 400
    if not insurance_id:
        return jsonify({"success": False, "error": "Insurance code is required"}), 400
    if not policy_number:
        return jsonify({"success": False, "error": "Policy number is required"}), 400

    try:
        with conn.cursor() as cursor:
            # Check if claims_code already exists
            cursor.execute("SELECT id FROM claims WHERE claims_code = %s", (claims_code,))
            existing = cursor.fetchone()
            if existing:
                return jsonify({"success": False, "error": "Claims code already exists. Please use a different code."}), 400
            
            sql = """
                INSERT INTO claims
                (user_id, claims_code, insurance_id, claim_details, time_of_loss, situation_of_loss, cause_of_loss, is_active, status, created_by, policy_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id, claims_code, insurance_id, claim_details,
                time_of_loss, situation_of_loss, cause_of_loss,
                1, 'inactive', user_id, policy_number
            ))
            conn.commit()
            inserted_id = cursor.lastrowid
        
        # Return JSON success response instead of redirect
        return jsonify({
            "success": True, 
            "message": "Claim created successfully",
            "claims_id": inserted_id,
            "claims_code": claims_code
        }), 201
        
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Error inserting claims: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()


@insurance_pages_bp.route('/damaged_property_image', methods=['GET'])
def damaged_property_image():
    """Render damaged property image upload page"""
    claims_id = request.args.get('claims_id')
    claims_code = request.args.get('claims_code')
    return render_template('damaged_property_image.html', claims_id=claims_id, claims_code=claims_code)


@insurance_pages_bp.route('/submit_damaged_property_image', methods=['POST'])
def submit_damaged_property_image():
    """Handle damaged property image submission with AI analysis"""
    conn = get_db()

    if 'file_name' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file_name']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    try:
        # Image Analysis - Calculate crack area
        from app.routes.image_area_calculater import calculate_crack_area
        image_response = calculate_crack_area(filepath)
        crack_area = image_response['crack_area']
        crack_file_image_path = image_response['plot_path']
        crack_filename = image_response['filename']
        damage_length = image_response['length_ft']
        damage_breadth = image_response['width_ft']
    except Exception as e:
        current_app.logger.error(f"Failed to calculate crack area: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    # AI Detection - Crack classification
    with open(filepath, 'rb') as img_file:
        from app.routes.earthquake_detection import e_detect_earthquake
        response, status_code = e_detect_earthquake(img_file)
        detection_data = response.json
        confidence = detection_data.get("confidence")
        crack_percent = detection_data.get("probabilities", {}).get("Positive (Crack Detected)")
        non_crack_percent = detection_data.get("probabilities", {}).get("Negative (No Crack)")
        ai_decision = detection_data.get("predicted_class")

    data = request.form
    claims_id = data.get('claims_id')
    claims_code = data.get('claims_code')
    file_format = data.get('file_format')
    file_desc = data.get('file_desc')

    try:
        with conn.cursor() as cursor:
            # Save to claim_property_details table
            claim_property_details_sql = """
                INSERT INTO claim_property_details
                (claims_id, damage_area, damage_length, damage_breadth)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(claim_property_details_sql, (
                claims_id, crack_area, damage_length, damage_breadth
            ))
            claim_property_details_id = cursor.lastrowid

            # Save to claim_property_assessment table
            if claims_id and detection_data:
                sql_assessment = """
                    INSERT INTO claim_property_assessment
                    (claims_id, confidence, crack_percent, non_crack_percent, ai_decision)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_assessment, (
                    claims_id, confidence, crack_percent, non_crack_percent, ai_decision
                ))

            # Save file info to claim_property_image table
            sql_image = """
                INSERT INTO claim_property_image
                (claim_property_details_id, file_name, file_location, file_format, file_desc, is_active, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_image, (
                claim_property_details_id, crack_filename, crack_file_image_path,
                file_format, file_desc, 1, 'inactive'
            ))
            conn.commit()
    except Exception as e:
        conn.rollback()
        error_message = f"Error saving file or assessment info: {e}\n{traceback.format_exc()}"
        current_app.logger.error(error_message)
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    return redirect(f'/damaged_property_details?claims_id={claims_id}&claim_property_details_id={claim_property_details_id}&claims_code={claims_code}')


@insurance_pages_bp.route('/damaged_property_details', methods=['GET'])
def damaged_property_details():
    """Render damaged property details page"""
    claims_id = request.args.get('claims_id')
    claims_code = request.args.get('claims_code')
    claim_property_details_id = request.args.get('claim_property_details_id')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql_damage_area = "SELECT damage_area FROM claim_property_details WHERE id = %s"
            cursor.execute(sql_damage_area, (claim_property_details_id,))
            damage_area = cursor.fetchone()
        
        return render_template(
            'damaged_property_details.html',
            claims_id=claims_id,
            claim_property_details_id=claim_property_details_id,
            damage_area=damage_area,
            claims_code=claims_code
        )
    finally:
        conn.close()


@insurance_pages_bp.route('/submit_damaged_property', methods=['POST'])
def submit_damaged_property():
    """Handle damaged property details form submission"""
    conn = get_db()
    data = request.form
    claims_id = data.get('claims_id')
    claim_property_details_id = data.get('claim_property_details_id')
    claims_code = data.get('claims_code')
    property_type = data.get('property_type')
    wall_type = data.get('wall_type')
    damage_area = float(data.get('damage_area', 0))
    damage_height = float(1)
    rate_per_sqft = float(data.get('rate_per_sqft', 0))
    exchange_rate = 88
    claim_recommended = damage_area * rate_per_sqft
    claim_recommended_usd = claim_recommended / exchange_rate

    if not claim_property_details_id or not claims_id:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE claim_property_details
                SET claims_id = %s, property_type = %s, wall_type = %s,
                    damage_area = %s, damage_height = %s, rate_per_sqft = %s,
                    is_active = %s, status = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                claims_id, property_type, wall_type, damage_area,
                damage_height, rate_per_sqft, 1, 'inactive',
                claim_property_details_id
            ))
            
            if claims_id and claim_recommended:
                sql_claims_value = """
                    INSERT INTO claims_value (claims_id, claim_recommended)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_claims_value, (claims_id, claim_recommended_usd))
            
            conn.commit()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Error updating damaged property: {e}")
        return jsonify({"success": False, "message": "Error saving damaged property details"}), 500
    finally:
        conn.close()

    return redirect(f'/new_report?claims_id={claims_id}&claim_property_details_id={claim_property_details_id}&claims_code={claims_code}')


@insurance_pages_bp.route('/new_report', methods=['GET'])
def new_report():
    """Render new report page"""
    claims_id = request.args.get('claims_id')
    claim_property_details_id = request.args.get('claim_property_details_id')
    claims_code = request.args.get('claims_code')
    
    # claims_code is required, claims_id is optional (we can fetch it)
    if not claims_code:
        abort(400, description="Missing claims_code")

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Get claim details including claims_id, user_id, insurance_id, and policy_number
            cursor.execute(
                "SELECT id, user_id, insurance_id, policy_number FROM claims WHERE claims_code=%s", 
                (claims_code,)
            )
            claim_data = cursor.fetchone()
            
            if claim_data is None:
                abort(404, description="Claim not found")
            
            # Extract data from claim
            claims_id = claim_data['id']
            user_id = claim_data['user_id']
            
            # Get insurance codes for user
            cursor.execute("SELECT insurance_code FROM insurance WHERE user_id=%s", (user_id,))
            all_insurance_code = cursor.fetchall()

            # Get selected insurance
            selected_insurance = {'insurance_id': claim_data['insurance_id']}

            # Get selected policy
            selected_policy = {'policy_number': claim_data['policy_number']}

            # Get selected claim
            selected_claim = {'claims_code': claims_code}
            
            # Get claim_property_details_id if not provided
            if not claim_property_details_id:
                cursor.execute(
                    "SELECT id FROM claim_property_details WHERE claims_id=%s ORDER BY id DESC LIMIT 1",
                    (claims_id,)
                )
                cpd = cursor.fetchone()
                if cpd:
                    claim_property_details_id = cpd['id']

        return render_template(
            'new_report.html',
            all_insurance_code=all_insurance_code,
            get_select_insurance_code_one=selected_insurance,
            get_select_policy_number_one=selected_policy,
            get_select_claims_code_one=selected_claim,
            claims_id=claims_id,
            claim_property_details_id=claim_property_details_id,
            claims_code=claims_code
        )
    except Exception as e:
        current_app.logger.error(f"DB error in new_report: {e}")
        abort(500, description="Database error")
    finally:
        conn.close()


@insurance_pages_bp.route('/submit_claim_report', methods=['POST'])
def submit_claim_report():
    """Handle claim report submission"""
    data = request.form
    claims_id = data.get('claims_id')
    claim_property_details_id = data.get('claim_property_details_id')
    claims_code = data.get('claims_code')
    cpa_id = data.get('cpa_id')
    user_inference = data.get('user_inference')
    final_damage_area = data.get('final_damage_area') or 0
    final_damage_cost = data.get('final_damage_cost') or 0

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE claim_property_assessment
                SET user_inference = %s, final_damage_area = %s, final_damage_cost = %s
                WHERE id = %s
            """
            cursor.execute(sql, (user_inference, final_damage_area, final_damage_cost, cpa_id))
            conn.commit()

        return redirect(f'/new_report?claims_id={claims_id}&claim_property_details_id={claim_property_details_id}&claims_code={claims_code}&user_inference={user_inference}&final_damage_area={final_damage_area}&final_damage_cost={final_damage_cost}')
    finally:
        conn.close()


@insurance_pages_bp.route('/damaged_property_calculation', methods=['GET'])
def damaged_property_calculation():
    """Render damaged property calculation page"""
    claims_id = request.args.get('claims_id')
    conn = get_db()
    
    try:
        with conn.cursor() as cursor:
            sql_user_id = "SELECT user_id FROM claims WHERE id=%s"
            cursor.execute(sql_user_id, (claims_id,))
            result = cursor.fetchone()
            
            user_id = result.get('user_id') if result else 'NULL'
            
            sql = """
                SELECT 
                    u.name, c.insurance_id AS insurance_id,
                    c.policy_number AS policy_number, c.claims_code AS claim_id,
                    cpi.file_name, cpa.ai_decision, cpa.confidence,
                    cpa.crack_percent, cpa.non_crack_percent,
                    cv.claim_recommended
                FROM users as u
                INNER JOIN claims as c ON c.user_id = u.id
                LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
                LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
                LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
                LEFT JOIN claims_value cv ON cv.claims_id = c.id
                WHERE u.id= %s
            """
            cursor.execute(sql, (user_id,))
            records = cursor.fetchall()
        
        return render_template('damaged_property_calculation.html', records=records)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"success": False, "message": f"Page not found error: {str(e)}"}), 500
    finally:
        conn.close()


@insurance_pages_bp.route('/insurance_report', methods=['GET'])
def insurance_report():
    """Render insurance report page"""
    return render_template("report.html")


@insurance_pages_bp.route('/analyse_image', methods=['GET'])
def analyse_image():
    """Render image analysis page for batch processing"""
    return render_template("analyse_image.html")
