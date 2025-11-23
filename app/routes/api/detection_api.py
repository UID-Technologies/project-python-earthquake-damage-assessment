"""
Detection API Routes
Handles AI-based crack/earthquake detection
"""
from flask import Blueprint, request, jsonify
import torch
from PIL import Image
import os
from werkzeug.utils import secure_filename
from app.models.crack_classifier import CrackClassifier, inference_transforms, device, model, CLASS_LABELS
from app.routes.image_area_calculater import calculate_crack_area
from app.routes.earthquake_detection import e_detect_earthquake

detection_api_bp = Blueprint("detection_api", __name__, url_prefix="/api/detection")


@detection_api_bp.route("/crack", methods=["POST"])
def detect_crack():
    """
    Detect cracks in uploaded image using AI model
    Returns classification result with confidence scores
    """
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "Image file missing"}), 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    try:
        img = Image.open(image_file).convert("RGB")
        img_tensor = inference_transforms(img).to(device)
        
        with torch.no_grad():
            output = model(img_tensor.unsqueeze(0))
        
        probabilities = torch.softmax(output, dim=1).squeeze().tolist()
        max_prob_idx = int(torch.argmax(output, dim=1).item())

        result = {
            "success": True,
            "predicted_class": CLASS_LABELS[max_prob_idx], 
            "confidence": round(probabilities[max_prob_idx] * 100, 2),
            "probabilities": {
                CLASS_LABELS[i]: round(p * 100, 2) 
                for i, p in enumerate(probabilities)
            }
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@detection_api_bp.route("/crack-with-visualization", methods=["POST"])
def detect_crack_with_visualization():
    """
    Detect cracks in uploaded image and generate visualization
    Returns classification result with processed image path
    """
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "Image file missing"}), 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    try:
        # Save the uploaded image temporarily
        filename = secure_filename(image_file.filename)
        upload_folder = os.path.join('app', 'static', 'upload_image')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save with unique name
        import time
        base_name = f"temp_{int(time.time())}_{filename}"
        filepath = os.path.join(upload_folder, base_name)
        image_file.save(filepath)
        
        # Run AI detection
        img = Image.open(filepath).convert("RGB")
        img_tensor = inference_transforms(img).to(device)
        
        with torch.no_grad():
            output = model(img_tensor.unsqueeze(0))
        
        probabilities = torch.softmax(output, dim=1).squeeze().tolist()
        max_prob_idx = int(torch.argmax(output, dim=1).item())
        
        # Generate crack visualization using OpenCV (handle errors gracefully)
        crack_data = None
        processed_image_url = None
        try:
            crack_data = calculate_crack_area(filepath)
            if crack_data and crack_data.get('status') == 'success' and crack_data.get('plot_path'):
                # The plot_path is the full path to the visualization image
                # Extract just the filename to create a URL
                processed_image_url = f"/static/upload_image/{os.path.basename(crack_data['plot_path'])}"
        except Exception as crack_error:
            print(f"Warning: Crack area calculation failed: {crack_error}")
            crack_data = None
        
        # Note: e_detect_earthquake returns a Flask Response object, not a dict
        # So we won't include it in the JSON response (it's already handled by the main model above)
        
        result = {
            "success": True,
            "predicted_class": CLASS_LABELS[max_prob_idx], 
            "confidence": round(probabilities[max_prob_idx] * 100, 2),
            "probabilities": {
                CLASS_LABELS[i]: round(p * 100, 2) 
                for i, p in enumerate(probabilities)
            },
            "processed_image_url": processed_image_url,
            "crack_data": {
                "length_ft": crack_data.get('length_ft', 0) if crack_data and crack_data.get('status') == 'success' else 0,
                "width_ft": crack_data.get('width_ft', 0) if crack_data and crack_data.get('status') == 'success' else 0,
                "area_sqft": crack_data.get('crack_area', 0) if crack_data and crack_data.get('status') == 'success' else 0
            },
            "original_image_url": f"/static/upload_image/{base_name}"
        }
        
        return jsonify(result), 200

    except Exception as e:
        import traceback
        print(f"Error in crack detection with visualization: {traceback.format_exc()}")
        return jsonify({"success": False, "error": str(e)}), 500


