(() => {
  const API = "";
  const READY_KEY = "wniosekpl_mos_ready";
  const PURPOSE_KEY = "wniosekpl_mos_purpose";

  function lang() {
    return localStorage.getItem("wniosekpl_lang") || "pl";
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

  async function loadMosGuide() {
    const res = await fetch(`${API}/api/mos/guide?lang=${encodeURIComponent(lang())}`);
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
    setText("mos-disclaimer", copy.disclaimer);

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

    const state = loadReady();
    const readyBox = document.getElementById("mos-ready");
    if (readyBox) {
      readyBox.innerHTML = "";
      const view = (data.ready || []).map((step) => ({
        ...step,
        done: !!state[step.id],
      }));
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
        });
        readyBox.appendChild(label);
      });
      renderProgress(view);
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

  function wire() {
    loadMosGuide().catch(() => {});
    window.addEventListener("wniosekpl:lang", () => loadMosGuide().catch(() => {}));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  // expose for index.html lang switcher if needed
  window.wniosekplLoadMos = loadMosGuide;
})();
