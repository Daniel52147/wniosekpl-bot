(() => {
  const API = "";
  const PLAN_KEY = "wniosekpl_onboarding_plan";
  const PURPOSE_KEY = "wniosekpl_mos_purpose";
  const READY_KEY = "wniosekpl_mos_ready";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";
  const LANG_KEY = "wniosekpl_lang";

  let state = {
    purpose: localStorage.getItem(PURPOSE_KEY) || "",
    has_pesel: null,
    due_at: "",
  };
  let ui = null;

  function lang() {
    return localStorage.getItem(LANG_KEY) || "pl";
  }
  function token() {
    return localStorage.getItem(TOKEN_KEY) || "";
  }
  function userId() {
    return Number(localStorage.getItem(USER_KEY) || 0) || undefined;
  }
  function headers() {
    const h = { "Content-Type": "application/json" };
    if (token()) h.Authorization = `Bearer ${token()}`;
    return h;
  }
  function loadPlan() {
    try {
      return JSON.parse(localStorage.getItem(PLAN_KEY) || "null");
    } catch (_) {
      return null;
    }
  }
  function savePlan(plan) {
    localStorage.setItem(PLAN_KEY, JSON.stringify(plan));
  }
  function loadReady() {
    try {
      return JSON.parse(localStorage.getItem(READY_KEY) || "{}");
    } catch (_) {
      return {};
    }
  }
  function saveReady(ready) {
    localStorage.setItem(READY_KEY, JSON.stringify(ready));
  }

  function showStep(n) {
    ["1", "2", "3"].forEach((i) => {
      const el = document.getElementById(`ob-step-${i}`);
      if (el) el.hidden = String(n) !== i;
    });
    const done = document.getElementById("ob-done");
    if (done) done.hidden = n !== "done";
  }

  function setWorkspaceVisible(on) {
    const workspace = document.getElementById("now-workspace");
    const ob = document.getElementById("onboarding");
    if (workspace) workspace.hidden = !on;
    if (!ob) return;
    if (on) {
      ob.classList.add("ob-compact");
      // slim bar: title + restart only
      ["ob-sub", "ob-step-1", "ob-step-2", "ob-step-3", "ob-summary"].forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.hidden = true;
      });
      const done = document.getElementById("ob-done");
      if (done) done.hidden = false;
      const start = document.getElementById("ob-start");
      if (start) start.hidden = true;
      const kicker = document.getElementById("ob-kicker");
      if (kicker) kicker.textContent = "Plan";
    } else {
      ob.classList.remove("ob-compact");
      const start = document.getElementById("ob-start");
      if (start) start.hidden = false;
      const sub = document.getElementById("ob-sub");
      if (sub) sub.hidden = false;
    }
  }

  function applyCopy(copy) {
    ui = copy;
    const map = [
      ["ob-title", "title"],
      ["ob-sub", "sub"],
      ["ob-q1", "q1"],
      ["ob-q2", "q2"],
      ["ob-q3", "q3"],
      ["ob-q3-hint", "q3_hint"],
      ["ob-pesel-yes", "yes"],
      ["ob-pesel-no", "no"],
      ["ob-deadline-next", "next"],
      ["ob-deadline-skip", "skip"],
      ["ob-start", "start"],
      ["ob-restart", "restart"],
    ];
    map.forEach(([id, key]) => {
      const el = document.getElementById(id);
      if (el && copy[key]) el.textContent = copy[key];
    });
    const kicker = document.getElementById("ob-kicker");
    if (kicker) kicker.textContent = "1 / 3";
  }

  function renderPurposes() {
    const box = document.getElementById("ob-purposes");
    if (!box || !ui) return;
    box.innerHTML = "";
    Object.entries(ui.purpose || {}).forEach(([id, label]) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = label;
      if (state.purpose === id) btn.classList.add("active");
      btn.addEventListener("click", () => {
        state.purpose = id;
        localStorage.setItem(PURPOSE_KEY, id);
        box.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const kicker = document.getElementById("ob-kicker");
        if (kicker) kicker.textContent = "2 / 3";
        showStep(2);
      });
      box.appendChild(btn);
    });
  }

  function renderSummary(plan) {
    const ul = document.getElementById("ob-summary");
    if (!ul) return;
    ul.innerHTML = "";
    (plan.summary_lines || []).forEach((line) => {
      const li = document.createElement("li");
      li.textContent = line;
      ul.appendChild(li);
    });
  }

  async function finish() {
    const body = {
      user_id: userId(),
      purpose: state.purpose || "work",
      has_pesel: !!state.has_pesel,
      due_at: state.due_at || null,
      lang: lang(),
    };
    let plan;
    let steps = loadReady();
    try {
      const res = await fetch(`${API}/api/onboarding`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) throw new Error("onboarding");
      plan = data.plan;
      steps = { ...steps, ...(data.steps || {}) };
    } catch (_) {
      // offline fallback
      plan = {
        purpose: body.purpose,
        has_pesel: body.has_pesel,
        due_at: body.due_at,
        summary_lines: [
          (ui?.summary_purpose || "{purpose}").replace(
            "{purpose}",
            ui?.purpose?.[body.purpose] || body.purpose
          ),
          body.has_pesel ? ui?.summary_pesel_yes : ui?.summary_pesel_no,
        ].filter(Boolean),
        first_step: body.has_pesel ? "trusted_profile" : "pesel",
        copy: ui,
      };
      if (body.has_pesel) steps.pesel = true;
      if (body.due_at) steps.legal_stay = true;
    }
    saveReady(steps);
    localStorage.setItem(PURPOSE_KEY, plan.purpose);
    plan.completed = true;
    savePlan(plan);
    renderSummary(plan);
    const kicker = document.getElementById("ob-kicker");
    if (kicker) kicker.textContent = "✓";
    showStep("done");
  }

  function enterWorkspace() {
    const plan = loadPlan();
    if (plan) plan.entered = true;
    if (plan) savePlan(plan);
    setWorkspaceVisible(true);
    if (window.wniosekplLoadMos) window.wniosekplLoadMos().catch(() => {});
    if (window.wniosekplRefreshProfile) window.wniosekplRefreshProfile();
    if (window.wniosekplRefreshAccountLink) window.wniosekplRefreshAccountLink();
    document.getElementById("mos-next")?.scrollIntoView({ behavior: "smooth", block: "start" });
    // Soft nudge: one account across phone + browser.
    const banner = document.getElementById("tg-link-banner");
    if (banner && localStorage.getItem("wniosekpl_tg_banner_dismissed") !== "1") {
      banner.hidden = false;
    }
  }

  function resetOnboarding() {
    localStorage.removeItem(PLAN_KEY);
    state = { purpose: "", has_pesel: null, due_at: "" };
    setWorkspaceVisible(false);
    const kicker = document.getElementById("ob-kicker");
    if (kicker) kicker.textContent = "1 / 3";
    showStep(1);
    renderPurposes();
  }

  function wire() {
    document.getElementById("ob-pesel-yes")?.addEventListener("click", () => {
      state.has_pesel = true;
      const kicker = document.getElementById("ob-kicker");
      if (kicker) kicker.textContent = "3 / 3";
      showStep(3);
    });
    document.getElementById("ob-pesel-no")?.addEventListener("click", () => {
      state.has_pesel = false;
      const kicker = document.getElementById("ob-kicker");
      if (kicker) kicker.textContent = "3 / 3";
      showStep(3);
    });
    document.getElementById("ob-deadline-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      state.due_at = document.getElementById("ob-deadline-date")?.value || "";
      await finish();
    });
    document.getElementById("ob-deadline-skip")?.addEventListener("click", async () => {
      state.due_at = "";
      await finish();
    });
    document.getElementById("ob-start")?.addEventListener("click", enterWorkspace);
    document.getElementById("ob-restart")?.addEventListener("click", resetOnboarding);
  }

  async function boot() {
    wire();
    try {
      const res = await fetch(`${API}/api/onboarding/copy?lang=${lang()}`);
      if (res.ok) {
        const data = await res.json();
        applyCopy(data.copy || {});
      }
    } catch (_) {
      applyCopy({
        title: "3 pytania — Twój plan",
        sub: "Od razu wiemy, od czego zacząć.",
        q1: "Jaki jest cel pobytu?",
        q2: "Masz już numer PESEL?",
        q3: "Do kiedy masz legalny pobyt?",
        q3_hint: "Jeśli nie wiesz — pomiń.",
        yes: "Tak",
        no: "Nie / nie wiem",
        skip: "Nie wiem — pomiń",
        next: "Dalej",
        start: "Zaczynam",
        restart: "Zmień odpowiedzi",
        purpose: { work: "Praca", study: "Studia", family: "Rodzina", business: "Biznes" },
      });
    }
    renderPurposes();

    const plan = loadPlan();
    if (plan?.completed) {
      renderSummary(plan);
      if (plan.entered) {
        setWorkspaceVisible(true);
        // keep a compact summary card
        showStep("done");
        const sub = document.getElementById("ob-sub");
        if (sub) sub.hidden = true;
      } else {
        setWorkspaceVisible(false);
        showStep("done");
      }
    } else {
      setWorkspaceVisible(false);
      showStep(1);
    }
  }

  window.wniosekplResetOnboarding = resetOnboarding;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
