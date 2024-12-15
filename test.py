import google.generativeai as genai
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini API Configuration
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

# Disease Detection Functions
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def clean_response_text(response_text):
    clean_text = re.sub(r'[*,]+', '', response_text)
    return clean_text

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

# Crop Recommendation Function
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

# Integrated Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green")) as demo:
    gr.Markdown(
        """
        # 🌱 Agricultural Assistant
        ### Disease Detection & Crop Recommendation System
        """
    )
    
    with gr.Tabs():
        # Disease Detection Tab with Geo-tagging
        with gr.Tab("Disease Detection"):
            with gr.Row():
                # Left column for inputs
                with gr.Column(scale=1):
                    upload_button = gr.UploadButton(
                        "Upload Plant Image",
                        file_types=["image"],
                        variant="primary"
                    )
                    language = gr.Dropdown(
                        ["English", "Hindi", "Malayalam", "Tamil", "Telugu"],
                        label="Select Language",
                        value="English"
                    )
                    
                    # Location Details Box
                    gr.Markdown("### 📍 Location Details")
                    area = gr.Textbox(
                        label="Area/Village",
                        placeholder="e.g., Kuttanad"
                    )
                    district = gr.Textbox(
                        label="District",
                        placeholder="e.g., Alappuzha"
                    )
                    state = gr.Textbox(
                        label="State",
                        placeholder="e.g., Kerala"
                    )
                
                # Right column for outputs
                with gr.Column(scale=2):
                    image_output = gr.Image(label="Uploaded Image")
                    with gr.Accordion("Analysis Results", open=True):
                        analysis_output = gr.Textbox(
                            label="Disease Analysis",
                            lines=6
                        )
                        regional_insights = gr.Textbox(
                            label="Regional Disease Insights",
                            lines=6
                        )
            
            def process_image_and_location(file, lang, dist, st, ar):
                if not file:
                    return None, "Please upload an image first.", ""
                
                # Generate both disease analysis and regional insights
                disease_analysis = generate_disease_analysis(file.name, lang, dist, st, ar)
                region_insights = get_regional_disease_insights(dist, st, ar)
                
                return file.name, disease_analysis, region_insights
            
            upload_button.upload(
                process_image_and_location,
                inputs=[upload_button, language, district, state, area],
                outputs=[image_output, analysis_output, regional_insights]
            )
        
        # Crop Recommendation Tab
        with gr.Tab("Crop Recommendation"):
            with gr.Row():
                with gr.Column():
                    soil_type = gr.Textbox(
                        label="Soil Type",
                        placeholder="e.g., Clay, Sandy, Loamy"
                    )
                    ph_level = gr.Textbox(
                        label="pH Level",
                        placeholder="e.g., 6.5"
                    )
                    nutrients = gr.Textbox(
                        label="Nutrient Content",
                        placeholder="e.g., High N, Low P"
                    )
                    texture = gr.Textbox(
                        label="Soil Texture",
                        placeholder="e.g., 60% sand, 30% silt"
                    )
                    location = gr.Textbox(
                        label="Location",
                        placeholder="e.g., Kerala, India"
                    )
                    
                    submit_btn = gr.Button(
                        "Get Recommendations",
                        variant="primary"
                    )
                
                with gr.Column():
                    recommendation_output = gr.Textbox(
                        label="Crop Recommendations",
                        lines=8
                    )
            
            submit_btn.click(
                get_crop_suggestions,
                inputs=[
                    soil_type,
                    ph_level,
                    nutrients,
                    texture,
                    location
                ],
                outputs=recommendation_output
            )

# Launch the integrated application
demo.launch(server_port=8001)