import sys
sys.path.append("src")

import click # noqa E402

from services.ocr import ( # noqa F401
    split_pdf,
    clean_text,
    process_document_ocr_sample,
)
from services.gcs import CloudStorage # noqa F401
from services.embeddings import Embedding # noqa F401
from settings import get_settings # noqa F401

settings = get_settings()


@click.command()
@click.argument('episode')
@click.argument('page')
def main(episode, page):
    # 1. Split Harrpy Potter PDF to several file for OCR
    # split_pdf(
    #     input_pdf_path="/Users/apple/Code/Ikala/ai/src/harry_potter/original/harry_potter_1.pdf",
    #     output_path="/Users/apple/Code/Ikala/ai/src/harry_potter/en",
    #     output_prefix="episode_1"
    # )

    # 2. OCR pdf
    text_lines = process_document_ocr_sample(
        project_id=settings.GCP_PROJECT_ID,
        location="us",
        processor_id=settings.PROCESSOR_ID,
        processor_version=settings.PROCESSOR_VERSION_ID,
        file_path=f"/Users/apple/Code/Ikala/ai/src/harry_potter/en/episode_{episode}/{page}.pdf",
        mime_type="application/pdf",
    )

    # 3. clean text
    cleaned_text_lines = clean_text(text_lines)
    print("cleaned_text_lines is ->", cleaned_text_lines)

    # 4. Embedding texts, and upload files to GCS
    source_dir = f'src/static/harry_potter/en/episode_{episode}'
    embed = Embedding(source_dir=source_dir)
    embed.clear_dir()
    id = 1
    for sentence in cleaned_text_lines:
        embeded_texts = embed.embed_text(
            [sentence],
            "RETRIEVAL_DOCUMENT",
            "text-embedding-004",
            100,
        )
        embed.embed_to_json(
            str(id),
            embeded_texts[0],
            page,
        )
        id += 1

    # 5. Upload to Cloud Storage
    gcs = CloudStorage(
        project_id=settings.GCP_PROJECT_ID,
        bucket_name=settings.GCS_BUCKET_NAME
    )
    gcs.upload_files(
        source_dir=source_dir
    )


if __name__ == "__main__":
    main()
