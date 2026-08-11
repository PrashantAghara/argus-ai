from config import get_configs
from langchain_groq import ChatGroq

_configs = get_configs()

MODEL = "openai/gpt-oss-120b"


def get_llm():
    return ChatGroq(model=MODEL, api_key=_configs.groq_api_key, temperature=0)
