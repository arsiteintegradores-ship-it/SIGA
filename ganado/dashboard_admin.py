from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from django.shortcuts import render

from .models import GanadoAnimal, GanadoFinca, GanadoLote


def _apply_filters(qs, params):
    finca_id = params.get("finca_id") or ""
    lote_id = params.get("lote_id") or ""
    estado = params.get("estado") or ""
    sexo = params.get("sexo") or ""

    if finca_id.isdigit():
        qs = qs.filter(finca_id=int(finca_id))
    if lote_id.isdigit():
        qs = qs.filter(lote_id=int(lote_id))
    if estado:
        qs = qs.filter(estado=estado)
    if sexo:
        qs = qs.filter(sexo=sexo)

    return qs


@staff_member_required
def admin_dashboard(request):
    base_qs = GanadoAnimal.objects.all()
    qs = _apply_filters(base_qs, request.GET)

    # 1) Conteo por etapa
    por_etapa = (
        qs.values("estado")  # placeholder para no evaluar qs 2 veces
    )
    # Como etapa_desarrollo es @property, se calcula en Python:
    etapa_counts = {}
    for a in qs.only("fecha_nacimiento", "sexo"):
        etapa = getattr(a, "etapa_desarrollo", "SIN_DATO") or "SIN_DATO"
        etapa_counts[etapa] = etapa_counts.get(etapa, 0) + 1
    etapa_labels = list(etapa_counts.keys())
    etapa_values = list(etapa_counts.values())

    # 2) Promedio de peso destete por finca
    avg_destete = (
        qs.filter(peso_destete__isnull=False)
          .values("finca__nombre")
          .annotate(prom=Avg("peso_destete"), n=Count("id"))
          .order_by("finca__nombre")
    )
    finca_labels = [r["finca__nombre"] or "SIN_FINCA" for r in avg_destete]
    finca_prom = [float(r["prom"]) if r["prom"] is not None else 0 for r in avg_destete]

    # 3) Conteo por estado
    por_estado = (
        qs.values("estado")
          .annotate(n=Count("id"))
          .order_by("estado")
    )
    estado_labels = [r["estado"] for r in por_estado]
    estado_values = [r["n"] for r in por_estado]

    # 4) Distribución edad en meses por rangos (0-6, 6-12, 12-18, 18+)
    rangos = {"0-6": 0, "6-12": 0, "12-18": 0, "18+": 0, "SIN_FECHA": 0}
    for a in qs.only("fecha_nacimiento"):
        dias = getattr(a, "edad_dias", None)
        if dias is None:
            rangos["SIN_FECHA"] += 1
            continue
        meses = dias / 30.4375
        if meses < 6:
            rangos["0-6"] += 1
        elif meses < 12:
            rangos["6-12"] += 1
        elif meses < 18:
            rangos["12-18"] += 1
        else:
            rangos["18+"] += 1
    edad_labels = list(rangos.keys())
    edad_values = list(rangos.values())

    # datos para filtros (dropdowns)
    fincas = GanadoFinca.objects.all().order_by("nombre")
    lotes = GanadoLote.objects.all().order_by("nombre")

    context = {
        "fincas": fincas,
        "lotes": lotes,
        "selected": {
            "finca_id": request.GET.get("finca_id", ""),
            "lote_id": request.GET.get("lote_id", ""),
            "estado": request.GET.get("estado", ""),
            "sexo": request.GET.get("sexo", ""),
        },
        "chart": {
            "etapa_labels": etapa_labels,
            "etapa_values": etapa_values,
            "finca_labels": finca_labels,
            "finca_prom": finca_prom,
            "estado_labels": estado_labels,
            "estado_values": estado_values,
            "edad_labels": edad_labels,
            "edad_values": edad_values,
        }
    }
    return render(request, "admin/dashboard.html", context)
