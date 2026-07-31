(() => {
  const API = "";
  const HOW_KEY = "wniosekpl_how_dismissed";
  const WHATS_NEW_KEY = "wniosekpl_whats_new_v244";
  const LANG_KEY = "wniosekpl_lang";
  const READY_KEY = "wniosekpl_mos_ready";
  const PLAN_KEY = "wniosekpl_onboarding_plan";

  function lang() {
    return localStorage.getItem(LANG_KEY) || "pl";
  }

  function planCompleted() {
    try {
      const plan = JSON.parse(localStorage.getItem(PLAN_KEY) || "null");
      return !!(plan && plan.completed);
    } catch (_) {
      return false;
    }
  }

  function detectStage() {
    try {
      const plan = JSON.parse(localStorage.getItem(PLAN_KEY) || "null");
      const ready = JSON.parse(localStorage.getItem(READY_KEY) || "{}");
      const steps = Object.values(ready).filter(Boolean).length;
      if (steps >= 7) return "file";
      if (plan && plan.completed && steps >= 1) return "check";
      if (plan && plan.completed) return "prepare";
      return "prepare";
    } catch (_) {
      return "prepare";
    }
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (el && value != null) el.textContent = value;
  }

  function renderOfficialBar(links, note, kicker) {
    const bar = document.getElementById("official-bar");
    if (!bar) return;
    setText("official-kicker", kicker || "");
    setText("official-note", note || "");
    const box = document.getElementById("official-links");
    if (!box) return;
    box.innerHTML = "";
    (links || []).forEach((item) => {
      const a = document.createElement("a");
      a.href = item.url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = item.label;
      box.appendChild(a);
    });
  }

  function renderPath(path, stage) {
    const box = document.getElementById("journey-path");
    if (!box) return;
    box.innerHTML = "";
    (path || []).forEach((step) => {
      const li = document.createElement("li");
      li.className = "journey-step";
      if (step.id === stage) li.classList.add("current");
      const order = ["prepare", "check", "file"];
      if (order.indexOf(step.id) < order.indexOf(stage)) li.classList.add("done");
      li.innerHTML = "<strong></strong><p></p>";
      li.querySelector("strong").textContent = step.title || "";
      li.querySelector("p").textContent = step.body || "";
      box.appendChild(li);
    });
  }

  function syncJourneyVisibility() {
    const card = document.getElementById("journey-card");
    if (!card) return;
    // Hide the 3-stage card until onboarding is done — fewer first-visit walls.
    card.hidden = !planCompleted();
  }

  function renderHow(copy) {
    const card = document.getElementById("how-card");
    if (!card) return;
    if (localStorage.getItem(HOW_KEY) === "1") {
      card.hidden = true;
      return;
    }
    card.hidden = false;
    setText("how-title", copy.how_title || "");
    const list = document.getElementById("how-list");
    if (list) {
      list.innerHTML = "";
      (copy.how_items || []).forEach((line) => {
        const li = document.createElement("li");
        li.textContent = line;
        list.appendChild(li);
      });
    }
    const btn = document.getElementById("how-dismiss");
    if (btn) {
      btn.textContent = copy.how_dismiss || "OK";
      btn.onclick = () => {
        localStorage.setItem(HOW_KEY, "1");
        card.hidden = true;
      };
    }
  }

  function renderWhatsNew(copy) {
    const card = document.getElementById("whats-new");
    if (!card) return;
    if (localStorage.getItem(WHATS_NEW_KEY) === "1") {
      card.hidden = true;
      return;
    }
    card.hidden = false;
    setText("whats-new-title", copy.whats_new_title || "");
    const list = document.getElementById("whats-new-list");
    if (list) {
      list.innerHTML = "";
      (copy.whats_new_items || []).forEach((line) => {
        const li = document.createElement("li");
        li.textContent = line;
        list.appendChild(li);
      });
    }
    const btn = document.getElementById("whats-new-dismiss");
    if (btn) {
      btn.textContent = copy.whats_new_dismiss || "OK";
      btn.onclick = () => {
        localStorage.setItem(WHATS_NEW_KEY, "1");
        card.hidden = true;
      };
    }
  }

  function applyAccountLabels(copy) {
    const map = [
      ["acc-session-title", "acc_session_title"],
      ["acc-session-hint", "acc_session_hint"],
      ["acc-billing-title", "acc_billing_title"],
      ["tg-link-title", "acc_tg_title"],
      ["tg-link-hint", "acc_tg_hint"],
      ["btn-account-login", "acc_login"],
      ["btn-account-register", "acc_register"],
      ["btn-open-login", "acc_login"],
      ["btn-open-register", "acc_register"],
    ];
    map.forEach(([id, key]) => {
      const el = document.getElementById(id);
      if (el && copy[key]) el.textContent = copy[key];
    });
  }

  function applyCabinetLabels(copy) {
    setText("profile-title", copy.cabinet_title);
    setText("profile-sub", copy.cabinet_sub);
    setText("app-crumb-text", copy.crumb);
    const tabs = [
      ["tab-now", "tab_now", "tab_now_hint"],
      ["tab-docs", "tab_docs", "tab_docs_hint"],
      ["tab-account", "tab_account", "tab_account_hint"],
    ];
    tabs.forEach(([id, key, hintKey]) => {
      const btn = document.getElementById(id);
      if (!btn || !copy[key]) return;
      const hint = btn.querySelector(".tab-hint");
      if (hint) {
        hint.textContent = copy[hintKey] || "";
        const label = document.createTextNode(copy[key] + " ");
        while (btn.firstChild && btn.firstChild !== hint) {
          btn.removeChild(btn.firstChild);
        }
        btn.insertBefore(label, hint);
      } else {
        btn.textContent = copy[key];
      }
    });
    applyAccountLabels(copy);
    // Expose shared strings for docs/MOS error UI
    window.wniosekplGuideCopy = copy;
  }

  function applyLanding(copy, links) {
    setText("path-section-title", copy.landing_path_title);
    setText("path-section-sub", copy.landing_path_sub);
    const cta = document.getElementById("cta-profile");
    if (cta && copy.landing_cta) cta.textContent = copy.landing_cta;
    const band = document.getElementById("band-cta");
    if (band && copy.landing_cta) band.textContent = copy.landing_cta;
    renderOfficialBar(links, copy.official_note, copy.official_kicker);
  }

  async function loadGuide() {
    const stage = detectStage();
    const res = await fetch(`${API}/api/guide?lang=${lang()}&stage=${stage}`);
    if (!res.ok) return;
    const data = await res.json();
    const copy = data.copy || {};

    renderOfficialBar(data.official_links, copy.official_note, copy.official_kicker);
    setText("journey-title", copy.path_title);
    renderPath(data.path, data.stage || stage);
    syncJourneyVisibility();
    renderHow(copy);
    renderWhatsNew(copy);

    if (document.getElementById("profile-title")) {
      applyCabinetLabels(copy);
    }
    if (document.getElementById("path-section-title")) {
      applyLanding(copy, data.official_links);
      const landingPath = document.getElementById("landing-path");
      if (landingPath) {
        landingPath.innerHTML = "";
        (data.path || []).forEach((step) => {
          const art = document.createElement("article");
          art.innerHTML = "<strong></strong><p></p>";
          art.querySelector("strong").textContent = step.title || "";
          art.querySelector("p").textContent = step.body || "";
          landingPath.appendChild(art);
        });
      }
    }
  }

  function wire() {
    loadGuide().catch(() => {});
    window.addEventListener("storage", () => loadGuide().catch(() => {}));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  window.wniosekplLoadGuide = loadGuide;
  window.wniosekplSyncJourney = syncJourneyVisibility;
})();
