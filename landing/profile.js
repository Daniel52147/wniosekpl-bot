(() => {
  const API = "";
  const TODO_KEY = "wniosekpl_profile_todos";
  const READY_KEY = "wniosekpl_mos_ready";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";
  const LANG_KEY = "wniosekpl_lang";
  const TAB_KEY = "wniosekpl_profile_tab";

  function lang() {
    return localStorage.getItem(LANG_KEY) || "pl";
  }
  function token() {
    return localStorage.getItem(TOKEN_KEY) || "";
  }
  function userId() {
    return Number(localStorage.getItem(USER_KEY) || 0) || undefined;
  }
  function t(key, fallback) {
    const pack = (window.wniosekplCopy && window.wniosekplCopy[lang()]) || {};
    return pack[key] || fallback;
  }
  function authHeaders(json = true) {
    const h = {};
    if (json) h["Content-Type"] = "application/json";
    if (token()) h.Authorization = `Bearer ${token()}`;
    return h;
  }

  function loadTodos() {
    try {
      return JSON.parse(localStorage.getItem(TODO_KEY) || "[]");
    } catch (_) {
      return [];
    }
  }
  function saveTodos(items) {
    localStorage.setItem(TODO_KEY, JSON.stringify(items.slice(0, 20)));
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

  function setTab(tabId, { updateHash = true } = {}) {
    const id = tabId || "overview";
    localStorage.setItem(TAB_KEY, id);
    document.querySelectorAll("[data-profile-tab]").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-profile-tab") === id);
    });
    document.querySelectorAll("[data-profile-panel]").forEach((panel) => {
      panel.hidden = panel.getAttribute("data-profile-panel") !== id;
    });
    if (updateHash && location.hash.startsWith("#profile")) {
      history.replaceState(null, "", `#profile?tab=${id}`);
    }
  }

  function tabFromLocation() {
    const hash = location.hash || "";
    if (hash.startsWith("#account")) return localStorage.getItem(TAB_KEY) || "account";
    if (!hash.startsWith("#profile")) return localStorage.getItem(TAB_KEY) || "overview";
    const q = hash.includes("?") ? hash.split("?")[1] : "";
    const params = new URLSearchParams(q);
    return params.get("tab") || localStorage.getItem(TAB_KEY) || "overview";
  }

  function pushTodos(actions, topic) {
    if (!actions || !actions.length) return;
    const list = loadTodos();
    const now = Date.now();
    actions.forEach((action) => {
      const key = `${action.type}:${action.id}`;
      const existing = list.find((x) => x.key === key && !x.done);
      if (existing) {
        existing.label = action.label || existing.label;
        existing.href = action.href || existing.href;
        existing.topic = topic || existing.topic;
        existing.updated = now;
        return;
      }
      list.unshift({
        key,
        type: action.type,
        id: action.id,
        label: action.label || action.id,
        href: action.href || "",
        topic: topic || "",
        done: false,
        updated: now,
      });
    });
    saveTodos(list);
    renderTodos();
    updateTeaser();
  }

  function markTodoDone(key) {
    const list = loadTodos().map((item) =>
      item.key === key ? { ...item, done: true, updated: Date.now() } : item
    );
    saveTodos(list);
    renderTodos();
    updateTeaser();
  }

  function runAction(action) {
    if (!action) return;
    if (action.type === "open_doc" && window.wniosekplOpenDoc) {
      window.wniosekplOpenDoc(action.id);
      return;
    }
    if (action.type === "goto" || action.href) {
      const href = action.href || "#mos";
      if (href.startsWith("#")) {
        location.hash = href;
        document.querySelector(href)?.scrollIntoView({ behavior: "smooth" });
      } else {
        window.open(href, "_blank", "noopener");
      }
    }
  }

  function renderTodoList(box, items, { limit = 20, emptyKey = "profileEmptyTodo" } = {}) {
    if (!box) return;
    box.innerHTML = "";
    if (!items.length) {
      const p = document.createElement("p");
      p.className = "profile-empty";
      p.textContent = t(emptyKey, "Na razie pusto.");
      box.appendChild(p);
      return;
    }
    items.slice(0, limit).forEach((item) => {
      const el = document.createElement("div");
      el.className = "profile-item";
      el.innerHTML = `<p></p><div class="row-actions"></div>`;
      el.querySelector("p").textContent = item.label;
      const actions = el.querySelector(".row-actions");
      const openBtn = document.createElement("button");
      openBtn.type = "button";
      openBtn.className = "primary";
      openBtn.textContent = t("profileOpen", "Otwórz");
      openBtn.addEventListener("click", () => runAction(item));
      const doneBtn = document.createElement("button");
      doneBtn.type = "button";
      doneBtn.textContent = t("profileDone", "Gotowe");
      doneBtn.addEventListener("click", () => markTodoDone(item.key));
      actions.appendChild(openBtn);
      actions.appendChild(doneBtn);
      box.appendChild(el);
    });
  }

  function renderTodos() {
    const open = loadTodos().filter((x) => !x.done);
    renderTodoList(document.getElementById("profile-todo"), open);
    renderTodoList(document.getElementById("profile-todo-preview"), open, {
      limit: 3,
      emptyKey: "profileEmptyTodo",
    });
    updateTeaser(open.length);
  }

  function renderMosNext(nxt) {
    const box = document.getElementById("profile-mos");
    if (!box) return;
    box.innerHTML = "";
    const el = document.createElement("div");
    el.className = "profile-item";
    el.innerHTML = `<p></p><span class="muted"></span><div class="row-actions"></div>`;
    el.querySelector("p").textContent = nxt.title || "MOS";
    el.querySelector(".muted").textContent = nxt.complete
      ? `${nxt.done_count || 0}/${nxt.total || 0}`
      : `${nxt.hint || ""} · ${nxt.done_count || 0}/${nxt.total || 0}`;
    const openBtn = document.createElement("a");
    openBtn.className = "primary";
    openBtn.href = nxt.link || "#mos";
    openBtn.textContent = t("profileOpen", "Otwórz");
    if ((nxt.link || "").startsWith("http")) {
      openBtn.target = "_blank";
      openBtn.rel = "noopener";
    }
    el.querySelector(".row-actions").appendChild(openBtn);
    box.appendChild(el);
  }

  function renderCalendar(events) {
    const boxes = [
      document.getElementById("profile-cal"),
      document.getElementById("profile-cal-preview"),
    ];
    boxes.forEach((box, idx) => {
      if (!box) return;
      box.innerHTML = "";
      if (!events || !events.length) {
        const p = document.createElement("p");
        p.className = "profile-empty";
        p.textContent = t("profileEmptyCal", "Brak terminów.");
        box.appendChild(p);
        return;
      }
      const slice = idx === 1 ? events.slice(0, 1) : events.slice(0, 8);
      slice.forEach((ev) => {
        const el = document.createElement("div");
        el.className = "profile-item";
        el.innerHTML = `<p></p><span class="muted"></span>`;
        el.querySelector("p").textContent = ev.title || "Termin";
        el.querySelector(".muted").textContent = ev.due_at || "";
        box.appendChild(el);
      });
    });
    // keep tools calendar-list in sync if present
    const tools = document.getElementById("calendar-list");
    if (tools && !tools.hidden) {
      /* left for platform.js */
    }
  }

  async function syncMosStep(stepId, done) {
    if (!token() && !userId()) return;
    try {
      await fetch(`${API}/api/mos/step`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({ user_id: userId(), step_id: stepId, done }),
      });
    } catch (_) {
      /* ignore */
    }
  }

  function renderMosChecklist(readySteps, saved) {
    const box = document.getElementById("profile-mos-list");
    if (!box) return;
    const state = { ...loadReady(), ...(saved || {}) };
    saveReady(state);
    box.innerHTML = "";
    (readySteps || []).forEach((step) => {
      const done = !!state[step.id];
      const label = document.createElement("label");
      if (done) label.classList.add("done");
      label.innerHTML = `<input type="checkbox" /><div><strong style="display:block"></strong><span class="muted"></span></div>`;
      const input = label.querySelector("input");
      input.checked = done;
      label.querySelector("strong").textContent = step.title;
      label.querySelector("span").textContent = step.hint || "";
      input.addEventListener("change", () => {
        state[step.id] = input.checked;
        saveReady(state);
        label.classList.toggle("done", input.checked);
        syncMosStep(step.id, input.checked);
        if (window.wniosekplLoadMos) window.wniosekplLoadMos().catch(() => {});
        refreshProfile();
      });
      box.appendChild(label);
    });
  }

  function updateTeaser(todoCount) {
    const body = document.getElementById("profile-teaser-body");
    const title = document.getElementById("profile-teaser-title");
    const cta = document.getElementById("profile-teaser-cta");
    const n = todoCount != null ? todoCount : loadTodos().filter((x) => !x.done).length;
    if (title) title.textContent = t("profileTitle", "Twój profil");
    if (body) {
      body.textContent = t("profileTeaserBody", "{n} zadań · MOS, terminy, płatności w zakładkach").replace(
        "{n}",
        String(n)
      );
    }
    if (cta) {
      cta.textContent = t("profileOpenFull", "Otwórz profil");
      cta.href = "#profile?tab=overview";
    }
  }

  function applyCopy() {
    const map = [
      ["profile-title", "profileTitle"],
      ["profile-sub", "profileSub"],
      ["tab-overview", "tabOverview"],
      ["tab-tasks", "tabTasks"],
      ["tab-mos", "tabMos"],
      ["tab-calendar", "tabCalendar"],
      ["tab-billing", "tabBilling"],
      ["tab-account", "tabAccount"],
      ["overview-plan-title", "overviewPlan"],
      ["overview-next-title", "overviewNext"],
      ["overview-tasks-title", "overviewTasks"],
      ["overview-cal-title", "overviewCal"],
      ["overview-ask", "overviewAsk"],
      ["overview-mos-link", "overviewMos"],
      ["overview-all-tasks", "overviewAllTasks"],
      ["overview-all-cal", "overviewAllCal"],
      ["tasks-hint", "tasksHint"],
      ["mos-tab-title", "mosTabTitle"],
      ["mos-tab-hint", "mosTabHint"],
      ["cal-tab-title", "calTabTitle"],
      ["profile-cal-btn", "calAddBtn"],
    ];
    map.forEach(([id, key]) => {
      const el = document.getElementById(id);
      if (el) el.textContent = t(key, el.textContent);
    });
    updateTeaser();
  }

  async function refreshProfile() {
    applyCopy();
    renderTodos();
    const qs = new URLSearchParams({ lang: lang() });
    if (userId()) qs.set("user_id", String(userId()));
    try {
      const [resumeRes, guideRes] = await Promise.all([
        fetch(`${API}/api/resume?${qs}`, { headers: authHeaders(false) }),
        fetch(`${API}/api/mos/guide?${qs}`, { headers: authHeaders(false) }),
      ]);
      if (resumeRes.ok) {
        const data = await resumeRes.json();
        renderMosNext(data.mos_next || {});
        renderCalendar(data.calendar || []);
      }
      if (guideRes.ok) {
        const guide = await guideRes.json();
        renderMosChecklist(guide.ready || [], guide.saved_progress || {});
        if (guide.next_action) renderMosNext(guide.next_action);
      }
    } catch (_) {
      /* offline */
    }
    if (window.wniosekplRefreshCabinet) {
      try {
        await window.wniosekplRefreshCabinet();
      } catch (_) {
        /* ignore */
      }
    }
  }

  function wireTabs() {
    document.querySelectorAll("[data-profile-tab]").forEach((btn) => {
      btn.addEventListener("click", () => setTab(btn.getAttribute("data-profile-tab")));
    });
    document.querySelectorAll("[data-goto-tab]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.getAttribute("data-goto-tab");
        setTab(tab);
        document.getElementById("profile")?.scrollIntoView({ behavior: "smooth" });
      });
    });
    window.addEventListener("hashchange", () => {
      if (location.hash.startsWith("#profile") || location.hash.startsWith("#account")) {
        setTab(tabFromLocation(), { updateHash: false });
        refreshProfile();
      }
    });
    setTab(tabFromLocation(), { updateHash: false });
  }

  function wireCalendarForm() {
    const form = document.getElementById("profile-cal-form");
    if (!form || form.dataset.wired) return;
    form.dataset.wired = "1";
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const note = document.getElementById("profile-cal-note");
      const title = document.getElementById("profile-cal-title")?.value.trim();
      const due = document.getElementById("profile-cal-due")?.value;
      if (!title || !due) return;
      if (!token() && !userId()) {
        if (note) note.textContent = t("profileLogin", "Zaloguj się");
        document.getElementById("btn-open-login")?.click();
        return;
      }
      const res = await fetch(`${API}/api/calendar`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({
          user_id: userId(),
          title,
          due_at: due,
          kind: "custom",
        }),
      });
      if (!res.ok) {
        if (note) note.textContent = "Error";
        return;
      }
      if (note) note.textContent = t("calAdded", "Dodano termin.");
      form.reset();
      refreshProfile();
    });
  }

  window.wniosekplPushTodos = pushTodos;
  window.wniosekplRunAction = runAction;
  window.wniosekplRefreshProfile = refreshProfile;
  window.wniosekplOpenProfileTab = (tab) => {
    setTab(tab || "overview");
    location.hash = `#profile?tab=${tab || "overview"}`;
    document.getElementById("profile")?.scrollIntoView({ behavior: "smooth" });
  };

  function boot() {
    if (location.hash === "#account") {
      history.replaceState(null, "", "#profile?tab=account");
    }
    wireTabs();
    wireCalendarForm();
    refreshProfile();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
