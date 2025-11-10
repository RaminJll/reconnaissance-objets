import os
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
model = keras.models.load_model("./mon_model.keras")

if not model:
    model = None

LABELS = ['Clavier', 'Manette', 'Tasse', 'Verre']


def predict_image(subject):
    img = image.load_img(subject, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.extend_dims(img_array, axis = 0)
    
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    predictions = model.predict(img_array)
    prediction_class = np.argmax(predictions[0])
    
    return LABELS[prediction_class], float(predictions[0][prediction_class])



@app.route('/predict', methods=['POST'])
def predict():
    if model == None:
        return jsonify({"error": "Modèle non chargé"}), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "Aucun dichier d'image reouvé"}), 400
    
    fichier = request.files['file']
    file_path = 'temp_subject.jpg'
    fichier.save(file_path)
    
    label, probabilite = predict_image(file_path)
    
    os.remove(file_path)
    
    return jsonify({"objet" : label, 'probabilite' : round(probabilite, 4)})

  
if __name__ ==  '__main__':
    app.run(debug=True)