from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, Response
from PIL import Image
import io
import cv2
import torch
from models.DERT_object_detection import ObjectDetector
from utils.image_with_bbox import show_boxes


# FastAPI app
app = FastAPI()

# Инициализация модели трансформера
DERT_model = ObjectDetector('facebook/detr-resnet-50')


@app.post("/predict/image/")
async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    target_sizes = torch.tensor([image.size[::-1]])
    image = image.convert('RGB')
    image = DERT_model.predict(inpIm=image, target_sizes=target_sizes)

    # Конвертация изображени в байтовый формат
    _, buffer = cv2.imencode(".jpg", image)
    image_bytes = buffer.tobytes()
    # Создадим типа контента - изображение 
    headers = {
        "Content-Type": "image/jpeg"
    }

    # Возвращаем детектированное изображение с объектами
    return Response(content=image_bytes, headers=headers)
