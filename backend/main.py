from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from tasks import create_task, get_task, update_task, delete_task
from image_processor import enhance_image
from ml_model import get_ml_parameters
import os

app = FastAPI(title="ML Image Enhancer", description="Улучшение изображений с помощью нейросети")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_results"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/api/tasks")
async def create_processing_task(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    # Проверка формата (HEIC уже сконвертирован фронтендом в JPEG)
    if file.content_type not in ["image/jpeg", "image/png", "image/bmp"]:
        raise HTTPException(400, "Unsupported format. Use JPG, PNG, BMP")
    
    image_bytes = await file.read()
    
    # Получаем параметры от ML-модели
    try:
        ml_params = get_ml_parameters(image_bytes)
        brightness = ml_params["brightness"]
        contrast = ml_params["contrast"]
        saturation = ml_params["saturation"]
        print(f"[API] ML предсказал: яркость={brightness:.2f}, контраст={contrast:.2f}, насыщ={saturation:.2f}")
    except Exception as e:
        print(f"[API] Ошибка ML: {e}, используются параметры по умолчанию")
        brightness, contrast, saturation = 1.0, 1.0, 1.0
    
    task_id = create_task(file.filename, brightness, contrast, saturation)
    background_tasks.add_task(process_task, task_id, image_bytes, brightness, contrast, saturation)
    
    return {"task_id": task_id, "status": "pending"}


def process_task(task_id: str, image_bytes: bytes, brightness: float, contrast: float, saturation: float):
    try:
        update_task(task_id, status="processing", progress=10)
        update_task(task_id, progress=30)
        
        result = enhance_image(image_bytes, brightness, contrast, saturation)
        
        update_task(task_id, progress=70)
        update_task(task_id, status="completed", progress=100, result_bytes=result)
        
        temp_file = os.path.join(TEMP_DIR, f"{task_id}.png")
        with open(temp_file, "wb") as f:
            f.write(result)
        update_task(task_id, result_path=temp_file)
        
    except Exception as e:
        update_task(task_id, status="failed", error=str(e))


@app.get("/api/tasks/{task_id}/status")
def get_task_status(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return {
        "task_id": task["id"],
        "status": task["status"],
        "progress": task.get("progress", 0),
        "error": task.get("error"),
        "brightness": task.get("brightness"),
        "contrast": task.get("contrast"),
        "saturation": task.get("saturation")
    }


@app.get("/api/tasks/{task_id}/result")
def get_task_result(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task["status"] != "completed":
        raise HTTPException(400, f"Task not ready. Status: {task['status']}")
    
    original_name = task.get("original_filename", "image")
    base = os.path.splitext(original_name)[0]
    download_name = f"{base}_enhanced.png"
    
    if task.get("result_path") and os.path.exists(task["result_path"]):
        return FileResponse(task["result_path"], filename=download_name)
    elif task.get("result_bytes"):
        return Response(content=task["result_bytes"], media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename={download_name}"
        })
    else:
        raise HTTPException(500, "No result found")


@app.delete("/api/tasks/{task_id}")
def abort_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task["status"] in ["completed", "failed", "aborted"]:
        raise HTTPException(400, f"Cannot abort task in status {task['status']}")
    
    update_task(task_id, status="aborted", progress=0)
    delete_task(task_id)
    return {"status": "aborted", "task_id": task_id}


@app.get("/api/ml/info")
def ml_info():
    return {
        "status": "active",
        "model_loaded": True,
        "model_path": "enhancer_15class",   # актуальное имя папки модели
        "input_size": "128x128"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)