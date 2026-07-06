from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass
