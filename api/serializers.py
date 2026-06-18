from rest_framework import serializers
from agenda.models import Contacto, Direccion, Telefono
from catalogos.models import Estado
from django.db import transaction

# Serializer de Estados
# Convierte objetos Estado a JSON y viceversa
# Se usa para mostrar información adicional del estado
class EstadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estado
        fields = ['id', 'clave', 'nombre']

# Serializer de Teléfonos
# Convierte objetos Teléfono a JSON y viceversa
# Maneja la información de cada teléfono asociado a un contacto
class TelefonoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telefono
        fields = ['id', 'tipo', 'alias', 'numero']

# Serializer de Direcciones
# Convierte objetos Dirección a JSON y viceversa
# Maneja la información de la dirección del contacto
class DireccionSerializer(serializers.ModelSerializer):

    # Muestra la información del Estado además del id
    estado_info = EstadoSerializer(
        source='estado',
        read_only=True
    )

    class Meta:
        model = Direccion
        fields = ['id', 'calle', 'numero_exterior', 'numero_interior',
            'colonia', 'municipio', 'estado', 'estado_info', 'referencias'
        ]

# Serializer de Contactos
# Maneja la información anidada (Relación a Teléfono y Dirección)
# También se encarga de crear y actualizar Dirección y Teléfonos
class ContactoSerializer(serializers.ModelSerializer):

    # Relación con Dirección
    direccion = DireccionSerializer()

    # Relación con Teléfonos
    telefonos = TelefonoSerializer(many=True)

    class Meta:
        model = Contacto
        fields = ['id', 'nombre', 'apellidos', 'fotografia', 'fecha_nacio',
            'direccion', 'telefonos']

    # Crear contacto
    # Se ejecuta en serializer.save()
    @transaction.atomic
    def create(self, validated_data):

        # Extraemos la información anidada
        direccion_data = validated_data.pop('direccion')
        telefonos_data = validated_data.pop('telefonos')

        # Creamos el contacto
        contacto = Contacto.objects.create(**validated_data)

        # Creamos la dirección
        Direccion.objects.create(
            contacto=contacto,
            **direccion_data
        )

        # Creamos todos los teléfonos enviados
        for tel_data in telefonos_data:
            Telefono.objects.create(
                contacto=contacto,
                **tel_data
            )

        return contacto

    # Actualizar contacto
    # Se ejecuta en PUT
    @transaction.atomic
    def update(self, instance, validated_data):

        # Extraemos la información anidada
        direccion_data = validated_data.pop('direccion', None)
        telefonos_data = validated_data.pop('telefonos', None)

        # Actualizamos los campos del contacto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Actualizamos la dirección
        if direccion_data is not None:

            direccion = instance.direccion

            for attr, value in direccion_data.items():
                setattr(direccion, attr, value)

            direccion.save()

        # Actualizamos teléfonos
        # Desactivar anteriores y crear nuevos
        if telefonos_data is not None:

            instance.telefonos.update(activo=False)

            for telefono_data in telefonos_data:
                Telefono.objects.create(
                    contacto=instance,
                    **telefono_data
                )

        return instance

# Serializer para Listar Nombre y Teléfonos
class ContactoListadoSerializer(serializers.ModelSerializer):

    telefonos = TelefonoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Contacto
        fields = ['id', 'nombre', 'apellidos', 'telefonos']
