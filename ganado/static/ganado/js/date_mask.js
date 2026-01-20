(function () {
  "use strict";

  function onlyDigits(s) {
    return (s || "").replace(/\D/g, "");
  }

  function formatDDMMYYYY(digits) {
    const d = digits.slice(0, 2);
    const m = digits.slice(2, 4);
    const y = digits.slice(4, 8);

    let out = "";
    if (d.length) out += d;
    if (m.length) out += (out.length ? "/" : "") + m;
    if (y.length) out += (out.length ? "/" : "") + y;
    return out;
  }

  function caretFromDigitsCount(formattedValue, digitsCount) {
    if (digitsCount <= 0) return 0;
    let count = 0;
    for (let i = 0; i < formattedValue.length; i++) {
      if (/\d/.test(formattedValue[i])) count++;
      if (count >= digitsCount) return i + 1;
    }
    return formattedValue.length;
  }

  function applyMask(input) {
    const prevValue = input.value || "";
    const prevPos = input.selectionStart || 0;

    const digitsBeforeCursor = onlyDigits(prevValue.slice(0, prevPos)).length;
    const digits = onlyDigits(prevValue).slice(0, 8);
    const formatted = formatDDMMYYYY(digits);

    input.value = formatted;

    const newPos = caretFromDigitsCount(formatted, digitsBeforeCursor);
    input.setSelectionRange(newPos, newPos);
  }

  function attach(input) {
    if (input.dataset.dateMaskAttached === "1") return;
    input.dataset.dateMaskAttached = "1";

    input.setAttribute("inputmode", "numeric");
    input.setAttribute("autocomplete", "off");
    input.setAttribute("placeholder", input.getAttribute("placeholder") || "dd/mm/aaaa");

    input.addEventListener("input", function () {
      applyMask(input);
    });

    input.addEventListener("blur", function () {
      if (input.value && input.value.length !== 10) {
        applyMask(input);
      }
    });

    if (input.value) applyMask(input);
  }

  function init() {
    // Django admin: el input real suele ser id_fecha_nacimiento
    const direct = document.querySelectorAll("input#id_fecha_nacimiento");
    for (let i = 0; i < direct.length; i++) attach(direct[i]);

    // También soporta clase genérica
    const generic = document.querySelectorAll("input.js-date-mask");
    for (let j = 0; j < generic.length; j++) attach(generic[j]);

    // Por si se agregan inlines dinámicamente
    const observer = new MutationObserver(function (mutations) {
      for (const m of mutations) {
        for (const node of m.addedNodes || []) {
          if (!node || !node.querySelectorAll) continue;
          const newInputs = node.querySelectorAll("input#id_fecha_nacimiento, input.js-date-mask");
          for (let k = 0; k < newInputs.length; k++) attach(newInputs[k]);
        }
      }
    });

    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
