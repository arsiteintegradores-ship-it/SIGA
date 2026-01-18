from datetime import timedelta

from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


from .models import (
    GanadoAnimal, GanadoFinca, GanadoLote,
    GanadoRaza, GanadoColor, GanadoProductor,
    GanadoUpp, GanadoRegistro,
)

admin.site.site_header = "SIGA - Administración"
admin.site.site_title = "SIGA Admin"
admin.site.index_title = "Captura guiada (recomendado): 1) Animal  2) Productores/UPP  3) Fincas  4) Lotes 5) Razas/Colores"


# =========================
# Filtros por rango (sin paquetes)
# =========================

class FechaNacimientoFilter(admin.SimpleListFilter):
    title = "Fecha nacimiento (rango)"
    parameter_name = "fn_rango"

    def lookups(self, request, model_admin):
        return (
            ("hoy", "Hoy"),
            ("30", "Últimos 30 días"),
            ("90", "Últimos 90 días"),
            ("365", "Últimos 365 días"),
            ("ant", "Más de 365 días"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset

        today = timezone.localdate()
        if val == "hoy":
            return queryset.filter(fecha_nacimiento=today)
        if val in ("30", "90", "365"):
            days = int(val)
            return queryset.filter(fecha_nacimiento__gte=today - timedelta(days=days))
        if val == "ant":
            return queryset.filter(fecha_nacimiento__lt=today - timedelta(days=365))
        return queryset


class PesoNacimientoFilter(admin.SimpleListFilter):
    title = "Peso nacimiento (kg)"
    parameter_name = "pn_rango"

    def lookups(self, request, model_admin):
        return (
            ("0-25", "0 a 25"),
            ("25-35", "25 a 35"),
            ("35-45", "35 a 45"),
            ("45+", "45+"),
            ("null", "Sin dato"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        if val == "null":
            return queryset.filter(peso_nacimiento__isnull=True)
        if val == "45+":
            return queryset.filter(peso_nacimiento__gte=45)
        a, b = val.split("-")
        return queryset.filter(peso_nacimiento__gte=float(a), peso_nacimiento__lt=float(b))


class PesoDesteteFilter(admin.SimpleListFilter):
    title = "Peso destete (kg)"
    parameter_name = "pd_rango"

    def lookups(self, request, model_admin):
        return (
            ("0-150", "0 a 150"),
            ("150-200", "150 a 200"),
            ("200-250", "200 a 250"),
            ("250+", "250+"),
            ("null", "Sin dato"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        if val == "null":
            return queryset.filter(peso_destete__isnull=True)
        if val == "250+":
            return queryset.filter(peso_destete__gte=250)
        a, b = val.split("-")
        return queryset.filter(peso_destete__gte=float(a), peso_destete__lt=float(b))


# =========================
# Exportar a Excel (XLSX)
# =========================
def export_animales_xlsx(modeladmin, request, queryset):
    """
    Exporta animales seleccionados a XLSX.
    Incluye Edad (texto) y Etapa de desarrollo.
    """
    try:
        from openpyxl import Workbook
    except ImportError:
        return HttpResponse(
            "Falta openpyxl. Instala con: pip install openpyxl",
            content_type="text/plain",
            status=500,
        )

    wb = Workbook()
    ws = wb.active
    ws.title = "Animales"

    headers = [
        "ID", "Id interno", "Id SINIGA", "Nombre", "Sexo",
        "Raza", "Color", "Finca", "Lote", "Estado",
        "Fecha nac",
        "Edad (Años, Meses, Días)", "Etapa de desarrollo",
        "Peso nac", "Peso destete",
        "Padre", "Madre", "Productor", "UPP", "Notas",
        "Creado", "Actualizado",
    ]
    ws.append(headers)

    queryset = queryset.select_related(
        "raza", "color", "finca", "lote", "padre", "madre", "productor", "upp"
    )

    for a in queryset:
        # OJO: usar 'edad' (texto). NO usar 'edad_amd' (tupla).
        edad_txt = str(getattr(a, "edad", "") or "")
        etapa_txt = str(getattr(a, "etapa_desarrollo", "") or "")

        ws.append([
            a.id,
            a.id_interno,
            a.id_siniga,
            a.nombre_bov,
            a.sexo,
            str(a.raza) if a.raza_id else "",
            str(a.color) if a.color_id else "",
            str(a.finca) if a.finca_id else "",
            str(a.lote) if a.lote_id else "",
            a.estado,
            a.fecha_nacimiento.isoformat() if a.fecha_nacimiento else "",
            edad_txt,
            etapa_txt,
            float(a.peso_nacimiento) if a.peso_nacimiento is not None else "",
            float(a.peso_destete) if a.peso_destete is not None else "",
            str(a.padre) if a.padre_id else "",
            str(a.madre) if a.madre_id else "",
            str(a.productor) if a.productor_id else "",
            str(a.upp) if a.upp_id else "",
            a.notas or "",
            a.created_at.isoformat() if a.created_at else "",
            a.updated_at.isoformat() if a.updated_at else "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="siga_animales.xlsx"'
    wb.save(response)
    return response

export_animales_xlsx.short_description = "Exportar animales seleccionados a Excel (XLSX)"


def imprimir_reporte_animales_pdf(modeladmin, request, queryset):
    """
    Genera un PDF listo para imprimir de los animales seleccionados.
    Incluye Edad (texto) y Etapa.
    """
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_animales.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Estilos básicos
    margin_x = 1.5 * cm
    y = height - 2 * cm
    line_h = 14

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "SIGA - Reporte de Animales")
    y -= 18

    # Fecha
    c.setFont("Helvetica", 10)
    c.drawString(margin_x, y, f"Fecha: {timezone.localdate().isoformat()}")
    y -= 18

    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 9)
    headers = ["ID", "ID interno", "Nombre", "Sexo", "F. Nac", "Edad", "Etapa", "Finca", "Lote", "Estado"]
    cols = [35, 70, 110, 35, 55, 95, 80, 90, 70, 55]  # anchos aprox
    x = margin_x

    for h, w in zip(headers, cols):
        c.drawString(x, y, h)
        x += w

    y -= 10
    c.line(margin_x, y, width - margin_x, y)
    y -= 14

    # Optimiza FKs
    queryset = queryset.select_related("finca", "lote")

    c.setFont("Helvetica", 8)

    def nueva_pagina():
        nonlocal y
        c.showPage()
        y = height - 2 * cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_x, y, "SIGA - Reporte de Animales (continuación)")
        y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(margin_x, y, f"Fecha: {timezone.localdate().isoformat()}")
        y -= 18

        c.setFont("Helvetica-Bold", 9)
        x2 = margin_x
        for h2, w2 in zip(headers, cols):
            c.drawString(x2, y, h2)
            x2 += w2
        y -= 10
        c.line(margin_x, y, width - margin_x, y)
        y -= 14
        c.setFont("Helvetica", 8)

    for a in queryset:
        if y < 2.2 * cm:
            nueva_pagina()

        # datos
        fila = [
            str(a.id),
            str(a.id_interno or ""),
            str(a.nombre_bov or ""),
            str(a.sexo or ""),
            a.fecha_nacimiento.isoformat() if a.fecha_nacimiento else "",
            str(getattr(a, "edad", "") or ""),                 # texto "X años, Y meses..."
            str(getattr(a, "etapa_desarrollo", "") or ""),
            str(a.finca) if a.finca_id else "",
            str(a.lote) if a.lote_id else "",
            str(a.estado or ""),
        ]

        x = margin_x
        for val, w in zip(fila, cols):
            # recorte simple para que no se desborde (puedes ajustar)
            txt = val[:18] + "…" if len(val) > 19 and w <= 95 else val
            c.drawString(x, y, txt)
            x += w

        y -= line_h

    # Pie
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(margin_x, 1.5 * cm, "Generado por SIGA")
    c.save()
    return response

imprimir_reporte_animales_pdf.short_description = "Imprimir reporte PDF (seleccionados)"




# =========================
# Acciones rápidas (estado)
# =========================
def set_estado(estado):
    def _action(modeladmin, request, queryset):
        queryset.update(estado=estado)

    _action.short_description = f"Marcar como {estado}"
    _action.__name__ = f"marcar_{estado.lower()}"
    return _action


class GanadoAnimalAdminForm(forms.ModelForm):
    class Meta:
        model = GanadoAnimal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.finca_id:
            self.fields["lote"].queryset = GanadoLote.objects.filter(finca_id=self.instance.finca_id)
        else:
            self.fields["lote"].queryset = GanadoLote.objects.none()

    def clean(self):
        cleaned = super().clean()

        finca = cleaned.get("finca")
        lote = cleaned.get("lote")
        fecha_nacimiento = cleaned.get("fecha_nacimiento")
        padre = cleaned.get("padre")
        madre = cleaned.get("madre")

        if fecha_nacimiento and fecha_nacimiento > timezone.localdate():
            self.add_error("fecha_nacimiento", "La fecha de nacimiento no puede ser futura.")

        if finca and lote and lote.finca_id != finca.id:
            self.add_error("lote", "Ese lote no pertenece a la finca seleccionada.")

        if padre and getattr(padre, "sexo", None) and padre.sexo != "M":
            self.add_error("padre", "El PADRE debe ser sexo 'M' (macho).")

        if madre and getattr(madre, "sexo", None) and madre.sexo != "H":
            self.add_error("madre", "La MADRE debe ser sexo 'H' (hembra).")

        if self.instance and self.instance.pk:
            if padre and padre.pk == self.instance.pk:
                self.add_error("padre", "Un animal no puede ser su propio padre.")
            if madre and madre.pk == self.instance.pk:
                self.add_error("madre", "Un animal no puede ser su propia madre.")

        return cleaned


# =========================
# Admins de catálogos
# =========================
@admin.register(GanadoFinca)
class GanadoFincaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "ubicacion", "telefono", "activo")
    search_fields = ("nombre", "ubicacion", "propietario", "telefono")
    list_filter = ("activo",)
    ordering = ("nombre",)


@admin.register(GanadoLote)
class GanadoLoteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "finca", "activo")
    search_fields = ("nombre", "descripcion", "finca__nombre")
    list_filter = ("activo", "finca")
    ordering = ("finca__nombre", "nombre")
    autocomplete_fields = ("finca",)


@admin.register(GanadoRaza)
class GanadoRazaAdmin(admin.ModelAdmin):
    list_display = ("id", "raza")
    search_fields = ("raza",)
    ordering = ("raza",)


@admin.register(GanadoColor)
class GanadoColorAdmin(admin.ModelAdmin):
    list_display = ("id", "color")
    search_fields = ("color",)
    ordering = ("color",)


@admin.register(GanadoProductor)
class GanadoProductorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido_paterno", "apellido_materno", "telefono", "email", "activo")
    search_fields = ("nombre", "apellido_paterno", "apellido_materno", "telefono", "email")
    list_filter = ("activo",)
    ordering = ("nombre", "apellido_paterno", "apellido_materno")


@admin.register(GanadoUpp)
class GanadoUppAdmin(admin.ModelAdmin):
    list_display = ("id", "clave", "finca", "productor")
    search_fields = ("clave", "finca__nombre", "productor__nombre", "productor__apellido_paterno", "productor__apellido_materno")
    list_filter = ("finca", "productor")
    ordering = ("finca__nombre", "clave")
    autocomplete_fields = ("finca", "productor")


@admin.register(GanadoRegistro)
class GanadoRegistroAdmin(admin.ModelAdmin):
    list_display = ("id", "id_bovino", "id_madre", "id_padre")
    search_fields = ("id_bovino", "id_madre", "id_padre", "id_abuelo", "id_abuela")
    ordering = ("-id",)


# =========================
# Admin principal: ANIMAL
# =========================
@admin.register(GanadoAnimal)
class GanadoAnimalAdmin(admin.ModelAdmin):
    form = GanadoAnimalAdminForm

    list_display = (
        "id", "id_interno", "id_siniga", "nombre_bov", "sexo",
        "fecha_nacimiento", "edad", "etapa_desarrollo",
        "raza", "color", "finca", "lote", "estado",
        "peso_nacimiento", "peso_destete",
        "created_at", "updated_at",
    )

    search_fields = (
        "id_interno", "id_siniga", "nombre_bov",
        "raza__raza", "color__color",
        "finca__nombre", "lote__nombre",
    )

    list_filter = (
        "sexo", "estado", "raza", "color", "finca", "lote",
        FechaNacimientoFilter, PesoNacimientoFilter, PesoDesteteFilter
    )

    ordering = ("-id",)

    autocomplete_fields = ("productor", "upp", "color", "raza", "registro", "finca", "lote", "padre", "madre")

    readonly_fields = ("edad", "etapa_desarrollo", "created_at", "updated_at")

    actions = [
        set_estado("ACTIVO"),
        set_estado("VENDIDO"),
        set_estado("MUERTO"),
        set_estado("BAJA"),
        export_animales_xlsx,
        imprimir_reporte_animales_pdf,
    ]
        
    fieldsets = (
        ("Identificación", {"fields": ("id_interno", "id_siniga", "nombre_bov", "sexo")}),
        ("Origen / Ubicación", {"fields": ("finca", "lote", "productor", "upp")}),
        ("Características", {"fields": ("raza", "color", "estado", "notas")}),
        ("Pesos / Fechas", {"fields": ("fecha_nacimiento", "peso_nacimiento", "peso_destete")}),
        ("Edad / Etapa (calculado)", {"fields": ("edad", "etapa_desarrollo")}),
        ("Genealogía", {"fields": ("padre", "madre", "registro")}),
        ("Sistema", {"fields": ("created_at", "updated_at")}),
    )
