import base64
import uuid
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from agenda.models import Contacto, Telefono
from api.serializers import ContactoSerializer, ContactoListadoSerializer

def procesar_foto_base64(base64_string):
    """
    Decodifica un string base64 y retorna un ContentFile
    listo para asignarlo al ImageField de fotografia"
    """
    if not base64_string:
        return None
    try:
        # Si viene con header "data:image/jpeg;base64,"
        if ';base64,' in base64_string:
            header, data = base64_string.split(';base64,')
            extension    = header.split('/')[-1]
        else:
            # Sin header, jpg por defecto
            data      = base64_string
            extension = 'jpg'

        # Decodificamos el string base64 a bytes
        archivo_decodificado = base64.b64decode(data)

        # Generamos un nombre único para el archivo
        nombre_archivo = f"{uuid.uuid4()}.{extension}"

        return ContentFile(archivo_decodificado, name=nombre_archivo)

    except Exception:
        return None

@api_view(['GET', 'POST'])
def listar_crear_contactos(request):
    """
    GET  /api/contactos/ = Listado paginado de contactos con búsqueda por nombre, apellidos o teléfono
    POST /api/contactos/ = Crear nuevo contacto con dirección y teléfonos
    """

    if request.method == 'GET':

        # Obtenemos el parámetro de búsqueda si existe
        search   = request.query_params.get('search', '')

        # Solo traemos contactos activos
        queryset = Contacto.objects.prefetch_related('telefonos').filter(activo=True)

        # Búsqueda por nombre, apellidos o número de teléfono
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search)    |
                Q(apellidos__icontains=search) |
                Q(telefonos__numero__icontains=search)
            ).distinct()

        # Paginado, page_size y page son parámetros opcionales en la URL
        page_size = int(request.query_params.get('page_size', 10))
        page_num  = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, page_size)
        page      = paginator.get_page(page_num)

        # Serializamos solo los campos de listado (nombre y teléfonos)
        serializer = ContactoListadoSerializer(page.object_list, many=True)

        return Response({
            'count':       paginator.count,
            'total_pages': paginator.num_pages,
            'page':        page_num,
            'results':     serializer.data,
        })

    elif request.method == 'POST':

        # Extraemos key contacto
        data = request.data.get('contacto', request.data)

        # Extraemos la foto para convertir el base64
        foto_base64 = data.pop('fotografia', None) if isinstance(data, dict) else None

        # Extraemos la key de telefonos
        telefonos_data = data.pop('telefonos', []) if isinstance(data, dict) else []

        serializer = ContactoSerializer(data=data)

        if serializer.is_valid():

            # Guardamos el contacto con la dirección anidada
            contacto = serializer.save()

            # Creamos cada teléfono asociado al contacto
            for tel_data in telefonos_data:
                Telefono.objects.create(contacto=contacto, **tel_data)

            # Procesamos y guardamos la foto si viene en el request
            if foto_base64:
                foto = procesar_foto_base64(foto_base64)
                if foto:
                    contacto.fotografia.save(foto.name, foto, save=True)

            # Retornamos el contacto creado
            return Response(
                {'contacto': ContactoSerializer(contacto).data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Acepta métodos para listar, actualizar o borrar contacto
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_contacto(request, id):
    """
    GET    /api/contactos/<id>/  = Listar contacto
    PUT    /api/contactos/<id>/  = Actualizar contacto
    DELETE /api/contactos/<id>/  = Borrar contacto (se desactiva)
    """

    # Buscamos el contacto solo entre los activos
    # Si no existe o está inactivo retornamos 404
    try:
        contacto = Contacto.objects.prefetch_related('telefonos').select_related('direccion').get(
            id=id,
            activo=True
        )
    except Contacto.DoesNotExist:
        return Response(
            {'error': 'Contacto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        # Retorna datos del contacto, dirección y teléfonos activos
        serializer = ContactoSerializer(contacto)
        return Response({'contacto': serializer.data})

    elif request.method == 'PUT':

        # Extraemos la key contacto
        data = request.data.get('contacto', request.data)

        # Extraemos foto y teléfonos
        foto_base64    = data.pop('fotografia', None) if isinstance(data, dict) else None
        telefonos_data = data.pop('telefonos', None)  if isinstance(data, dict) else None

        # partial=True permite actualizar solo los campos enviados
        serializer = ContactoSerializer(contacto, data=data, partial=True)

        if serializer.is_valid():

            # Guardamos los cambios del contacto y dirección
            contacto = serializer.save()

            # Eliminamos los teléfonos anteriores (desactivados)
            # Creamos los nuevos
            if telefonos_data is not None:
                contacto.telefonos.update(activo=False)
                for tel_data in telefonos_data:
                    Telefono.objects.create(contacto=contacto, **tel_data)

            # Si viene foto nueva, la reemplazamos
            if foto_base64:
                if contacto.fotografia:
                    contacto.fotografia.delete(save=False)
                foto = procesar_foto_base64(foto_base64)
                if foto:
                    contacto.fotografia.save(foto.name, foto, save=True)

            # Retornamos el contacto actualizado
            return Response({'contacto': ContactoSerializer(contacto).data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        # Eliminar contacto
        # Solo se marca como inactivo
        contacto.activo = False
        contacto.save()

        return Response(
            {'mensaje': 'Contacto eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )
