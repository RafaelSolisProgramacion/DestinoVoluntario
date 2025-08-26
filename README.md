# Destino Voluntario

Plataforma para conectar voluntarios con organizacines sociales. Proyecto desarrollad oen Django con enfoque modular.

## Estructura del proyecto

DESTINOVOLUNTARIO/
├── config/                  # 📁 Proyecto Django (settings y configuración central)
│   ├── __init__.py
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs raíz del sitio
│   ├── wsgi.py
│   └── asgi.py
├── apps/                    # 📦 Tus apps personalizadas (modularización)
│   ├── core/                # Usuarios, roles, autentificación
│   ├── organizaciones/      # CRUD de organizaciones
│   ├── proyectos/           # Publicación y gestión de proyectos
│   └── postulaciones/       # Aplicaciones de voluntarios
├── templates/               # 🧠 Plantillas HTML globales (con subcarpetas por app)
│   ├── base.html            # Layout base
│   └── [app_name]/          # Templates por app
├── static/                  # 🎨 Archivos estáticos: CSS, JS, imágenes
│   └── [app_name]/          # Agrupados por funcionalidad
├── media/                   # 📷 Archivos subidos (si usas imágenes/documentos)
├── manage.py                # Comando principal de Django
├── requirements.txt         # 📌 Paquetes y dependencias
└── README.md                # 📝 Información del proyecto (ideal para el equipo)


- 'config/': configuracion base de Django
- 'apps/': apps organizadas por funcionalidad
- 'core/': gestion de usuarios y roles
- 'organizaciones/': CRUD para instituciones
- 'proyectos/': publicacion de oportunidades
- 'postulaciones/': inscripcion de voluntarios
- 'templates/': plantillas HTML agrupadas por app
- 'static/': estilos y scripts
- 'media/': archivos subidos por usuarios

## Instalacion rapidaa

1- git clone https://github.com/RafaelSolisProgramacion/DestinoVoluntario.git (el usuario debe tener permiso de colaborador en el repo)

2- cd destinovoluntario
3- pipenv install (instala las dependecias del proyecto, incluyendo django y django-htmx)
    pipenv install Django (si Django no esta instalado, por lo general esta)
    pipenv install django-htmx (solo si da error del modulo faltante htmx)
4- pipenv shell
python manage.py migrate (sino se ha cargado el archivo SQLite con el clone)
5- python manage.py runserver