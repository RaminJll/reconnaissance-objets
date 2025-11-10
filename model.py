import tensorflow as tf
from tensorflow._api.v2.config import optimizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.utils import image_dataset_from_directory

train_dataset = image_dataset_from_directory(
    "./images_train",
    labels="inferred",
    label_mode="categorical",
    image_size=(224, 224),
    interpolation="nearest",
    batch_size=32,
    shuffle=True,
)

CLASS_NAMES = train_dataset.class_names
print(f"Ordre des classes : {CLASS_NAMES}")
NUM_CLASSES = len(CLASS_NAMES)


def prep_data(image, label):
    image = tf.cast(image, tf.float32) 
    
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    
    return image, label


train_dataset = (train_dataset.map(prep_data).cache().prefetch(buffer_size=tf.data.AUTOTUNE))

base_model = MobileNetV2(
    weights = "imagenet",
    include_top = False,
    input_shape = (224, 224, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)

x = Dense(1024, activation='relu')(x)

predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs = base_model.input, outputs = predictions)

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

print("début d'entrainement")

history = model.fit(train_dataset, epochs = 10)

model.save("mon_modele.h5")