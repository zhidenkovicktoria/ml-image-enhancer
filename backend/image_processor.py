from PIL import Image, ImageEnhance
import io

def enhance_image(image_bytes: bytes, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0):
    """
    brightness: 0.5..1.5 (1 = оригинал)
    contrast:   0.5..1.5
    saturation: 0.0..2.0 (1 = оригинал, 0 = ч/б)
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Яркость
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    
    # Контраст
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # Цветность (насыщенность)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)
    
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


def analyze_image(image_bytes: bytes):
    """Анализирует изображение для ML-модели (заглушка)"""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Простейший анализ: средняя яркость
    pixels = list(img.getdata())
    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)
    avg_brightness = (avg_r + avg_g + avg_b) / 3
    
    return {
        "avg_brightness": avg_brightness,
        "width": img.width,
        "height": img.height,
        "format": img.format
    }