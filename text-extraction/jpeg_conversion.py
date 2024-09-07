import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def convert_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, 'JPEG')
        print(f"Converted: {input_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")

def batch_convert(input_folder, output_folder, batch_size=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    jp2_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.jp2')]
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for i in range(0, len(jp2_files), batch_size):
            batch = jp2_files[i:i+batch_size]
            futures = []
            for file in batch:
                input_path = os.path.join(input_folder, file)
                output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.jpg')
                futures.append(executor.submit(convert_image, input_path, output_path))
            
            for future in futures:
                future.result()

if __name__ == "__main__":
    input_folder = "/Users/samxp/Documents/CESTA-Summer/bub_gb_MbxYAAAAcAAJ_jp2"
    output_folder = "/Users/samxp/Documents/CESTA-Summer/all-pages-as-jpeg"
    batch_convert(input_folder, output_folder)