@detection_api_bp.route("/batch-analyze", methods=["POST"])
def batch_analyze_images():
    """
    Analyze multiple images in batch and return instant reports
    Accepts multiple images and returns analysis for each
    """
    if 'images' not in request.files:
        return jsonify({"success": False, "error": "No images provided"}), 400
    
    images = request.files.getlist('images')
    
    if not images or len(images) == 0:
        return jsonify({"success": False, "error": "No images selected"}), 400
    
    results = []
    upload_folder = os.path.join('app', 'static', 'upload_image')
    os.makedirs(upload_folder, exist_ok=True)
    
    import time
    
    for idx, image_file in enumerate(images):
        if image_file.filename == '':
            continue
            
        try:
            # Save the uploaded image temporarily
            filename = secure_filename(image_file.filename)
            base_name = f"batch_{int(time.time())}_{idx}_{filename}"
            filepath = os.path.join(upload_folder, base_name)
            image_file.save(filepath)
            
            # Run AI detection
            img = Image.open(filepath).convert("RGB")
            img_tensor = inference_transforms(img).to(device)
            
            with torch.no_grad():
                output = model(img_tensor.unsqueeze(0))
            
            probabilities = torch.softmax(output, dim=1).squeeze().tolist()
            max_prob_idx = int(torch.argmax(output, dim=1).item())
            
            # Generate crack visualization using OpenCV
            crack_data = None
            processed_image_url = None
            try:
                crack_data = calculate_crack_area(filepath)
                if crack_data and crack_data.get('status') == 'success' and crack_data.get('plot_path'):
                    processed_image_url = f"/static/upload_image/{os.path.basename(crack_data['plot_path'])}"
            except Exception as crack_error:
                print(f"Warning: Crack area calculation failed for image {idx}: {crack_error}")
                crack_data = None
            
            # Build result for this image
            result = {
                "success": True,
                "filename": filename,
                "predicted_class": CLASS_LABELS[max_prob_idx], 
                "confidence": round(probabilities[max_prob_idx] * 100, 2),
                "probabilities": {
                    CLASS_LABELS[i]: round(p * 100, 2) 
                    for i, p in enumerate(probabilities)
                },
                "crack_detected": max_prob_idx == 1,
                "processed_image_url": processed_image_url,
                "crack_data": {
                    "length_ft": crack_data.get('length_ft', 0) if crack_data and crack_data.get('status') == 'success' else 0,
                    "width_ft": crack_data.get('width_ft', 0) if crack_data and crack_data.get('status') == 'success' else 0,
                    "area_sqft": crack_data.get('crack_area', 0) if crack_data and crack_data.get('status') == 'success' else 0
                },
                "original_image_url": f"/static/upload_image/{base_name}"
            }
            
            results.append(result)
            
        except Exception as e:
            import traceback
            print(f"Error processing image {idx}: {traceback.format_exc()}")
            results.append({
                "success": False,
                "filename": image_file.filename,
                "error": str(e)
            })
    
    return jsonify({
        "success": True,
        "total_images": len(images),
        "processed_images": len(results),
        "results": results
    }), 200


