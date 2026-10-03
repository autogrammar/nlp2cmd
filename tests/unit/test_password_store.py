"""Tests for password_store.py — multi-backend credential reader."""

import os
from unittest.mock import patch, MagicMock

import pytest

from nlp2cmd.automation.password_store import (
    Credential,
    EnvPasswordReader,
    SessionPasswordStore,
    FirefoxPasswordReader,
    KeePassXCReader,
    BitwardenReader,
)


# ── Credential matching ──────────────────────────────────────────

class TestCredentialMatching:
    def test_exact_hostname_match(self):
        c = Credential(url="https://openrouter.ai", hostname="openrouter.ai", username="u", password="p")
        assert c.matches_domain("openrouter.ai")

    def test_subdomain_match(self):
        c = Credential(url="https://console.anthropic.com", hostname="console.anthropic.com", username="u", password="p")
        assert c.matches_domain("anthropic.com")

    def test_partial_match(self):
        c = Credential(url="https://github.com/login", hostname="github.com", username="u", password="p")
        assert c.matches_domain("github")

    def test_no_match(self):
        c = Credential(url="https://github.com", hostname="github.com", username="u", password="p")
        assert not c.matches_domain("gitlab.com")

    def test_url_in_domain(self):
        c = Credential(url="https://auth.openai.com", hostname="auth.openai.com", username="u", password="p")
        assert c.matches_domain("openai")


# ── EnvPasswordReader ─────────────────────────────────────────────

class TestEnvPasswordReader:
    def test_reads_service_credentials(self):
        reader = EnvPasswordReader()
        with patch.dict(os.environ, {
            "OPENROUTER_EMAIL": "test@example.com",
            "OPENROUTER_PASSWORD": "secret123",
        }):
            cred = reader.get_credentials("openrouter.ai")
            assert cred is not None
            assert cred.username == "test@example.com"
            assert cred.password == "secret123"
            assert cred.source == "env"

    def test_reads_username_variant(self):
        reader = EnvPasswordReader()
        with patch.dict(os.environ, {
            "GITHUB_USERNAME": "myuser",
            "GITHUB_PASSWORD": "mypass",
        }):
            cred = reader.get_credentials("github.com")
            assert cred is not None
            assert cred.username == "myuser"

    def test_no_credentials_returns_none(self):
        reader = EnvPasswordReader()
        with patch.dict(os.environ, {}, clear=True):
            cred = reader.get_credentials("unknown-service.com")
            assert cred is None

    def test_huggingface_hf_prefix(self):
        reader = EnvPasswordReader()
        with patch.dict(os.environ, {
            "HF_EMAIL": "hf@example.com",
            "HF_PASSWORD": "hfpass",
        }):
            cred = reader.get_credentials("huggingface.co")
            assert cred is not None
            assert cred.username == "hf@example.com"


# ── KeePassXCReader ───────────────────────────────────────────────

class TestKeePassXCReader:
    def test_not_available_without_db(self):
        reader = KeePassXCReader(db_path="")
        assert not reader.available()

    def test_not_available_without_cli(self):
        with patch("shutil.which", return_value=None):
            reader = KeePassXCReader(db_path="/tmp/test.kdbx")
            assert not reader.available()

    def test_returns_empty_when_unavailable(self):
        reader = KeePassXCReader(db_path="")
        assert reader.read_passwords() == []
        assert reader.search("github.com") == []


# ── BitwardenReader ───────────────────────────────────────────────

class TestBitwardenReader:
    def test_not_available_without_session(self):
        reader = BitwardenReader(session="")
        assert not reader.available()

    def test_not_available_without_cli(self):
        with patch("shutil.which", return_value=None):
            reader = BitwardenReader(session="test-session")
            assert not reader.available()

    def test_returns_empty_when_unavailable(self):
        reader = BitwardenReader(session="")
        assert reader.search("github.com") == []


# ── SessionPasswordStore ──────────────────────────────────────────

class TestSessionPasswordStore:
    def test_env_backend_always_available(self):
        store = SessionPasswordStore(backend="env")
        backends = store.list_backends()
        assert backends["env"] is True

    def test_get_credentials_from_env(self):
        store = SessionPasswordStore(backend="env")
        with patch.dict(os.environ, {
            "GITHUB_EMAIL": "test@gh.com",
            "GITHUB_PASSWORD": "ghpass",
        }):
            cred = store.get_credentials("github.com")
            assert cred is not None
            assert cred.username == "test@gh.com"
            assert cred.source == "env"

    def test_no_credentials_returns_none(self):
        store = SessionPasswordStore(backend="env")
        with patch.dict(os.environ, {}, clear=True):
            cred = store.get_credentials("nonexistent-service.xyz")
            assert cred is None

    def test_cached_count(self):
        store = SessionPasswordStore(backend="env")
        assert store.cached_count == 0

    def test_diagnose_providers_returns_list(self):
        store = SessionPasswordStore(backend="env")
        results = store.diagnose_providers()
        assert isinstance(results, list)
        assert len(results) > 0
        for r in results:
            assert "service" in r
            assert "has_api_key" in r
            assert "has_login" in r
            assert "can_auto_login" in r

    def test_diagnose_providers_with_custom_providers(self):
        store = SessionPasswordStore(backend="env")
        custom = {
            "test_svc": {
                "base_url": "https://test.example.com",
                "keys_url": "https://test.example.com/keys",
                "env_var": "TEST_API_KEY",
            }
        }
        results = store.diagnose_providers(providers=custom)
        assert len(results) == 1
        assert results[0]["service"] == "test_svc"

    def test_get_all_for_domain(self):
        store = SessionPasswordStore(backend="env")
        with patch.dict(os.environ, {
            "OPENAI_EMAIL": "ai@test.com",
            "OPENAI_PASSWORD": "aipass",
        }):
            results = store.get_all_for_domain("openai.com")
            assert len(results) >= 1
            assert any(c.username == "ai@test.com" for c in results)


