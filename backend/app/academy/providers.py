"""Adapters chỉ nhận ngữ liệu đã duyệt, không nhận hồ sơ hoặc bài làm trẻ."""

from typing import Protocol

import httpx

from app.core.config import settings


class AIProvider(Protocol):
    def generate(self, approved_context: dict, template: str) -> str: ...


class SimulationProvider:
    def generate(self, approved_context: dict, template: str) -> str:
        return approved_context["approved_hint"]


class OllamaProvider:
    def generate(self, approved_context: dict, template: str) -> str:
        config = settings()
        for retry in range(2):
            try:
                response = httpx.post(
                    config.ai_ollama_url.rstrip("/") + "/api/chat",
                    json={
                        "model": config.ai_ollama_model,
                        "stream": False,
                        "messages": [
                            {"role": "system", "content": template},
                            {"role": "user", "content": str(approved_context)},
                        ],
                        "options": {"temperature": 0.2, "num_predict": 200},
                    },
                    timeout=8,
                    follow_redirects=False,
                )
                response.raise_for_status()
                return response.json()["message"]["content"]
            except (httpx.ConnectError, httpx.TimeoutException):
                if retry:
                    raise
        raise RuntimeError("Provider unavailable")


class ApprovedSVGProvider:
    """SVG từ mẫu đã duyệt, không giả vờ là mô hình tạo ảnh raster."""

    def generate(self, template: str, palette: int) -> bytes:
        from app.academy.media import scene, svg

        return svg(scene({"robot": 23, "poster": 25, "comic": 24}[template], palette % 4)).encode(
            "utf-8"
        )
