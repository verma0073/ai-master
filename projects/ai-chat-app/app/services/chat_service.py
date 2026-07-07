from app.services.provider_factory import ProviderFactory


class ChatService:

    def generate_response(self, message: str) -> str:

        provider = ProviderFactory.get_provider("gemini")

        return provider.generate_response(message)
