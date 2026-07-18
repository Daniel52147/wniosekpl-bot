(() => {
  const API = "";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";
  const DISMISS_KEY = "wniosekpl_tg_banner_dismissed";

  const copy = {
    pl: {
      needLogin: "Zaloguj się na stronie, potem wygeneruj kod i otwórz bota.",
      linked: "Połączono z Telegram — MOS, szkice, terminy i subskrypcja są wspólne.",
      notLinked: "Jeszcze nie połączono. Kod działa 15 minut.",
      generate: "Połącz z Telegram",
      unlink: "Odłącz",
      howto: "Albo w Telegram napisz: /link KOD",
      open: "Otwórz bota z kodem",
      bannerTitle: "Jeden postęp: strona + Telegram",
      bannerBody: "Połącz konta — checklista MOS, szkice PDF i terminy będą wspólne.",
      bannerCta: "Połącz Telegram",
      later: "Później",
    },
    ru: {
      needLogin: "Войди на сайте, затем сгенерируй код и открой бота.",
      linked: "Связано с Telegram — MOS, черновики, сроки и подписка общие.",
      notLinked: "Ещё не связано. Код действует 15 минут.",
      generate: "Связать с Telegram",
      unlink: "Отвязать",
      howto: "Или в Telegram: /link КОД",
      open: "Открыть бота с кодом",
      bannerTitle: "Один прогресс: сайт + Telegram",
      bannerBody: "Свяжи аккаунты — чеклист MOS, черновики PDF и сроки будут общими.",
      bannerCta: "Связать Telegram",
      later: "Позже",
    },
    en: {
      needLogin: "Log in on the site, then generate a code and open the bot.",
      linked: "Linked to Telegram — MOS, drafts, deadlines and subscription are shared.",
      notLinked: "Not linked yet. Code works for 15 minutes.",
      generate: "Link Telegram",
      unlink: "Unlink",
      howto: "Or in Telegram: /link CODE",
      open: "Open bot with code",
      bannerTitle: "One progress: website + Telegram",
      bannerBody: "Link accounts — MOS checklist, PDF drafts and deadlines stay shared.",
      bannerCta: "Link Telegram",
      later: "Later",
    },
    ua: {
      needLogin: "Увійди на сайті, потім згенеруй код і відкрий бота.",
      linked: "Повʼязано з Telegram — MOS, чернетки, строки і підписка спільні.",
      notLinked: "Ще не повʼязано. Код діє 15 хвилин.",
      generate: "Повʼязати Telegram",
      unlink: "Відʼєднати",
      howto: "Або в Telegram: /link КОД",
      open: "Відкрити бота з кодом",
      bannerTitle: "Один прогрес: сайт + Telegram",
      bannerBody: "Повʼяжи акаунти — чекліст MOS, чернетки PDF і строки будуть спільні.",
      bannerCta: "Повʼязати Telegram",
      later: "Пізніше",
    },
  };

  function lang() {
    return localStorage.getItem("wniosekpl_lang") || "pl";
  }
  function t() {
    return copy[lang()] || copy.pl;
  }
  function token() {
    return localStorage.getItem(TOKEN_KEY) || "";
  }
  function userId() {
    return Number(localStorage.getItem(USER_KEY) || 0) || undefined;
  }
  function headers(json = true) {
    const h = {};
    if (json) h["Content-Type"] = "application/json";
    if (token()) h.Authorization = `Bearer ${token()}`;
    return h;
  }
  function loggedIn() {
    return !!(token() || userId());
  }

  function goAccountAndGenerate() {
    if (window.wniosekplSetProfileTab) window.wniosekplSetProfileTab("account");
    else document.querySelector('[data-profile-tab="account"]')?.click();
    setTimeout(() => generateCode().catch(() => {}), 120);
  }

  async function refreshBanner(linked) {
    const banner = document.getElementById("tg-link-banner");
    if (!banner) return;
    const ui = t();
    const title = document.getElementById("tg-banner-title");
    const body = document.getElementById("tg-banner-body");
    const cta = document.getElementById("tg-banner-cta");
    const dismiss = document.getElementById("tg-banner-dismiss");
    if (title) title.textContent = ui.bannerTitle;
    if (body) body.textContent = ui.bannerBody;
    if (cta) cta.textContent = ui.bannerCta;
    if (dismiss) dismiss.textContent = ui.later;
    const dismissed = localStorage.getItem(DISMISS_KEY) === "1";
    const force = new URLSearchParams(location.search).get("link") === "1";
    banner.hidden = !!(linked || (dismissed && !force));
  }

  async function refreshStatus() {
    const statusEl = document.getElementById("tg-link-status");
    const codeWrap = document.getElementById("tg-link-code-wrap");
    const unlinkBtn = document.getElementById("tg-link-unlink");
    const genBtn = document.getElementById("tg-link-generate");
    const ui = t();
    if (genBtn) genBtn.textContent = ui.generate;
    if (unlinkBtn) unlinkBtn.textContent = ui.unlink;
    const howto = document.getElementById("tg-link-howto");
    if (howto) howto.textContent = ui.howto;
    const open = document.getElementById("tg-link-open");
    if (open) open.textContent = ui.open;

    if (!loggedIn()) {
      if (statusEl) statusEl.textContent = ui.needLogin;
      if (codeWrap) codeWrap.hidden = true;
      if (unlinkBtn) unlinkBtn.hidden = true;
      await refreshBanner(false);
      return;
    }
    try {
      const qs = userId() ? `?user_id=${userId()}` : "";
      const res = await fetch(`${API}/api/account/link${qs}`, { headers: headers(false) });
      if (!res.ok) throw new Error("status");
      const data = await res.json();
      if (data.linked) {
        if (statusEl) statusEl.textContent = ui.linked;
        if (codeWrap) codeWrap.hidden = true;
        if (unlinkBtn) unlinkBtn.hidden = false;
        localStorage.removeItem(DISMISS_KEY);
      } else {
        if (statusEl) statusEl.textContent = ui.notLinked;
        if (unlinkBtn) unlinkBtn.hidden = true;
      }
      await refreshBanner(!!data.linked);
    } catch (_) {
      if (statusEl) statusEl.textContent = ui.notLinked;
      await refreshBanner(false);
    }
  }

  async function generateCode() {
    const statusEl = document.getElementById("tg-link-status");
    const ui = t();
    if (!loggedIn()) {
      document.getElementById("btn-account-login")?.click() ||
        document.getElementById("btn-open-login")?.click();
      if (statusEl) statusEl.textContent = ui.needLogin;
      return;
    }
    const qs = userId() ? `?user_id=${userId()}` : "";
    const res = await fetch(`${API}/api/account/link-code${qs}`, {
      method: "POST",
      headers: headers(false),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (statusEl) statusEl.textContent = data.detail || "Error";
      return;
    }
    const codeWrap = document.getElementById("tg-link-code-wrap");
    const codeEl = document.getElementById("tg-link-code");
    const open = document.getElementById("tg-link-open");
    if (codeWrap) codeWrap.hidden = false;
    if (codeEl) codeEl.textContent = data.code || "";
    if (open) open.href = data.deep_link || "#";
    if (statusEl) statusEl.textContent = ui.notLinked;
  }

  async function unlink() {
    if (!loggedIn()) return;
    await fetch(`${API}/api/account/unlink`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ user_id: userId() }),
    });
    const codeWrap = document.getElementById("tg-link-code-wrap");
    if (codeWrap) codeWrap.hidden = true;
    await refreshStatus();
  }

  function wire() {
    document.getElementById("tg-link-generate")?.addEventListener("click", () => {
      generateCode().catch(() => {});
    });
    document.getElementById("tg-link-unlink")?.addEventListener("click", () => {
      unlink().catch(() => {});
    });
    document.getElementById("tg-banner-cta")?.addEventListener("click", () => {
      goAccountAndGenerate();
    });
    document.getElementById("tg-banner-dismiss")?.addEventListener("click", () => {
      localStorage.setItem(DISMISS_KEY, "1");
      const banner = document.getElementById("tg-link-banner");
      if (banner) banner.hidden = true;
    });

    const params = new URLSearchParams(location.search);
    if (params.get("tab") === "account" || params.get("link") === "1") {
      if (window.wniosekplSetProfileTab) window.wniosekplSetProfileTab("account");
      else document.querySelector('[data-profile-tab="account"]')?.click();
      if (params.get("link") === "1") {
        setTimeout(() => generateCode().catch(() => {}), 200);
      }
    }

    refreshStatus().catch(() => {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  window.wniosekplRefreshAccountLink = refreshStatus;
  window.wniosekplPromptTelegramLink = goAccountAndGenerate;
})();
