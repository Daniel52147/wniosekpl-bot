(() => {
  const API = "";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";

  const copy = {
    pl: {
      needLogin: "Zaloguj się na stronie, potem wygeneruj kod i otwórz bota.",
      linked: "Połączono z Telegram — postęp MOS i szkice są wspólne.",
      notLinked: "Jeszcze nie połączono. Kod działa 15 minut.",
      generate: "Połącz z Telegram",
      unlink: "Odłącz",
      howto: "Albo w Telegram napisz: /link KOD",
      open: "Otwórz bota z kodem",
    },
    ru: {
      needLogin: "Войди на сайте, затем сгенерируй код и открой бота.",
      linked: "Связано с Telegram — прогресс MOS и черновики общие.",
      notLinked: "Ещё не связано. Код действует 15 минут.",
      generate: "Связать с Telegram",
      unlink: "Отвязать",
      howto: "Или в Telegram: /link КОД",
      open: "Открыть бота с кодом",
    },
    en: {
      needLogin: "Log in on the site, then generate a code and open the bot.",
      linked: "Linked to Telegram — MOS progress and drafts are shared.",
      notLinked: "Not linked yet. Code works for 15 minutes.",
      generate: "Link Telegram",
      unlink: "Unlink",
      howto: "Or in Telegram: /link CODE",
      open: "Open bot with code",
    },
    ua: {
      needLogin: "Увійди на сайті, потім згенеруй код і відкрий бота.",
      linked: "Повʼязано з Telegram — прогрес MOS і чернетки спільні.",
      notLinked: "Ще не повʼязано. Код діє 15 хвилин.",
      generate: "Повʼязати Telegram",
      unlink: "Відʼєднати",
      howto: "Або в Telegram: /link КОД",
      open: "Відкрити бота з кодом",
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

  async function refreshStatus() {
    const statusEl = document.getElementById("tg-link-status");
    const codeWrap = document.getElementById("tg-link-code-wrap");
    const unlinkBtn = document.getElementById("tg-link-unlink");
    const genBtn = document.getElementById("tg-link-generate");
    if (!statusEl) return;
    const ui = t();
    if (genBtn) genBtn.textContent = ui.generate;
    if (unlinkBtn) unlinkBtn.textContent = ui.unlink;
    const howto = document.getElementById("tg-link-howto");
    if (howto) howto.textContent = ui.howto;
    const open = document.getElementById("tg-link-open");
    if (open) open.textContent = ui.open;

    if (!loggedIn()) {
      statusEl.textContent = ui.needLogin;
      if (codeWrap) codeWrap.hidden = true;
      if (unlinkBtn) unlinkBtn.hidden = true;
      return;
    }
    try {
      const qs = userId() ? `?user_id=${userId()}` : "";
      const res = await fetch(`${API}/api/account/link${qs}`, { headers: headers(false) });
      if (!res.ok) throw new Error("status");
      const data = await res.json();
      if (data.linked) {
        statusEl.textContent = ui.linked;
        if (codeWrap) codeWrap.hidden = true;
        if (unlinkBtn) unlinkBtn.hidden = false;
      } else {
        statusEl.textContent = ui.notLinked;
        if (unlinkBtn) unlinkBtn.hidden = true;
      }
    } catch (_) {
      statusEl.textContent = ui.notLinked;
    }
  }

  async function generateCode() {
    const statusEl = document.getElementById("tg-link-status");
    const ui = t();
    if (!loggedIn()) {
      document.getElementById("btn-account-login")?.click();
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
    refreshStatus().catch(() => {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  window.wniosekplRefreshAccountLink = refreshStatus;
})();
