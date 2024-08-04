import vertexai

from vertexai.generative_models import GenerativeModel, Part

from settings import get_settings

settings = get_settings()


def llm():
    vertexai.init(
        project="ann-project-390401", 
        location="us-central1"
    )

    model = GenerativeModel("gemini-1.5-pro-001")
    response = model.generate_content(
        "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
    )
    print(response.text)