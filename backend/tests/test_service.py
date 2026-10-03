from unittest.mock import patch, MagicMock

from app.services.sentiment_service import process_text


def test_process_text_calls_ai_and_db_correctly():
    fake_db = MagicMock()
    fake_row = MagicMock(id=1, input_text="hello", sentiment_result="positive")

    with patch("app.services.sentiment_service.analyze_sentiment") as mock_ai, \
         patch("app.services.sentiment_service.crud.create_history") as mock_crud:

        mock_ai.return_value = {"label": "positive", "score": 0.95}
        mock_crud.return_value = fake_row

        result = process_text(fake_db, "hello")

    mock_ai.assert_called_once_with("hello")
    mock_crud.assert_called_once_with(fake_db, input_text="hello", sentiment_result="positive")
    assert result == {"id": 1, "text": "hello", "label": "positive", "score": 0.95}