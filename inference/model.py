import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import MobileNetV2

model = MobileNetV2(
    weights = 'imagenet',
    include_top = True,
    input_shape = (224, 224, 3)
)

model.save('mon_modele.keras')