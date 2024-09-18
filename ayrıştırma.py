from flask import Flask, request, jsonify
import os
from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np

app = Flask(__name__)

# Model ve etiket yolları


def get_class(image_path, model_path, labels_path):
    np.set_printoptions(suppress=True)

    # Modeli yükle
    model = load_model(model_path, compile=False)

    # Sınıf etiketlerini yükle
    class_names = open(labels_path, "r").readlines()

    # Görseli işle
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")

    # Görseli yeniden boyutlandır ve normalize et
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Tahmin yap
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]
    
    return class_name, confidence_score
