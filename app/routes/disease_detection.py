
import os
import requests
import zipfile
from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import tensorflow as tf

router = APIRouter(prefix="/models", tags=["models"])

FILE_ID = "1ji-PAZZOVxl5AuiM1_BRIz1qSvMoIKny"
ZIP_PATH = "model_kakao_farmer_app.zip"
MODEL_PATH = "model.tflite"  # The actual .tflite file name inside the zip

def download_and_extract_model():
    """Downloads the model from Google Drive and extracts it if not present."""
    if not os.path.exists(MODEL_PATH):
        # Download zip if not present
        if not os.path.exists(ZIP_PATH):
            print("Downloading model from Google Drive...")
            response = requests.get(f"https://drive.google.com/uc?id={FILE_ID}", stream=True)
            response.raise_for_status()
            
            with open(ZIP_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("Model downloaded successfully.")
        
        # Extract the zip file
        print("Extracting model file...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall('.')
        print("Model extracted successfully.")
        
        # Clean up zip file
        os.remove(ZIP_PATH)

def load_tflite_model(model_path):
    """Load TFLite model from file."""
    if not os.path.exists(model_path):
        download_and_extract_model()
    
    try:
        # Load the TFLite model and allocate tensors
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        raise ValueError(f"Error loading model: {str(e)}. Please ensure the model file is a valid TFLite model.")

# Disease information dictionary
disease_info = {
    "black_pod_rot": {
        "description": """🌿 *Pourriture Noire de la Cabosse (Black Pod Rot)* 🌿  
        La pourriture noire est une **maladie fongique** grave causée par *Phytophthora spp.*...""",
        "causes": """- **Humidité élevée et fortes pluies**...""",
        "treatment": """1. Remove and destroy infected pods
                       2. Apply appropriate fungicides
                       3. Improve drainage in the plantation"""
    },
    "pod_borer": {
        "description": """🦋 *Foreur de Cabosse (Pod Borer)* 🦋  
        Le foreur de cabosse (*Conopomorpha cramerella*)...""",
        "causes": """- **Présence de papillons adultes pondant sur les cabosses**...""",
        "treatment": """1. Regular monitoring of pods
                       2. Use of pheromone traps
                       3. Application of appropriate insecticides"""
    },
    "healthy": {
        "description": """🌱 *Cabosse en Bonne Santé* 🌱  
        Félicitations ! 🎉 Votre cabosse est **saine et en parfait état**...""",
        "causes": None,
        "treatment": """Continue good agricultural practices:
                       1. Regular pruning
                       2. Proper irrigation
                       3. Maintain field hygiene"""
    }
}

# Initialize the interpreter
try:
    interpreter = load_tflite_model(MODEL_PATH)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
except Exception as e:
    print(f"Error initializing model: {str(e)}")
    raise

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for model input."""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array and normalize
    image_array = np.array(image, dtype=np.float32)
    image_array = image_array / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

def predict_with_tflite(interpreter, image_array):
    """Run prediction on the image using the TFLite model."""
    # Get input details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Check and prepare input
    input_shape = input_details[0]['shape']
    required_dtype = input_details[0]['dtype']
    
    # Ensure input matches required shape and type
    if image_array.shape != tuple(input_shape):
        image_array = np.resize(image_array, input_shape)
    image_array = image_array.astype(required_dtype)
    
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], image_array)
    
    # Run inference
    interpreter.invoke()
    
    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """Endpoint for making predictions on uploaded images."""
    try:
        # Read and preprocess image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = predict_with_tflite(interpreter, processed_image)
        class_idx = np.argmax(predictions[0])
        
        # Get class names and probabilities
        class_names = ["black_pod_rot", "healthy", "pod_borer"]
        predicted_class = class_names[class_idx]
        
        # Prepare detailed response
        result = {
            "status": "success",
            "predicted_class": predicted_class,
            "confidence": float(predictions[0][class_idx]),
            "predictions": {
                name: float(prob) 
                for name, prob in zip(class_names, predictions[0])
            },
            "disease_info": disease_info[predicted_class]
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )