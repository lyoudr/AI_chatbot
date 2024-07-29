import sys
sys.path.append("src")

import click # noqa E402

from services.gcs import CloudStorage # noqa E402
from services.embeddings import Embedding # noqa E402
from settings import get_settings


settings = get_settings()


@click.command()
def main():
    # 1. Embedding texts
    source_dir = 'src/static'
    texts = [
        "Art is a diverse range of human activities involving the creation of visual, auditory, or performed artifacts.",
        "These artifacts express the creator's imaginative or technical skill.",
        "They are intended to be appreciated for their beauty or emotional power.",
        "The oldest documented forms of art include visual arts.",
        "Visual arts encompass the creation of images or objects in fields including painting, sculpture, printmaking, photography, and other visual media.",
        "Architecture is often included as one of the visual arts.",
        "Like the decorative arts, it involves the creation of objects where the practical considerations of use are essential.",
        "Music, theatre, film, dance, and other performing arts are included in a broader definition of the arts.",
        "Literature and other media such as interactive media are also part of this broader definition.",
        "Until the 17th century, art referred to any skill or mastery.",
        "Art was not differentiated from crafts or sciences.",
        "In modern usage after the 17th century, aesthetic considerations are paramount.",
        "The fine arts are separated and distinguished from acquired skills in general.",
        "This includes the decorative or applied arts.",
        "Art may be characterized in terms of mimesis, expression, communication of emotion, or other qualities.",
        "During the Romantic period, art came to be seen as a special faculty of the human mind.",
        "It was classified with religion and science.",
        "The definition of what constitutes art is disputed and has changed over time.",
        "General descriptions center on the idea of imaginative or technical skill stemming from human agency and creation.",
        "Art at its simplest is a form of communication.",
        "It means whatever it is intended to mean by the artist."
    ]

    embed = Embedding(source_dir=source_dir)
    id = 1
    for sentence in texts:
        embeded_texts = embed.embed_text(
            [sentence],
            "RETRIEVAL_DOCUMENT",
            "text-embedding-004",
            100,
        )
        embed.embed_to_json(
            str(id),
            embeded_texts[0],
        )
        id += 1

    # 2. Upload to Cloud Storage
    gcs = CloudStorage(
        project_id=settings.GCP_PROJECT_ID,
        bucket_name=settings.GCS_BUCKET_NAME
    )
    gcs.upload_files(
        source_dir=source_dir
    )


if __name__ == '__main__':
    main()
