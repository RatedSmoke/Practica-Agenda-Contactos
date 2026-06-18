from django.urls import include, path
from api.views import *

urlpatterns = [
    path('contactos/', include([
        path('', listar_crear_contactos, name='listar_crear_contactos'),
        path('<int:id>/', detalle_contacto, name='detalle_contacto'),
    ]))
]