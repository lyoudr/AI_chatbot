import sys
sys.path.append("src")

import click
import json
import pprint
from typing import List

from services.vector import vector_search_find_neighbors
from services.embeddings import Embedding
from settings import get_settings

settings = get_settings()


@click.command()
@click.argument("input_text")
@click.argument("ids")
def main(input_text: str = None, ids: List[str] = []):
    if input_text:
        embed = Embedding()
        embeded_text = embed.embed_text(
            texts=[input_text],
            task="RETRIEVAL_DOCUMENT",
            model_name="text-embedding-004",
            dimensionality=100
        )
    else:
        # build dicts for ids
        text_embs = {}
        with open('src/static/output.json') as f:
            for l in f.readlines():
                p = json.loads(l)
                id = p['id']
                text_embs[id] = p['embedding']
    if ids:
        queries = [text_embs[id] for id in ids]
    else:
        queries = [embeded_text]
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


if __name__ == "__main__":
    main()
