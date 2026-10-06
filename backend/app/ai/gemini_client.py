import json

import httpx

from app.core.config import settings

MODEL_NAME = "gemini-3.5-flash"
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


def analyze_aspects(text: str) -> dict:
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }
    try:
        response = httpx.post(
            API_URL,
            headers={
                "x-goog-api-key": settings.GEMINI_API_KEY,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
        raw = "".join(p.get("text", "") for p in parts)
        return json.loads(raw)
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Gemini API error {e.response.status_code}: {e.response.text}")
    except httpx.HTTPError as e:
        raise RuntimeError(f"Không gọi được Gemini API: {e}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Gemini trả về dữ liệu không hợp lệ: {e}")