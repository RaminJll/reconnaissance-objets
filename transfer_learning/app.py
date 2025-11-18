import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
CORS(app)
model = keras.models.load_model("./mon_modele.keras")

if not model:
    model = None

LABELS = ['Clavier', 'Manette', 'Tasse', 'Verre']


def predict_image(subject):
    img = image.load_img(subject, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis = 0)
    
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    predictions = model.predict(img_array)

    # top 3 des classe avec la probabilité la plus forte 
    # renvoie un tab donc faut que je modifie le front si j'utilise cette methode
    '''preds_array = predictions[0]
    top3 = np.argsort(preds_array)[::-1][:3]

    results = []
    # Boucler sur ces 3 meilleurs indices
    for i in top3:
        label = LABELS[i]
        confiance = float(preds_array[i])
    
    # Ajout des résultat formaté à la liste
    results.append({
        "objet": label,
        "confiance": f"{confiance * 100:.2f}%"
    })

    return results'''

    # directement la classe avec la probabilité la plus forte
    prediction_class = np.argmax(predictions[0])
    
    return LABELS[prediction_class], float(predictions[0][prediction_class])

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
    file_path = 'temp_subject.jpg'
    fichier.save(file_path)
    
    label, probabilite = predict_image(file_path)
    
    #top3_results = predict_image(file_path)

    os.remove(file_path)

    #return jsonify(top3_results)

    return jsonify({'objet' : label, 'probabilite' : round(probabilite, 4)})

  
if __name__ ==  '__main__':
    app.run(debug=True, port=5001)