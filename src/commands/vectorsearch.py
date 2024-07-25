import sys
sys.path.append("src")

import click

from services.vector import vector_search_find_neighbors
from services.embeddings import Embedding
from settings import get_settings

settings = get_settings()


@click.command()
def main():
    # 1. Eembedding search
    embed = Embedding()
    embeded_texts = embed.embed_text(
        ["banana"],
        "RETRIEVAL_DOCUMENT",
        "text-embedding-004",
        100,
    )
    print("embeded_texts is ->", embeded_texts)
    # 2. vector search
    search_results = vector_search_find_neighbors(
        project=settings.GCP_PROJECT_ID,
        location=settings.REGION,
        index_endpoint_name=settings.INDEX_ENDPOINT_NAME,
        deployed_index_id=settings.DEPLOYED_INDEX_ID,
        queries=embeded_texts,
        num_neighbors=2
    )
    print("search result is ->", search_results)


if __name__ == "__main__":
    main()