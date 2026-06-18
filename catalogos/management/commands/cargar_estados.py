from django.core.management.base import BaseCommand
from catalogos.models import Estado

class Command(BaseCommand):
    help = 'Carga o actualiza el catálogo de estados de México'

    def handle(self, *args, **kwargs):
        self.cargar_estados()

    def cargar_estados(self):
        estados = [
            ('AGS', 'Aguascalientes'),
            ('BC',  'Baja California'),
            ('BCS', 'Baja California Sur'),
            ('CAM', 'Campeche'),
            ('CHS', 'Chiapas'),
            ('CHI', 'Chihuahua'),
            ('CMX', 'Ciudad de México'),
            ('COA', 'Coahuila de Zaragoza'),
            ('COL', 'Colima'),
            ('DGO', 'Durango'),
            ('MEX', 'Estado de México'),
            ('GTO', 'Guanajuato'),
            ('GRO', 'Guerrero'),
            ('HGO', 'Hidalgo'),
            ('JAL', 'Jalisco'),
            ('MIC', 'Michoacán de Ocampo'),
            ('MOR', 'Morelos'),
            ('NAY', 'Nayarit'),
            ('NL',  'Nuevo León'),
            ('OAX', 'Oaxaca'),
            ('PUE', 'Puebla'),
            ('QRO', 'Querétaro'),
            ('QR',  'Quintana Roo'),
            ('SLP', 'San Luis Potosí'),
            ('SIN', 'Sinaloa'),
            ('SON', 'Sonora'),
            ('TAB', 'Tabasco'),
            ('TAM', 'Tamaulipas'),
            ('TLX', 'Tlaxcala'),
            ('VER', 'Veracruz de Ignacio de la Llave'),
            ('YUC', 'Yucatán'),
            ('ZAC', 'Zacatecas'),
        ]

        creados      = 0
        actualizados = 0

        for clave, nombre in estados:
            estado, created = Estado.objects.get_or_create(
                clave=clave,
                defaults={'nombre': nombre, 'activo': True}
            )

            if not created:
                cambios = False
                if estado.nombre != nombre:
                    estado.nombre = nombre
                    cambios = True
                if not estado.activo:
                    estado.activo = True
                    cambios = True
                if cambios:
                    estado.save()
                    actualizados += 1
            else:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f'{creados} estados creados'))
        self.stdout.write(self.style.SUCCESS(f'{actualizados} estados actualizados'))
        self.stdout.write(self.style.SUCCESS(f'{len(estados)} estados en total'))
