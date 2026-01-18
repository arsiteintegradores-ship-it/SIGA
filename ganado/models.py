# ganado/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from .utils import (
    calculate_age_amd,
    calculate_age_days,
    format_age,
    get_weight_limit,
    normalize_identifier,
    etapa_desarrollo_from_dias,
    validate_identifier,
    validate_weight,
)


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

    def clean(self):
        errors = {}
        today = timezone.localdate()

        if self.fecha_nacimiento and self.fecha_nacimiento > today:
            errors["fecha_nacimiento"] = "La fecha de nacimiento no puede ser futura."

        # Validación de identificadores
        normalized_interno = normalize_identifier(self.id_interno)
        if normalized_interno:
            try:
                validate_identifier(normalized_interno, "El ID interno")
            except ValidationError as exc:
                errors["id_interno"] = exc.messages
            else:
                dup = GanadoAnimal.objects.filter(
                    Q(id_interno__iexact=normalized_interno)
                    | Q(id_interno__iexact=self.id_interno or "")
                )
                if self.pk:
                    dup = dup.exclude(pk=self.pk)
                if dup.exists():
                    errors["id_interno"] = "Ya existe un animal con este ID interno."

        normalized_siniga = normalize_identifier(self.id_siniga)
        if normalized_siniga:
            try:
                validate_identifier(normalized_siniga, "El ID SINIGA")
            except ValidationError as exc:
                errors["id_siniga"] = exc.messages
            else:
                dup = GanadoAnimal.objects.filter(
                    Q(id_siniga__iexact=normalized_siniga)
                    | Q(id_siniga__iexact=self.id_siniga or "")
                )
                if self.pk:
                    dup = dup.exclude(pk=self.pk)
                if dup.exists():
                    errors["id_siniga"] = "Ya existe un animal con este ID SINIGA."

        # Validación de pesos (límites configurables en settings)
        peso_nac_max = get_weight_limit("GANADO_PESO_NACIMIENTO_MAX", 80)
        peso_destete_max = get_weight_limit("GANADO_PESO_DESTETE_MAX", 400)

        try:
            validate_weight(self.peso_nacimiento, "El peso al nacimiento", peso_nac_max)
        except ValidationError as exc:
            errors["peso_nacimiento"] = exc.messages

        try:
            validate_weight(self.peso_destete, "El peso al destete", peso_destete_max)
        except ValidationError as exc:
            errors["peso_destete"] = exc.messages

        # Consistencia de genealogía
        if self.pk and self.madre_id and self.madre_id == self.pk:
            errors["madre"] = "La madre no puede ser el mismo animal."
        if self.pk and self.padre_id and self.padre_id == self.pk:
            errors["padre"] = "El padre no puede ser el mismo animal."
        if self.padre_id and self.madre_id and self.padre_id == self.madre_id:
            errors["padre"] = "Padre y madre no pueden ser el mismo animal."
            errors["madre"] = "Padre y madre no pueden ser el mismo animal."

        if self.padre_id and self.padre and self.padre.sexo != "M":
            errors["padre"] = "El padre debe ser macho."
        if self.madre_id and self.madre and self.madre.sexo != "H":
            errors["madre"] = "La madre debe ser hembra."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Normaliza identificadores antes de guardar.
        self.id_interno = normalize_identifier(self.id_interno)
        self.id_siniga = normalize_identifier(self.id_siniga)
        super().save(*args, **kwargs)

    # -----------------------------
    # EDAD EN DIAS
    # -----------------------------
    @property
    def edad_dias(self):
        """Edad en días (int) o None si no hay fecha o si es futura."""
        return calculate_age_days(self.fecha_nacimiento)

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
        return etapa_desarrollo_from_dias(self.edad_dias, self.sexo)

    # -----------------------------
    # EDAD EN AÑOS / MESES / DIAS (exacto)
    # -----------------------------
    @property
    def edad_amd(self):
        """
        Devuelve (años, meses, días) exactos como tupla.
        Ej: (2, 3, 12)
        """
        return calculate_age_amd(self.fecha_nacimiento)

    @property
    def edad(self):
        """Texto: '2 años, 3 meses, 12 días'."""
        return format_age(self.edad_amd)
