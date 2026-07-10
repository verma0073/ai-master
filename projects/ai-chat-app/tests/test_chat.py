from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

from app.core.exceptions import AIServiceError

client = TestClient(app)


@patch("app.api.route.chat_service.generate_response")
def test_chat_endpoint(mock_generate_response):

    mock_generate_response.return_value = "Mock AI Response"

    response = client.post(
        "/chat",
        json={
            "message": "hello"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Mock AI Response"
    }

@patch("app.api.route.chat_service.generate_response")
def test_chat_endpoint_ai_failure(mock_generate_response):

    mock_generate_response.side_effect = AIServiceError(
        "Failed to generate AI response"
    )

    response = client.post(
        "/chat",
        json={
            "message": "hello"
        }
    )

    assert response.status_code == 503

    assert response.json() == {
        "detail": "AI service unavailable"
    }
