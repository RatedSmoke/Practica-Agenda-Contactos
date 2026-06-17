# Práctica Agenda para contactos

Proyecto de Django para gestión de una agenda para contactos mediante una 
API REST desarrollada con Django REST Framework.

## Requisitos

- Python 3.9.18+
- PostgreSQL 15+

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
CREATE USER nombre_de_tu_usuario WITH PASSWORD 'password_de_tu_bd';
GRANT ALL PRIVILEGES ON DATABASE nombre_de_tu_bd TO nombre_de_tu_usuario;
GRANT ALL ON SCHEMA public TO nombre_de_tu_usuario;
ALTER DATABASE nombre_de_tu_bd OWNER TO nombre_de_tu_usuario;
```

> Usa los mismos valores que pongas en tu archivo `.env`

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Correr el servidor
```bash
python manage.py runserver