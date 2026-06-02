# ML Image Enhancer

Автоматическое улучшение изображений (яркость, контраст, насыщенность) с помощью нейросети.  
**Модель работает прямо в вашем браузере** (TensorFlow.js). Никакого бэкенда, ничего не нужно устанавливать.

🔗 **Демо:** [https://zhidenkovicktoria.github.io/ml-image-enhancer/](https://zhidenkovicktoria.github.io/ml-image-enhancer/)

📦 **Скачать архив проекта:** [ZIP](https://github.com/zhidenkovicktoria/ml-image-enhancer/archive/refs/heads/main.zip)

---

## 🎯 Выполненные требования

| Требование | Статус |
|------------|--------|
| ML-модель в браузере пользователя | ✅ |
| Улучшение яркости, контраста, цветности | ✅ |
| Работа во всех браузерах | ✅ |
| Объём клиентского кода ≤10 МБ | ✅ |
| Обработка до 15 Мп | ✅ |
| Время обработки ≤30 с (обычно 2–5 с) | ✅ |
| Форматы JPG, PNG, BMP, HEIC | ✅ |
| Асинхронность (не блокирует UI) | ✅ |
| API-методы (create, status, abort, result) | ✅ (эмуляция на клиенте) |
| События статуса / прогресс | ✅ |
| ML подбирает параметры | ✅ |

---

## 🚀 Демонстрация (без установки)

Просто перейдите по ссылке:  
[https://zhidenkovicktoria.github.io/ml-image-enhancer/](https://zhidenkovicktoria.github.io/ml-image-enhancer/)

1. Дождитесь загрузки модели (кнопка активируется).
2. Загрузите изображение (JPG, PNG, BMP, HEIC).
3. Нажмите «Запустить улучшение».
4. Получите результат и скачайте его.

---

## 📁 Структура репозитория 
```bash
ml-image-enhancer/
├── docs/
│ ├── index.html # главный интерфейс (TensorFlow.js)
│ └── tfjs_model/ # конвертированная модель
│ ├── model.json
│ └── *.bin # файлы весов
├── samples/ # тестовые изображения
└── README.md
```

## 🧪 Локальное тестирование (опционально)

Если вы хотите запустить копию на своём компьютере без интернета:

```bash
cd docs
python -m http.server 3000
```
Затем откройте http://localhost:3000

## 🧠 ML-модель
 * Архитектура: классификация на 15 действий (комбинации изменения яркости, контраста, насыщенности).

 * Обучение: на датасете CIFAR-10 с синтетическими искажениями (включая пересвеченные примеры).

 * Формат: TensorFlow.js (конвертирована из SavedModel).

 * Вход: изображение 128×128 пикселей.

 * Выход: коэффициенты (brightness, contrast, saturation), применяемые через Canvas API.

## Ноутбуки Google Colab
Обучение модели: [открыть в Colab](https://colab.research.google.com/drive/1awmR3FsPO_MayBPQDHhfS6VPPQ7FETaB?usp=sharing)

Конвертация в TensorFlow.js: [открыть в Colab](https://colab.research.google.com/drive/1D6JRr4ufSGbbBgeM42FGy6TCOSUxjnvP?usp=sharing)

## 📸 Тестирование

В папке `samples/` вы найдёте примеры фотографий с разными дефектами:

* `dark_room.bmp` и `dark_owl.heic` – слишком тёмное

* `low_contrast.png` – бледное

* `highlighted.jpg` – пересвеченное

их можно использовать для проверки

## 🛠️ Технологии
 * **Frontend:** HTML5, CSS3, JavaScript (ES6), TensorFlow.js, Canvas API, heic2any

 * **ML**: Keras (TensorFlow), конвертация в TensorFlow.js

 * **Хостинг**: GitHub Pages (полностью статический)
