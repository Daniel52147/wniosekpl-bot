from src import llm as llm_mod


def test_llm_status_without_keys(monkeypatch):
    monkeypatch.setattr(llm_mod, "OMNIROUTE_ENABLED", True)
    monkeypatch.setattr(llm_mod, "OMNIROUTE_API_KEY", "")
    monkeypatch.setattr(llm_mod, "OPENAI_API_KEY", "")
    monkeypatch.setattr(llm_mod, "GROQ_API_KEY", "")
    monkeypatch.setattr(llm_mod, "OPENROUTER_API_KEY", "")
    assert llm_mod.llm_configured() is False
    status = llm_mod.llm_status()
    assert status["configured"] is False
    assert status["fallback_chain"] == []


def test_omniroute_first_in_chain(monkeypatch):
    monkeypatch.setattr(llm_mod, "OMNIROUTE_ENABLED", True)
    monkeypatch.setattr(llm_mod, "OMNIROUTE_API_KEY", "omni-key")
    monkeypatch.setattr(llm_mod, "OMNIROUTE_BASE_URL", "http://127.0.0.1:20128/v1")
    monkeypatch.setattr(llm_mod, "OMNIROUTE_MODEL", "auto")
    monkeypatch.setattr(llm_mod, "OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(llm_mod, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(llm_mod, "OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(llm_mod, "GROQ_API_KEY", "gsk-test")
    monkeypatch.setattr(llm_mod, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(
        llm_mod,
        "LLM_FALLBACK_MODELS",
        {"groq": "llama-3.3-70b-versatile", "openrouter": "openrouter/free"},
    )
    chain = [ep.name for ep in llm_mod._endpoints()]
    assert chain[0] == "omniroute"
    assert "openai" in chain
    assert "groq" in chain


def test_complete_chat_falls_through(monkeypatch):
    import asyncio

    class FakeResp:
        def __init__(self, ok: bool, text: str = ""):
            self._ok = ok
            self._text = text

        def raise_for_status(self):
            if not self._ok:
                raise RuntimeError("fail")

        def json(self):
            return {"choices": [{"message": {"content": self._text}}]}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.calls = 0

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def post(self, url, headers=None, json=None):
            self.calls += 1
            if "20128" in url:
                return FakeResp(False)
            return FakeResp(True, "hello from groq")

    monkeypatch.setattr(llm_mod, "OMNIROUTE_ENABLED", True)
    monkeypatch.setattr(llm_mod, "OMNIROUTE_API_KEY", "omni")
    monkeypatch.setattr(llm_mod, "OMNIROUTE_BASE_URL", "http://127.0.0.1:20128/v1")
    monkeypatch.setattr(llm_mod, "OMNIROUTE_MODEL", "auto")
    monkeypatch.setattr(llm_mod, "OPENAI_API_KEY", "")
    monkeypatch.setattr(llm_mod, "GROQ_API_KEY", "gsk")
    monkeypatch.setattr(llm_mod, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(
        llm_mod,
        "LLM_FALLBACK_MODELS",
        {"groq": "llama-3.3-70b-versatile", "openrouter": "openrouter/free"},
    )
    monkeypatch.setattr(llm_mod.httpx, "AsyncClient", FakeClient)

    text = asyncio.run(llm_mod.complete_chat("sys", "user"))
    assert text == "hello from groq"
