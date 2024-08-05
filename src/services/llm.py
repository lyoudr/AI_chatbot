import vertexai

from vertexai.generative_models import GenerativeModel, Part

from settings import get_settings

settings = get_settings()


def llm(question: str, vertex_search_result: str) -> str:
    vertexai.init(
        project=settings.GCP_PROJECT_ID, 
        location="us-central1"
    )

    model = GenerativeModel("gemini-1.5-pro-001")
    prompt = f"{question} According to the search result: {vertex_search_result}"
    response = model.generate_content(prompt)
    res = response.candidates[0].content.parts[0].text
    res = res.replace('\n', ' ')
    return res