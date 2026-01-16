import math
import pandas as pd

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from ganado.models import (
    GanadoAnimal,
    GanadoFinca,
    GanadoRaza,
    GanadoProductor,
    GanadoUpp,
)

ESTADOS_VALIDOS = {"ACTIVO", "VENDIDO", "MUERTO", "BAJA"}
SEXOS_VALIDOS = {"M", "H"}


def _empty(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def _s(v):
    if _empty(v):
        return None
    return str(v).strip()


def _to_intlike_str(v):
    """101.0 -> '101'"""
    if _empty(v):
        return None
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return str(v)
    txt = str(v).strip()
    if txt.endswith(".0"):
        txt = txt[:-2]
    return txt


def _clean_siniga(v):
    """Convierte 'Sin Sinniga' a None y normaliza números."""
    txt = _to_intlike_str(v)
    if not txt:
        return None
    low = txt.lower()
    if "sin" in low and "sinig" in low:
        return None
    return txt


def _to_float(v):
    if _empty(v):
        return None
    try:
        return float(v)
    except Exception:
        return None


def _to_date(v):
    """pandas Timestamp/datetime -> date"""
    if _empty(v):
        return None
    try:
        # Timestamp/datetime/date
        return v.date() if hasattr(v, "date") else v
    except Exception:
        return None


class Command(BaseCommand):
    help = "Importa rancho_las_Adas.xlsx (hoja 'Rancho Las Adas ') al SIGA."

    def add_arguments(self, parser):
        parser.add_argument("excel_path", type=str, help="Ruta al archivo .xlsx")
        parser.add_argument("--sheet", type=str, default=None, help="Nombre de hoja. Default: primera hoja.")
        parser.add_argument("--dry-run", action="store_true", help="Valida sin guardar en BD")
        parser.add_argument("--update", action="store_true", help="Si existe (por id_interno o id_siniga), actualiza")
        parser.add_argument("--limit", type=int, default=0, help="0=todas. >0 limita filas")

    def handle(self, *args, **opts):
        path = opts["excel_path"]
        sheet = opts["sheet"]
        dry = opts["dry_run"]
        do_update = opts["update"]
        limit = opts["limit"]

        xl = pd.ExcelFile(path)
        sheet_name = sheet or xl.sheet_names[0]

        # ayuda: si el usuario pone el nombre sin el espacio final
        if sheet and sheet_name not in xl.sheet_names:
            for s in xl.sheet_names:
                if s.strip() == sheet.strip():
                    sheet_name = s
                    break

        df = pd.read_excel(path, sheet_name=sheet_name)
        df.columns = [str(c).strip() for c in df.columns]

        required = {
            "Id_inter", "id_siniga", "nombre_bovino", "facha_nac",
            "Pnacer", "Pdestete", "raza", "sexo",
            "id_madre", "id_padre", "productor", "finca", "upp", "estatus"
        }
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise SystemExit(f"Faltan columnas en el Excel: {missing}")

        if limit and limit > 0:
            df = df.head(limit)

        errores = []
        creados = 0
        actualizados = 0
        refs_parent = []  # (child_id_interno, madre_id_interno, padre_id_interno)

        ctx = transaction.atomic() if not dry else _Noop()

        with ctx:
            # 1) crea/actualiza animales (sin padres)
            for i, row in df.iterrows():
                fila_excel = i + 2
                try:
                    id_interno = _to_intlike_str(row.get("Id_inter"))
                    id_siniga = _clean_siniga(row.get("id_siniga"))

                    if not id_interno and not id_siniga:
                        raise ValueError("Debe venir Id_inter o id_siniga")

                    sexo = _s(row.get("sexo"))
                    if not sexo or sexo not in SEXOS_VALIDOS:
                        raise ValueError("sexo debe ser M o H")

                    estado = (_s(row.get("estatus")) or "ACTIVO").upper()
                    if estado not in ESTADOS_VALIDOS:
                        raise ValueError("estatus inválido (ACTIVO/VENDIDO/MUERTO/BAJA)")

                    finca_nombre = _s(row.get("finca"))
                    if not finca_nombre:
                        raise ValueError("finca es obligatoria")

                    productor_nombre = _s(row.get("productor"))
                    upp_clave = _s(row.get("upp"))
                    raza_txt = _s(row.get("raza"))

                    finca, _ = GanadoFinca.objects.get_or_create(
                        nombre=finca_nombre,
                        defaults={"activo": 1, "created_at": timezone.now(), "updated_at": timezone.now()},
                    )

                    raza = None
                    if raza_txt:
                        raza, _ = GanadoRaza.objects.get_or_create(
                            raza=raza_txt,
                            defaults={"created_at": timezone.now(), "updated_at": timezone.now()},
                        )

                    productor = None
                    if productor_nombre:
                        productor, _ = GanadoProductor.objects.get_or_create(
                            nombre=productor_nombre,
                            apellido_paterno=None,
                            apellido_materno=None,
                            defaults={"activo": 1, "created_at": timezone.now(), "updated_at": timezone.now()},
                        )

                    upp = None
                    if upp_clave and productor:
                        upp, _ = GanadoUpp.objects.get_or_create(
                            clave=upp_clave,
                            defaults={"finca": finca, "productor": productor, "created_at": timezone.now(), "updated_at": timezone.now()},
                        )
                        if upp.finca_id != finca.id or upp.productor_id != productor.id:
                            upp.finca = finca
                            upp.productor = productor
                            upp.updated_at = timezone.now()
                            if not dry:
                                upp.save(update_fields=["finca", "productor", "updated_at"])

                    datos = dict(
                        id_interno=id_interno,
                        id_siniga=id_siniga,
                        nombre_bov=_s(row.get("nombre_bovino")),
                        fecha_nacimiento=_to_date(row.get("facha_nac")),
                        peso_nacimiento=_to_float(row.get("Pnacer")),
                        peso_destete=_to_float(row.get("Pdestete")),
                        sexo=sexo,
                        estado=estado,
                        finca=finca,
                        raza=raza,
                        productor=productor,
                        upp=upp,
                        updated_at=timezone.now(),
                    )

                    q = GanadoAnimal.objects.none()
                    if id_interno:
                        q = GanadoAnimal.objects.filter(id_interno=id_interno)
                    if (not q.exists()) and id_siniga:
                        q = GanadoAnimal.objects.filter(id_siniga=id_siniga)

                    if q.exists():
                        if do_update:
                            a = q.first()
                            for k, v in datos.items():
                                setattr(a, k, v)
                            if not dry:
                                a.save()
                            actualizados += 1
                    else:
                        datos["created_at"] = timezone.now()
                        if not dry:
                            GanadoAnimal.objects.create(**datos)
                        creados += 1

                    madre_id = _to_intlike_str(row.get("id_madre"))
                    padre_id = _to_intlike_str(row.get("id_padre"))
                    if madre_id or padre_id:
                        refs_parent.append((id_interno, madre_id, padre_id))

                except Exception as e:
                    errores.append({"fila": fila_excel, "error": str(e)})

            # 2) asigna padre/madre por Id_inter
            for (child_id, madre_id, padre_id) in refs_parent:
                if not child_id:
                    continue
                child = GanadoAnimal.objects.filter(id_interno=child_id).first()
                if not child:
                    continue

                madre = GanadoAnimal.objects.filter(id_interno=madre_id).first() if madre_id else None
                padre = GanadoAnimal.objects.filter(id_interno=padre_id).first() if padre_id else None

                if madre and madre.sexo != "H":
                    madre = None
                if padre and padre.sexo != "M":
                    padre = None
                if madre and madre.id == child.id:
                    madre = None
                if padre and padre.id == child.id:
                    padre = None

                child.madre = madre
                child.padre = padre
                child.updated_at = timezone.now()
                if not dry:
                    child.save(update_fields=["madre", "padre", "updated_at"])

        self.stdout.write(self.style.SUCCESS(
            f"✅ Importación terminada. Creados: {creados}, Actualizados: {actualizados}, Errores: {len(errores)}"
        ))

        if errores:
            out = "import_errores.csv"
            pd.DataFrame(errores).to_csv(out, index=False, encoding="utf-8")
            self.stdout.write(self.style.WARNING(f"⚠️ Se generó {out} con el detalle de errores."))


class _Noop:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): return False
