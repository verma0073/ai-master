from app.core.config import get_settings
from app.providers.provider_factory import ProviderFactory

settings = get_settings()


class ChatService:

    def generate_response(self, message: str) -> str:

        print("DEFAULT_PROVIDER =", settings.DEFAULT_PROVIDER)


        provider = ProviderFactory.get_provider(
            settings.DEFAULT_PROVIDER
        )

        return provider.generate_response(message)
