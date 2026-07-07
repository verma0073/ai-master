from app.services.llm_provider import LLMProvider


class GeminiProvider(LLMProvider):

    def generate_response(self, message: str) -> str:
        return "Gemini Mock Response: Hello"
