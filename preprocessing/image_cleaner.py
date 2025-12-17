import cv2
import numpy as np
from utils.logger import app_logger

class ImageCleaner:
    """
    Handles image cleaning, normalization, and noise removal.
    """
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """
        Normalizes the image intensity values.
        """
        try:
            norm_img = np.zeros((image.shape[0], image.shape[1]))
            final_img = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
            return final_img
        except Exception as e:
            app_logger.error(f"Error in normalizing image: {e}")
            return image

    @staticmethod
    def remove_noise(image: np.ndarray) -> np.ndarray:
        """
        Removes noise using Gaussian Blur and Median Blur.
        """
        try:
            # Denoising
            dst = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            return dst
        except Exception as e:
            app_logger.error(f"Error in removing noise: {e}")
            return image

    @staticmethod
    def preprocess_for_ocr(image_path: str) -> np.ndarray:
        """
        Full preprocessing pipeline for OCR.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image at {image_path}")
            
            # 1. Remove Noise
            clean_image = ImageCleaner.remove_noise(image)
            
            # 2. Convert to Grayscale
            gray = cv2.cvtColor(clean_image, cv2.COLOR_BGR2GRAY)
            
            # 3. Thresholding (Binarization)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
        except Exception as e:
            app_logger.error(f"Error in preprocessing pipeline: {e}")
            raise
