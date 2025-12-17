class ConfidenceEngine:
    """
    Calculates aggregate confidence scores from various components.
    """
    
    @staticmethod
    def calculate_ocr_confidence(ocr_data: dict) -> float:
        """
        Average confidence of extracted fields.
        """
        if not ocr_data or "documents" not in ocr_data:
            return 0.0
            
        try:
            doc = ocr_data["documents"][0]
            fields = doc.get("fields", {})
            
            if not fields:
                return 0.0
                
            total_conf = sum(f["confidence"] for f in fields.values())
            avg_conf = total_conf / len(fields)
            
            return avg_conf
        except Exception:
            return 0.0
