import sys
sys.path.append("src")

from fastapi import APIRouter, File, UploadFile, Depends

from settings import get_settings
from models.chatbot import ChatBotResponse
from services.ocr import (
    process_document_ocr_sample,
    clean_text
)
from services.gcs import CloudStorage
from services.embeddings import Embedding
from services.vector import vector_search_find_neighbors

import os
import json
import pprint

router = APIRouter(prefix="/chatbot")
settings = get_settings()

@router.post(
    "/ocr",
    tags = ["chatbot"],
    summary = "ask question about Harry Potter",
    response_model=ChatBotResponse
)
def chat_bot(
    file: UploadFile = File(None),
):
    upload_dir = "/src/static"  # Define your upload directory
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, "output.pdf")

    with open(file_path, "wb") as local_file:
        content = file.read()  # Read the uploaded file content
        local_file.write(content)  # Write the content to the local file
    
    # OCR pdf
    text_lines = process_document_ocr_sample(
        project_id=settings.GCP_PROJECT_ID,
        location="us",
        processor_id=settings.PROCESSOR_ID,
        processor_version=settings.PROCESSOR_VERSION_ID,
        file_path=file_path,
        mime_type="application/pdf",
    )

    # clean text
    cleaned_text_lines = clean_text(text_lines)

    # Embedding texts, and upload files to GCS
    # 4. Embedding texts, and upload files to GCS
    source_dir = f'src/static'
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
            page=id,
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

    # vector search
    text_embs = {}
    with open('src/static/output.json') as f:
        for l in f.readlines():
            p = json.loads(l)
            id = p['id']
            text_embs[id] = p['embedding']
    ids = [2, 4]
    if ids:
        queries = [text_embs[id] for id in ids]
    
    # 2. vector search
    search_results = vector_search_find_neighbors(
        project=settings.GCP_PROJECT_ID,
        location=settings.REGION,
        index_endpoint_name=settings.INDEX_ENDPOINT_NAME,
        deployed_index_id=settings.DEPLOYED_INDEX_ID,
        queries=queries,
        num_neighbors=3
    )
    pprint.pprint(search_results)
        
