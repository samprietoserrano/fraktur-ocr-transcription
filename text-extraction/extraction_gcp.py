from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import io
import os
from PIL import Image
from tqdm import tqdm


def ocr_image(file_path, exit_path):
    credential_path = '/Users/USER/Documents/CESTA-Summer/gcp_cesta-sum-2024_processor-key.json' # add path, json file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    PROJECT_ID = "cesta-sum-2024"
    LOCATION = "us"  # Format is 'us' or 'eu'
    PROCESSOR_ID = "793faa77f36a7161"  # Create processor in Cloud Console

    # The local file in your current working directory
    FILE_PATH = file_path
    # Refer to https://cloud.google.com/document-ai/docs/file-types
    # for supported file types
    MIME_TYPE = "image/jpeg"

    # Instantiates a client
    docai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
    )

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    # Read the file into memory
    with open(FILE_PATH, "rb") as image:
        img = Image.open(image)
        box = (243, 0, 1340, 2500)
        img = img.crop(box)

    # TypeError: <PIL.Image.Image image mode=RGB size=1220x2500 at 0x103F894D0> has type Image, but expected one of: bytes
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    image_content = buf.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

    # Configure the process request
    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = docai_client.process_document(request=request)

    document_object = result.document

    # Split the filename into name and extension
    base_name, _ = os.path.splitext(exit_path)
    
    # Create a new filename with the new extension
    new_exit_path = f"{base_name}.txt"
    with open(new_exit_path, 'w', encoding='utf-8') as file:
        # Write text from the string object to the file
        file.write(document_object.text)


def process_folder(folder_path, exit_folder):
    with tqdm(total=774, desc="OCRing txt", unit="file") as pbar:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.jpg'):
                file_path = os.path.join(folder_path, file_name)
                exit_path = os.path.join(exit_folder, file_name)
                ocr_image(file_path, exit_path)
                print(f"Processed: '{file_name}'")
                pbar.update(1)


def main():
    folder_path = '/Users/USER/Documents/CESTA-Summer/all-pages-as-jpeg/main-only'

    # Batch process the entire folder of images containing the main-text of the book
    exit_folder = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script'
    os.makedirs(exit_folder, exist_ok=True)
    process_folder(folder_path, exit_folder)


if __name__ == "__main__":
    main()

