from app.services.llm_provider import LLMProvider


class DeepSeekProvider(LLMProvider):

    def generate_response(self, message: str) -> str:
        return "Not implemented yet"
