import sys
sys.path.append("src")

from fastapi import APIRouter, File, UploadFile, Form

from settings import get_settings
from models.chatbot import (
    ChatBotResponse, 
    RAGLLMResponse,
    MultipleResponse,
    MultiTasksResponse
)
from models.request import (
    MultipleQuestionRequest,
    RAGLLMQuestionRequest
)
from services.ocr import (
    process_document_ocr_sample,
    clean_text
)
from services.gcs import CloudStorage
from services.embeddings import Embedding
from services.vector import vector_search_find_neighbors
from services.llm import llm
from services.cloud_tasks import create_http_task

import os
import pprint

router = APIRouter(prefix="/chatbot")
settings = get_settings()


@router.post(
    "/ocr-embedding",
    tags = ["chatbot"],
    summary = "ocr, embed text to cloud",
    response_model=ChatBotResponse
)
async def chat_bot(
    file: UploadFile = File(None),
):
    upload_dir = "/Users/annmac/Code/Ann/AI_chatbot/src/static"  # Define your upload directory
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, "output.pdf")

    with open(file_path, "wb") as local_file:
        content = await file.read()  # Read the uploaded file content
        local_file.write(content)  # Write the content to the local file
    
    # OCR pdf
    print("settings.GCP_PROJECT_ID is ->", settings.GCP_PROJECT_ID)
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
    return ChatBotResponse(status = 'Upload file to cloud storage successfully.')


@router.post(
    "/rag_llm",
    tags = ["chatbot"],
    summary = "ask question about uploaded file",
    response_model = RAGLLMResponse
)
async def vector_serach(
    question: RAGLLMQuestionRequest
):
    # Process the form data as needed
    # For demonstration, let's just return the question back
    
    # vector search
    embed = Embedding()
    embeded_text = embed.embed_text(
        texts=[question],
        task="RETRIEVAL_DOCUMENT",
        model_name="text-embedding-004",
        dimensionality=100
    )
    
    # 2. vector search
    search_results = vector_search_find_neighbors(
        project=settings.GCP_PROJECT_ID,
        location=settings.REGION,
        index_endpoint_name=settings.INDEX_ENDPOINT_NAME,
        deployed_index_id=settings.DEPLOYED_INDEX_ID,
        queries=[embeded_text],
        num_neighbors=3
    )
    pprint.pprint(search_results)
    
    search_results = "Adobe PDF is an ideal format \
    for electronic document distribution as it overcomes \
    the problems commonly encountered with electronic file sharing."
    
    # 3. LLM generate response 
    response = llm(
        question=question,
        vertex_search_result=search_results
    )
    return RAGLLMResponse(response=response)


@router.post(
    "/handle_multiple",
    tags = ["chatbot"],
    summary = "handle multiple tasks at one time",
    response_model = MultipleResponse
)
def handle_multiple_question(
    payload: MultipleQuestionRequest
):
    create_http_task(
        project=settings.GCP_PROJECT_ID,
        location=settings.REGION,
        queue='llm-question',
        url=f"{settings.SELF_HOST}/rag_llm",
        json_payload=payload.dict()
    )
    return MultiTasksResponse(status = 'ok')