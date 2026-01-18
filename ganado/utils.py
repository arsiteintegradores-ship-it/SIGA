from __future__ import annotations

from dataclasses import dataclass
import calendar
from datetime import date, datetime
import re
from typing import Optional, Tuple

from django.core.exceptions import ValidationError
from django.utils import timezone


DATE_INPUT_FORMATS = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d")
DATE_SEPARATOR_RE = re.compile(r"[./-]")
DATE_COMPACT_RE = re.compile(r"^\d{8}$")


def normalize_text(value: Optional[str], *, upper: bool = False) -> Optional[str]:
    if value is None:
        return None
    normalized = " ".join(value.strip().split())
    if not normalized:
        return None
    return normalized.upper() if upper else normalized


def parse_es_date(value: Optional[str | date]) -> Optional[date]:
    if value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    value = value.strip()
    if not value:
        return None
    if DATE_COMPACT_RE.match(value):
        value = f"{value[:2]}/{value[2:4]}/{value[4:]}"
    if DATE_SEPARATOR_RE.search(value):
        for fmt in DATE_INPUT_FORMATS:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    raise ValidationError("Formato de fecha inválido. Usa dd/mm/aaaa.")


@dataclass(frozen=True)
class AgeComponents:
    years: int
    months: int
    days: int

    def format_spanish(self) -> str:
        return f"{self.years} años, {self.months} meses, {self.days} días"


def calculate_age_components(
    birth_date: Optional[date], *, today: Optional[date] = None
) -> Optional[AgeComponents]:
    if not birth_date:
        return None
    if today is None:
        today = timezone.localdate()
    if birth_date > today:
        return None
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    if days < 0:
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        last_day_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += last_day_prev_month
        months -= 1
    if months < 0:
        months += 12
        years -= 1
    if years < 0:
        return None
    return AgeComponents(years=years, months=months, days=days)


def max_birth_date(years_back: int = 30) -> date:
    today = timezone.localdate()
    try:
        return today.replace(year=today.year - years_back)
    except ValueError:
        return today.replace(year=today.year - years_back, day=28)
