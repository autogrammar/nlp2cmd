"""
Tests for the automation package: MouseController, EnvExtractor, CaptchaSolver, ComplexPlanner.
"""

import json
import math
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ── MouseController tests ────────────────────────────────────────────


class TestMouseControllerPoint:
    """Test Point dataclass operations."""

    def test_point_creation(self):
        from nlp2cmd.automation.mouse_controller import Point
        p = Point(100, 200)
        assert p.x == 100
        assert p.y == 200

    def test_point_add(self):
        from nlp2cmd.automation.mouse_controller import Point
        a = Point(10, 20)
        b = Point(30, 40)
        c = a + b
        assert c.x == 40
        assert c.y == 60

    def test_point_sub(self):
        from nlp2cmd.automation.mouse_controller import Point
        a = Point(50, 60)
        b = Point(10, 20)
        c = a - b
        assert c.x == 40
        assert c.y == 40

    def test_point_mul(self):
        from nlp2cmd.automation.mouse_controller import Point
        p = Point(10, 20) * 3
        assert p.x == 30
        assert p.y == 60

    def test_point_distance(self):
        from nlp2cmd.automation.mouse_controller import Point
        a = Point(0, 0)
        b = Point(3, 4)
        assert a.distance_to(b) == 5.0


class TestMouseControllerBezier:
    """Test Bézier curve computation."""

    def test_bezier_linear(self):
        from nlp2cmd.automation.mouse_controller import MouseController, Point
        mc = MouseController(page=MagicMock(), human_like=False)
        pts = mc._compute_bezier([Point(0, 0), Point(100, 100)], steps=10)
        assert len(pts) == 11
        assert abs(pts[0].x) < 0.01
        assert abs(pts[-1].x - 100) < 0.01

    def test_bezier_quadratic(self):
        from nlp2cmd.automation.mouse_controller import MouseController, Point
        mc = MouseController(page=MagicMock(), human_like=False)
        pts = mc._compute_bezier(
            [Point(0, 0), Point(50, 100), Point(100, 0)], steps=20
        )
        assert len(pts) == 21
        # Midpoint should be elevated
        mid = pts[10]
        assert mid.y > 0


# ── EnvExtractor tests ───────────────────────────────────────────────


