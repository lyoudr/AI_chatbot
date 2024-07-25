import sys
sys.path.append("src")

import json
from typing import List, Optional
from google.cloud import aiplatform
from vertexai.language_models import (
    TextEmbeddingInput,
    TextEmbeddingModel
)


class Embedding:
    def embed_text(
        self,
        texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?", "I like banana", "It's a great thing."],
        task: str = "RETRIEVAL_DOCUMENT",
        model_name: str = "text-embedding-004",
        dimensionality: Optional[int] = 100,
    ) -> List[List[float]]:
        """Embeds texts with a pre-trained, foundational model."""
        # Print the current project ID and location
        model = TextEmbeddingModel.from_pretrained(model_name)
        inputs = [TextEmbeddingInput(text, task) for text in texts]
        kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
        embeddings = model.get_embeddings(inputs, **kwargs)
        return [embedding.values for embedding in embeddings]

    def embed_to_json(
        self,
        texts: List[str],
        source_dir: str
    ):
        print("length is ->", len(texts))
        id, i, j = 1, 0, 512
        while i < len(texts):
            record = {"id": str(id), "embedding": texts[i:j]}
            file_name = f'{source_dir}/output_{id}.json'
            with open(file_name, 'w') as json_file:
                json.dump(record, json_file, separators=(',', ':'))
            id += 1
            i += 512
            j += 512