# ── FirefoxPasswordReader (mocked NSS) ────────────────────────────

class TestFirefoxPasswordReader:
    def test_no_profile_returns_empty(self):
        reader = FirefoxPasswordReader(profile_path=None)
        with patch.object(reader, "_find_profile", return_value=None):
            assert reader.read_passwords() == []

    def test_no_logins_json_returns_empty(self, tmp_path):
        reader = FirefoxPasswordReader(profile_path=tmp_path)
        # No logins.json in tmp_path
        assert reader.read_passwords() == []


# ── Integration: provider scenarios ───────────────────────────────

class TestProviderScenarios:
    """Test realistic scenarios for different API providers."""

    def _make_store_with_firefox_creds(self, creds: list[Credential]) -> SessionPasswordStore:
        """Create a store pre-loaded with mock Firefox credentials."""
        store = SessionPasswordStore(backend="env")
        store._all_loaded = True
        for c in creds:
            key = f"{c.hostname}:{c.username}".lower()
            store._cache[key] = c
        return store

    def test_scenario_openrouter_full(self):
        """OpenRouter: API key in env + Firefox login → fully automated."""
        creds = [Credential("https://openrouter.ai", "openrouter.ai", "user@test.com", "pass123", "firefox")]
        store = self._make_store_with_firefox_creds(creds)

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-or-v1-abc123"}):
            results = store.diagnose_providers()
            or_result = next(r for r in results if r["service"] == "openrouter")
            assert or_result["has_api_key"] is True
            assert or_result["has_login"] is True
            assert or_result["can_extract_key"] is True
            assert or_result["can_auto_login"] is True

    def test_scenario_github_login_only(self):
        """GitHub: Firefox login only, no API key → can auto-login to create token."""
        creds = [Credential("https://github.com", "github.com", "myuser", "mypass", "firefox")]
        store = self._make_store_with_firefox_creds(creds)

        with patch.dict(os.environ, {}, clear=True), patch("dotenv.load_dotenv"):
            cred = store.get_credentials("github.com")
            assert cred is not None
            assert cred.username == "myuser"
            assert cred.source == "firefox"

            results = store.diagnose_providers()
            gh = next(r for r in results if r["service"] == "github")
            assert gh["has_api_key"] is False
            assert gh["has_login"] is True
            assert gh["can_auto_login"] is True

    def test_scenario_anthropic_no_creds(self):
        """Anthropic: no credentials anywhere → manual login required."""
        store = self._make_store_with_firefox_creds([])

        with patch.dict(os.environ, {}, clear=True), patch("dotenv.load_dotenv"):
            cred = store.get_credentials("anthropic.com")
            assert cred is None

            results = store.diagnose_providers()
            anth = next(r for r in results if r["service"] == "anthropic")
            assert anth["has_api_key"] is False
            assert anth["has_login"] is False
            assert anth["can_auto_login"] is False

    def test_scenario_openai_env_password(self):
        """OpenAI: credentials set via environment variables."""
        store = SessionPasswordStore(backend="env")
        store._all_loaded = True

        with patch.dict(os.environ, {
            "OPENAI_EMAIL": "user@openai.test",
            "OPENAI_PASSWORD": "openai-pass",
            "OPENAI_API_KEY": "sk-test123",
        }):
            cred = store.get_credentials("openai.com")
            assert cred is not None
            assert cred.username == "user@openai.test"
            assert cred.source == "env"

            results = store.diagnose_providers()
            oai = next(r for r in results if r["service"] == "openai")
            assert oai["has_api_key"] is True
            assert oai["has_login"] is True

    def test_scenario_huggingface_token_only(self):
        """HuggingFace: only API token in env, no login credentials."""
        store = SessionPasswordStore(backend="env")
        store._all_loaded = True

        with patch.dict(os.environ, {"HF_TOKEN": "hf_abc123456789"}, clear=True):
            results = store.diagnose_providers()
            hf = next(r for r in results if r["service"] == "huggingface")
            assert hf["has_api_key"] is True
            assert hf["has_login"] is False
            assert hf["can_extract_key"] is True
            assert hf["can_auto_login"] is False

    def test_scenario_multiple_firefox_creds_for_same_domain(self):
        """Multiple Firefox accounts for same domain → first match returned."""
        creds = [
            Credential("https://github.com", "github.com", "work-account", "work-pass", "firefox"),
            Credential("https://github.com", "github.com", "personal", "personal-pass", "firefox"),
        ]
        store = self._make_store_with_firefox_creds(creds)

        all_creds = store.get_all_for_domain("github.com")
        assert len(all_creds) >= 2

    def test_scenario_env_overrides_firefox(self):
        """Environment credentials take priority over Firefox."""
        creds = [Credential("https://github.com", "github.com", "firefox-user", "ff-pass", "firefox")]
        store = self._make_store_with_firefox_creds(creds)

        with patch.dict(os.environ, {
            "GITHUB_EMAIL": "env-user@test.com",
            "GITHUB_PASSWORD": "env-pass",
        }):
            cred = store.get_credentials("github.com")
            assert cred is not None
            assert cred.source == "env"
            assert cred.username == "env-user@test.com"
