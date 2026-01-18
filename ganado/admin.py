
# Register your models here.

from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django import forms


from .models import (
    GanadoAnimal, GanadoFinca, GanadoLote,
    GanadoRaza, GanadoColor, GanadoProductor,
    GanadoUpp, GanadoRegistro,
)
from .utils import DATE_INPUT_FORMATS, parse_es_date

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

    # Ajusta rangos a tu rancho si quieres
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

    # Ajusta rangos a tu rancho si quieres
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
    Requiere openpyxl (ya lo instalaste si usas pandas/openpyxl).
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
        "Fecha nac", "Peso nac", "Peso destete",
        "Padre", "Madre", "Productor", "UPP", "Notas",
        "Creado", "Actualizado",
    ]
    ws.append(headers)

    # Optimiza consultas para FKs
    queryset = queryset.select_related(
        "raza", "color", "finca", "lote", "padre", "madre", "productor", "upp"
    )

    for a in queryset:
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


# =========================
# Acciones rápidas (estado)
# =========================
def set_estado(estado):
    def _action(modeladmin, request, queryset):
        queryset.update(estado=estado)

    _action.short_description = f"Marcar como {estado}"
    _action.__name__ = f"marcar_{estado.lower()}"  # ✅ nombre único para Django
    return _action


class GanadoAnimalAdminForm(forms.ModelForm):
    
    class Meta:
        model = GanadoAnimal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar lote por finca (cuando se edita)
        if self.instance and self.instance.finca_id:
            self.fields["lote"].queryset = GanadoLote.objects.filter(finca_id=self.instance.finca_id)
        else:
            # En alta nueva: no mostrar todos los lotes
            self.fields["lote"].queryset = GanadoLote.objects.none()
        if "fecha_nacimiento" in self.fields:
            self.fields["fecha_nacimiento"].input_formats = DATE_INPUT_FORMATS
            self.fields["fecha_nacimiento"].widget.attrs.update(
                {"placeholder": "dd/mm/aaaa", "inputmode": "numeric"}
            )

    def clean_fecha_nacimiento(self):
        raw_value = self.data.get("fecha_nacimiento", "")
        return parse_es_date(raw_value)

    def _clean_decimal(self, field_name: str):
        raw_value = self.data.get(field_name, "")
        if raw_value in ("", None):
            return None
        if isinstance(raw_value, (int, float, Decimal)):
            return raw_value
        normalized = str(raw_value).replace(",", ".").strip()
        try:
            return Decimal(normalized)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError("Ingresa un número válido.")

    def clean_peso_nacimiento(self):
        return self._clean_decimal("peso_nacimiento")

    def clean_peso_destete(self):
        return self._clean_decimal("peso_destete")

    def clean(self):
        cleaned = super().clean()

        finca = cleaned.get("finca")
        lote = cleaned.get("lote")
        fecha_nacimiento = cleaned.get("fecha_nacimiento")
        padre = cleaned.get("padre")
        madre = cleaned.get("madre")

        # 1) Fecha no futura
        if fecha_nacimiento and fecha_nacimiento > timezone.localdate():
            self.add_error("fecha_nacimiento", "La fecha de nacimiento no puede ser futura.")

        # 2) Lote debe pertenecer a la finca
        if finca and lote and lote.finca_id != finca.id:
            self.add_error("lote", "Ese lote no pertenece a la finca seleccionada.")

        # 3) Padre debe ser macho
        if padre and getattr(padre, "sexo", None) and padre.sexo != "M":
            self.add_error("padre", "El PADRE debe ser sexo 'M' (macho).")

        # 4) Madre debe ser hembra
        if madre and getattr(madre, "sexo", None) and madre.sexo != "H":
            self.add_error("madre", "La MADRE debe ser sexo 'H' (hembra).")

        # 5) No se puede poner a sí mismo como padre/madre
        if self.instance and self.instance.pk:
            if padre and padre.pk == self.instance.pk:
                self.add_error("padre", "Un animal no puede ser su propio padre.")
            if madre and madre.pk == self.instance.pk:
                self.add_error("madre", "Un animal no puede ser su propia madre.")

        return cleaned

    class Media:
        js = ("ganado/js/date_mask.js",)




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
        "raza", "finca", "lote", "estado",
        "fecha_nacimiento", "peso_nacimiento", "peso_destete", "edad_formateada",
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

    readonly_fields = ("created_at", "updated_at", "edad_formateada")

    actions = [
        set_estado("ACTIVO"),
        set_estado("VENDIDO"),
        set_estado("MUERTO"),
        set_estado("BAJA"),
        export_animales_xlsx,
    ]

    fieldsets = (
        ("Identificación", {"fields": ("id_interno", "id_siniga", "nombre_bov", "sexo")}),
        ("Origen / Ubicación", {"fields": ("finca", "lote", "productor", "upp")}),
        ("Características", {"fields": ("raza", "color", "estado", "notas")}),
        ("Pesos / Fechas", {"fields": ("fecha_nacimiento", "peso_nacimiento", "peso_destete", "edad_formateada")}),
        ("Genealogía", {"fields": ("padre", "madre", "registro")}),
        ("Sistema", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Edad")
    def edad_formateada(self, obj):
        return obj.edad or "Sin fecha"