class TestEnvExtractor:
    """Test EnvExtractor service detection and env path extraction."""

    def test_detect_service_openrouter(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_service("wyciągnij klucz z OpenRouter") == "openrouter"

    def test_detect_service_anthropic(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_service("get Claude API key") == "anthropic"

    def test_detect_service_github(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_service("extract github token") == "github"

    def test_detect_service_none(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_service("something random") is None

    def test_detect_env_path_explicit(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_env_path("zapisz do pliku .env.local") == ".env.local"

    def test_detect_env_path_default(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        assert EnvExtractor.detect_env_path("no path here") == ".env"

    def test_list_services(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        extractor = EnvExtractor()
        services = extractor.list_services()
        assert "openrouter" in services
        assert "anthropic" in services
        assert "openai" in services

    def test_mask_key_long(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        masked = EnvExtractor._mask_key("sk-or-v1-abcdef1234567890abcdef1234567890")
        assert masked.startswith("sk-or-v1")
        assert "…" in masked
        assert len(masked) < len("sk-or-v1-abcdef1234567890abcdef1234567890")

    def test_mask_key_short(self):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        masked = EnvExtractor._mask_key("sk-short")
        assert "…" in masked

    def test_save_to_env_creates_file(self, tmp_path):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        env_file = tmp_path / ".env"
        EnvExtractor._save_to_env("test-key-123", "MY_API_KEY", str(env_file))
        content = env_file.read_text()
        assert "MY_API_KEY=test-key-123" in content

    def test_save_to_env_updates_existing(self, tmp_path):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        env_file = tmp_path / ".env"
        env_file.write_text("MY_API_KEY=old-value\nOTHER=keep\n")
        EnvExtractor._save_to_env("new-value", "MY_API_KEY", str(env_file))
        content = env_file.read_text()
        assert "MY_API_KEY=new-value" in content
        assert "OTHER=keep" in content
        assert "old-value" not in content

    def test_save_to_env_appends_new(self, tmp_path):
        from nlp2cmd.automation.env_extractor import EnvExtractor
        env_file = tmp_path / ".env"
        env_file.write_text("EXISTING=value\n")
        EnvExtractor._save_to_env("new-key", "NEW_VAR", str(env_file))
        content = env_file.read_text()
        assert "EXISTING=value" in content
        assert "NEW_VAR=new-key" in content


# ── ComplexCommandPlanner tests ──────────────────────────────────────


class TestComplexPlanner:
    """Test ComplexCommandPlanner template matching."""

    def test_match_ladybug(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("narysuj biedronkę na jspaint.app")
        assert plan is not None
        assert plan.source == "template"
        assert len(plan.steps) > 5
        actions = [s.action for s in plan.steps]
        assert "navigate" in actions

    def test_match_circle(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("narysuj okrąg")
        assert plan is not None
        assert any(s.action == "draw_circle" for s in plan.steps)

    def test_match_rectangle(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("narysuj prostokąt")
        assert plan is not None
        assert any(s.action == "draw_rectangle" for s in plan.steps)

    def test_match_check_email(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("sprawdz poczte w Thunderbird")
        assert plan is not None
        assert any(s.action == "launch_app" for s in plan.steps)

    def test_match_minimize_all(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("zminimalizuj wszystko")
        assert plan is not None

    def test_match_screenshot(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("zrób screenshot ekranu")
        assert plan is not None

    def test_no_match_returns_none(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        planner = ComplexCommandPlanner()
        plan = planner._match_template("completely unrelated query about databases")
        assert plan is None

    def test_extract_color(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        assert ComplexCommandPlanner._extract_color("czerwone koło") == "#FF0000"
        assert ComplexCommandPlanner._extract_color("blue circle") == "#0000FF"
        assert ComplexCommandPlanner._extract_color("#FFA500") == "#FFA500"
        assert ComplexCommandPlanner._extract_color("no color here") is None

    def test_extract_url(self):
        from nlp2cmd.automation.complex_planner import ComplexCommandPlanner
        assert ComplexCommandPlanner._extract_url("go to https://jspaint.app") == "https://jspaint.app"
        assert ComplexCommandPlanner._extract_url("open jspaint.app") == "https://jspaint.app"
        assert ComplexCommandPlanner._extract_url("no url here") is None

    def test_action_step_to_dict(self):
        from nlp2cmd.automation.complex_planner import ActionStep
        step = ActionStep("navigate", {"url": "https://jspaint.app"}, "Open JSPaint", 3000)
        d = step.to_dict()
        assert d["action"] == "navigate"
        assert d["params"]["url"] == "https://jspaint.app"
        assert d["description"] == "Open JSPaint"
        assert d["wait_after_ms"] == 3000

    def test_execution_plan_to_dict(self):
        from nlp2cmd.automation.complex_planner import ExecutionPlan, ActionStep
        plan = ExecutionPlan(
            query="test",
            steps=[ActionStep("navigate", {"url": "https://example.com"})],
            source="template",
        )
        d = plan.to_dict()
        assert d["query"] == "test"
        assert len(d["steps"]) == 1
        assert d["source"] == "template"


# ── CaptchaSolver tests ──────────────────────────────────────────────


class TestCaptchaSolver:
    """Test CaptchaSolver initialization and config."""

    def test_init_defaults(self):
        from nlp2cmd.automation.captcha_solver import CaptchaSolver
        solver = CaptchaSolver()
        assert solver.model == "google/gemini-2.5-pro-preview"

    def test_init_custom_model(self):
        from nlp2cmd.automation.captcha_solver import CaptchaSolver
        solver = CaptchaSolver(model="anthropic/claude-3.5-sonnet")
        assert solver.model == "anthropic/claude-3.5-sonnet"

    def test_solve_without_api_key(self):
        """Solve should fail gracefully without API key."""
        from nlp2cmd.automation.captcha_solver import CaptchaSolver, CaptchaInfo
        solver = CaptchaSolver(api_key=None)
        solver.api_key = None  # force no key

        import asyncio
        info = CaptchaInfo(captcha_type="image_captcha", element=MagicMock())
        result = asyncio.get_event_loop().run_until_complete(
            solver.solve(MagicMock(), info)
        )
        assert result["success"] is False
        assert "OPENROUTER_API_KEY" in result.get("error", "")


# ── CanvasAdapter tests ──────────────────────────────────────────────


class TestCanvasAdapter:
    """Test CanvasAdapter NL → drawing plan generation."""

    def test_generate_ladybug(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        plan = {"text": "narysuj biedronkę na jspaint.app", "confidence": 0.8}
        result = adapter.generate(plan)
        data = json.loads(result)
        assert data["dsl"] == "canvas_dql.v1"
        assert data["app"] == "jspaint"
        assert len(data["steps"]) > 10  # ladybug has many steps

    def test_generate_circle(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        plan = {"text": "narysuj koło", "confidence": 0.8}
        result = adapter.generate(plan)
        data = json.loads(result)
        assert data["dsl"] == "canvas_dql.v1"
        steps = [s["action"] for s in data["steps"]]
        assert "draw_circle" in steps or "draw_filled_circle" in steps

    def test_generate_rectangle(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        plan = {"text": "draw a rectangle", "confidence": 0.8}
        result = adapter.generate(plan)
        data = json.loads(result)
        steps = [s["action"] for s in data["steps"]]
        assert "draw_rectangle" in steps

    def test_extract_colors(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        colors = adapter._extract_colors("czerwone koło z niebieskim tłem")
        assert "#FF0000" in colors
        assert "#0000FF" in colors

    def test_extract_shapes(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        shapes = adapter._extract_shapes("narysuj koło i prostokąt")
        assert "circle" in shapes
        assert "rectangle" in shapes

    def test_validate_syntax_valid(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        cmd = json.dumps({"dsl": "canvas_dql.v1", "steps": [{"action": "draw_circle"}]})
        result = adapter.validate_syntax(cmd)
        assert result["valid"] is True

    def test_validate_syntax_invalid(self):
        from nlp2cmd.adapters.canvas import CanvasAdapter
        adapter = CanvasAdapter()
        result = adapter.validate_syntax("not json")
        assert result["valid"] is False


# ── DesktopAdapter extended tests ────────────────────────────────────


class TestDesktopAdapterExtended:
    """Test extended DesktopAdapter with new intents."""

    def test_detect_new_tab_intent(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        intent, conf = adapter.detect_intent("nowy tab")
        assert intent == "new_tab"
        assert conf > 0

    def test_detect_email_check_intent(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        intent, conf = adapter.detect_intent("sprawdź pocztę")
        assert intent == "email_check"

    def test_detect_minimize_all(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        intent, conf = adapter.detect_intent("zminimalizuj wszystko")
        assert intent == "minimize_all"

    def test_generate_open_app(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        result = adapter.generate({"text": "otwórz firefox", "intent": "open_app"})
        data = json.loads(result)
        assert data["dsl"] == "desktop_dql.v1"
        actions = [a["action"] for a in data["actions"]]
        assert "type" in actions or "shell" in actions

    def test_generate_new_tab_with_url(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        result = adapter.generate({"text": "nowy tab https://github.com", "intent": "new_tab"})
        data = json.loads(result)
        actions = data["actions"]
        assert any(a.get("text") == "https://github.com" for a in actions)

    def test_generate_email_compose(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        result = adapter.generate({
            "text": "napisz maila do jan@test.com z tematem 'Raport'",
            "intent": "email_compose",
            "entities": {},
        })
        data = json.loads(result)
        actions = data["actions"]
        # Should contain keyboard shortcut for compose + type recipient
        assert any(a.get("keys") == "ctrl+n" for a in actions)

    def test_known_apps_expanded(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        assert "thunderbird" in adapter.KNOWN_APPS
        assert "vscode" in adapter.KNOWN_APPS
        assert "libreoffice writer" in adapter.KNOWN_APPS
        assert "gimp" in adapter.KNOWN_APPS

    def test_email_shortcuts(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        tb = adapter.EMAIL_SHORTCUTS["thunderbird"]
        assert "check_mail" in tb
        assert "new_message" in tb
        assert "reply" in tb

    def test_extract_url(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        assert DesktopAdapter._extract_url("go to https://github.com") == "https://github.com"
        assert DesktopAdapter._extract_url("open github.com") == "https://github.com"

    def test_extract_email_address(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        assert DesktopAdapter._extract_email_address("mail to jan@test.com") == "jan@test.com"
        assert DesktopAdapter._extract_email_address("no email here") is None

    def test_build_xdotool_chain(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        actions = [
            {"action": "type", "text": "hello", "delay": 30},
            {"action": "key", "key": "Return"},
        ]
        chain = DesktopAdapter.build_xdotool_chain(actions)
        assert "xdotool type" in chain
        assert "xdotool key" in chain

    def test_desktop_action_dataclass(self):
        from nlp2cmd.adapters.desktop import DesktopAction
        action = DesktopAction(app="firefox", action="launch", params={"url": "https://github.com"})
        assert action.app == "firefox"
        assert action.action == "launch"
        assert action.params["url"] == "https://github.com"

    def test_build_wmctrl_command(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter, DesktopAction
        action = DesktopAction(app="Firefox", action="focus")
        cmd = DesktopAdapter.build_wmctrl_command(action)
        assert "wmctrl -a" in cmd
        assert "Firefox" in cmd

    def test_get_supported_intents(self):
        from nlp2cmd.adapters.desktop import DesktopAdapter
        adapter = DesktopAdapter()
        intents = adapter.get_supported_intents()
        assert "open_app" in intents
        assert "new_tab" in intents
        assert "email_check" in intents
        assert "email_compose" in intents
        assert "minimize_all" in intents


# ── LLM/OpenRouter tests ────────────────────────────────────────────


class TestOpenRouterClient:
    """Test OpenRouterClient configuration."""

    def test_init_defaults(self):
        from nlp2cmd.llm.openrouter import OpenRouterClient
        client = OpenRouterClient()
        assert client.default_model == "google/gemini-2.5-pro-preview"
        assert client.timeout == 30

    def test_is_configured_false(self):
        from nlp2cmd.llm.openrouter import OpenRouterClient
        client = OpenRouterClient(api_key=None)
        client.api_key = None
        assert client.is_configured is False

    def test_is_configured_true(self, monkeypatch):
        from nlp2cmd.llm import openrouter as or_mod
        from nlp2cmd.llm.openrouter import OpenRouterClient

        monkeypatch.setattr(or_mod, "available_routes", lambda *args, **kwargs: True)
        client = OpenRouterClient(api_key="test-key")
        assert client.is_configured is True

    def test_models_dict(self):
        from nlp2cmd.llm.openrouter import OpenRouterClient
        assert "vision" in OpenRouterClient.MODELS
        assert "planning" in OpenRouterClient.MODELS
        assert "code" in OpenRouterClient.MODELS

    def test_llm_response_dataclass(self):
        from nlp2cmd.llm.openrouter import LLMResponse
        resp = LLMResponse(content="hello", model="test", usage={"total_tokens": 42})
        assert resp.tokens_used == 42
        assert resp.success is True


# ── Desktop templates tests ──────────────────────────────────────────


class TestDesktopTemplates:
    """Test desktop templates exist and are valid."""

    def test_templates_loaded(self):
        from nlp2cmd.generation.templates.desktop_templates import DESKTOP_TEMPLATES
        assert isinstance(DESKTOP_TEMPLATES, dict)
        assert len(DESKTOP_TEMPLATES) > 50

    def test_key_templates_exist(self):
        from nlp2cmd.generation.templates.desktop_templates import DESKTOP_TEMPLATES
        assert "launch_browser" in DESKTOP_TEMPLATES
        assert "email_check" in DESKTOP_TEMPLATES
        assert "minimize_all" in DESKTOP_TEMPLATES
        assert "new_tab" in DESKTOP_TEMPLATES
        assert "screenshot_full" in DESKTOP_TEMPLATES
        assert "type_text" in DESKTOP_TEMPLATES

    def test_templates_in_package_init(self):
        from nlp2cmd.generation.templates import DESKTOP_TEMPLATES
        assert isinstance(DESKTOP_TEMPLATES, dict)
