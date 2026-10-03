from unittest.mock import patch, MagicMock

from app.ai.huggingface_client import analyze_sentiment


def test_analyze_sentiment_returns_label_and_score():
    fake_result = MagicMock(label="positive", score=0.987654)

    with patch("app.ai.huggingface_client.client.text_classification") as mock_call:
        mock_call.return_value = [fake_result]

        result = analyze_sentiment("I love this")

    assert result["label"] == "positive"
    assert result["score"] == 0.9877  # đã làm tròn 4 chữ số trong code thật


def test_analyze_sentiment_raises_runtime_error_on_api_failure():
    with patch("app.ai.huggingface_client.client.text_classification") as mock_call:
        mock_call.side_effect = Exception("API down")

        try:
            analyze_sentiment("test")
            assert False, "Phải raise RuntimeError"
        except RuntimeError as e:
            assert "Hugging Face API error" in str(e)