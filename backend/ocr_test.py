from services.ocr_service import extract_text


image_path = "test.png"

text = extract_text(image_path)

print("===== EXTRACTED TEXT =====")
print(text)