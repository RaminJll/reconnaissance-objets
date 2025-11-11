import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import loead_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
model = keras.models.load_model("./mon_model.keras")

if not model:
    model = None
    print("Modèle non changé")

def predict_image(subject):
    img = image.load_img(subject, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis = 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    predictions = model.predict(img_array)
    prediction_class = np.argmax(predictions[0])