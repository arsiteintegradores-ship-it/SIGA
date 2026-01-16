# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

from django.core.validators import RegexValidator


class GanadoAnimal(models.Model):
    id_interno = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id_siniga = models.CharField(unique=True, max_length=50, blank=True, null=True)
    nombre_bov = models.CharField(max_length=80, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso_nacimiento = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    peso_destete = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    productor = models.ForeignKey('GanadoProductor', models.DO_NOTHING, blank=True, null=True)
    upp = models.ForeignKey('GanadoUpp', models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey('GanadoColor', models.DO_NOTHING, blank=True, null=True)
    raza = models.ForeignKey('GanadoRaza', models.DO_NOTHING, blank=True, null=True)
    registro = models.ForeignKey('GanadoRegistro', models.DO_NOTHING, blank=True, null=True)
    sexo = models.CharField(max_length=1)
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
        db_table = 'ganado_finca'
        
    def __str__(self):
        return self.nombre



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



class GanadoRaza(models.Model):
    raza = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_raza'
        
    def __str__(self):
        return self.raza



class GanadoColor(models.Model):
    color = models.CharField(unique=True, max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_color'

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
        db_table = 'ganado_productor'
        unique_together = (('nombre', 'apellido_paterno', 'apellido_materno'),)

    def __str__(self):
        parts = [self.nombre, self.apellido_paterno, self.apellido_materno]
        return " ".join([p for p in parts if p])


class GanadoUpp(models.Model):
    finca = models.ForeignKey('GanadoFinca', models.DO_NOTHING)
    productor = models.ForeignKey('GanadoProductor', models.DO_NOTHING)
    clave = models.CharField(unique=True, max_length=30, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ganado_upp'

    def __str__(self):
        # muestra la clave, o algo legible si está vacía
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
        db_table = 'ganado_registro'

    def __str__(self):
        return self.id_bovino or f"Registro #{self.id}"
