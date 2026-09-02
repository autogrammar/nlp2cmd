import asyncio

from nlp2cmd.llm import openrouter


def test_text_completion_uses_central_subllm(monkeypatch):
    captured = {}

    def fake_complete(application, function, messages, **kwargs):
        captured.update(application=application, function=function, messages=messages, kwargs=kwargs)
        return type(
            "Response",
            (),
            {"content": "done", "model": "glm-5.3", "usage": {}, "finish_reason": "stop"},
        )()

    monkeypatch.setattr(openrouter, "subllm_complete", fake_complete)
    response = asyncio.run(openrouter.OpenRouterClient(api_key="test-key").complete("plan"))

    assert response.content == "done"
    assert response.model == "glm-5.3"
    assert captured["application"] == "autogrammar-nlp2cmd"
    assert captured["function"] == "generate"


def test_vision_uses_central_subllm(monkeypatch):
    captured = {}

    def fake_complete(application, function, messages, **kwargs):
        captured.update(application=application, function=function, messages=messages, kwargs=kwargs)
        return type(
            "Response",
            (),
            {"content": "cat", "model": "z-ai/glm-4.5v", "usage": {}, "finish_reason": "stop"},
        )()

    monkeypatch.setattr(openrouter, "subllm_complete", fake_complete)
    response = asyncio.run(
        openrouter.OpenRouterClient(api_key="test-key").vision("aaa", "what is this?")
    )

    assert response.content == "cat"
    assert captured["application"] == "autogrammar-nlp2cmd"
    assert captured["function"] == "vision"
    assert captured["messages"][0]["content"][0]["type"] == "image_url"
    assert captured["kwargs"]["credentials"] == {"openrouter": "test-key"}
