from huggingface_hub import InferenceClient
from app.core.config import settings

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

client = InferenceClient(
    token=settings.HF_API_TOKEN, 
    model=MODEL_NAME,
    provider="hf-inference",
)


def analyze_sentiment(text: str) -> dict:
    try:
        results = client.text_classification(text=text)
        top = results[0]
        return {"label": top.label, "score": round(top.score, 4)}
    except Exception as e:
        raise RuntimeError(f"Hugging Face API error: {e}")