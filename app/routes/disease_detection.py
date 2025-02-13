import os
import requests
from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
#import tensorflow as tf
import tensorflow_lite as tflite


# User router
router = APIRouter(prefix="/models", tags=["models"])

# model link : https://drive.google.com/file/d/1ji-PAZZOVxl5AuiM1_BRIz1qSvMoIKny/view?usp=sharing
# ID du fichier Google Drive (modifie avec le tien)
FILE_ID = "1ji-PAZZOVxl5AuiM1_BRIz1qSvMoIKny"
MODEL_PATH = "model_kakao_farmer_app.zip" #"cacao_disease_model.h5"

# URL de téléchargement directe depuis Google Drive
GDRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

def download_model():
    """Télécharge le modèle depuis Google Drive si non présent en local."""
    if not os.path.exists(MODEL_PATH):
        print("Téléchargement du modèle depuis Google Drive...")
        response = requests.get(GDRIVE_URL, stream=True)
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Modèle téléchargé avec succès.")

# Télécharger le modèle au démarrage
# print("Download model")
# download_model()
# print("Finish to download model")

# Charger le modèle entraîné
def load_tflite_model(model_path):
    """Load TFLite model from file."""
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

# Load the TFLite model
interpreter = load_tflite_model(MODEL_PATH)

def predict_with_tflite(interpreter, image_array):
    """Run prediction on the image using the TFLite model."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data
#model = tf.keras.models.load_model(MODEL_PATH)

# Dictionnaire contenant les descriptions et causes des maladies
disease_info = {
    "black_pod_rot": {
        "description": """🌿 *Pourriture Noire de la Cabosse (Black Pod Rot)* 🌿  
        La pourriture noire est une **maladie fongique** grave causée par *Phytophthora spp.*...""",
        "causes": """- **Humidité élevée et fortes pluies**..."""
    },
    "pod_borer": {
        "description": """🦋 *Foreur de Cabosse (Pod Borer)* 🦋  
        Le foreur de cabosse (*Conopomorpha cramerella*)...""",
        "causes": """- **Présence de papillons adultes pondant sur les cabosses**..."""
    },
    "healthy": {
        "description": """🌱 *Cabosse en Bonne Santé* 🌱  
        Félicitations ! 🎉 Votre cabosse est **saine et en parfait état**...""",
        "causes": None  # Pas de causes affichées pour un cacao sain
    }
}

# app = FastAPI()

# @app.post("/predict/")
@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    # Prétraitement de l'image
    image = image.resize((224, 224))  # Redimensionner selon votre modèle
    image_array = np.array(image) / 255.0  # Normaliser si nécessaire
    image_array = np.expand_dims(image_array, axis=0).astype(np.float32)  # Ajouter une dimension pour le batch

    # Faire la prédiction avec TFLite
    predictions = predict_with_tflite(interpreter, image_array)
    class_idx = np.argmax(predictions)  # Obtenir l'index de la classe prédite

    # Classes du modèle
    class_names = ["black_pod_rot", "healthy", "pod_borer"]
    predicted_class = class_names[class_idx]

    # 📌 Obtenir la description et les causes associées
    description = disease_info[predicted_class]["description"]
    causes = disease_info[predicted_class]["causes"]

    # Préparer la réponse
    result = {
        "predicted_class": predicted_class,
        "description": description,
        "causes": causes if causes else "Aucune cause à signaler pour une culture saine."
    }

    return JSONResponse(content=result)