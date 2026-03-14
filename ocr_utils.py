import pytesseract
from PIL import Image
import re

def extract_aadhaar_data(image_path):

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)

    name_match = re.search(r"[A-Z][a-z]+\s[A-Z][a-z]+", text)
    address_match = re.search(r"Address(.+)", text)

    name = name_match.group() if name_match else "Unknown"
    address = address_match.group() if address_match else "Unknown"

    return {
        "name": name,
        "address": address
    }