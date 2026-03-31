import json
import os


def generate_html_report(json_path, output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔥 Safety check
    if not isinstance(data, dict):
        print("[ERROR] Invalid JSON format, using fallback")
        data = {
            "summary": "Error in report generation",
            "areas": [],
            "additional_notes": "",
            "missing_info": ""
        }

    # Load HTML template
    with open("src/generator/templates/report_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    areas_html = ""

    images_path = "data/extracted/images/inspection"

    # ✅ THIS IS WHERE YOU APPLY SORTING FIX
    if os.path.exists(images_path):
        images = sorted(os.listdir(images_path))[:6] 
    else:
        images = []

    for area in data.get("areas", []):
        images_html = ""

        for img in images:
            img_path = f"data/extracted/images/inspection/{img}"
            images_html += f'<img src="{img_path}">'

        areas_html += f"""
        <div class="area">
            <h3>{area.get("area", "")}</h3>

            <p><span class="label">Observation:</span> {area.get("observation", "")}</p>
            <p><span class="label">Root Cause:</span> {area.get("root_cause", "")}</p>
            <p><span class="label">Evidence:</span> {area.get("evidence", "")}</p>
            <p><span class="label">Severity:</span> {area.get("severity", "")}</p>
            <p><span class="label">Recommendation:</span> {area.get("recommendation", "")}</p>

            <div class="images">
                {images_html}
            </div>
        </div>
        """

    # Replace placeholders
    template = template.replace("{{SUMMARY}}", data.get("summary", ""))
    template = template.replace("{{AREAS}}", areas_html)
    template = template.replace("{{NOTES}}", data.get("additional_notes", ""))
    template = template.replace("{{MISSING}}", data.get("missing_info", ""))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)

    print("[INFO] Styled HTML report generated!")