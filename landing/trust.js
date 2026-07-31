(() => {
  const API = "";

  function lang() {
    return localStorage.getItem("wniosekpl_lang") || "pl";
  }

  function fillTrust(root, data) {
    if (!root || !data) return;
    const copy = data.copy || {};
    const set = (sel, text) => {
      const el = root.querySelector(sel) || document.getElementById(sel.replace("#", ""));
      if (el && text != null) el.textContent = text;
    };
    set("#trust-kicker", copy.kicker);
    set("#trust-title", copy.title);
    set("#trust-body", copy.body);
    set("#trust-gov-title", copy.gov_title);
    set("#trust-faq-title", copy.faq_title);
    set("#trust-contact-label", copy.contact);

    const contact = root.querySelector("#trust-contact") || document.getElementById("trust-contact");
    if (contact) {
      contact.href = `mailto:${data.contact_email || "hello@wniosekpl.pl"}`;
      contact.textContent = copy.contact_cta || data.contact_email || "Kontakt";
    }

    const links = root.querySelector("#trust-gov-links") || document.getElementById("trust-gov-links");
    if (links) {
      links.innerHTML = "";
      (data.gov_links || []).forEach((item) => {
        const a = document.createElement("a");
        a.href = item.url;
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = item.label;
        links.appendChild(a);
      });
    }

    const faq = root.querySelector("#trust-faq") || document.getElementById("trust-faq");
    if (faq) {
      faq.innerHTML = "";
      (data.faq || []).forEach((item) => {
        const details = document.createElement("details");
        details.innerHTML = "<summary></summary><p></p>";
        details.querySelector("summary").textContent = item.q;
        details.querySelector("p").textContent = item.a;
        faq.appendChild(details);
      });
    }
  }

  async function loadTrust(rootSelector) {
    const root = rootSelector
      ? document.querySelector(rootSelector)
      : document.getElementById("trust") || document.getElementById("trust-cabinet");
    if (!root) return;
    try {
      const res = await fetch(`${API}/api/trust?lang=${lang()}`);
      if (!res.ok) return;
      fillTrust(root, await res.json());
    } catch (_) {
      /* offline */
    }
  }

  function wire() {
    loadTrust("#trust");
    loadTrust("#trust-cabinet");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  window.wniosekplLoadTrust = loadTrust;
})();
