import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
model = keras.models.load_model("./mon_modele.keras")

if not model:
    model = None
    print("Modèle non changé")

def predict_image(subject):
    img_read = io.BytesIO(subject.read())
    img = Image.open(img_read).convert('RGB')
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis = 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    predictions = model.predict(img_array)

    decoded_results = decode_predictions(predictions, top=3)[0]

    results = []
    for i, label, score in decoded_results:
        results.append({
            "label": label, # Make labels more readable
            "probabilite": f"{score * 100:.2f}%"
        })
            
    return results


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if model == None:
        return jsonify({"error": "Modèle non chargé"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Aucun dichier d'image reouvé"}), 400

    fichier = request.files['file']
    predictions_list = predict_image(fichier)

    return jsonify({'predictions': predictions_list})

if __name__ ==  '__main__':
    app.run(debug=True)