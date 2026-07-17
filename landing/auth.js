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

  async function refreshAuthUI() {
    const box = document.getElementById("auth-user-box");
    const billingLine = document.getElementById("billing-status-line");
    const invoices = document.getElementById("invoices-box");
    if (!token()) {
      if (box) box.textContent = "Nie zalogowano";
      return;
    }
    const me = await fetch(`${API}/api/auth/me`, { headers: headers(false) });
    if (!me.ok) {
      if (box) box.textContent = "Sesja wygasła — zaloguj się ponownie";
      return;
    }
    const data = await me.json();
    const u = data.user || {};
    if (box) {
      box.innerHTML = `${u.email || u.name || u.user_id} · plan: ${(data.plan || {}).plan || "free"}
        · <a href="#" id="btn-logout">Wyloguj</a>
        · <a href="#" id="btn-export">RODO export</a>`;
      document.getElementById("btn-logout")?.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch(`${API}/api/auth/logout`, { method: "POST", headers: headers(false) });
        localStorage.removeItem(TOKEN_KEY);
        box.textContent = "Wylogowano";
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
    const note = document.getElementById("magic-note");
    if (!res.ok) {
      if (note) note.textContent = data.detail || "Błąd rejestracji";
      return;
    }
    saveSession(data.session, data.user);
    if (note) {
      note.textContent = data.verify_url
        ? `Konto utworzone. Potwierdź email: ${data.verify_url}`
        : "Konto utworzone.";
    }
    refreshAuthUI();
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
    const note = document.getElementById("magic-note");
    if (!res.ok) {
      if (note) note.textContent = data.detail || "Błędne dane";
      return;
    }
    saveSession(data.session, data.user);
    if (note) note.textContent = "Zalogowano.";
    refreshAuthUI();
  }

  async function checkout(product) {
    const uid = userId();
    if (!uid) {
      alert("Najpierw załóż konto / zaloguj się");
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
    const note = document.getElementById("magic-note");
    if (note) note.textContent = res.ok ? `Subskrypcja: ${data.status}` : data.detail || "Błąd";
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
      g.textContent = "Google (ustaw GOOGLE_CLIENT_*)";
      g.addEventListener("click", (e) => e.preventDefault());
    }
    if (f && !p.facebook) {
      f.href = "#";
      f.textContent = "Facebook (ustaw FACEBOOK_APP_*)";
      f.addEventListener("click", (e) => e.preventDefault());
    }
  }

  function wire() {
    const params = new URLSearchParams(location.search);
    if (params.get("token")) localStorage.setItem(TOKEN_KEY, params.get("token"));
    if (params.get("user_id")) localStorage.setItem(USER_KEY, params.get("user_id"));

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

    wireProviders();
    refreshAuthUI();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
