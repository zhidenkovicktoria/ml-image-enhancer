import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "enhancer_15class")

# Таблица действий (15 классов)
ACTION_PARAMS = [
    (1.0, 1.0, 1.0),    # 0
    (1.3, 1.0, 1.0),    # 1
    (0.7, 1.0, 1.0),    # 2
    (1.0, 1.3, 1.0),    # 3
    (1.0, 0.7, 1.0),    # 4
    (1.0, 1.0, 1.3),    # 5
    (1.0, 1.0, 0.7),    # 6
    (1.2, 1.2, 1.0),    # 7
    (0.8, 0.8, 1.0),    # 8
    (1.0, 1.2, 1.2),    # 9
    (1.0, 0.8, 0.8),    # 10
    (1.2, 1.0, 1.2),    # 11
    (0.8, 1.0, 0.8),    # 12
    (1.15, 1.15, 1.15), # 13
    (0.85, 0.85, 0.85)  # 14
]

class EnhancerClassifier:
    def __init__(self):
        self.model = None
        self.input_size = (128, 128)
        self._load_model()
    
    def _load_model(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Модель не найдена: {MODEL_PATH}. Распакуйте enhancer_15class.zip в папку backend.")
        self.model = tf.saved_model.load(MODEL_PATH)
        self.infer = self.model.signatures['serving_default']
        print("[ML] Загружена модель классификации на 15 действий")
    
    def preprocess(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize(self.input_size)
        arr = np.array(img) / 255.0
        return tf.convert_to_tensor([arr], dtype=tf.float32)
    
    def predict_parameters(self, image_bytes):
        tensor = self.preprocess(image_bytes)
        outputs = self.infer(tensor)
        preds = list(outputs.values())[0].numpy()[0]  # вектор из 15 вероятностей
        action_idx = int(np.argmax(preds))
        brightness, contrast, saturation = ACTION_PARAMS[action_idx]
        print(f"[ML] Класс {action_idx} → ярк={brightness:.2f}, конт={contrast:.2f}, нас={saturation:.2f}")
        return {
            "brightness": brightness,
            "contrast": contrast,
            "saturation": saturation
        }

classifier = EnhancerClassifier()

def get_ml_parameters(image_bytes: bytes):
    return classifier.predict_parameters(image_bytes)