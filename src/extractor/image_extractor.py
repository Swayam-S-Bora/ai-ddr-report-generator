import fitz
import os
from PIL import Image
import io


def extract_images_from_pdf(pdf_path, output_folder, min_size=10000, max_images=200):
    try:
        doc = fitz.open(pdf_path)
        os.makedirs(output_folder, exist_ok=True)

        image_count = 0
        saved_hashes = set()

        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                if image_count >= max_images:
                    print("[INFO] Reached max image limit")
                    return

                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Skip small images (noise)
                if len(image_bytes) < min_size:
                    continue

                # Remove duplicates
                img_hash = hash(image_bytes)
                if img_hash in saved_hashes:
                    continue
                saved_hashes.add(img_hash)

                image = Image.open(io.BytesIO(image_bytes))
                image_ext = base_image["ext"]

                image_filename = f"page_{page_index+1}_img_{image_count+1}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)

                image.save(image_path)
                image_count += 1

        print(f"[INFO] Extracted {image_count} filtered images to {output_folder}")

    except Exception as e:
        print(f"[ERROR] Failed to extract images: {e}")