# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone

from .utils import (
    calculate_age_components,
    max_birth_date,
    normalize_text,
)

ID_REGEX = RegexValidator(
    regex=r"^[A-Za-z0-9-_.]+$",
    message="Solo se permiten letras, números, guion (-), guion bajo (_) y punto (.).",
)
PHONE_REGEX = RegexValidator(
    regex=r"^[0-9+()\\s-]{7,25}$",
    message="Teléfono inválido. Usa solo números, espacios o símbolos +()-.",
)


class GanadoAnimal(models.Model):
    id_interno = models.CharField(
        unique=True,
        max_length=50,
        blank=True,
        null=True,
        validators=[ID_REGEX],
    )
    id_siniga = models.CharField(
        unique=True,
        max_length=50,
        blank=True,
        null=True,
        validators=[ID_REGEX],
    )
    nombre_bov = models.CharField(max_length=80, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso_nacimiento = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    peso_destete = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    productor = models.ForeignKey('GanadoProductor', models.DO_NOTHING, blank=True, null=True)
    upp = models.ForeignKey('GanadoUpp', models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey('GanadoColor', models.DO_NOTHING, blank=True, null=True)
    raza = models.ForeignKey('GanadoRaza', models.DO_NOTHING, blank=True, null=True)
    registro = models.ForeignKey('GanadoRegistro', models.DO_NOTHING, blank=True, null=True)
    SEXO_CHOICES = (("M", "Macho"), ("H", "Hembra"))
    padre = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    madre = models.ForeignKey('self', models.DO_NOTHING, related_name='ganadoanimal_madre_set', blank=True, null=True)
    finca = models.ForeignKey('GanadoFinca', models.DO_NOTHING)
    lote = models.ForeignKey('GanadoLote', models.DO_NOTHING, blank=True, null=True)
    ESTADO_CHOICES = (
        ("ACTIVO", "ACTIVO"),
        ("VENDIDO", "VENDIDO"),
        ("MUERTO", "MUERTO"),
        ("BAJA", "BAJA"),
    )
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado = models.CharField(max_length=7, choices=ESTADO_CHOICES, default="ACTIVO")



    class Meta:
        managed = False
        db_table = 'ganado_animal'
        
    def __str__(self):
        return self.id_interno or self.id_siniga or str(self.id)

    @property
    def edad(self):
        age = calculate_age_components(self.fecha_nacimiento)
        return age.format_spanish() if age else None

    def clean(self):
        errors = {}
        self.id_interno = normalize_text(self.id_interno, upper=True)
        self.id_siniga = normalize_text(self.id_siniga, upper=True)
        self.nombre_bov = normalize_text(self.nombre_bov)
        if self.notas is not None:
            self.notas = self.notas.strip() or None

        if not self.id_interno and not self.id_siniga:
            errors["id_interno"] = "Debes capturar al menos un identificador (interno o SINIGA)."
            errors["id_siniga"] = "Debes capturar al menos un identificador (interno o SINIGA)."

        if self.fecha_nacimiento:
            if self.fecha_nacimiento > timezone.localdate():
                errors["fecha_nacimiento"] = "La fecha de nacimiento no puede ser futura."
            min_date = max_birth_date()
            if self.fecha_nacimiento < min_date:
                errors["fecha_nacimiento"] = (
                    "La fecha de nacimiento es demasiado antigua para el rango permitido."
                )

        if self.peso_destete is not None and self.peso_nacimiento is not None:
            if self.peso_destete < self.peso_nacimiento:
                errors["peso_destete"] = "El peso de destete no puede ser menor al peso de nacimiento."

        if self.finca_id and self.lote_id and self.lote.finca_id != self.finca_id:
            errors["lote"] = "Ese lote no pertenece a la finca seleccionada."

        if self.padre_id and self.padre_id == self.id:
            errors["padre"] = "Un animal no puede ser su propio padre."
        if self.madre_id and self.madre_id == self.id:
            errors["madre"] = "Un animal no puede ser su propia madre."

        if self.padre_id and getattr(self.padre, "sexo", None) and self.padre.sexo != "M":
            errors["padre"] = "El PADRE debe ser sexo 'M' (macho)."
        if self.madre_id and getattr(self.madre, "sexo", None) and self.madre.sexo != "H":
            errors["madre"] = "La MADRE debe ser sexo 'H' (hembra)."

        if errors:
            raise ValidationError(errors)



class GanadoFinca(models.Model):
    nombre = models.CharField(unique=True, max_length=120)
    ubicacion = models.CharField(max_length=180, blank=True, null=True)
    hectareas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    propietario = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        validators=[PHONE_REGEX],
    )
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

    class Meta:
        managed = False
        db_table = 'ganado_finca'
        
    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = normalize_text(self.nombre)
        self.ubicacion = normalize_text(self.ubicacion)
        self.propietario = normalize_text(self.propietario)
        self.telefono = normalize_text(self.telefono)



class GanadoLote(models.Model):
    finca = models.ForeignKey('GanadoFinca', models.DO_NOTHING)
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

    class Meta:
        managed = False
        db_table = 'ganado_lote'
        unique_together = (('finca', 'nombre'),)
        
    def __str__(self):
        return f"{self.nombre} ({self.finca_id})"

    def clean(self):
        self.nombre = normalize_text(self.nombre)
        self.descripcion = normalize_text(self.descripcion)



class GanadoRaza(models.Model):
    raza = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_raza'
        
    def __str__(self):
        return self.raza

    def clean(self):
        self.raza = normalize_text(self.raza)



class GanadoColor(models.Model):
    color = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_color'

    def __str__(self):
        return self.color

    def clean(self):
        self.color = normalize_text(self.color)



class GanadoProductor(models.Model):
    nombre = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=120, blank=True, null=True)
    apellido_materno = models.CharField(max_length=120, blank=True, null=True)
    direccion = models.CharField(max_length=180, blank=True, null=True)
    telefono = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        validators=[PHONE_REGEX],
    )
    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[EmailValidator(message="Correo electrónico inválido.")],
    )
    activo = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_productor'
        unique_together = (('nombre', 'apellido_paterno', 'apellido_materno'),)

    def __str__(self):
        parts = [self.nombre, self.apellido_paterno, self.apellido_materno]
        return " ".join([p for p in parts if p])

    def clean(self):
        self.nombre = normalize_text(self.nombre)
        self.apellido_paterno = normalize_text(self.apellido_paterno)
        self.apellido_materno = normalize_text(self.apellido_materno)
        self.direccion = normalize_text(self.direccion)
        self.telefono = normalize_text(self.telefono)
        email = normalize_text(self.email, upper=False)
        self.email = email.lower() if email else None


class GanadoUpp(models.Model):
    finca = models.ForeignKey('GanadoFinca', models.DO_NOTHING)
    productor = models.ForeignKey('GanadoProductor', models.DO_NOTHING)
    clave = models.CharField(
        unique=True,
        max_length=30,
        blank=True,
        null=True,
        validators=[ID_REGEX],
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_upp'

    def __str__(self):
        # muestra la clave, o algo legible si está vacía
        return self.clave or f"UPP #{self.id}"

    def clean(self):
        self.clave = normalize_text(self.clave, upper=True)



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
        db_table = 'ganado_registro'

    def __str__(self):
        return self.id_bovino or f"Registro #{self.id}"

    def clean(self):
        self.id_madre = normalize_text(self.id_madre, upper=True)
        self.id_padre = normalize_text(self.id_padre, upper=True)
        self.id_abuelo = normalize_text(self.id_abuelo, upper=True)
        self.id_abuela = normalize_text(self.id_abuela, upper=True)
        self.id_bovino = normalize_text(self.id_bovino, upper=True)
