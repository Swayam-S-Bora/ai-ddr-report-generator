import pdfkit


def generate_pdf(html_path, output_pdf_path):
    try:
        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        )

        pdfkit.from_file(
            html_path,
            output_pdf_path,
            configuration=config,
            options={
                "enable-local-file-access": ""
            }
        )

        print(f"[INFO] PDF generated at {output_pdf_path}")

    except Exception as e:
        print(f"[ERROR] PDF generation failed: {e}")