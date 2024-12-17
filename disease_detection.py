<<<<<<< HEAD
import google.generativeai as genai
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration and functions remain unchanged
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

def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def clean_response_text(response_text):
    clean_text = re.sub(r'[*,]+', '', response_text)
    return clean_text

def generate_gemini_response(prompt, image_path, language):
    language_prompt = f"Provide the following response in {language}: {prompt}"
    image_data = read_image_data(image_path)
    response = model.generate_content([language_prompt, image_data])
    return clean_response_text(response.text)

def get_common_diseases(state, location, area):
    region_prompt = f"""
    As an expert plant pathologist, provide a short and concise response about common plant diseases that affect plants in the region specified below:
    
    **Area:** {area}
    **Location:** {location}
    **State:** {state}
    
    Focus on providing common diseases relevant to the specified region in under 100 words.
    """
    response = model.generate_content(region_prompt)
    return clean_response_text(response.text)

input_prompt = """
As a highly skilled plant pathologist, your expertise is indispensable in our pursuit of maintaining optimal plant health..."""

def process_uploaded_files(files, language, state, location, area):
    file_path = files[0] if files else None
    image_response = (
        generate_gemini_response(input_prompt, file_path, language)
        if file_path and language
        else "Error: Missing file or language selection."
    )
    
    region_response = (
        get_common_diseases(state, location, area)
        if state and location and area
        else "Error: Missing region information."
    )
    
    return file_path, image_response, region_response

# Enhanced Gradio UI with Green and White Theme
with gr.Blocks(css="""
    body {
        font-family: 'Roboto', sans-serif;
        background: #ffffff;
        color: #2e7d32;
    }

    .gradio-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 10px;
        background: #e8f5e9;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }

    #header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #81c784, #4caf50);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    #header h1 {
        font-size: 2.5rem;
        margin: 0;
    }

    .btn {
        background: #388e3c;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.3s, background-color 0.3s;
    }

    .btn:hover {
        background: #2e7d32;
        transform: scale(1.05);
    }

    .output-section {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .sidebar {
        background: #c8e6c9;
        border-radius: 10px;
        padding: 15px;
        margin-right: 20px;
    }

    .main-content {
        background: white;
        border-radius: 10px;
        padding: 20px;
    }
""") as app:

    gr.HTML("""
        <div id="header">
            <h1>🌱 Plant Health Diagnosis</h1>
            <p>Analyze plant images and get regional disease insights</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(elem_classes="sidebar"):
            gr.Textbox(label="Area", placeholder="Enter the area", elem_id="area")
            gr.Textbox(label="Location", placeholder="Enter the location", elem_id="location")
            gr.Textbox(label="State", placeholder="Enter the state", elem_id="state")
            gr.Dropdown(
                ["English", "Hindi", "Malayalam", "Tamil", "Telugu"],
                label="Select Language",
                value="English",
                elem_id="language"
            )
            gr.UploadButton("Upload Plant Image", file_types=["image"], elem_classes="btn")

        with gr.Column(elem_classes="main-content"):
            gr.Image(label="Uploaded Image Preview", interactive=False)
            gr.Textbox(label="AI Analysis", interactive=False, elem_classes="output-section")
            gr.Textbox(label="Regional Disease Insights", interactive=False, elem_classes="output-section")

    app.launch()
=======
import google.generativeai as genai
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration and functions remain unchanged
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

def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def clean_response_text(response_text):
    clean_text = re.sub(r'[*,]+', '', response_text)
    return clean_text

def generate_gemini_response(prompt, image_path, language):
    language_prompt = f"Provide the following response in {language}: {prompt}"
    image_data = read_image_data(image_path)
    response = model.generate_content([language_prompt, image_data])
    return clean_response_text(response.text)

def get_common_diseases(state, location, area):
    region_prompt = f"""
    As an expert plant pathologist, provide a short and concise response about common plant diseases that affect plants in the region specified below:
    
    **Area:** {area}
    **Location:** {location}
    **State:** {state}
    
    Focus on providing common diseases relevant to the specified region in under 100 words.
    """
    response = model.generate_content(region_prompt)
    return clean_response_text(response.text)

input_prompt = """
As a highly skilled plant pathologist, your expertise is indispensable in our pursuit of maintaining optimal plant health..."""

def process_uploaded_files(files, language, state, location, area):
    file_path = files[0] if files else None
    image_response = (
        generate_gemini_response(input_prompt, file_path, language)
        if file_path and language
        else "Error: Missing file or language selection."
    )
    
    region_response = (
        get_common_diseases(state, location, area)
        if state and location and area
        else "Error: Missing region information."
    )
    
    return file_path, image_response, region_response

# Enhanced Gradio UI with Green and White Theme
with gr.Blocks(css="""
    body {
        font-family: 'Roboto', sans-serif;
        background: #ffffff;
        color: #2e7d32;
    }

    .gradio-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 10px;
        background: #e8f5e9;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }

    #header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #81c784, #4caf50);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    #header h1 {
        font-size: 2.5rem;
        margin: 0;
    }

    .btn {
        background: #388e3c;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.3s, background-color 0.3s;
    }

    .btn:hover {
        background: #2e7d32;
        transform: scale(1.05);
    }

    .output-section {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .sidebar {
        background: #c8e6c9;
        border-radius: 10px;
        padding: 15px;
        margin-right: 20px;
    }

    .main-content {
        background: white;
        border-radius: 10px;
        padding: 20px;
    }
""") as app:

    gr.HTML("""
        <div id="header">
            <h1>🌱 Plant Health Diagnosis</h1>
            <p>Analyze plant images and get regional disease insights</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(elem_classes="sidebar"):
            gr.Textbox(label="Area", placeholder="Enter the area", elem_id="area")
            gr.Textbox(label="Location", placeholder="Enter the location", elem_id="location")
            gr.Textbox(label="State", placeholder="Enter the state", elem_id="state")
            gr.Dropdown(
                ["English", "Hindi", "Malayalam", "Tamil", "Telugu"],
                label="Select Language",
                value="English",
                elem_id="language"
            )
            gr.UploadButton("Upload Plant Image", file_types=["image"], elem_classes="btn")

        with gr.Column(elem_classes="main-content"):
            gr.Image(label="Uploaded Image Preview", interactive=False)
            gr.Textbox(label="AI Analysis", interactive=False, elem_classes="output-section")
            gr.Textbox(label="Regional Disease Insights", interactive=False, elem_classes="output-section")

    app.launch()
>>>>>>> f2163d61f39c5991650498c1a71b1e6280d8f15b
