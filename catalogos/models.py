from django.db import models

class Estado(models.Model):
    clave  = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Estado'
        verbose_name_plural = 'Estados'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.clave} - {self.nombre}"
