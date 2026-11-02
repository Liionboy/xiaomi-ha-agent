"""Xiaomi API client."""

import httpx
from typing import Optional, AsyncGenerator


class XiaomiClient:
    """Client for Xiaomi AI API (OpenAI-compatible)."""

    def __init__(
        self,
        api_key: str,
        api_base: str = "https://api.xiaomi.com/v1",
        model: str = "mimo-v2.6-pro",
    ):
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.client = httpx.AsyncClient(
            base_url=self.api_base,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def chat_completion(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> dict | AsyncGenerator[dict, None]:
        """Send chat completion request."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            payload["tools"] = tools

        if stream:
            payload["stream"] = True
            return self._stream_completion(payload)
        else:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            return response.json()

    async def _stream_completion(self, payload: dict) -> AsyncGenerator[dict, None]:
        """Stream chat completion response."""
        async with self.client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    yield data

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
