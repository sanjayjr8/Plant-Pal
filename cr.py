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

def generate_disease_analysis(image_path, language):
    input_prompt = """
    As a highly skilled plant pathologist, analyze this plant image and provide:
    1. Disease identification (if any)
    2. Severity assessment
    3. Treatment recommendations
    Please be concise and practical in your response.
    """
    
    language_prompt = f"Provide the following response in {language}: {input_prompt}"
    image_data = read_image_data(image_path)
    response = model.generate_content([language_prompt, image_data])
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
        # Disease Detection Tab
        with gr.Tab("Disease Detection"):
            with gr.Row():
                with gr.Column():
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
                
                with gr.Column():
                    image_output = gr.Image(label="Uploaded Image")
                    analysis_output = gr.Textbox(
                        label="Disease Analysis",
                        lines=5
                    )
            
            def process_image(file, lang):
                if not file:
                    return None, "Please upload an image first."
                return file.name, generate_disease_analysis(file.name, lang)
            
            upload_button.upload(
                process_image,
                inputs=[upload_button, language],
                outputs=[image_output, analysis_output]
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
demo.launch(server_port=8000)