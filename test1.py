import os
import re
from pathlib import Path
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask App Configuration
app = Flask(__name__, static_folder='frontend', template_folder='frontend')

# Gemini API Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Utility Functions (Directly copied from original script)
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def clean_response_text(response_text):
    clean_text = re.sub(r'[*,]+', '', response_text)
    return clean_text

# Core Functions (Directly from original script)
def generate_disease_analysis(image_path, language, district, state, area):
    input_prompt = f"""
    As a highly skilled plant pathologist, analyze this plant image for a farmer in {area}, {district}, {state}. Please provide:
    1. Disease identification (if any)
    2. Severity assessment
    3. Treatment recommendations
    4. Regional context: Is this disease common in {district}? What factors in this region might affect its spread?
    5. Preventive measures specific to this geographical area
    
    Consider local climate patterns and common agricultural practices in {state} when making recommendations.
    Please be concise and practical in your response.
    """
    
    language_prompt = f"Provide the following response in {language}: {input_prompt}"
    image_data = read_image_data(image_path)
    response = model.generate_content([language_prompt, image_data])
    return clean_response_text(response.text)

def get_regional_disease_insights(district, state, area):
    prompt = f"""
    As an agricultural expert, provide insights about plant diseases in {area}, {district}, {state}:
    1. What are the most common plant diseases in this region?
    2. Which seasons are these diseases most prevalent?
    3. What are the unique environmental factors in {district} that affect plant health?
    4. What preventive measures do you recommend for farmers in this specific area?
    
    Provide a concise, practical response focusing on local relevance.
    """
    
    response = model.generate_content([prompt])
    return clean_response_text(response.text)

def get_crop_suggestions(soil_type, ph_level, nutrients, texture, location):
    prompt = f"""
    As an expert agricultural advisor, based on the following details:
    - Soil Type: {soil_type}
    - pH Level: {ph_level}
    - Nutrient Content: {nutrients}
    - Soil Texture: {texture}
    - Location: {location}
    
    Suggest the best crops that can be planted in this region and soil type. 
    Provide reasons for your suggestions, including compatibility with soil, climate, and market demand. 
    Your response should be concise and farmer-friendly.
    """
    
    response = model.generate_content([prompt])
    return response.text.strip()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/disease-detection', methods=['POST'])
def disease_detection_api():
    # Validate and process image upload
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image = request.files['image']
    
    # Collect additional parameters
    params = {
        'language': request.form.get('language', 'English'),
        'district': request.form.get('district', ''),
        'state': request.form.get('state', ''),
        'area': request.form.get('area', '')
    }
    
    # Save temporary image
    temp_path = f"/tmp/{image.filename}"
    image.save(temp_path)
    
    try:
        # Generate analyses
        disease_analysis = generate_disease_analysis(
            temp_path, 
            params['language'], 
            params['district'], 
            params['state'], 
            params['area']
        )
        
        regional_insights = get_regional_disease_insights(
            params['district'], 
            params['state'], 
            params['area']
        )
        
        return jsonify({
            "disease_analysis": disease_analysis,
            "regional_insights": regional_insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/crop-recommendation', methods=['POST'])
def crop_recommendation_api():
    # Get input data
    data = request.json
    
    # Validate inputs
    required_fields = ['soil_type', 'ph_level', 'nutrients', 'texture', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    
    # Generate recommendations
    recommendations = get_crop_suggestions(
        data['soil_type'],
        data['ph_level'],
        data['nutrients'],
        data['texture'],
        data['location']
    )
    
    return jsonify({"recommendations": recommendations})

# Error Handling
@app.errorhandler(500)
def handle_500(error):
    return jsonify({"error": "Internal Server Error"}), 500

# Main Entry Point
if __name__ == '__main__':
import os
import re
from pathlib import Path
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask App Configuration
app = Flask(__name__, static_folder='frontend', template_folder='frontend')

# Gemini API Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Utility Functions (Directly copied from original script)
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def clean_response_text(response_text):
    clean_text = re.sub(r'[*,]+', '', response_text)
    return clean_text

# Core Functions (Directly from original script)
def generate_disease_analysis(image_path, language, district, state, area):
    input_prompt = f"""
    As a highly skilled plant pathologist, analyze this plant image for a farmer in {area}, {district}, {state}. Please provide:
    1. Disease identification (if any)
    2. Severity assessment
    3. Treatment recommendations
    4. Regional context: Is this disease common in {district}? What factors in this region might affect its spread?
    5. Preventive measures specific to this geographical area
    
    Consider local climate patterns and common agricultural practices in {state} when making recommendations.
    Please be concise and practical in your response.
    """
    
    language_prompt = f"Provide the following response in {language}: {input_prompt}"
    image_data = read_image_data(image_path)
    response = model.generate_content([language_prompt, image_data])
    return clean_response_text(response.text)

def get_regional_disease_insights(district, state, area):
    prompt = f"""
    As an agricultural expert, provide insights about plant diseases in {area}, {district}, {state}:
    1. What are the most common plant diseases in this region?
    2. Which seasons are these diseases most prevalent?
    3. What are the unique environmental factors in {district} that affect plant health?
    4. What preventive measures do you recommend for farmers in this specific area?
    
    Provide a concise, practical response focusing on local relevance.
    """
    
    response = model.generate_content([prompt])
    return clean_response_text(response.text)

def get_crop_suggestions(soil_type, ph_level, nutrients, texture, location):
    prompt = f"""
    As an expert agricultural advisor, based on the following details:
    - Soil Type: {soil_type}
    - pH Level: {ph_level}
    - Nutrient Content: {nutrients}
    - Soil Texture: {texture}
    - Location: {location}
    
    Suggest the best crops that can be planted in this region and soil type. 
    Provide reasons for your suggestions, including compatibility with soil, climate, and market demand. 
    Your response should be concise and farmer-friendly.
    """
    
    response = model.generate_content([prompt])
    return response.text.strip()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/disease-detection', methods=['POST'])
def disease_detection_api():
    # Validate and process image upload
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image = request.files['image']
    
    # Collect additional parameters
    params = {
        'language': request.form.get('language', 'English'),
        'district': request.form.get('district', ''),
        'state': request.form.get('state', ''),
        'area': request.form.get('area', '')
    }
    
    # Save temporary image
    temp_path = f"/tmp/{image.filename}"
    image.save(temp_path)
    
    try:
        # Generate analyses
        disease_analysis = generate_disease_analysis(
            temp_path, 
            params['language'], 
            params['district'], 
            params['state'], 
            params['area']
        )
        
        regional_insights = get_regional_disease_insights(
            params['district'], 
            params['state'], 
            params['area']
        )
        
        return jsonify({
            "disease_analysis": disease_analysis,
            "regional_insights": regional_insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/crop-recommendation', methods=['POST'])
def crop_recommendation_api():
    # Get input data
    data = request.json
    
    # Validate inputs
    required_fields = ['soil_type', 'ph_level', 'nutrients', 'texture', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    
    # Generate recommendations
    recommendations = get_crop_suggestions(
        data['soil_type'],
        data['ph_level'],
        data['nutrients'],
        data['texture'],
        data['location']
    )
    
    return jsonify({"recommendations": recommendations})

# Error Handling
@app.errorhandler(500)
def handle_500(error):
    return jsonify({"error": "Internal Server Error"}), 500

# Main Entry Point
if __name__ == '__main__':
    app.run(debug=True)