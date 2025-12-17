import shutil
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from preprocessing.image_cleaner import ImageCleaner
from preprocessing.deskew import Deskew
from preprocessing.quality_metrics import QualityMetrics
from ocr.azure_ocr import AzureOCR
from ocr.field_extractor import FieldExtractor
from ocr.validator import Validator
from llm.openai_refiner import OpenAIRefiner
from fraud_detection.yolo_detector import YoloDetector
from fraud_detection.anomaly_model import AnomalyModel
from fraud_detection.forgery_rules import ForgeryRules
from scoring.confidence_engine import ConfidenceEngine
from scoring.decision_engine import DecisionEngine
from utils.logger import app_logger

router = APIRouter()

# Initialize services
azure_ocr = AzureOCR()
openai_refiner = OpenAIRefiner()
yolo_detector = YoloDetector()
anomaly_model = AnomalyModel()

@router.post("/verify-document")
async def verify_document(file: UploadFile = File(...)):
    """
    Main endpoint to verify Aadhaar document.
    """
    temp_file_path = ""
    try:
        # 1. Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_file_path = tmp.name
            
        app_logger.info(f"Processing file: {temp_file_path}")

        # 2. Preprocessing
        # Load image for CV tasks
        clean_img = ImageCleaner.preprocess_for_ocr(temp_file_path)
        deskewed_img = Deskew.deskew_image(clean_img)
        
        # Quality Check
        quality_report = QualityMetrics.assess_quality(deskewed_img)
        if not quality_report["quality_pass"]:
            app_logger.warning(f"Image quality failed: {quality_report}")
            # We continue but flag it? Or return error? 
            # For now, we continue but note it.

        # 3. Fraud Detection
        yolo_result = yolo_detector.detect_fraud_features(temp_file_path)
        anomaly_score = anomaly_model.predict_anomaly(deskewed_img)
        forgery_score = ForgeryRules.calculate_forgery_score({}, temp_file_path) # OCR result not ready yet
        
        combined_fraud_score = max(yolo_result["fraud_score"], forgery_score)

        # 4. OCR Extraction
        # Read file bytes for Azure OCR
        with open(temp_file_path, "rb") as f:
            file_bytes = f.read()
            
        ocr_result = azure_ocr.analyze_document(file_bytes)
        extracted_fields = FieldExtractor.extract_aadhaar_fields(ocr_result)
        
        # 5. Validation & Refinement
        validation_report = Validator.validate_extracted_data(extracted_fields)
        
        # Use LLM to refine if needed (e.g. if validation fails or just to normalize)
        refined_data = openai_refiner.refine_extracted_data(extracted_fields)
        
        # 6. Scoring
        ocr_conf = ConfidenceEngine.calculate_ocr_confidence(ocr_result)
        
        final_risk = DecisionEngine.calculate_risk_score(
            ocr_conf=ocr_conf,
            yolo_fraud_score=combined_fraud_score,
            anomaly_score=anomaly_score
        )
        
        decision = DecisionEngine.make_decision(final_risk)
        
        return {
            "extracted_data": refined_data,
            "validation_report": validation_report,
            "quality_metrics": quality_report,
            "scores": {
                "ocr_confidence": ocr_conf,
                "fraud_score": combined_fraud_score,
                "anomaly_score": anomaly_score,
                "final_risk_score": final_risk
            },
            "decision": decision,
            "fraud_details": yolo_result["detections"]
        }

    except Exception as e:
        app_logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
