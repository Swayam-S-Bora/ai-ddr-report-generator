import fitz
import os


def extract_text_from_pdf(pdf_path, output_txt_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num, page in enumerate(doc):
            text = page.get_text()
            full_text += f"\n\n--- Page {page_num + 1} ---\n"
            full_text += text

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)

        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"[INFO] Text extracted and saved to: {output_txt_path}")

    except Exception as e:
        print(f"[ERROR] Failed to extract text: {e}")