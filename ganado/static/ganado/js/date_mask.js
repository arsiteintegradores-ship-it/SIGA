(function ($) {
    "use strict";
  
    function applyMaskTo(el) {
      if (!el) return;
  
      el.setAttribute("autocomplete", "off");
      el.setAttribute("placeholder", "DD/MM/AAAA");
  
      const format = () => {
        let v = el.value.replace(/\D/g, "").slice(0, 8); // ddmmyyyy
  
        if (v.length >= 5) el.value = v.slice(0, 2) + "/" + v.slice(2, 4) + "/" + v.slice(4);
        else if (v.length >= 3) el.value = v.slice(0, 2) + "/" + v.slice(2);
        else el.value = v;
      };
  
      el.addEventListener("input", format);
      el.addEventListener("paste", () => setTimeout(format, 0));
    }
  
    // Django Admin: usa jQuery propio (django.jQuery)
    $(function () {
      // Cubre TODOS los casos:
      // 1) el id normal
      // 2) por nombre del campo
      // 3) por clase del admin (vDateField)
      const el =
        document.getElementById("id_fecha_nacimiento") ||
        document.querySelector('input[name="fecha_nacimiento"]') ||
        document.querySelector("input.vDateField");
  
      applyMaskTo(el);
    });
  })(django.jQuery);
  