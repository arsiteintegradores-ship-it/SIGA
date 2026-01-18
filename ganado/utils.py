import calendar
import re
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


IDENTIFIER_RE = re.compile(r"^[A-Z0-9-]+$")


def normalize_identifier(value):
    """Normaliza identificadores: trim, uppercase y colapsa espacios/guiones."""
    if value is None:
        return None
    value = value.strip().upper()
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"-{2,}", "-", value)
    value = value.strip("-")
    return value or None


def validate_identifier(value, field_label):
    if not value:
        return
    if not IDENTIFIER_RE.fullmatch(value):
        raise ValidationError(f"{field_label} solo puede contener letras, números y guiones.")


def get_weight_limit(setting_name, default):
    return getattr(settings, setting_name, default)


def validate_weight(value, field_label, max_value, allow_zero=False):
    if value is None:
        return
    min_value = Decimal("0") if allow_zero else Decimal("0.01")
    if value < min_value:
        msg = "mayor o igual a 0" if allow_zero else "mayor a 0"
        raise ValidationError(f"{field_label} debe ser {msg}.")
    if max_value is not None and value > Decimal(str(max_value)):
        raise ValidationError(
            f"{field_label} excede el límite razonable ({max_value})."
        )


def calculate_age_days(birth_date, today=None):
    if not birth_date:
        return None
    today = today or timezone.localdate()
    days = (today - birth_date).days
    return days if days >= 0 else None


def _add_months(current_date, months):
    """Suma meses a una fecha respetando el fin de mes."""
    year = current_date.year + (current_date.month - 1 + months) // 12
    month = (current_date.month - 1 + months) % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    day = min(current_date.day, last_day)
    return date(year, month, day)


def calculate_age_amd(birth_date, today=None):
    """
    Devuelve (años, meses, días) exactos como tupla.
    Ej: (2, 3, 12)
    """
    if not birth_date:
        return None
    today = today or timezone.localdate()
    if birth_date > today:
        return None

    years = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1

    base_year = birth_date.year + years
    base_day = min(birth_date.day, calendar.monthrange(base_year, birth_date.month)[1])
    base = date(base_year, birth_date.month, base_day)

    months = (today.year - base.year) * 12 + (today.month - base.month)
    if today.day < base.day:
        months -= 1

    base_after_months = _add_months(base, months)
    days = (today - base_after_months).days
    return years, months, days


def format_age(amd_tuple):
    """Texto: '2 años, 3 meses, 12 días'."""
    if not amd_tuple:
        return "SIN_FECHA"
    years, months, days = amd_tuple
    return f"{years} años, {months} meses, {days} días"


def etapa_desarrollo_from_dias(edad_dias, sexo):
    """
    Reglas:
    1-210  => Lactantes
    211-365 => Crías
    366-730 => Hembra: Vaquilla / Macho: Novillo
    >730 => Macho: Semental / Hembra: Vaca
    """
    if edad_dias is None:
        return "SIN_FECHA"
    if edad_dias <= 0:
        return "REVISAR_FECHA"

    if 1 <= edad_dias <= 210:
        return "Lactantes"
    if 211 <= edad_dias <= 365:
        return "Crías"
    if 366 <= edad_dias <= 730:
        return "Vaquilla" if sexo == "H" else "Novillo"
    return "Vaca" if sexo == "H" else "Semental"