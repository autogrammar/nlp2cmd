"""
OpenRouter API client for NLP2CMD.

Provides unified access to LLM models via OpenRouter with support for:
- Text completions
- Vision (image analysis)
- Structured JSON output
- Streaming responses

Environment:
    OPENROUTER_API_KEY — required for all API calls
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Optional

try:
    from subllm import available_routes, complete as subllm_complete
except ImportError:
    available_routes = None
    subllm_complete = None

_DEBUG = os.environ.get("NLP2CMD_DEBUG", "").lower() in ("1", "true", "yes")


def _debug(msg: str) -> None:
    if _DEBUG:
        print(f"DEBUG [OpenRouter] {msg}", file=sys.stderr, flush=True)


@dataclass
class LLMResponse:
    """Response from OpenRouter API."""
    content: str = ""
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    finish_reason: str = ""
    success: bool = True
    error: Optional[str] = None

    @property
    def tokens_used(self) -> int:
        return self.usage.get("total_tokens", 0)


class OpenRouterClient:
    """
    OpenRouter API client with text and vision support.

    Models:
    - google/gemini-2.5-pro-preview — best for vision/CAPTCHA
    - anthropic/claude-3.5-sonnet — best for complex planning
    - meta-llama/llama-3.1-70b-instruct — cost-effective text
    - qwen/qwen-2.5-coder-32b-instruct — code generation

    Usage:
        client = OpenRouterClient()
        resp = await client.complete("What is 2+2?")
        resp = await client.vision(image_b64, "What's in this image?")
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Recommended models for different tasks
    MODELS = {
        "vision": "google/gemini-2.5-pro-preview",
        "planning": "google/gemini-2.5-pro-preview",
        "code": "qwen/qwen-2.5-coder-32b-instruct",
        "fast": "meta-llama/llama-3.1-8b-instruct",
        "default": "google/gemini-2.5-pro-preview",
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Args:
            api_key: OpenRouter API key. Falls back to OPENROUTER_API_KEY env var.
            default_model: Default model for completions.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.default_model = default_model or self.MODELS["default"]
        self.timeout = timeout

    @property
    def is_configured(self) -> bool:
        """Check whether the central NLP2CMD route has a usable credential."""
        if available_routes is None:
            return False
        credentials = {"OPENROUTER_API_KEY": self.api_key} if self.api_key else None
        return bool(
            available_routes(
                "autogrammar-nlp2cmd", "generate", credentials=credentials
            )
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv(
                "OPENROUTER_APP_URL", "https://github.com/autogrammar/nlp2cmd"
            ),
            "X-OpenRouter-Title": os.getenv("OPENROUTER_APP_NAME", "NLP2CMD"),
        }

    async def complete(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.3,
        json_mode: bool = False,
    ) -> LLMResponse:
        """
        Text completion.

        Args:
            prompt: User message
            system: Optional system message
            model: Model override
            max_tokens: Maximum response tokens
            temperature: Sampling temperature
            json_mode: Request JSON-formatted response

        Returns:
            LLMResponse
        """
        if subllm_complete is None:
            return LLMResponse(success=False, error="subactor-subllm is not available")

        messages: list[dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        credentials = {"OPENROUTER_API_KEY": self.api_key} if self.api_key else None
        try:
            response = await asyncio.to_thread(
                subllm_complete,
                "autogrammar-nlp2cmd",
                "generate",
                messages,
                timeout_seconds=self.timeout,
                credentials=credentials,
            )
            return LLMResponse(
                content=response.content,
                model=response.model,
                usage=dict(response.usage),
                finish_reason=response.finish_reason,
            )
        except Exception as exc:
            return LLMResponse(success=False, error=f"SubLLM request failed: {exc}")

    async def vision(
        self,
        image_b64: str,
        prompt: str,
        *,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.1,
    ) -> LLMResponse:
        """
        Vision analysis — send image + text prompt.

        Args:
            image_b64: Base64-encoded PNG image
            prompt: Text prompt about the image
            system: Optional system message
            model: Model override (defaults to vision model)
            max_tokens: Maximum response tokens
            temperature: Sampling temperature

        Returns:
            LLMResponse
        """
        if subllm_complete is None:
            return LLMResponse(success=False, error="subactor-subllm is not available")
        if not self.api_key:
            return LLMResponse(success=False, error="OPENROUTER_API_KEY not set")

        messages: list[dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})

        messages.append({
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{image_b64}"
                }},
                {"type": "text", "text": prompt},
            ],
        })

        credentials = {"openrouter": self.api_key}
        try:
            response = await asyncio.to_thread(
                subllm_complete,
                "autogrammar-nlp2cmd",
                "vision",
                messages,
                timeout_seconds=self.timeout,
                credentials=credentials,
            )
            return LLMResponse(
                content=response.content,
                model=response.model,
                usage=dict(response.usage),
                finish_reason=response.finish_reason,
            )
        except Exception as exc:
            return LLMResponse(success=False, error=f"SubLLM vision request failed: {exc}")

    async def plan_actions(
        self,
        query: str,
        available_actions: Optional[list[str]] = None,
    ) -> LLMResponse:
        """
        Plan a sequence of actions for a complex command.

        Args:
            query: Natural language command to decompose
            available_actions: List of available action names

        Returns:
            LLMResponse with JSON action plan
        """
        system = (
            "You are an action planner for desktop/browser automation. "
            "Decompose the user's command into a JSON array of steps. "
            "Each step: {\"action\": \"...\", \"params\": {...}, \"description\": \"...\"}. "
            "Reply with ONLY valid JSON array, no explanation."
        )
        if available_actions:
            system += f"\nAvailable actions: {', '.join(available_actions)}"

        return await self.complete(
            query,
            system=system,
            max_tokens=2000,
            temperature=0.1,
            json_mode=True,
        )

    async def _request(self, body: dict[str, Any]) -> LLMResponse:
        """Execute API request."""
        try:
            import httpx

            _debug(f"Request: model={body.get('model')}, tokens={body.get('max_tokens')}")

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.BASE_URL,
                    headers=self._headers(),
                    json=body,
                    timeout=self.timeout,
                )

                if resp.status_code != 200:
                    error_text = resp.text[:300]
                    _debug(f"API error {resp.status_code}: {error_text}")
                    return LLMResponse(
                        success=False,
                        error=f"API error {resp.status_code}: {error_text}",
                    )

                data = resp.json()
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})

                return LLMResponse(
                    content=message.get("content", "").strip(),
                    model=data.get("model", body.get("model", "")),
                    usage=data.get("usage", {}),
                    finish_reason=choice.get("finish_reason", ""),
                    success=True,
                )

        except ImportError:
            return LLMResponse(
                success=False,
                error="httpx is required: pip install httpx",
            )
        except Exception as e:
            _debug(f"Request error: {e}")
            return LLMResponse(success=False, error=str(e))

    async def check_balance(self) -> dict[str, Any]:
        """Check OpenRouter account balance and usage."""
        if not self.api_key:
            return {"error": "OPENROUTER_API_KEY not set"}

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://openrouter.ai/api/v1/auth/key",
                    headers=self._headers(),
                    timeout=10,
                )
                if resp.status_code == 200:
                    return resp.json()
                return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}
