
# Create your models here.

from django.db import models


class Raza(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Finca(models.Model):
    nombre = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    nombre = models.CharField(max_length=100)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.finca.nombre}"


class Animal(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    identificacion = models.CharField(max_length=50, unique=True)
    raza = models.ForeignKey(Raza, on_delete=models.PROTECT)
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    peso_nacimiento = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.identificacion