@detection_api_bp.route("/crack-openai", methods=["POST"])
def detect_crack_openai():
    """
    Detect cracks in uploaded image using OpenAI Vision API
    Returns classification result with detailed analysis
    """
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "Image file missing"}), 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    try:
        from app.config import Config
        from openai import OpenAI
        import base64
        
        # Check if API key is configured
        if not Config.OPENAI_API_KEY:
            return jsonify({
                "success": False, 
                "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in environment variables."
            }), 500
        
        # Validate and clean API key
        api_key = Config.OPENAI_API_KEY.strip()
        if not api_key.startswith('sk-'):
            return jsonify({
                "success": False,
                "error": "Invalid API key format. OpenAI API keys should start with 'sk-'"
            }), 400
        
        # Initialize OpenAI client
        try:
            client = OpenAI(api_key=api_key)
        except Exception as init_error:
            return jsonify({
                "success": False,
                "error": f"Failed to initialize OpenAI client: {str(init_error)}"
            }), 500
        
        # Save the uploaded image temporarily
        filename = secure_filename(image_file.filename)
        upload_folder = os.path.join('app', 'static', 'upload_image')
        os.makedirs(upload_folder, exist_ok=True)
        
        import time
        base_name = f"openai_{int(time.time())}_{filename}"
        filepath = os.path.join(upload_folder, base_name)
        image_file.save(filepath)
        
        # Read and encode image to base64
        with open(filepath, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Determine image MIME type
        file_ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(file_ext, 'image/jpeg')
        
        # Prepare prompt for crack detection with expert insurance appraiser criteria
        prompt = """You are an expert Insurance Appraiser who deals in Earthquake Damage Assessments. As a primary assessor, Analyze the attached image in detail.

Identify the main objects, understand the pattern and refer to the major assessment criteria:

1. Emanating from columns/beams - Check if cracks originate from structural elements like columns or beams
2. Pattern - Usually diagonal / X-shaped / stair-step can be considered as earthquake damage indicators
3. Width - Wide (> 3mm), often widening cracks are more serious
4. Depth - Deep, through wall structure cracks indicate severe damage
5. Progression - Sudden + keeps widening after quake suggests active structural failure
6. Associated signs - Doors jamming, sloping floors, multiple cracks, adjacent beam or pillar damage
7. Distinguish between False Positive and Positive for verification - Rule out non-earthquake related cracks (settling, thermal, etc.)
8. Identify the Negative Use Images for rejection - This is critical. Only mark as Positive if clear earthquake damage indicators are present
9. Achieve 80% confidence Level - Be confident in your assessment before marking as Positive
10. Provide the output in a structured bulleted list format

    Based on your expert analysis, provide:
    - Detection result: "Positive (Crack Detected)" or "Negative (No Seismic Crack)"
    - Confidence level: A percentage (0-100) - must be at least 80% for Positive detection
- Detailed description: Structured bulleted list describing:
  * What you observe in the image
  * Which assessment criteria are met or not met
  * Location and characteristics of any damage
  * Pattern analysis (diagonal, X-shaped, stair-step, etc.)
  * Width and depth assessment
  * Any associated signs observed
  * Distinction between earthquake damage vs. other causes
- Recommendations: Professional recommendations including:
  * Safety concerns
  * Urgency of repair
  * Structural assessment needs
  * Insurance claim considerations

    Format your response as JSON with these keys:
    - "detection": "Positive (Crack Detected)" or "Negative (No Seismic Crack)"
    - "confidence": number between 0-100 (must be >= 80 for Positive)
- "description": detailed structured description with bullet points
- "recommendations": professional recommendations text
- "conclusion": A concise summary conclusion (2-3 sentences) that summarizes your expert assessment, the key findings, and the overall determination

Respond ONLY with valid JSON, no additional text."""
        
        # Call OpenAI Vision API
        try:
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=600,
                temperature=0.3
            )
        except Exception as api_error:
            error_msg = str(api_error)
            if "invalid_api_key" in error_msg or "401" in error_msg or "Incorrect API key" in error_msg:
                return jsonify({
                    "success": False,
                    "error": "Invalid OpenAI API key. Please verify your API key at https://platform.openai.com/account/api-keys. The key may be expired, revoked, or incorrect. Make sure to copy the complete key without any extra spaces."
                }), 401
            elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                return jsonify({
                    "success": False,
                    "error": "OpenAI API rate limit exceeded. Please try again later or check your usage limits."
                }), 429
            else:
                return jsonify({
                    "success": False,
                    "error": f"OpenAI API error: {error_msg}"
                }), 500
        
        # Parse response
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response (handle cases where model adds extra text)
        import json
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            analysis_data = json.loads(json_match.group())
        else:
            # Fallback: parse manually if JSON extraction fails
            analysis_data = {
                "detection": "Unknown",
                "confidence": 50,
                "description": response_text,
                "recommendations": "Unable to parse analysis",
                "conclusion": "Unable to generate conclusion due to parsing error"
            }
        
        # Determine predicted class
        detection_text = analysis_data.get("detection", "").lower()
        if "positive" in detection_text or "crack detected" in detection_text:
            predicted_class = "Positive (Crack Detected)"
            crack_detected = True
        elif "negative" in detection_text or "no crack" in detection_text or "no seismic" in detection_text:
            predicted_class = "Negative (No Seismic Crack)"
            crack_detected = False
        else:
            predicted_class = "Unknown"
            crack_detected = False
        
        confidence = float(analysis_data.get("confidence", 50))
        
        # Calculate probabilities (approximate based on confidence)
        if crack_detected:
            crack_prob = confidence
            no_crack_prob = 100 - confidence
        else:
            crack_prob = 100 - confidence
            no_crack_prob = confidence
        
        result = {
            "success": True,
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": {
                "Positive (Crack Detected)": round(crack_prob, 2),
                "Negative (No Seismic Crack)": round(no_crack_prob, 2)
            },
            "crack_detected": crack_detected,
            "description": analysis_data.get("description", ""),
            "recommendations": analysis_data.get("recommendations", ""),
            "original_image_url": f"/static/upload_image/{base_name}",
            "analysis_model": "OpenAI GPT-4 Vision"
        }
        
        return jsonify(result), 200
        
    except ImportError:
        return jsonify({
            "success": False, 
            "error": "OpenAI library not installed. Please run: pip install openai"
        }), 500
    except Exception as e:
        import traceback
        print(f"Error in OpenAI crack detection: {traceback.format_exc()}")
        return jsonify({"success": False, "error": str(e)}), 500


