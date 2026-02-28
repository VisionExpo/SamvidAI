import os
from google import genai
from samvidai.llm.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """
    Gemini 2.5 Pro provider for legal reasoning
    """

    def __init__(self, model: str = "gemini-2.5-pro"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0.0,
                "top_p": 0.1,
                "max_output_tokens": 220,
            },
        )

        return (response.text or "").strip()
