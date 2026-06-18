from django.db import models
from catalogos.models import Estado

class Contacto(models.Model):
    nombre      = models.CharField(max_length=60)
    apellidos   = models.CharField(max_length=120, blank=True)
    fotografia  = models.ImageField(upload_to='fotos_contactos/', blank=True)
    fecha_nacio = models.DateField(blank=True, null=True)
    activo      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering            = ['apellidos', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Direccion(models.Model):
    contacto        = models.OneToOneField(Contacto, on_delete=models.CASCADE, related_name='direccion')
    calle           = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True)
    colonia         = models.CharField(max_length=255)
    municipio       = models.CharField(max_length=255)
    estado          = models.ForeignKey(Estado, on_delete=models.PROTECT)
    referencias     = models.TextField(blank=True)
    activo          = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Dirección'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle} {self.numero_exterior}, {self.municipio} - {self.contacto}"

class Telefono(models.Model):
    TIPO_CHOICES = [
        (1, 'Casa'),
        (2, 'Teléfono móvil'),
    ]

    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name='telefonos')
    tipo     = models.IntegerField(choices=TIPO_CHOICES, default=2)
    alias    = models.CharField(max_length=255, blank=True)
    numero   = models.CharField(max_length=50)
    activo   = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Teléfono'
        verbose_name_plural = 'Teléfonos'

    def __str__(self):
        return f"{self.numero} - {self.get_tipo_display()} - {self.contacto}"
    