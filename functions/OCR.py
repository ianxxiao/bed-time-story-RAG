import base64
import requests
import os
from mistralai import Mistral
from pathlib import Path
from functions.helper import ensure_directory_exists

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return "Error: The file was not found."
    except Exception as e:
        return f"Error: {e}"

def get_combined_markdown(ocr_response) -> tuple:
    markdowns = []
    raw_markdowns = []
    for page in ocr_response.pages:
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))
        raw_markdowns.append(page.markdown)
    return "\n\n".join(markdowns), "\n\n".join(raw_markdowns)

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})")
    return markdown_str

def perform_ocr_file(file, ocr_method="Mistral OCR"):

    print(f"Performing OCR on file: {file}")    

    try:
        api_key = os.environ["MISTRAL_API_KEY"]
        client = Mistral(api_key=api_key)

        if ocr_method == "Mistral OCR":
            if file.name.endswith('.pdf'):

                print(f"Uploading file to Mistral: {file.name}")
                
                uploaded_pdf = client.files.upload(
                    file={
                        "file_name": file.name,
                        "content": open(str(Path(__file__).parent / "data" / "rawData" / file.name), "rb"),
                    },
                    purpose="ocr"
                )

                signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
                
                print(f"Extracting: {file.name}")
                ocr_response = client.ocr.process(
                    model="mistral-ocr-latest",
                    document={
                        "type": "document_url",
                        "document_url": signed_url.url,
                    },
                    include_image_base64=True
                )

                client.files.delete(file_id=uploaded_pdf.id)

            elif file.name.endswith(('.png', '.jpg', '.jpeg')):

                base64_image = encode_image(file.name)
                
                ocr_response = client.ocr.process(
                    model="mistral-ocr-latest",
                    document={
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    },
                    include_image_base64=True
                )

            combined_markdown, raw_markdown = get_combined_markdown(ocr_response)

            # Save processed data to files
            processed_data_dir = Path(__file__).parent / "data" / "processedData"
            ensure_directory_exists(processed_data_dir)
            
            # Create filenames based on input file
            base_name = file.stem
            combined_path = processed_data_dir / f"{base_name}_combined.md"
            raw_path = processed_data_dir / f"{base_name}_raw.md"
            
            # Write the markdown files
            combined_path.write_text(combined_markdown)
            raw_path.write_text(raw_markdown)

            return True, None

        return False, None
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, f"Error: {str(e)}"
