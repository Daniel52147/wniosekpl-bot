(() => {
  const API = "";
  const TODO_KEY = "wniosekpl_profile_todos";
  const READY_KEY = "wniosekpl_mos_ready";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";
  const LANG_KEY = "wniosekpl_lang";
  const TAB_KEY = "wniosekpl_profile_tab";

  const TAB_ALIASES = {
    overview: "now",
    tasks: "now",
    mos: "now",
    calendar: "now",
    billing: "account",
    now: "now",
    docs: "docs",
    documents: "docs",
    account: "account",
  };

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

  function normalizeTab(tabId) {
    return TAB_ALIASES[tabId] || "now";
  }

  function setTab(tabId, { updateHash = true } = {}) {
    const id = normalizeTab(tabId);
    localStorage.setItem(TAB_KEY, id);
    document.querySelectorAll("[data-profile-tab]").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-profile-tab") === id);
    });
    document.querySelectorAll("[data-profile-panel]").forEach((panel) => {
      panel.hidden = panel.getAttribute("data-profile-panel") !== id;
    });
    if (updateHash && (location.pathname === "/profile" || location.pathname === "/app")) {
      const url = new URL(location.href);
      url.searchParams.set("tab", id);
      url.hash = "";
      history.replaceState(null, "", url.pathname + url.search);
    }
  }

  function tabFromLocation() {
    const search = new URLSearchParams(location.search || "");
    if (search.get("tab")) return normalizeTab(search.get("tab"));
    const hash = location.hash || "";
    if (hash.startsWith("#account") || hash.startsWith("#pricing")) return "account";
    if (hash.startsWith("#documents") || hash.startsWith("#docs")) return "docs";
    if (hash.startsWith("#assistant") || hash.startsWith("#mos") || hash.startsWith("#profile")) {
      return "now";
    }
    return normalizeTab(localStorage.getItem(TAB_KEY) || "now");
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
  }

  function markTodoDone(key) {
    const list = loadTodos().map((item) =>
      item.key === key ? { ...item, done: true, updated: Date.now() } : item
    );
    saveTodos(list);
    renderTodos();
  }

  function runAction(action) {
    if (!action) return;
    if (action.type === "open_doc" && window.wniosekplOpenDoc) {
      setTab("docs");
      window.wniosekplOpenDoc(action.id);
      return;
    }
    if (action.type === "goto" || action.href) {
      const href = action.href || "#profile";
      if (href.includes("mos") || href === "#mos") {
        setTab("now");
        document.getElementById("mos-next")?.scrollIntoView({ behavior: "smooth" });
        return;
      }
      if (href.includes("document") || href.includes("#documents")) {
        setTab("docs");
        return;
      }
      if (href.startsWith("#")) {
        location.hash = href;
      } else if (href.startsWith("http")) {
        window.open(href, "_blank", "noopener");
      }
    }
  }

  function renderTodos() {
    const box = document.getElementById("profile-todo");
    if (!box) return;
    const open = loadTodos().filter((x) => !x.done);
    box.innerHTML = "";
    if (!open.length) {
      const p = document.createElement("p");
      p.className = "profile-empty";
      p.textContent = t("profileEmptyTodo", "Brak otwartych zadań z AI.");
      box.appendChild(p);
      return;
    }
    open.slice(0, 5).forEach((item) => {
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

  function renderCalendar(events) {
    const box = document.getElementById("profile-cal");
    if (!box) return;
    box.innerHTML = "";
    if (!events || !events.length) return;
    events.slice(0, 2).forEach((ev) => {
      const el = document.createElement("div");
      el.className = "profile-item";
      el.innerHTML = `<p></p><span class="muted"></span>`;
      el.querySelector("p").textContent = ev.title || "Termin";
      el.querySelector(".muted").textContent = ev.due_at || "";
      box.appendChild(el);
    });
  }

  function applyCopy() {
    const map = [
      ["profile-title", "profileTitle"],
      ["profile-sub", "profileSub"],
      ["tab-now", "tabNow"],
      ["tab-docs", "tabDocs"],
      ["tab-account", "tabAccount"],
      ["now-checklist-title", "mosTabTitle"],
      ["now-side-title", "nowSideTitle"],
      ["now-deadline-title", "deadline_title"],
      ["app-crumb-text", "appCrumb"],
      ["app-home-link", "appHome"],
    ];
    map.forEach(([id, key]) => {
      const el = document.getElementById(id);
      const val = t(key, null);
      if (el && val) el.textContent = val;
    });
    // home link keep arrow
    const home = document.getElementById("app-home-link");
    if (home) home.textContent = t("appHome", "← Strona główna");
  }

  async function refreshProfile() {
    applyCopy();
    renderTodos();
    const qs = new URLSearchParams({ lang: lang() });
    if (userId()) qs.set("user_id", String(userId()));
    try {
      const res = await fetch(`${API}/api/resume?${qs}`, { headers: authHeaders(false) });
      if (res.ok) {
        const data = await res.json();
        renderCalendar(data.calendar || []);
      }
    } catch (_) {
      /* offline */
    }
    if (window.wniosekplLoadMos) {
      try {
        await window.wniosekplLoadMos();
      } catch (_) {
        /* ignore */
      }
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
    document.querySelectorAll("[data-profile-tab-link]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        setTab(a.getAttribute("data-profile-tab-link"));
      });
    });
    window.addEventListener("hashchange", () => {
      setTab(tabFromLocation(), { updateHash: false });
    });
    setTab(tabFromLocation(), { updateHash: false });
  }

  window.wniosekplPushTodos = pushTodos;
  window.wniosekplRunAction = runAction;
  window.wniosekplRefreshProfile = refreshProfile;
  window.wniosekplSetProfileTab = (tab) => setTab(tab || "now");
  window.wniosekplOpenProfileTab = (tab) => {
    setTab(tab || "now");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  function boot() {
    if (location.hash === "#account") {
      history.replaceState(null, "", "/profile?tab=account");
    }
    wireTabs();
    refreshProfile();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
