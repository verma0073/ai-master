class AIServiceError(Exception):
    """Raised when AI provider is unavailable."""
    pass


class ProviderConfigurationError(Exception):
    """Raised when provider configuration is invalid."""
    pass
