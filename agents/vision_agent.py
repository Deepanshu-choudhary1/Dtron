import pytesseract
from PIL import Image
import mss
import os

# Update this path if needed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def read_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # main screen
        screenshot = sct.grab(monitor)

        img = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

    text = pytesseract.image_to_string(img)
    return text.strip()
