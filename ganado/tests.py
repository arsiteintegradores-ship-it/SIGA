from datetime import date, timedelta
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, override_settings

from .models import GanadoAnimal
from .utils import (
    calculate_age_amd,
    calculate_age_days,
    etapa_desarrollo_from_dias,
    format_age,
    normalize_identifier,
    validate_identifier,
    validate_weight,
)


class UtilsCalculosTests(SimpleTestCase):
    def test_calculate_age_days(self):
        today = date(2025, 1, 2)
        birth = date(2024, 1, 1)
        self.assertEqual(calculate_age_days(birth, today=today), 367)

    def test_calculate_age_amd(self):
        today = date(2025, 1, 2)
        birth = date(2024, 1, 1)
        self.assertEqual(calculate_age_amd(birth, today=today), (1, 0, 1))

    def test_format_age(self):
        self.assertEqual(format_age((2, 3, 12)), "2 años, 3 meses, 12 días")
        self.assertEqual(format_age(None), "SIN_FECHA")

    def test_etapa_desarrollo_from_dias(self):
        self.assertEqual(etapa_desarrollo_from_dias(10, "M"), "Lactantes")
        self.assertEqual(etapa_desarrollo_from_dias(300, "H"), "Crías")
        self.assertEqual(etapa_desarrollo_from_dias(400, "H"), "Vaquilla")
        self.assertEqual(etapa_desarrollo_from_dias(400, "M"), "Novillo")
        self.assertEqual(etapa_desarrollo_from_dias(800, "H"), "Vaca")
        self.assertEqual(etapa_desarrollo_from_dias(800, "M"), "Semental")
        self.assertEqual(etapa_desarrollo_from_dias(None, "M"), "SIN_FECHA")


class ModeloCalculosTests(SimpleTestCase):
    def test_str_prefiere_id_interno(self):
        animal = GanadoAnimal(id_interno="INT-001", id_siniga="SIN-123")
        self.assertEqual(str(animal), "INT-001")

    def test_str_usa_siniga_si_no_hay_interno(self):
        animal = GanadoAnimal(id_interno=None, id_siniga="SIN-123")
        self.assertEqual(str(animal), "SIN-123")

    def test_edad_amd_y_texto(self):
        animal = GanadoAnimal(fecha_nacimiento=date(2024, 1, 1))
        with patch("ganado.utils.timezone.localdate", return_value=date(2025, 1, 2)):
            self.assertEqual(animal.edad_amd, (1, 0, 1))
            self.assertEqual(animal.edad, "1 años, 0 meses, 1 días")


class ValidacionesTests(SimpleTestCase):
    def test_normalize_identifier(self):
        self.assertEqual(normalize_identifier(" ab- 12 "), "AB-12")

    def test_validate_identifier(self):
        validate_identifier("ABC-123", "ID interno")
        with self.assertRaises(ValidationError):
            validate_identifier("abc 123", "ID interno")

    @override_settings(GANADO_PESO_NACIMIENTO_MAX=80)
    def test_validate_weight(self):
        validate_weight(10, "Peso", 80)
        with self.assertRaises(ValidationError):
            validate_weight(0, "Peso", 80)
        with self.assertRaises(ValidationError):
            validate_weight(100, "Peso", 80)

    def test_clean_fecha_nacimiento_futura(self):
        animal = GanadoAnimal(fecha_nacimiento=date.today() + timedelta(days=1))
        with self.assertRaises(ValidationError) as ctx:
            animal.clean()
        self.assertIn("fecha_nacimiento", ctx.exception.message_dict)

    def test_clean_id_interno_duplicado(self):
        class DummyQueryset:
            def __init__(self, exists=False):
                self._exists = exists

            def exclude(self, **kwargs):
                return self

            def exists(self):
                return self._exists

        def filter_side_effect(**kwargs):
            if "id_interno__iexact" in kwargs:
                return DummyQueryset(True)
            if "id_siniga__iexact" in kwargs:
                return DummyQueryset(False)
            return DummyQueryset(False)

        animal = GanadoAnimal(id_interno="ABC-123")
        with patch("ganado.models.GanadoAnimal.objects.filter", side_effect=filter_side_effect):
            with self.assertRaises(ValidationError) as ctx:
                animal.clean()
        self.assertIn("id_interno", ctx.exception.message_dict)
