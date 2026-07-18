(() => {
  const API = "";
  const READY_KEY = "wniosekpl_mos_ready";
  const PURPOSE_KEY = "wniosekpl_mos_purpose";
  const TOKEN_KEY = "wniosekpl_session_token";
  const USER_KEY = "wniosekpl_web_user_id";

  function lang() {
    return localStorage.getItem("wniosekpl_lang") || "pl";
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

  function renderProgress(ready) {
    const done = ready.filter((s) => s.done).length;
    const el = document.getElementById("mos-progress");
    if (el) el.textContent = `${done} / ${ready.length}`;
  }

  function renderNext(next) {
    const box = document.getElementById("mos-next");
    const title = document.getElementById("mos-next-title");
    const body = document.getElementById("mos-next-body");
    const cta = document.getElementById("mos-next-cta");
    if (!box || !next) return;
    box.hidden = false;
    if (title) title.textContent = next.complete ? next.title : `Następny krok: ${next.title}`;
    if (body) body.textContent = next.hint || "";
    if (cta) {
      cta.href = next.link || "#mos";
      cta.textContent = next.complete ? "Otwórz MOS" : "Zrób ten krok";
      if ((next.link || "").startsWith("http")) {
        cta.target = "_blank";
        cta.rel = "noopener";
      } else {
        cta.removeAttribute("target");
      }
    }
  }

  function renderPurposeItems(purpose) {
    const box = document.getElementById("mos-purpose-items");
    if (!box || !purpose) {
      if (box) box.hidden = true;
      return;
    }
    box.hidden = false;
    box.innerHTML = `<strong></strong><ul></ul>`;
    box.querySelector("strong").textContent = purpose.title;
    const ul = box.querySelector("ul");
    (purpose.items || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
  }

  async function syncStep(stepId, done) {
    if (!token() && !userId()) return;
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

  async function loadMosGuide() {
    const qs = new URLSearchParams({ lang: lang() });
    if (userId()) qs.set("user_id", String(userId()));
    const res = await fetch(`${API}/api/mos/guide?${qs}`, {
      headers: token() ? { Authorization: `Bearer ${token()}` } : {},
    });
    if (!res.ok) return;
    const data = await res.json();
    const copy = data.copy || {};

    const setText = (id, value) => {
      const el = document.getElementById(id);
      if (el && value != null) el.textContent = value;
    };
    setText("mos-title", copy.title);
    setText("mos-sub", copy.sub);
    setText("mos-ready-title", copy.ready_title);
    setText("mos-purpose-title", copy.purpose_title);
    setText("mos-walk-title", copy.walk_title);
    setText("mos-disclaimer", copy.disclaimer);
    setText("mos-deadline-title", copy.deadline_title);
    setText("mos-deadline-hint", copy.deadline_hint);
    setText("mos-deadline-btn", copy.deadline_btn);
    setText("mos-next-title", copy.next_title);

    const open = document.getElementById("mos-open");
    if (open) {
      open.href = data.portal_url || "https://mos.cudzoziemcy.gov.pl";
      open.textContent = copy.cta || copy.open_mos || open.textContent;
    }
    const info = document.getElementById("mos-info");
    if (info) {
      info.href = data.info_url || info.href;
      info.textContent = copy.info || info.textContent;
    }

    const journey = document.getElementById("mos-journey");
    if (journey) {
      journey.innerHTML = "";
      (data.journey || []).forEach((step) => {
        const art = document.createElement("article");
        art.innerHTML = `<strong></strong><span></span>`;
        art.querySelector("strong").textContent = `${step.id}.`;
        art.querySelector("span").textContent = step.title;
        journey.appendChild(art);
      });
    }

    const walk = document.getElementById("mos-walk");
    if (walk) {
      walk.innerHTML = "";
      (data.walkthrough || []).forEach((step) => {
        const art = document.createElement("article");
        art.innerHTML = `<strong></strong><p></p><a class="ghost"></a>`;
        art.querySelector("strong").textContent = step.title;
        art.querySelector("p").textContent = step.body;
        const a = art.querySelector("a");
        a.href = step.href || "#mos";
        a.textContent = step.cta || "Dalej";
        if ((step.href || "").startsWith("http")) {
          a.target = "_blank";
          a.rel = "noopener";
        }
        walk.appendChild(art);
      });
    }

    const employer = data.employer_helper || {};
    setText("mos-employer-title", employer.title);
    setText("mos-employer-body", employer.body);
    const msg = document.getElementById("mos-employer-msg");
    if (msg) msg.textContent = employer.message || "";
    const copyBtn = document.getElementById("mos-employer-copy");
    if (copyBtn) {
      copyBtn.textContent = copy.copy_employer || "Kopiuj";
      copyBtn.onclick = async () => {
        try {
          await navigator.clipboard.writeText(employer.message || "");
          copyBtn.textContent = "✓";
          setTimeout(() => {
            copyBtn.textContent = copy.copy_employer || "Kopiuj";
          }, 1200);
        } catch (_) {
          copyBtn.textContent = "!";
        }
      };
    }

    let state = loadReady();
    if (data.saved_progress && typeof data.saved_progress === "object") {
      state = { ...state, ...data.saved_progress };
      saveReady(state);
    }

    const readyBox = document.getElementById("mos-ready");
    if (readyBox) {
      readyBox.innerHTML = "";
      const view = (data.ready || []).map((step) => ({
        ...step,
        done: !!state[step.id],
      }));
      const refreshNext = () => {
        const doneMap = Object.fromEntries(view.map((s) => [s.id, !!state[s.id]]));
        // recompute next locally from current checklist order
        const incomplete = view.find((s) => !doneMap[s.id]);
        if (incomplete) {
          renderNext({
            complete: false,
            title: incomplete.title,
            hint: incomplete.hint,
            link: incomplete.link,
          });
        } else {
          renderNext(data.next_action?.complete ? data.next_action : {
            complete: true,
            title: copy.open_mos || "Otwórz MOS",
            hint: data.next_action?.hint || "",
            link: data.portal_url,
          });
        }
      };

      view.forEach((step) => {
        const label = document.createElement("label");
        if (step.done) label.classList.add("done");
        label.innerHTML = `<input type="checkbox" /><div><span class="title"></span><span class="hint"></span></div>`;
        const input = label.querySelector("input");
        input.checked = step.done;
        label.querySelector(".title").textContent = step.title;
        label.querySelector(".hint").textContent = step.hint || "";
        input.addEventListener("change", () => {
          state[step.id] = input.checked;
          saveReady(state);
          label.classList.toggle("done", input.checked);
          renderProgress(
            view.map((s) => ({ ...s, done: s.id === step.id ? input.checked : !!state[s.id] }))
          );
          refreshNext();
          syncStep(step.id, input.checked);
        });
        readyBox.appendChild(label);
      });
      renderProgress(view);
      refreshNext();
    } else if (data.next_action) {
      renderNext(data.next_action);
    }

    const purposes = document.getElementById("mos-purposes");
    if (purposes) {
      purposes.innerHTML = "";
      const selected = localStorage.getItem(PURPOSE_KEY) || (data.purposes?.[0]?.id ?? "");
      let current = data.purposes?.find((p) => p.id === selected) || data.purposes?.[0];
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

  function wireDeadline() {
    document.getElementById("mos-deadline-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const note = document.getElementById("mos-deadline-note");
      const due = document.getElementById("mos-deadline-date")?.value;
      if (!due) return;
      if (!token() && !userId()) {
        if (note) note.textContent = "Zaloguj się (prawy górny róg), żeby zapisać przypomnienie.";
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
        if (note) note.textContent = data.detail || "Nie udało się dodać";
        return;
      }
      if (note) {
        note.textContent = data.reminder_id
          ? "Dodano termin końca pobytu + przypomnienie na 14 dni wcześniej."
          : "Dodano termin końca legalnego pobytu.";
      }
      // also mark legal_stay ready
      const state = loadReady();
      state.legal_stay = true;
      saveReady(state);
      loadMosGuide().catch(() => {});
    });
  }

  function wire() {
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
