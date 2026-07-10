from app.core.config import get_settings
from app.core.exceptions import AIServiceError
from app.core.logger import logger
from app.providers.provider_factory import ProviderFactory

settings = get_settings()


class ChatService:

    def generate_response(self, message: str) -> str:

        logger.info(
            f"Using provider: {settings.DEFAULT_PROVIDER}"
        )

        provider = ProviderFactory.get_provider(
            settings.DEFAULT_PROVIDER
        )

        try:
            return provider.generate_response(message)

        except AIServiceError:
            logger.exception(
                "AI service failed while generating response"
            )
            raise
