class ForgeryRules:
    """
    Rule-based checks for potential forgery.
    """
    
    @staticmethod
    def check_font_consistency(ocr_result: dict) -> float:
        """
        Check if fonts are consistent (mock implementation).
        """
        # In a real system, we would analyze font metadata from OCR
        return 0.0

    @staticmethod
    def check_metadata(image_path: str) -> float:
        """
        Check EXIF data for editing software traces.
        """
        # Use PIL or exifread to check for 'Photoshop', 'GIMP', etc.
        return 0.0

    @staticmethod
    def calculate_forgery_score(ocr_result: dict, image_path: str) -> float:
        font_score = ForgeryRules.check_font_consistency(ocr_result)
        meta_score = ForgeryRules.check_metadata(image_path)
        
        return max(font_score, meta_score)
