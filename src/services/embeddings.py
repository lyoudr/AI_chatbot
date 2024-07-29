import sys
import json
import os
import shutil
sys.path.append("src")

from typing import List, Optional # noqa E402
from vertexai.language_models import ( # noqa E402
    TextEmbeddingInput,
    TextEmbeddingModel
)


class Embedding:
    def __init__(self, source_dir: str = None):
        self.source_dir = source_dir

    def embed_text(
        self,
        texts: List[str],
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
        id: int,
        texts: List[str],
        page: int = None,
    ):
        record = {"id": str(id), "embedding": texts}
        file_name = f'{self.source_dir}/{page}.json'
        # Open the file in append mode and write the new record as a JSON string
        with open(file_name, 'a') as json_file:
            json_file.write(json.dumps(record, separators=(',', ':')) + '\n')

    def clear_dir(self):
        for file in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
