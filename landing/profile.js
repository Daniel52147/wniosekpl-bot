(() => {
  const API = "";
  const TODO_KEY = "wniosekpl_profile_todos";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";
  const LANG_KEY = "wniosekpl_lang";

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

  function loadTodos() {
    try {
      return JSON.parse(localStorage.getItem(TODO_KEY) || "[]");
    } catch (_) {
      return [];
    }
  }

  function saveTodos(items) {
    localStorage.setItem(TODO_KEY, JSON.stringify(items.slice(0, 12)));
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

  function renderTodos() {
    const box = document.getElementById("profile-todo");
    if (!box) return;
    const open = loadTodos().filter((x) => !x.done);
    box.innerHTML = "";
    if (!open.length) {
      const p = document.createElement("p");
      p.className = "profile-empty";
      p.textContent = t("profileEmptyTodo", "Na razie pusto.");
      box.appendChild(p);
      return;
    }
    open.slice(0, 6).forEach((item) => {
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

  function renderMos(data) {
    const box = document.getElementById("profile-mos");
    if (!box) return;
    box.innerHTML = "";
    const nxt = data.mos_next || {};
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
    const box = document.getElementById("profile-cal");
    if (!box) return;
    box.innerHTML = "";
    if (!events || !events.length) {
      const p = document.createElement("p");
      p.className = "profile-empty";
      p.textContent = t("profileEmptyCal", "Brak terminów.");
      box.appendChild(p);
      return;
    }
    events.slice(0, 3).forEach((ev) => {
      const el = document.createElement("div");
      el.className = "profile-item";
      el.innerHTML = `<p></p><span class="muted"></span>`;
      el.querySelector("p").textContent = ev.title || "Termin";
      el.querySelector(".muted").textContent = ev.due_at || "";
      box.appendChild(el);
    });
  }

  async function refreshProfile() {
    renderTodos();
    const qs = new URLSearchParams({ lang: lang() });
    if (userId()) qs.set("user_id", String(userId()));
    const headers = {};
    if (token()) headers.Authorization = `Bearer ${token()}`;
    try {
      const res = await fetch(`${API}/api/resume?${qs}`, { headers });
      if (!res.ok) return;
      const data = await res.json();
      renderMos(data);
      renderCalendar(data.calendar || []);
      const sub = document.getElementById("profile-sub");
      if (sub && !data.logged_in) {
        // keep translated sub; optional login hint as title on rail
        document.getElementById("profile-rail")?.setAttribute(
          "data-sync",
          "local"
        );
      }
    } catch (_) {
      /* offline */
    }
  }

  window.wniosekplPushTodos = pushTodos;
  window.wniosekplRunAction = runAction;
  window.wniosekplRefreshProfile = refreshProfile;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", refreshProfile);
  } else {
    refreshProfile();
  }
})();
