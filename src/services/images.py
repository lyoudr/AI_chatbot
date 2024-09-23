import sys 
sys.path.append("src")
import vertexai

from vertexai.generative_models import GenerativeModel, Part

from settings import get_settings

settings = get_settings()

# TODO(developer): Update project_id and location
vertexai.init(
    project=settings.GCP_PROJECT_ID,
    location=settings.REGION
)

# Load images from Cloud Storage URI
image_file1 = Part.from_uri(
    f"gs://{settings.GCS_BUCKET_NAME}/america.jpeg",
    mime_type="image/jpeg"
)
image_file2 = Part.from_uri(
    f"gs://{settings.GCS_BUCKET_NAME}/england.jpeg",
    mime_type="image/jpeg",
)
image_file3 = Part.from_uri(
    f"gs://{settings.GCS_BUCKET_NAME}/paris.jpeg",
    mime_type="image/jpeg",
)

def recognize_image():
    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content(
        [
            image_file1,
            "country: America, landmark: the Colosseum",
            image_file2,
            "country: England, landmark: Tours",
            image_file3,
        ]
    )
    print(response.text)

def recognize_single():
    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content([image_file1, "what is this image?"])
    print(response.text)

if __name__ == "__main__":
    # recognize_image()
    recognize_single()