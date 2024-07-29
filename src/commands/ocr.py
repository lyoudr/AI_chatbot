import sys
sys.path.append("src")

import click # noqa E402

from services.ocr import (
    split_pdf,
    clean_text,
    process_document_ocr_sample,
)
from settings import get_settings

settings = get_settings()


@click.command()
@click.argument('page')
def main(page):
    # Split Harrpy Potter PDF to several file for OCR
    # split_pdf(
    #     input_pdf_path="/Users/apple/Code/Ikala/ai/src/harry_potter/original/harry_potter_1.pdf",
    #     output_path="/Users/apple/Code/Ikala/ai/src/harry_potter/en",
    #     output_prefix="episode_1"
    # )
    text_lines = process_document_ocr_sample(
        project_id=settings.GCP_PROJECT_ID,
        location="us",
        processor_id=settings.PROCESSOR_ID,
        processor_version=settings.PROCESSOR_VERSION_ID,
        file_path=f"/Users/apple/Code/Ikala/ai/src/harry_potter/en/episode_1/{page}.pdf",
        mime_type="application/pdf",
    )
    # TODO -> clean text
    # cleaned_text_lines = clean_text(text_lines)
    # print("cleaned_text_lines is ->", cleaned_text_lines)


if __name__ == "__main__":
    main()
