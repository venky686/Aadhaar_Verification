import cv2
import numpy as np
from utils.logger import app_logger

class QualityMetrics:
    """
    Calculates image quality metrics like blur and lighting.
    """
    
    @staticmethod
    def calculate_blur_score(image: np.ndarray) -> float:
        """
        Calculate the variance of Laplacian to detect blur.
        Higher score means sharper image.
        """
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            score = cv2.Laplacian(gray, cv2.CV_64F).var()
            return score
        except Exception as e:
            app_logger.error(f"Error calculating blur score: {e}")
            return 0.0

    @staticmethod
    def calculate_lighting_score(image: np.ndarray) -> float:
        """
        Calculate average brightness of the image.
        Range 0-255.
        """
        try:
            if len(image.shape) == 3:
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                brightness = np.mean(hsv[:, :, 2])
            else:
                brightness = np.mean(image)
            return brightness
        except Exception as e:
            app_logger.error(f"Error calculating lighting score: {e}")
            return 0.0

    @staticmethod
    def assess_quality(image: np.ndarray) -> dict:
        """
        Returns a dictionary of quality metrics.
        """
        blur_score = float(QualityMetrics.calculate_blur_score(image))
        lighting_score = float(QualityMetrics.calculate_lighting_score(image))
        
        is_blurry = bool(blur_score < 100.0) # Threshold can be tuned
        is_dark = bool(lighting_score < 50.0) # Threshold can be tuned
        is_overexposed = bool(lighting_score > 200.0)
        
        return {
            "blur_score": blur_score,
            "lighting_score": lighting_score,
            "is_blurry": is_blurry,
            "is_dark": is_dark,
            "is_overexposed": is_overexposed,
            "quality_pass": bool(not (is_blurry or is_dark or is_overexposed))
        }
