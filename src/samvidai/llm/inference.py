from samvidai.llm.providers.gemini_provider import GeminiProvider

_provider = None


def get_provider():
    global _provider
    if _provider is None:
        _provider = GeminiProvider()
    return _provider


def run_llm(prompt: str) -> str:
    """
    Unified LLM inference entrypoint (Gemini 2.5 Pro)
    """
    provider = get_provider()
    return provider.generate(prompt)
