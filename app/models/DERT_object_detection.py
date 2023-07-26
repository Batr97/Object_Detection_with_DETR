from PIL import Image
import torch
import numpy as np
from transformers import AutoModelForObjectDetection, AutoImageProcessor
from utils.image_with_bbox import show_boxes


class ObjectDetector():

    def __init__(self, model_path: str) -> None:

        self.model = AutoModelForObjectDetection.from_pretrained(model_path)
        self.image_processor = AutoImageProcessor.from_pretrained(model_path)

    def predict(self, inpIm: Image.Image, target_sizes: torch.Tensor) -> torch.Tensor:

        img_features = self.image_processor(inpIm, return_tensors="pt")
        with torch.no_grad():
            prediction = self.model(**img_features)
            results = self.image_processor.post_process_object_detection(prediction, threshold=0.5, target_sizes=target_sizes)[0]
        image = show_boxes(inpIm, results, self.model)
        return np.array(image)[:,:,::-1]
