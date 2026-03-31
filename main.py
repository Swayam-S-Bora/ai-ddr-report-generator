from src.extractor.image_extractor import extract_images_from_pdf
from src.extractor.text_extractor import extract_text_from_pdf
from src.processor.llm_handler import generate_ddr_report
from src.processor.reasoning import preprocess_text
from src.generator.html_generator import generate_html_report
from src.generator.pdf_generator import generate_pdf

import json
import re

from config import (
    INSPECTION_PDF,
    INSPECTION_TEXT,
    THERMAL_PDF,
    THERMAL_TEXT,
    INSPECTION_IMAGES,
    THERMAL_IMAGES
)

# Input files
inspection_pdf = INSPECTION_PDF
thermal_pdf = THERMAL_PDF

# Output paths
inspection_text = INSPECTION_TEXT
thermal_text = THERMAL_TEXT

inspection_images = INSPECTION_IMAGES
thermal_images = THERMAL_IMAGES


# 🔥 FIXED JSON CLEANER
def clean_json_output(raw_text):
    raw_text = re.sub(r"```json|```", "", raw_text).strip()

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)

    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except Exception as e:
            print("[ERROR] JSON parsing failed:", e)

    print("[WARNING] Using fallback JSON")

    return {
        "summary": "Failed to parse model output.",
        "areas": [],
        "additional_notes": "",
        "missing_info": ""
    }


def run_extraction():
    print("\n--- Extracting Inspection Report ---")
    extract_text_from_pdf(inspection_pdf, inspection_text)
    extract_images_from_pdf(inspection_pdf, inspection_images)

    print("\n--- Extracting Thermal Report ---")
    extract_text_from_pdf(thermal_pdf, thermal_text)
    extract_images_from_pdf(thermal_pdf, thermal_images)


def run_processing():
    with open(inspection_text, "r", encoding="utf-8") as f:
        inspection_data = f.read()

    with open(thermal_text, "r", encoding="utf-8") as f:
        thermal_data = f.read()

    # 🔥 LIMIT INPUT SIZE (IMPORTANT)
    inspection_data = inspection_data[:12000]
    thermal_data = thermal_data[:8000]

    context = preprocess_text(inspection_data, thermal_data)

    print("\n--- Generating DDR Report ---")

    report = generate_ddr_report(
        inspection_data + context,
        thermal_data
    )

    cleaned_report = clean_json_output(report)

    with open("output/report.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_report, f, indent=2)

    print("[INFO] DDR report generated at output/report.json")


def run_generation():
    generate_html_report(
        "output/report.json",
        "output/report.html"
    )


def run_pdf_generation():
    generate_pdf(
        "output/report.html",
        "output/report.pdf"
    )


if __name__ == "__main__":
    run_extraction()
    run_processing()
    run_generation()
    run_pdf_generation()