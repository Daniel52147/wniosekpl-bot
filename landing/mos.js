(() => {
  const API = "";
  const READY_KEY = "wniosekpl_mos_ready";
  const PURPOSE_KEY = "wniosekpl_mos_purpose";
  const TAB_KEY = "wniosekpl_mos_tab";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";

  let guideData = null;
  let readyState = {};
  let uiCopy = {};

  function lang() {
    return localStorage.getItem("wniosekpl_lang") || "pl";
  }
  function token() {
    return localStorage.getItem(TOKEN_KEY) || "";
  }
  function userId() {
    return Number(localStorage.getItem(USER_KEY) || 0) || undefined;
  }
  function loggedIn() {
    return !!(token() || userId());
  }
  function headers(json = true) {
    const h = {};
    if (json) h["Content-Type"] = "application/json";
    if (token()) h.Authorization = `Bearer ${token()}`;
    return h;
  }
  function setText(id, value) {
    const el = document.getElementById(id);
    if (el && value != null) el.textContent = value;
  }
  function loadReady() {
    try {
      return JSON.parse(localStorage.getItem(READY_KEY) || "{}");
    } catch (_) {
      return {};
    }
  }
  function saveReady(state) {
    localStorage.setItem(READY_KEY, JSON.stringify(state));
  }

  function computeNext(steps, portalUrl) {
    const incomplete = (steps || []).find((s) => !readyState[s.id]);
    if (incomplete) {
      return {
        id: incomplete.id,
        complete: false,
        title: incomplete.title,
        hint: incomplete.hint,
        link: incomplete.link || "#mos-ready",
      };
    }
    return {
      id: "open_mos",
      complete: true,
      title: uiCopy.open_mos || "Otwórz MOS",
      hint: (guideData && guideData.next_action && guideData.next_action.hint) || "",
      link: portalUrl || "https://mos.cudzoziemcy.gov.pl",
    };
  }

  function renderProgress(total) {
    const done = Object.values(readyState).filter(Boolean).length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    setText("mos-progress", `${done} / ${total}`);
    setText("mos-progress-pct", `${pct}%`);
    const fill = document.getElementById("mos-progress-fill");
    if (fill) fill.style.width = `${pct}%`;
  }

  function renderSync() {
    const el = document.getElementById("mos-sync");
    if (!el) return;
    el.textContent = loggedIn()
      ? uiCopy.sync_account || ""
      : uiCopy.sync_local || "";
  }

  function renderFinale(next) {
    const finale = document.getElementById("mos-ready-finale");
    const checklistWrap = document.getElementById("mos-checklist-wrap");
    const nextBox = document.getElementById("mos-next");
    if (!finale) return;
    const show = !!(next && next.complete && guideData && guideData.finale);
    finale.hidden = !show;
    if (checklistWrap) checklistWrap.hidden = show;
    if (nextBox) nextBox.hidden = show;
    if (!show) return;

    const f = guideData.finale;
    const fc = f.copy || {};
    setText("mos-finale-title", fc.title || uiCopy.next_done || "");
    setText("mos-finale-sub", fc.sub || "");
    setText("mos-finale-attach-title", fc.attach_title || "");
    setText("mos-finale-steps-title", fc.steps_title || "");
    setText("mos-finale-purpose", f.purpose_title || "");

    const attach = document.getElementById("mos-finale-attach");
    if (attach) {
      attach.innerHTML = "";
      (f.attachments || []).forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        attach.appendChild(li);
      });
    }
    const steps = document.getElementById("mos-finale-steps");
    if (steps) {
      steps.innerHTML = "";
      (f.steps || []).forEach((step) => {
        const li = document.createElement("li");
        li.innerHTML = "<span class=\"n\"></span><span class=\"t\"></span>";
        li.querySelector(".n").textContent = String(step.n || "");
        li.querySelector(".t").textContent = step.title || "";
        steps.appendChild(li);
      });
    }
    const cta = document.getElementById("mos-finale-cta");
    if (cta) {
      cta.href = f.portal_url || guideData.portal_url || "https://mos.cudzoziemcy.gov.pl";
      cta.textContent = fc.cta || uiCopy.open_mos_btn || "MOS";
      cta.target = "_blank";
      cta.rel = "noopener";
    }
    const toggle = document.getElementById("mos-finale-toggle-checklist");
    if (toggle) {
      toggle.textContent = uiCopy.finale_show_checklist || "Checklist";
      toggle.onclick = () => {
        if (!checklistWrap) return;
        const open = checklistWrap.hidden;
        checklistWrap.hidden = !open;
        toggle.textContent = open
          ? uiCopy.finale_hide_checklist || "Hide"
          : uiCopy.finale_show_checklist || "Checklist";
        if (open) checklistWrap.scrollIntoView({ behavior: "smooth", block: "nearest" });
      };
    }
    const purposeBtns = document.getElementById("mos-finale-purposes");
    if (purposeBtns && guideData.purposes) {
      purposeBtns.innerHTML = "";
      const selected =
        localStorage.getItem(PURPOSE_KEY) || f.purpose || guideData.purposes[0]?.id;
      guideData.purposes.forEach((p) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = p.title;
        if (p.id === selected) btn.classList.add("active");
        btn.addEventListener("click", () => {
          localStorage.setItem(PURPOSE_KEY, p.id);
          guideData.finale = {
            ...f,
            purpose: p.id,
            purpose_title: p.title,
            attachments: p.items || [],
          };
          renderFinale(next);
        });
        purposeBtns.appendChild(btn);
      });
    }
  }

  function renderNext(next) {
    const box = document.getElementById("mos-next");
    const title = document.getElementById("mos-next-title");
    const body = document.getElementById("mos-next-body");
    const cta = document.getElementById("mos-next-cta");
    const mark = document.getElementById("mos-mark-done");
    const label = document.getElementById("mos-next-label");
    if (!box || !next) return;
    if (label) {
      label.textContent = next.complete
        ? uiCopy.next_done || uiCopy.next_title || ""
        : uiCopy.next_title || "";
    }
    if (title) title.textContent = next.title || "";
    if (body) body.textContent = next.hint || "";
    if (cta) {
      cta.href = next.link || "#mos-ready";
      cta.textContent = next.complete
        ? uiCopy.open_mos_btn || uiCopy.cta || "MOS"
        : uiCopy.do_step || "Dalej";
      if ((next.link || "").startsWith("http")) {
        cta.target = "_blank";
        cta.rel = "noopener";
      } else {
        cta.removeAttribute("target");
        cta.removeAttribute("rel");
      }
    }
    if (mark) {
      mark.hidden = !!next.complete;
      mark.textContent = uiCopy.mark_done || "Dalej";
      mark.dataset.stepId = next.id || "";
    }
    renderFinale(next);
  }

  function highlightCurrent(nextId) {
    document.querySelectorAll("#mos-ready label").forEach((label) => {
      label.classList.toggle("current", label.dataset.stepId === nextId);
    });
  }

  function renderPurposeItems(purpose) {
    const box = document.getElementById("mos-purpose-items");
    if (!box || !purpose) {
      if (box) box.hidden = true;
      return;
    }
    box.hidden = false;
    box.innerHTML = "<strong></strong><ul></ul>";
    box.querySelector("strong").textContent = purpose.title;
    const ul = box.querySelector("ul");
    (purpose.items || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
  }

  function setTab(tabId) {
    const id = tabId || "purpose";
    localStorage.setItem(TAB_KEY, id);
    document.querySelectorAll("[data-mos-tab]").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-mos-tab") === id);
    });
    document.querySelectorAll("[data-mos-panel]").forEach((panel) => {
      panel.hidden = panel.getAttribute("data-mos-panel") !== id;
    });
  }

  async function syncStep(stepId, done) {
    if (!loggedIn()) return;
    try {
      await fetch(`${API}/api/mos/step`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ user_id: userId(), step_id: stepId, done }),
      });
    } catch (_) {
      /* ignore offline sync */
    }
  }

  function applyStepChange(stepId, done, steps) {
    readyState[stepId] = done;
    saveReady(readyState);
    const label = document.querySelector(`#mos-ready label[data-step-id="${stepId}"]`);
    if (label) {
      label.classList.toggle("done", done);
      const input = label.querySelector("input");
      if (input) input.checked = done;
    }
    renderProgress(steps.length);
    const next = computeNext(steps, guideData && guideData.portal_url);
    renderNext(next);
    highlightCurrent(next.complete ? "" : next.id);
    renderSync();
    syncStep(stepId, done);
  }

  function wireTabs() {
    document.querySelectorAll("[data-mos-tab]").forEach((btn) => {
      btn.addEventListener("click", () => setTab(btn.getAttribute("data-mos-tab")));
    });
    setTab(localStorage.getItem(TAB_KEY) || "purpose");
  }

  function wireMarkDone() {
    const mark = document.getElementById("mos-mark-done");
    if (!mark || mark.dataset.wired) return;
    mark.dataset.wired = "1";
    mark.addEventListener("click", () => {
      const stepId = mark.dataset.stepId;
      if (!stepId || !guideData) return;
      if (stepId === "legal_stay") {
        document.getElementById("mos-deadline-date")?.focus();
        document.getElementById("mos-deadline-date")?.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }
      if (stepId === "employer_ready") {
        const helpers = document.getElementById("mos-helpers");
        if (helpers) helpers.open = true;
        document.getElementById("mos-employer-copy")?.focus();
        return;
      }
      applyStepChange(stepId, true, guideData.ready || []);
      const nextLabel = document.querySelector("#mos-ready label.current");
      nextLabel?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  function wireDeadline() {
    const form = document.getElementById("mos-deadline-form");
    if (!form || form.dataset.wired) return;
    form.dataset.wired = "1";
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const note = document.getElementById("mos-deadline-note");
      const due = document.getElementById("mos-deadline-date")?.value;
      const calendar = document.getElementById("mos-deadline-account");
      if (!due) return;
      if (!loggedIn()) {
        if (note) note.textContent = uiCopy.deadline_login || "";
        document.getElementById("btn-open-login")?.click();
        return;
      }
      const res = await fetch(`${API}/api/mos/deadline`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ user_id: userId(), due_at: due, days_before: 14 }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        if (note) note.textContent = data.detail || "Error";
        return;
      }
      if (note) note.textContent = uiCopy.deadline_ok || "";
      if (calendar) calendar.hidden = false;
      if (guideData) applyStepChange("legal_stay", true, guideData.ready || []);
    });
  }

  async function loadMosGuide() {
    const qs = new URLSearchParams({ lang: lang() });
    if (userId()) qs.set("user_id", String(userId()));
    const purpose = localStorage.getItem(PURPOSE_KEY);
    if (purpose) qs.set("purpose", purpose);
    const res = await fetch(`${API}/api/mos/guide?${qs}`, {
      headers: token() ? { Authorization: `Bearer ${token()}` } : {},
    });
    if (!res.ok) return;
    const data = await res.json();
    guideData = data;
    uiCopy = data.copy || {};

    setText("mos-title", uiCopy.title);
    setText("mos-sub", uiCopy.sub);
    setText("mos-ready-title", uiCopy.ready_title);
    setText("mos-purpose-title", uiCopy.purpose_title);
    setText("mos-disclaimer", uiCopy.disclaimer);
    setText("mos-deadline-title", uiCopy.deadline_title);
    setText("mos-deadline-hint", uiCopy.deadline_hint);
    setText("mos-deadline-btn", uiCopy.deadline_btn);
    setText("mos-tab-purpose", uiCopy.tab_purpose);
    setText("mos-tab-employer", uiCopy.tab_employer);
    setText("mos-tab-deadline", uiCopy.tab_deadline);
    setText("mos-deadline-account", uiCopy.deadline_calendar);

    const open = document.getElementById("mos-open");
    if (open) {
      open.href = data.portal_url || "https://mos.cudzoziemcy.gov.pl";
      open.textContent = uiCopy.cta || open.textContent;
    }
    const info = document.getElementById("mos-info");
    if (info) {
      info.href = data.info_url || info.href;
      info.textContent = uiCopy.info || info.textContent;
    }

    const employer = data.employer_helper || {};
    setText("mos-employer-title", employer.title);
    setText("mos-employer-body", employer.body);
    const msg = document.getElementById("mos-employer-msg");
    if (msg) msg.textContent = employer.message || "";
    const copyBtn = document.getElementById("mos-employer-copy");
    if (copyBtn) {
      copyBtn.textContent = uiCopy.copy_employer || "Kopiuj";
      copyBtn.onclick = async () => {
        try {
          await navigator.clipboard.writeText(employer.message || "");
          copyBtn.textContent = uiCopy.copied || "✓";
          setTimeout(() => {
            copyBtn.textContent = uiCopy.copy_employer || "Kopiuj";
          }, 1200);
        } catch (_) {
          copyBtn.textContent = "!";
        }
      };
    }

    readyState = loadReady();
    if (data.saved_progress && typeof data.saved_progress === "object") {
      readyState = { ...readyState, ...data.saved_progress };
      saveReady(readyState);
    }

    const steps = data.ready || [];
    const readyBox = document.getElementById("mos-ready");
    if (readyBox) {
      readyBox.innerHTML = "";
      steps.forEach((step) => {
        const done = !!readyState[step.id];
        const label = document.createElement("label");
        label.dataset.stepId = step.id;
        if (done) label.classList.add("done");
        label.innerHTML =
          '<input type="checkbox" /><div><span class="title"></span><span class="hint"></span></div>';
        const input = label.querySelector("input");
        input.checked = done;
        label.querySelector(".title").textContent = step.title;
        label.querySelector(".hint").textContent = step.hint || "";
        input.addEventListener("change", () => {
          applyStepChange(step.id, input.checked, steps);
        });
        readyBox.appendChild(label);
      });
    }

    renderProgress(steps.length);
    const next = computeNext(steps, data.portal_url);
    renderNext(next);
    highlightCurrent(next.complete ? "" : next.id);
    renderSync();
    if (window.wniosekplLoadGuide) window.wniosekplLoadGuide().catch(() => {});

    const purposes = document.getElementById("mos-purposes");
    if (purposes) {
      purposes.innerHTML = "";
      const selected =
        localStorage.getItem(PURPOSE_KEY) || (data.purposes?.[0]?.id ?? "");
      let current =
        data.purposes?.find((p) => p.id === selected) || data.purposes?.[0];
      (data.purposes || []).forEach((purpose) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = purpose.title;
        if (current && purpose.id === current.id) btn.classList.add("active");
        btn.addEventListener("click", () => {
          localStorage.setItem(PURPOSE_KEY, purpose.id);
          purposes.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          renderPurposeItems(purpose);
        });
        purposes.appendChild(btn);
      });
      renderPurposeItems(current);
    }
  }

  function wire() {
    wireTabs();
    wireMarkDone();
    wireDeadline();
    loadMosGuide().catch(() => {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  window.wniosekplLoadMos = loadMosGuide;
})();
