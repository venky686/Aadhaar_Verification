class DecisionEngine:
    """
    Combines scores to make a final decision.
    """
    
    @staticmethod
    def calculate_risk_score(ocr_conf: float, yolo_fraud_score: float, anomaly_score: float) -> float:
        """
        Final Risk Score = (OCR Confidence * 0.4) + (YOLO Fraud Score * 0.4) + (Anomaly Score * 0.2)
        
        Wait, the formula in requirements is a bit ambiguous.
        "OCR Confidence" is usually "Goodness", while "Fraud Score" is "Badness".
        
        Let's invert OCR Confidence to "OCR Uncertainty" for a Risk Score.
        Risk = ((1 - OCR_Conf) * 0.4) + (YOLO_Fraud * 0.4) + (Anomaly * 0.2)
        
        Let's stick to the user's prompt but interpret it logically.
        If the user meant "Risk Score", then high OCR confidence should LOWER the risk.
        
        Let's assume the user wants a score from 0-100 where 100 is FRAUD.
        
        Risk = ( (1.0 - OCR_Conf) * 40 ) + ( YOLO_Fraud * 40 ) + ( Anomaly * 20 )
        
        This sums up to 100 max.
        """
        
        term1 = (1.0 - ocr_conf) * 40
        term2 = yolo_fraud_score * 40
        term3 = anomaly_score * 20
        
        final_score = term1 + term2 + term3
        return round(final_score, 2)

    @staticmethod
    def make_decision(risk_score: float) -> str:
        """
        0–40 → SAFE
        41–70 → REVIEW
        71–100 → FRAUD
        """
        if risk_score <= 40:
            return "SAFE"
        elif risk_score <= 70:
            return "REVIEW"
        else:
            return "FRAUD"
