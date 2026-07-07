from app.providers.deepseek_provider import DeepSeekProvider
from app.providers.gemini_provider import GeminiProvider

class ProviderFactory:

    @staticmethod
    def get_provider(provider_name: str):

        if provider_name == "gemini":
            return GeminiProvider()

        elif provider_name == "deepseek":
            return DeepSeekProvider()

        else:
            raise ValueError(f"Unknown provider: {provider_name}")
