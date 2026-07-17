(() => {
  const API = "";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";

  const token = () => localStorage.getItem(TOKEN_KEY) || "";
  const userId = () => Number(localStorage.getItem(USER_KEY) || 0);

  function saveSession(session, user) {
    if (session?.token) localStorage.setItem(TOKEN_KEY, session.token);
    const id = user?.user_id || session?.user_id;
    if (id) localStorage.setItem(USER_KEY, String(id));
  }

  function headers(json = true) {
    const h = {};
    if (json) h["Content-Type"] = "application/json";
    if (token()) h.Authorization = `Bearer ${token()}`;
    return h;
  }

  function setNote(text) {
    const modalNote = document.getElementById("auth-modal-note");
    const pageNote = document.getElementById("magic-note");
    if (modalNote) modalNote.textContent = text || "";
    if (pageNote) pageNote.textContent = text || "";
  }

  function openAuthModal(tab = "login") {
    const modal = document.getElementById("auth-modal");
    if (!modal) return;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    switchAuthTab(tab);
    setNote("");
    const focusId = tab === "register" ? "reg-email" : "login-email";
    document.getElementById(focusId)?.focus();
  }

  function closeAuthModal() {
    const modal = document.getElementById("auth-modal");
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  function switchAuthTab(tab) {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const title = document.getElementById("auth-modal-title");
    document.querySelectorAll("[data-auth-tab]").forEach((btn) => {
      const active = btn.getAttribute("data-auth-tab") === tab;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-selected", active ? "true" : "false");
    });
    if (loginForm) loginForm.style.display = tab === "login" ? "grid" : "none";
    if (registerForm) {
      registerForm.style.display = tab === "register" ? "grid" : "none";
    }
    if (title) {
      title.textContent = tab === "register" ? "Załóż konto" : "Zaloguj się";
    }
  }

  function setTopAuthState(loggedIn, label = "") {
    const guest = document.getElementById("auth-guest");
    const session = document.getElementById("auth-session");
    const chip = document.getElementById("auth-user-chip");
    if (guest) guest.classList.toggle("hidden", loggedIn);
    if (session) session.classList.toggle("hidden", !loggedIn);
    if (chip) {
      chip.textContent = label;
      chip.title = label || "Konto";
    }
  }

  async function logout() {
    try {
      await fetch(`${API}/api/auth/logout`, { method: "POST", headers: headers(false) });
    } catch (_) {
      /* ignore network errors on logout */
    }
    localStorage.removeItem(TOKEN_KEY);
    setTopAuthState(false);
    const box = document.getElementById("auth-user-box");
    if (box) box.textContent = "Wylogowano";
    setNote("Wylogowano.");
  }

  async function refreshAuthUI() {
    const box = document.getElementById("auth-user-box");
    const billingLine = document.getElementById("billing-status-line");
    const invoices = document.getElementById("invoices-box");
    if (!token()) {
      if (box) box.textContent = "Nie zalogowano — użyj przycisków u góry po prawej";
      setTopAuthState(false);
      return;
    }
    const me = await fetch(`${API}/api/auth/me`, { headers: headers(false) });
    if (!me.ok) {
      if (box) box.textContent = "Sesja wygasła — zaloguj się ponownie";
      setTopAuthState(false);
      return;
    }
    const data = await me.json();
    const u = data.user || {};
    const plan = (data.plan || {}).plan || "free";
    const label = u.email || u.name || String(u.user_id || "");
    setTopAuthState(true, label);
    if (box) {
      box.innerHTML = `${label} · plan: ${plan}
        · <a href="#" id="btn-logout">Wyloguj</a>
        · <a href="#" id="btn-export">RODO export</a>`;
      document.getElementById("btn-logout")?.addEventListener("click", async (e) => {
        e.preventDefault();
        await logout();
      });
      document.getElementById("btn-export")?.addEventListener("click", async (e) => {
        e.preventDefault();
        const res = await fetch(`${API}/api/account/export`, { headers: headers(false) });
        const blob = await res.blob();
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "wniosekpl-export.json";
        a.click();
      });
    }
    if (billingLine) {
      const b = data.billing || {};
      billingLine.textContent = b.stripe_configured
        ? "Stripe gotowy (live checkout)"
        : "Tryb demo (mock checkout) — dodaj STRIPE_* dla kart";
    }
    if (invoices) {
      const res = await fetch(`${API}/api/billing/invoices/${u.user_id}`, {
        headers: headers(false),
      });
      if (res.ok) {
        const inv = await res.json();
        invoices.innerHTML = (inv.items || [])
          .slice(0, 6)
          .map(
            (i) =>
              `<div>${i.created_at?.slice(0, 10) || ""} · ${i.product} · ${i.amount_pln} zł · ${i.status}</div>`
          )
          .join("") || "Brak płatności";
      }
    }
  }

  async function register(ev) {
    ev.preventDefault();
    const res = await fetch(`${API}/api/auth/register`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({
        name: document.getElementById("reg-name").value.trim(),
        email: document.getElementById("reg-email").value.trim(),
        password: document.getElementById("reg-password").value,
        lang: localStorage.getItem("wniosekpl_lang") || "pl",
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      setNote(data.detail || "Błąd rejestracji");
      return;
    }
    saveSession(data.session, data.user);
    setNote(
      data.verify_url
        ? `Konto utworzone. Potwierdź email: ${data.verify_url}`
        : "Konto utworzone."
    );
    await refreshAuthUI();
    closeAuthModal();
  }

  async function login(ev) {
    ev.preventDefault();
    const res = await fetch(`${API}/api/auth/login`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({
        email: document.getElementById("login-email").value.trim(),
        password: document.getElementById("login-password").value,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      setNote(data.detail || "Błędne dane");
      return;
    }
    saveSession(data.session, data.user);
    setNote("Zalogowano.");
    await refreshAuthUI();
    closeAuthModal();
  }

  async function checkout(product) {
    const uid = userId();
    if (!uid) {
      openAuthModal("login");
      setNote("Najpierw załóż konto / zaloguj się");
      return;
    }
    const res = await fetch(`${API}/api/billing/checkout`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ user_id: uid, product }),
    });
    const data = await res.json();
    if (data.checkout_url) window.location.href = data.checkout_url;
  }

  async function portal() {
    const res = await fetch(`${API}/api/billing/portal`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ user_id: userId() }),
    });
    const data = await res.json();
    if (data.portal_url) window.location.href = data.portal_url;
  }

  async function cancelSub() {
    if (!confirm("Anulować subskrypcję AI?")) return;
    const res = await fetch(`${API}/api/billing/cancel`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ user_id: userId() }),
    });
    const data = await res.json();
    setNote(res.ok ? `Subskrypcja: ${data.status}` : data.detail || "Błąd");
    refreshAuthUI();
  }

  async function forgot(ev) {
    ev.preventDefault();
    const res = await fetch(`${API}/api/auth/password/forgot`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({
        email: document.getElementById("reset-email").value.trim(),
      }),
    });
    const data = await res.json();
    const note = document.getElementById("reset-note");
    if (note) {
      note.textContent = data.reset_url
        ? `Demo reset link: ${data.reset_url}`
        : "Jeśli email istnieje — wysłaliśmy link.";
    }
  }

  async function wireProviders() {
    const res = await fetch(`${API}/api/auth/providers`);
    if (!res.ok) return;
    const p = await res.json();
    const g = document.getElementById("btn-google");
    const f = document.getElementById("btn-facebook");
    if (g && !p.google) {
      g.href = "#";
      g.textContent = "Google (ustaw w /setup)";
      g.addEventListener("click", (e) => e.preventDefault());
    }
    if (f && !p.facebook) {
      f.href = "#";
      f.textContent = "Facebook (ustaw w /setup)";
      f.addEventListener("click", (e) => e.preventDefault());
    }
  }

  function wireAuthModal() {
    document.getElementById("btn-open-login")?.addEventListener("click", () => openAuthModal("login"));
    document.getElementById("btn-open-register")?.addEventListener("click", () =>
      openAuthModal("register")
    );
    document.getElementById("btn-account-login")?.addEventListener("click", () => openAuthModal("login"));
    document.getElementById("btn-account-register")?.addEventListener("click", () =>
      openAuthModal("register")
    );
    document.getElementById("auth-modal-close")?.addEventListener("click", closeAuthModal);
    document.getElementById("btn-top-logout")?.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
    document.getElementById("auth-modal")?.addEventListener("click", (e) => {
      if (e.target?.id === "auth-modal") closeAuthModal();
    });
    document.querySelectorAll("[data-auth-tab]").forEach((btn) => {
      btn.addEventListener("click", () => switchAuthTab(btn.getAttribute("data-auth-tab")));
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeAuthModal();
    });
  }

  function wireTopbarScroll() {
    const bar = document.getElementById("topbar");
    if (!bar) return;
    const onScroll = () => bar.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function wire() {
    const params = new URLSearchParams(location.search);
    if (params.get("token")) localStorage.setItem(TOKEN_KEY, params.get("token"));
    if (params.get("user_id")) localStorage.setItem(USER_KEY, params.get("user_id"));

    wireAuthModal();
    wireTopbarScroll();

    document.getElementById("register-form")?.addEventListener("submit", register);
    document.getElementById("login-form")?.addEventListener("submit", login);
    document.getElementById("reset-form")?.addEventListener("submit", forgot);
    document.getElementById("pay-ai-account")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("ai_subscription");
    });
    document.getElementById("pay-review-account")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("human_review");
    });
    document.getElementById("btn-portal")?.addEventListener("click", (e) => {
      e.preventDefault();
      portal();
    });
    document.getElementById("btn-cancel-sub")?.addEventListener("click", (e) => {
      e.preventDefault();
      cancelSub();
    });

    if (params.get("reset_token")) {
      const pwd = prompt("Nowe hasło (min. 8 znaków):");
      if (pwd && pwd.length >= 8) {
        fetch(`${API}/api/auth/password/reset`, {
          method: "POST",
          headers: headers(),
          body: JSON.stringify({ token: params.get("reset_token"), password: pwd }),
        })
          .then((r) => r.json())
          .then((data) => {
            if (data.session) saveSession(data.session, data.user);
            refreshAuthUI();
          });
      }
    }

    if (params.get("auth") === "login") openAuthModal("login");
    if (params.get("auth") === "register") openAuthModal("register");

    wireProviders();
    refreshAuthUI();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
