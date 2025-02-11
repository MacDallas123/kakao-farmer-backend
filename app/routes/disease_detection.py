from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import tensorflow as tf

# Charger le modèle entraîné
model = tf.keras.models.load_model("trained_models/cacao_disease_model.h5")

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

app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    # Prétraitement de l'image
    image = image.resize((224, 224))  # Redimensionner selon votre modèle
    image_array = np.array(image) / 255.0  # Normaliser si nécessaire
    image_array = np.expand_dims(image_array, axis=0)  # Ajouter une dimension pour le batch

    # Faire la prédiction
    predictions = model.predict(image_array)
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