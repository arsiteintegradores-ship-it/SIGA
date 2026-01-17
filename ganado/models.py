# ganado/models.py

import calendar
from datetime import date

from django.db import models
from django.utils import timezone


class GanadoFinca(models.Model):
    nombre = models.CharField(unique=True, max_length=120)
    ubicacion = models.CharField(max_length=180, blank=True, null=True)
    hectareas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    propietario = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_finca"

    def __str__(self):
        return self.nombre


class GanadoLote(models.Model):
    finca = models.ForeignKey("GanadoFinca", models.DO_NOTHING)
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_lote"
        unique_together = (("finca", "nombre"),)

    def __str__(self):
        return f"{self.nombre} - {self.finca.nombre}" if self.finca_id else self.nombre


class GanadoRaza(models.Model):
    raza = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_raza"

    def __str__(self):
        return self.raza


class GanadoColor(models.Model):
    color = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_color"

    def __str__(self):
        return self.color


class GanadoProductor(models.Model):
    nombre = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=120, blank=True, null=True)
    apellido_materno = models.CharField(max_length=120, blank=True, null=True)
    direccion = models.CharField(max_length=180, blank=True, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_productor"
        unique_together = (("nombre", "apellido_paterno", "apellido_materno"),)

    def __str__(self):
        parts = [self.nombre, self.apellido_paterno, self.apellido_materno]
        return " ".join([p for p in parts if p])


class GanadoUpp(models.Model):
    finca = models.ForeignKey("GanadoFinca", models.DO_NOTHING)
    productor = models.ForeignKey("GanadoProductor", models.DO_NOTHING)
    clave = models.CharField(unique=True, max_length=30, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_upp"

    def __str__(self):
        return self.clave or f"UPP #{self.id}"


class GanadoRegistro(models.Model):
    id_madre = models.CharField(max_length=120, blank=True, null=True)
    id_padre = models.CharField(max_length=120, blank=True, null=True)
    id_abuelo = models.CharField(max_length=120, blank=True, null=True)
    id_abuela = models.CharField(max_length=120, blank=True, null=True)
    id_bovino = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "ganado_registro"

    def __str__(self):
        return self.id_bovino or f"Registro #{self.id}"


class GanadoAnimal(models.Model):
    id_interno = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id_siniga = models.CharField(unique=True, max_length=50, blank=True, null=True)
    nombre_bov = models.CharField(max_length=80, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso_nacimiento = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    peso_destete = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    productor = models.ForeignKey("GanadoProductor", models.DO_NOTHING, blank=True, null=True)
    upp = models.ForeignKey("GanadoUpp", models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey("GanadoColor", models.DO_NOTHING, blank=True, null=True)
    raza = models.ForeignKey("GanadoRaza", models.DO_NOTHING, blank=True, null=True)
    registro = models.ForeignKey("GanadoRegistro", models.DO_NOTHING, blank=True, null=True)

    SEXO_CHOICES = (("M", "Macho"), ("H", "Hembra"))
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    padre = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    madre = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="ganadoanimal_madre_set",
        blank=True,
        null=True,
    )

    finca = models.ForeignKey("GanadoFinca", models.DO_NOTHING)
    lote = models.ForeignKey("GanadoLote", models.DO_NOTHING, blank=True, null=True)

    ESTADO_CHOICES = (
        ("ACTIVO", "ACTIVO"),
        ("VENDIDO", "VENDIDO"),
        ("MUERTO", "MUERTO"),
        ("BAJA", "BAJA"),
    )
    estado = models.CharField(max_length=7, choices=ESTADO_CHOICES, default="ACTIVO")

    notas = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "ganado_animal"

    def __str__(self):
        return self.id_interno or self.id_siniga or f"Animal #{self.id}"

    # -----------------------------
    # EDAD EN DIAS
    # -----------------------------
    @property
    def edad_dias(self):
        """Edad en días (int) o None si no hay fecha."""
        if not self.fecha_nacimiento:
            return None
        return (timezone.localdate() - self.fecha_nacimiento).days

    # -----------------------------
    # ETAPA DE DESARROLLO
    # -----------------------------
    @property
    def etapa_desarrollo(self):
        """
        Reglas:
        1-210  => Lactantes
        211-365 => Crias
        366-730 => Hembra: Vaquilla / Macho: Novillo
        >730 => Macho: Semental / Hembra: Vaca
        """
        edad = self.edad_dias
        if edad is None:
            return "SIN_FECHA"
        if edad <= 0:
            return "REVISAR_FECHA"

        if 1 <= edad <= 210:
            return "Lactantes"
        if 211 <= edad <= 365:
            return "Crias"
        if 366 <= edad <= 730:
            return "Vaquilla" if self.sexo == "H" else "Novillo"
        return "Vaca" if self.sexo == "H" else "Semental"

    # -----------------------------
    # EDAD EN AÑOS / MESES / DIAS (exacto)
    # -----------------------------
    def _add_months(self, d: date, months: int) -> date:
        """Suma meses a una fecha respetando el fin de mes."""
        y = d.year + (d.month - 1 + months) // 12
        m = (d.month - 1 + months) % 12 + 1
        last_day = calendar.monthrange(y, m)[1]
        day = min(d.day, last_day)
        return date(y, m, day)

    @property
    def edad_amd(self):
        """
        Devuelve (años, meses, días) exactos.
        Ej: (2, 3, 12)
        """
        if not self.fecha_nacimiento:
            return None

        today = timezone.localdate()
        b = self.fecha_nacimiento

        if b > today:
            return None

        # Años completos
        years = today.year - b.year
        if (today.month, today.day) < (b.month, b.day):
            years -= 1

        # Base = nacimiento + years (cuidando fin de mes)
        base_year = b.year + years
        base_day = min(b.day, calendar.monthrange(base_year, b.month)[1])
        base = date(base_year, b.month, base_day)

        # Meses completos desde base
        months = (today.year - base.year) * 12 + (today.month - base.month)
        if today.day < base.day:
            months -= 1

        base2 = self._add_months(base, months)

        # Días restantes
        days = (today - base2).days

        return years, months, days

    @property
    def edad(self):
        """Ej: '2 años, 3 meses, 12 días'."""
        amd = self.edad_amd
        if not amd:
            return "SIN_FECHA"
        a, m, d = amd
        return f"{a} años, {m} meses, {d} días"
