# ML Image Enhancer

Автоматическое улучшение изображений (яркость, контраст, насыщенность) с помощью нейросети.  
Проект выполнен в рамках лабораторной работы.

## 📦 Скачать проект архивом

[Скачать ZIP-архив репозитория](https://github.com/zhidenkovicktoria/ml-image-enhancer/archive/refs/heads/main.zip)

## 🎯 Требования 

| Требование | Статус |
|------------|--------|
| Работа во всех браузерах | ✅ |
| Объём кода ≤10 МБ (клиент) | ✅ |
| Обработка до 15 Мп | ✅ |
| Время обработки ≤30 с | ✅ |
| Форматы JPG, PNG, BMP, HEIC | ✅ |
| Асинхронность (не блокирует UI) | ✅ |
| API: create, status, abort, get result | ✅ |
| События статуса / прогресс | ✅ |
| ML подбирает параметры | ✅ |

## 🖥️ Демонстрация

**Фронтенд (статическая демо-версия):**  
🔗 [https://zhidenkovicktoria.github.io/ml-image-enhancer/frontend/](https://zhidenkovicktoria.github.io/ml-image-enhancer/frontend/)  

*Для работы требуется запущенный бэкенд (см. инструкцию ниже). Без бэкенда кнопки не будут обрабатывать изображения.*

## 📦 Установка и запуск (локально)

### Требования
- Python 3.11+
- Установленные зависимости из `backend/requirements.txt`

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/zhidenkovicktoria/ml-image-enhancer.git
cd ml-image-enhancer
```
### 2. Запустите бэкенд
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Сервер будет доступен по адресу http://localhost:8000
Документация API: http://localhost:8000/docs

### 3. Откройте фронтенд
Откройте файл `frontend/index.html` в браузере или запустите простой HTTP сервер:

```bash
cd frontend
python -m http.server 3000
```
Перейдите на http://localhost:3000

### 📡 API

| Метод |	Эндпоинт	| Описание |
|-------|---------------|----------|
| POST	| `/api/tasks`	| Создать задачу (передать файл) |
| GET	| `/api/tasks/{id}/status` |	Получить статус, прогресс и предсказанные параметры |
| GET	| `/api/tasks/{id}/result`	| Скачать улучшенное изображение |
| DELETE |	`/api/tasks/{id}`	| Прервать задачу |

API документировано автоматически (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### 🧠 ML-модель
* Архитектура: классификация на 15 действий (комбинации изменения яркости, контраста, насыщенности).

* Обучена на датасете CIFAR-10 с синтетическими искажениями.

* Вход: изображение 128×128 пикселей.

* Выход: коэффициенты яркости, контраста, насыщенности

Модель сохранена в формате SavedModel (папка `backend/enhancer_15class`).

Ноутбук с обучением модели: [открыть в Colab](https://colab.research.google.com/drive/1awmR3FsPO_MayBPQDHhfS6VPPQ7FETaB?usp=sharing)

### 📸 Тестирование

Используйте изображения из папки `samples/` или свои.
В логах бэкенда отображается предсказанный класс и применённые коэффициенты.

В папке `samples/` вы найдёте примеры фотографий с разными дефектами:

* `dark_room.bmp` и `dark_owl.heic` – слишком тёмное

* `low_contrast.png` – бледное

* `highlighted.jpg` – пересвеченное

### 🛠️ Технологии
* Backend: FastAPI, TensorFlow 2.15, Pillow

* Frontend: HTML5, CSS3, JavaScript, heic2any

* ML: Keras (TensorFlow)