from unittest.mock import patch, MagicMock

from app.services.sentiment_service import process_text

FAKE_ANALYSIS = {
    "overall": "Tích cực",
    "overall_comment": "Tốt",
    "highlightedText": [],
    "aspects": [],
}


def test_process_text_calls_ai_and_db_correctly():
    fake_db = MagicMock()
    fake_row = MagicMock(id=1, input_text="hello", created_at="2026-10-06T00:00:00Z")

    with patch("app.services.sentiment_service.analyze_aspects") as mock_ai, \
         patch("app.services.sentiment_service.crud.create_analysis") as mock_crud:

        mock_ai.return_value = FAKE_ANALYSIS
        mock_crud.return_value = fake_row

        result = process_text(fake_db, "hello")

    mock_ai.assert_called_once_with("hello")
    mock_crud.assert_called_once_with(fake_db, input_text="hello", analysis_data=FAKE_ANALYSIS)
    assert result["id"] == 1
    assert result["analysis_data"] == FAKE_ANALYSIS
