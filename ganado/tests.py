from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils import timezone

from .models import GanadoAnimal
from .utils import calculate_age_components, parse_es_date


class FechaUtilsTests(SimpleTestCase):
    def test_parse_es_date_valid(self):
        self.assertEqual(parse_es_date("01/02/2024"), date(2024, 2, 1))
        self.assertEqual(parse_es_date("01022024"), date(2024, 2, 1))
        self.assertEqual(parse_es_date("01-02-2024"), date(2024, 2, 1))

    def test_parse_es_date_invalid(self):
        with self.assertRaises(ValidationError):
            parse_es_date("32/01/2024")
        with self.assertRaises(ValidationError):
            parse_es_date("2024/01/01")


class EdadTests(SimpleTestCase):
    def test_calculate_age_components(self):
        birth = date(2020, 1, 15)
        today = date(2023, 2, 20)
        age = calculate_age_components(birth, today=today)
        self.assertIsNotNone(age)
        self.assertEqual(age.format_spanish(), "3 años, 1 meses, 5 días")


class GanadoAnimalValidationTests(SimpleTestCase):
    def test_id_required(self):
        animal = GanadoAnimal(sexo="M")
        with self.assertRaises(ValidationError) as exc:
            animal.clean()
        self.assertIn("id_interno", exc.exception.message_dict)

    def test_future_birth_date_invalid(self):
        future_date = timezone.localdate() + timedelta(days=1)
        animal = GanadoAnimal(sexo="M", id_interno="A1", fecha_nacimiento=future_date)
        with self.assertRaises(ValidationError) as exc:
            animal.clean()
        self.assertIn("fecha_nacimiento", exc.exception.message_dict)

    def test_required_fields(self):
        animal = GanadoAnimal(sexo="M", id_interno="A1")
        with self.assertRaises(ValidationError) as exc:
            animal.full_clean()
        self.assertIn("finca", exc.exception.message_dict)
