(() => {
  const API = "";
  const userId = () => {
    const key = "wniosekpl_web_user_id";
    let id = Number(localStorage.getItem(key));
    if (!Number.isInteger(id) || id <= 0) {
      id = Math.floor(Math.random() * 900000000) + 100000000;
      localStorage.setItem(key, String(id));
    }
    return id;
  };

  const lang = () => localStorage.getItem("wniosekpl_lang") || "pl";

  async function refreshCabinet() {
    const box = document.getElementById("cabinet-box");
    if (!box) return;
    const res = await fetch(`${API}/api/cabinet/${userId()}`);
    if (!res.ok) return;
    const data = await res.json();
    const plan = data.plan || {};
    box.innerHTML = `
      <div class="plan featured">
        <strong>Plan: ${plan.plan || "free"}</strong>
        <p>AI today: ${plan.ai_used_today || 0}${plan.unlimited ? " (unlimited)" : ` / ${plan.ai_limit || 5}`}</p>
        <p>Payments: ${(data.payments || []).length} · Uploads: ${(data.uploads || []).length} · Calendar: ${(data.calendar || []).length}</p>
      </div>
    `;
    const karta = document.getElementById("karta-steps");
    if (karta) {
      karta.innerHTML = "";
      (data.karta || []).forEach((step) => {
        const row = document.createElement("label");
        row.style.display = "flex";
        row.style.gap = "0.55rem";
        row.style.margin = "0.35rem 0";
        row.innerHTML = `<input type="checkbox" ${step.done ? "checked" : ""} /><span></span>`;
        row.querySelector("span").textContent = step.title;
        row.querySelector("input").addEventListener("change", async (e) => {
          await fetch(`${API}/api/karta/step`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: userId(),
              step_id: step.id,
              done: e.target.checked,
            }),
          });
        });
        karta.appendChild(row);
      });
    }
    const cal = document.getElementById("calendar-list");
    if (cal) {
      cal.innerHTML = "";
      (data.calendar || []).forEach((ev) => {
        const li = document.createElement("div");
        li.className = "doc";
        li.innerHTML = `<strong></strong><p></p>`;
        li.querySelector("strong").textContent = ev.title;
        li.querySelector("p").textContent = `${ev.due_at} · ${ev.kind}`;
        cal.appendChild(li);
      });
    }
  }

  async function checkout(product) {
    const res = await fetch(`${API}/api/billing/checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId(), product }),
    });
    const data = await res.json();
    if (data.checkout_url) window.location.href = data.checkout_url;
  }

  async function loadServices() {
    const box = document.getElementById("services-box");
    if (!box) return;
    const res = await fetch(`${API}/api/services?city=Warszawa`);
    const data = await res.json();
    box.innerHTML = "";
    data.slice(0, 6).forEach((item) => {
      const el = document.createElement("article");
      el.className = "doc";
      el.innerHTML = `<strong></strong><p></p><a target="_blank" rel="noopener"></a>`;
      el.querySelector("strong").textContent = item.name;
      el.querySelector("p").textContent = `${item.city} · ${item.address}`;
      const a = el.querySelector("a");
      a.href = item.url;
      a.textContent = item.category;
      box.appendChild(el);
    });
  }

  async function generateLetter(ev) {
    ev.preventDefault();
    const out = document.getElementById("letter-out");
    const payload = {
      user_id: userId(),
      lang: lang(),
      name: document.getElementById("letter-name").value.trim(),
      city: document.getElementById("letter-city").value.trim() || "Warszawa",
      office: document.getElementById("letter-office").value.trim(),
      case_no: document.getElementById("letter-case").value.trim() || "brak",
      topic: document.getElementById("letter-topic").value.trim(),
      content: document.getElementById("letter-content").value.trim(),
    };
    const res = await fetch(`${API}/api/letters/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    out.textContent = data.letter || "Error";
  }

  async function analyzeUpload(ev) {
    ev.preventDefault();
    const fileInput = document.getElementById("upload-file");
    const out = document.getElementById("upload-out");
    if (!fileInput.files.length) return;
    const body = new FormData();
    body.append("file", fileInput.files[0]);
    out.textContent = "Analyzing…";
    const res = await fetch(
      `${API}/api/uploads/analyze?user_id=${userId()}&lang=${lang()}`,
      { method: "POST", body }
    );
    const data = await res.json();
    out.textContent = data.explanation || JSON.stringify(data);
    refreshCabinet();
  }

  async function addCalendar(ev) {
    ev.preventDefault();
    const title = document.getElementById("cal-title").value.trim();
    const due = document.getElementById("cal-due").value;
    if (!title || !due) return;
    await fetch(`${API}/api/calendar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId(),
        title,
        due_at: due,
        kind: "custom",
      }),
    });
    refreshCabinet();
  }

  function wire() {
    document.getElementById("pay-ai")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("ai_subscription");
    });
    document.getElementById("pay-review")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("human_review");
    });
    document.getElementById("ai-link")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("ai_subscription");
    });
    document.getElementById("review-link")?.addEventListener("click", (e) => {
      e.preventDefault();
      checkout("human_review");
    });
    document.getElementById("letter-form")?.addEventListener("submit", generateLetter);
    document.getElementById("upload-form")?.addEventListener("submit", analyzeUpload);
    document.getElementById("cal-form")?.addEventListener("submit", addCalendar);
    document.getElementById("seed-cal")?.addEventListener("click", async (e) => {
      e.preventDefault();
      await fetch(`${API}/api/demo/seed-calendar/${userId()}`);
      refreshCabinet();
    });
    refreshCabinet();
    loadServices();
    const params = new URLSearchParams(location.search);
    if (params.get("billing") === "success") {
      const note = document.getElementById("billing-note");
      if (note) note.textContent = `Payment success: ${params.get("product") || ""}`;
      refreshCabinet();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
