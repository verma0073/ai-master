from google import genai

from app.core.config import get_settings
from app.core.exceptions import AIServiceError
from app.core.logger import logger
from app.providers.llm_provider import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self):
        settings = get_settings()

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = settings.GEMINI_MODEL

    def generate_response(self, message: str) -> str:

        logger.info(
            f"Calling Gemini model: {self.model_name}"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=message
            )

        except Exception as e:
            logger.exception(
                "Gemini API call failed"
            )

            raise AIServiceError(
                "Failed to generate AI response"
            ) from e

        logger.info(
            "Received response from Gemini"
        )

        return response.text
