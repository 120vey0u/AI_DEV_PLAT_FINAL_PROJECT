import json
import time

import httpx

from app.core.config import settings

MODEL_NAME = "gemini-3.5-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

SYSTEM_PROMPT = """Bạn là một hệ thống phân tích cảm xúc văn bản tiếng Việt.
Với đoạn văn người dùng cung cấp, hãy:
1. Tách đoạn văn thành các cụm, mỗi cụm gắn nhãn sentiment (positive/negative/neutral).
2. Xác định các khía cạnh (aspect) được nhắc tới trong đoạn văn (ví dụ: cảnh quan, âm thanh, dịch vụ...), mỗi khía cạnh có điểm số 0-100 và sentiment.
3. Đưa ra đánh giá tổng quan ngắn gọn (overall): "Tích cực", "Tiêu cực", hoặc "Đan xen".
4. Viết một đoạn nhận xét tổng kết (overall_comment) 2-3 câu, giải thích vì sao có đánh giá đó, dựa trên các khía cạnh đã phân tích.

CHỈ trả về đúng 1 JSON object, không thêm chữ nào khác, không dùng markdown code block, theo đúng cấu trúc:
{
  "overall": "...",
  "overall_comment": "...",
  "highlightedText": [{"text": "...", "sentiment": "..."}],
  "aspects": [{"name": "...", "score": 0, "sentiment": "..."}]
}"""


RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "overall": {"type": "STRING"},
        "overall_comment": {"type": "STRING"},
        "highlightedText": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "text": {"type": "STRING"},
                    "sentiment": {"type": "STRING"},
                },
                "required": ["text", "sentiment"],
            },
        },
        "aspects": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "score": {"type": "INTEGER"},
                    "sentiment": {"type": "STRING"},
                },
                "required": ["name", "score", "sentiment"],
            },
        },
    },
    "required": ["overall", "overall_comment", "highlightedText", "aspects"],
}


def _call_gemini(text: str) -> httpx.Response:
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    return httpx.post(
        API_URL,
        headers={
            "x-goog-api-key": settings.GEMINI_API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )


def analyze_aspects(text: str) -> dict:
    last_error = None

    for attempt in range(3):
        try:
            response = _call_gemini(text)
            response.raise_for_status()
            parts = response.json()["candidates"][0]["content"]["parts"]
            raw = "".join(p.get("text", "") for p in parts)
            return json.loads(raw)
        except httpx.HTTPStatusError as e:
            last_error = e
            if e.response.status_code in (503, 429) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(f"Gemini API error {e.response.status_code}: {e.response.text}")
        except httpx.HTTPError as e:
            raise RuntimeError(f"Không gọi được Gemini API: {e}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Gemini trả về dữ liệu không hợp lệ: {e}")

    raise RuntimeError(f"Gemini API error sau 3 lần thử: {last_error}")