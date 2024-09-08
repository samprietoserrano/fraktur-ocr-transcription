import pytesseract
from PIL import Image

def main():
    # Open the image
    image = Image.open('/Users/USER/Downloads/bub_gb_MbxYAAAAcAAJ_0906.jpg')

    # Perform OCR
    text = pytesseract.image_to_string(image, lang='deu')  # 'deu' for German

    # Print the extracted text
    print(text)

if __name__ == '__main__':
    main()
