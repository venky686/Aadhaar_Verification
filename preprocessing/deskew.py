import cv2
import numpy as np
from utils.logger import app_logger

class Deskew:
    """
    Handles image deskewing to correct rotation.
    """
    
    @staticmethod
    def get_skew_angle(image: np.ndarray) -> float:
        """
        Calculate skew angle of an image.
        """
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
                
            # Blur and threshold
            blur = cv2.GaussianBlur(gray, (9, 9), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Dilate to merge text into blocks
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
            dilate = cv2.dilate(thresh, kernel, iterations=2)

            # Find contours
            contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            if not contours:
                return 0.0

            # Find largest contour and get minAreaRect
            largest_contour = contours[0]
            minAreaRect = cv2.minAreaRect(largest_contour)
            angle = minAreaRect[-1]
            
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
                
            return angle
        except Exception as e:
            app_logger.error(f"Error calculating skew angle: {e}")
            return 0.0

    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate the image around its center.
        """
        try:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated
        except Exception as e:
            app_logger.error(f"Error rotating image: {e}")
            return image

    @staticmethod
    def deskew_image(image: np.ndarray) -> np.ndarray:
        """
        Main method to deskew an image.
        """
        angle = Deskew.get_skew_angle(image)
        app_logger.info(f"Detected skew angle: {angle}")
        
        if abs(angle) > 0.5: # Only rotate if skew is significant
            return Deskew.rotate_image(image, angle)
        return image
