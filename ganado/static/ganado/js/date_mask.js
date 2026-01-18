(() => {
  const targets = document.querySelectorAll(
    'input[name$="fecha_nacimiento"], input.js-fecha'
  );

  const normalize = (value) => {
    const digits = value.replace(/\D/g, "").slice(0, 8);
    if (digits.length <= 2) return digits;
    if (digits.length <= 4) return `${digits.slice(0, 2)}/${digits.slice(2)}`;
    return `${digits.slice(0, 2)}/${digits.slice(2, 4)}/${digits.slice(4)}`;
  };

  targets.forEach((input) => {
    input.addEventListener("input", (event) => {
      const caret = input.selectionStart || 0;
      const before = input.value;
      input.value = normalize(input.value);
      if (before !== input.value) {
        input.setSelectionRange(caret, caret);
      }
    });

    input.addEventListener("paste", (event) => {
      event.preventDefault();
      const text = (event.clipboardData || window.clipboardData).getData("text");
      input.value = normalize(text);
    });
  });
})();
