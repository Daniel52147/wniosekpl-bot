from pathlib import Path

from src.keyboards import after_pdf_keyboard, ai_upgrade_keyboard, quick_keyboard, review_keyboard
from src.texts import t


def _button_texts(markup):
    return [button.text for row in markup.inline_keyboard for button in row]


def _callback_data(markup):
    return [button.callback_data for row in markup.inline_keyboard for button in row]


def test_review_offer_mentions_price_in_supported_languages():
    for lang in ("ru", "en", "ua", "pl"):
        assert "29 zł" in t("review_offer", lang)
        assert "29 zł" in t("review_btn", lang)


def test_review_entrypoints_are_visible_in_keyboards():
    assert t("review_btn", "en") in _button_texts(quick_keyboard("en"))
    assert t("review_btn", "en") in _button_texts(after_pdf_keyboard("en"))
    assert t("ai_ask_btn", "en") in _button_texts(quick_keyboard("en"))


def test_review_waitlist_keyboard_records_human_review_interest():
    callbacks = _callback_data(review_keyboard("en"))

    assert "waitlist:human_review" in callbacks


def test_ai_upgrade_keyboard_records_subscription_interest():
    callbacks = _callback_data(ai_upgrade_keyboard("en"))

    assert "waitlist:ai_subscription" in callbacks


def test_landing_exposes_paid_review_plan():
    root = Path(__file__).resolve().parent.parent / "landing"
    home = (root / "index.html").read_text(encoding="utf-8")
    app = (root / "app.html").read_text(encoding="utf-8")

    assert "29 zł" in home
    assert "19 zł" in home
    assert 'href="/profile"' in home
    assert "tg-status" in home
    assert "AI-asystent" in app
    assert "/api/assistant/ask" in app
    assert "/api/documents/" in app
    assert "Sprawdzenie przez człowieka" in app
