from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

MODEL=os.getenv("MODEL_ID")

def _build_llm():
    client=Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"),api_key=os.getenv("ANTHROPIC_API_KEY"))
    return client
