# Sistema de Actividades Extracurriculares (FastAPI)

Aplicacion web simple para gestionar actividades extracurriculares en una escuela.
Incluye:
- Backend con FastAPI.
- Frontend estatico (HTML, CSS, JavaScript).
- API para listar actividades y registrar estudiantes.

## Descripcion rapida

El proyecto permite:
- Ver actividades disponibles (descripcion, horario y cupos restantes).
- Registrar un correo de estudiante en una actividad.

La informacion se guarda en memoria dentro de [src/app.py](src/app.py), por lo que se reinicia cada vez que se apaga el servidor.

## Estructura del proyecto

```text
.
├── README.md
├── requirements.txt
└── src
    ├── app.py
    └── static
        ├── app.js
        ├── index.html
        └── styles.css
```

Archivos principales:
- [src/app.py](src/app.py): API FastAPI y datos iniciales.
- [src/static/index.html](src/static/index.html): interfaz web.
- [src/static/app.js](src/static/app.js): logica cliente para consumir la API.
- [src/static/styles.css](src/static/styles.css): estilos de la interfaz.

## Requisitos

- Python 3.10 o superior.
- pip.

Dependencias del proyecto en [requirements.txt](requirements.txt):
- fastapi
- uvicorn

## Instalacion

1. Clonar el repositorio.
2. (Opcional, recomendado) crear y activar entorno virtual.
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion local

Desde la raiz del proyecto ejecuta:

```bash
uvicorn src.app:app --reload
```

Luego abre en el navegador:
- Aplicacion web: http://127.0.0.1:8000/
- Documentacion Swagger: http://127.0.0.1:8000/docs

## Uso de la API

### 1) Listar actividades

`GET /activities`

Ejemplo:

```bash
curl http://127.0.0.1:8000/activities
```

### 2) Registrar estudiante en una actividad

`POST /activities/{activity_name}/signup?email=correo@dominio.com`

Ejemplo:

```bash
curl -X POST "http://127.0.0.1:8000/activities/Chess%20Club/signup?email=ana@merghigh.edu"
```

## Flujo de la aplicacion

1. El navegador abre [src/static/index.html](src/static/index.html).
2. [src/static/app.js](src/static/app.js) hace `GET /activities`.
3. El usuario envia el formulario.
4. Se hace `POST /activities/{activity_name}/signup` con el email.
5. Se muestra mensaje de exito o error en pantalla.

## Limitaciones actuales

- No hay base de datos (los cambios no son persistentes).
- No se valida si el estudiante ya esta inscrito.
- No se impide sobrepasar `max_participants`.

## Ideas de mejora

- Persistencia con SQLite o PostgreSQL.
- Validaciones de negocio (duplicados y cupos maximos).
- Autenticacion para administradores y estudiantes.
- Pruebas automaticas para endpoints.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta [LICENSE](LICENSE).

