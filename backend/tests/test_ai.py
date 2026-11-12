from unittest.mock import patch, MagicMock

from app.ai.gemini_client import analyze_aspects

FAKE_GEMINI_JSON = '{"overall": "Tích cực", "overall_comment": "Tốt", "highlightedText": [], "aspects": []}'


def _fake_response(json_text):
    fake_resp = MagicMock()
    fake_resp.raise_for_status.return_value = None
    fake_resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": json_text}]}}]
    }
    return fake_resp


def test_analyze_aspects_returns_parsed_json():
    with patch("app.ai.gemini_client.httpx.post") as mock_post:
        mock_post.return_value = _fake_response(FAKE_GEMINI_JSON)

        result = analyze_aspects("test text")

    assert result["overall"] == "Tích cực"
    assert result["overall_comment"] == "Tốt"


def test_analyze_aspects_raises_on_invalid_json():
    with patch("app.ai.gemini_client.httpx.post") as mock_post:
        mock_post.return_value = _fake_response("khong phai json")

        try:
            analyze_aspects("test")
            assert False, "Phải raise RuntimeError"
        except RuntimeError as e:
            assert "không hợp lệ" in str(e)