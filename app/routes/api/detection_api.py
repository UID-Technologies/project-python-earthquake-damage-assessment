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
