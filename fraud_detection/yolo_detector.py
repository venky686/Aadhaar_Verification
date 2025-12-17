from ultralytics import YOLO
from utils.config import settings
from utils.logger import app_logger
import cv2
import numpy as np

class YoloDetector:
    """
    Wrapper for YOLOv8 model to detect fraud indicators.
    """
    
    def __init__(self):
        self.model_path = settings.YOLO_MODEL_PATH
        try:
            self.model = YOLO(self.model_path)
        except Exception as e:
            app_logger.warning(f"Could not load YOLO model at {self.model_path}. Using default yolov8n.pt for demo.")
            self.model = YOLO("yolov8n.pt") # Fallback for development

    def detect_fraud_features(self, image_path: str) -> dict:
        """
        Run inference on the image to detect classes like:
        - 'tampered_text'
        - 'photoshop_artifact'
        - 'qr_code'
        - 'emblem'
        """
        try:
            results = self.model(image_path)
            
            detections = []
            fraud_score = 0.0
            
            # Example class mapping (needs to match trained model)
            # 0: tampered_text
            # 1: face
            # 2: qr_code
            # 3: emblem
            
            detected_classes = []
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = self.model.names[cls]
                    
                    detections.append({
                        "class": label,
                        "confidence": conf,
                        "bbox": box.xyxy[0].tolist()
                    })
                    
                    detected_classes.append(label)
                    
                    # Logic: If 'tampered_text' is detected with high confidence
                    if label == "tampered_text" and conf > 0.5:
                        fraud_score += 0.8
            
            # Check for missing mandatory elements
            if "qr_code" not in detected_classes:
                fraud_score += 0.2
            if "emblem" not in detected_classes:
                fraud_score += 0.1
                
            return {
                "detections": detections,
                "fraud_score": min(fraud_score, 1.0)
            }
            
        except Exception as e:
            app_logger.error(f"Error in YOLO detection: {e}")
            return {"detections": [], "fraud_score": 0.0}
