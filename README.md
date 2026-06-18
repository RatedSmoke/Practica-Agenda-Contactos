# Práctica Agenda para contactos

Proyecto de Django para gestión de una agenda para contactos mediante una 
API REST desarrollada con Django REST Framework.

## Requisitos

- Python 3.9.18+
- PostgreSQL 16+
- [Postman](https://www.postman.com/downloads/) — para probar los endpoints

## Pasos para instalar el proyecto

### 1. Clonar el repositorio
```bash
git clone <url>
cd practica_agenda
```

### 2. Crear y activar entorno virtual
```bash
python -m venv env_practica_agenda
source env_practica_agenda/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita el .env con tus valores
```

### 5. Crear base de datos en PostgreSQL

Entra a psql y ejecuta:

```sql
CREATE DATABASE nombre_de_tu_bd;
CREATE USER nombre_de_tu_usuario WITH PASSWORD 'password_usuario_de_tu_bd';
GRANT ALL PRIVILEGES ON DATABASE nombre_de_tu_bd TO nombre_de_tu_usuario;
GRANT ALL ON SCHEMA public TO nombre_de_tu_usuario;
ALTER DATABASE nombre_de_tu_bd OWNER TO nombre_de_tu_usuario;
```

> Usa los mismos valores que pongas en tu archivo `.env`

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Llenar catálogo de Estados
```bash
python manage.py cargar_estados
```

### 8. Correr el servidor
```bash
python manage.py runserver
```

## Colección Postman

En la raíz del proyecto encontrarás el archivo `Practica_Agenda_API.postman_collection.json`.

### Importar a Postman

1. Abre **Postman**
2. Clic en **Import** (arriba a la izquierda)
3. Arrastra el archivo `Practica_Agenda_API.postman_collection.json` o selecciónalo con **Choose Files**
4. Clic en **Import**

### Endpoints disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/contactos/` | Listado paginado de contactos |
| GET | `/api/contactos/?search=tony` | Búsqueda por nombre, apellidos o teléfono |
| POST | `/api/contactos/` | Crear contacto |
| GET | `/api/contactos/<id>/` | Detalle del contacto |
| PUT | `/api/contactos/<id>/` | Actualizar contacto |
| DELETE | `/api/contactos/<id>/` | Eliminar contacto |

> Después de crear un contacto con el POST, copia el `id` de la respuesta y actualiza la variable `contacto_id` en Postman para probar el GET, PUT y DELETE.
