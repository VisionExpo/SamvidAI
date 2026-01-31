import cv2
import numpy as np

def preprocess_image(image_path: str) -> str:
    """
    Clean image for OCR / Layout Model
    """
    img = cv2.imread(image_path, cv.IMREAD_GRAYSCALE)

    # Denoice
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Adaptive threshold
    img = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    cv2.imwrite(image_path, img)
    return image_path