@detection_api_bp.route("/batch-analyze-openai", methods=["POST"])
def batch_analyze_images_openai():
    """
    Analyze multiple images using OpenAI Vision API
    Returns analysis for each image
    """
    if 'images' not in request.files:
        return jsonify({"success": False, "error": "No images provided"}), 400
    
    images = request.files.getlist('images')
    
    if not images or len(images) == 0:
        return jsonify({"success": False, "error": "No images selected"}), 400
    
    try:
        from app.config import Config
        from openai import OpenAI
        import base64
        
        # Check if API key is configured
        if not Config.OPENAI_API_KEY:
            return jsonify({
                "success": False, 
                "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in environment variables."
            }), 500
        
        # Validate and clean API key
        api_key = Config.OPENAI_API_KEY.strip()
        if not api_key.startswith('sk-'):
            return jsonify({
                "success": False,
                "error": "Invalid API key format. OpenAI API keys should start with 'sk-'"
            }), 400
        
        # Initialize OpenAI client
        try:
            client = OpenAI(api_key=api_key)
        except Exception as init_error:
            return jsonify({
                "success": False,
                "error": f"Failed to initialize OpenAI client: {str(init_error)}"
            }), 500
        
        results = []
        upload_folder = os.path.join('app', 'static', 'upload_image')
        os.makedirs(upload_folder, exist_ok=True)
        
        import time
        import json
        import re
        
        for idx, image_file in enumerate(images):
            if image_file.filename == '':
                continue
            
            try:
                # Save the uploaded image temporarily
                filename = secure_filename(image_file.filename)
                base_name = f"openai_batch_{int(time.time())}_{idx}_{filename}"
                filepath = os.path.join(upload_folder, base_name)
                image_file.save(filepath)
                
                # Read and encode image to base64
                with open(filepath, 'rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Determine image MIME type
                file_ext = os.path.splitext(filename)[1].lower()
                mime_types = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }
                mime_type = mime_types.get(file_ext, 'image/jpeg')
                
                # Prepare prompt for crack detection with expert insurance appraiser criteria
                prompt = """You are an expert Insurance Appraiser who deals in Earthquake Damage Assessments. As a primary assessor, Analyze the attached image in detail.

Identify the main objects, understand the pattern and refer to the major assessment criteria:

1. Emanating from columns/beams - Check if cracks originate from structural elements like columns or beams
2. Pattern - Usually diagonal / X-shaped / stair-step can be considered as earthquake damage indicators
3. Width - Wide (> 3mm), often widening cracks are more serious
4. Depth - Deep, through wall structure cracks indicate severe damage
5. Progression - Sudden + keeps widening after quake suggests active structural failure
6. Associated signs - Doors jamming, sloping floors, multiple cracks, adjacent beam or pillar damage
7. Distinguish between False Positive and Positive for verification - Rule out non-earthquake related cracks (settling, thermal, etc.)
8. Identify the Negative Use Images for rejection - This is critical. Only mark as Positive if clear earthquake damage indicators are present
9. Achieve 80% confidence Level - Be confident in your assessment before marking as Positive
10. Provide the output in a structured bulleted list format

    Based on your expert analysis, provide:
    - Detection result: "Positive (Crack Detected)" or "Negative (No Seismic Crack)"
    - Confidence level: A percentage (0-100) - must be at least 80% for Positive detection
- Detailed description: Structured bulleted list describing:
  * What you observe in the image
  * Which assessment criteria are met or not met
  * Location and characteristics of any damage
  * Pattern analysis (diagonal, X-shaped, stair-step, etc.)
  * Width and depth assessment
  * Any associated signs observed
  * Distinction between earthquake damage vs. other causes
- Recommendations: Professional recommendations including:
  * Safety concerns
  * Urgency of repair
  * Structural assessment needs
  * Insurance claim considerations

    Format your response as JSON with these keys:
    - "detection": "Positive (Crack Detected)" or "Negative (No Seismic Crack)"
    - "confidence": number between 0-100 (must be >= 80 for Positive)
- "description": detailed structured description with bullet points
- "recommendations": professional recommendations text
- "conclusion": A concise summary conclusion (2-3 sentences) that summarizes your expert assessment, the key findings, and the overall determination

Respond ONLY with valid JSON, no additional text."""
                
                # Call OpenAI Vision API
                try:
                    response = client.chat.completions.create(
                        model=Config.OPENAI_MODEL,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{mime_type};base64,{image_data}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=600,
                        temperature=0.3
                    )
                except Exception as api_error:
                    error_msg = str(api_error)
                    if "invalid_api_key" in error_msg or "401" in error_msg or "Incorrect API key" in error_msg:
                        # For batch processing, add error to results and continue
                        results.append({
                            "success": False,
                            "filename": image_file.filename if hasattr(image_file, 'filename') else f"image_{idx}",
                            "error": "Invalid OpenAI API key. Please verify your API key at https://platform.openai.com/account/api-keys"
                        })
                        continue
                    elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                        results.append({
                            "success": False,
                            "filename": image_file.filename if hasattr(image_file, 'filename') else f"image_{idx}",
                            "error": "OpenAI API rate limit exceeded. Please try again later."
                        })
                        continue
                    else:
                        results.append({
                            "success": False,
                            "filename": image_file.filename if hasattr(image_file, 'filename') else f"image_{idx}",
                            "error": f"OpenAI API error: {error_msg}"
                        })
                        continue
                
                # If we get here, the API call was successful
                # Parse response
                response_text = response.choices[0].message.content.strip()
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis_data = json.loads(json_match.group())
                else:
                    analysis_data = {
                        "detection": "Unknown",
                        "confidence": 50,
                        "description": response_text,
                        "recommendations": "Unable to parse analysis",
                        "conclusion": "Unable to generate conclusion due to parsing error"
                    }
                
                # Determine predicted class
                detection_text = analysis_data.get("detection", "").lower()
                if "positive" in detection_text or "crack detected" in detection_text:
                    predicted_class = "Positive (Crack Detected)"
                    crack_detected = True
                elif "negative" in detection_text or "no crack" in detection_text or "no seismic" in detection_text:
                    predicted_class = "Negative (No Seismic Crack)"
                    crack_detected = False
                else:
                    predicted_class = "Unknown"
                    crack_detected = False
                
                confidence = float(analysis_data.get("confidence", 50))
                
                # Calculate probabilities
                if crack_detected:
                    crack_prob = confidence
                    no_crack_prob = 100 - confidence
                else:
                    crack_prob = 100 - confidence
                    no_crack_prob = confidence
                
                # Build result
                result = {
                    "success": True,
                    "filename": filename,
                    "predicted_class": predicted_class,
                    "confidence": round(confidence, 2),
                    "probabilities": {
                        "Positive (Crack Detected)": round(crack_prob, 2),
                        "Negative (No Seismic Crack)": round(no_crack_prob, 2)
                    },
                    "crack_detected": crack_detected,
                    "description": analysis_data.get("description", ""),
                    "recommendations": analysis_data.get("recommendations", ""),
                    "conclusion": analysis_data.get("conclusion", ""),
                    "original_image_url": f"/static/upload_image/{base_name}",
                    "analysis_model": "OpenAI GPT-4 Vision"
                }
                
                results.append(result)
                
            except Exception as e:
                import traceback
                print(f"Error processing image {idx}: {traceback.format_exc()}")
                results.append({
                    "success": False,
                    "filename": image_file.filename,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "total_images": len(images),
            "processed_images": len(results),
            "results": results
        }), 200
        
    except ImportError:
        return jsonify({
            "success": False, 
            "error": "OpenAI library not installed. Please run: pip install openai"
        }), 500
    except Exception as e:
        import traceback
        print(f"Error in OpenAI batch analysis: {traceback.format_exc()}")
        return jsonify({"success": False, "error": str(e)}), 500