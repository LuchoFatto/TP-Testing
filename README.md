# Testin de aplicaciones - Proyecto grupal (segundo parcial)

Proyecto base para la materia Testing de Aplicaciones.

## Qué ya viene resuelto

- Registro y login de usuarios cliente
- Login de admin y organizer desde usuarios semilla
- Gestión base de eventos
- Compra y cancelación de órdenes
- Persistencia en archivos JSON
- Logs básicos en backend
- Swagger/OpenAPI en `/docs`
- Frontend mínimo ya funcional en `/`

## Qué deben agregar los alumnos

- `DELETE /events/{event_id}`
- `PATCH /events/{event_id}/capacity`

## Usuarios semilla

- `admin1 / admin123`
- `organizer1 / org123`
- `organizer2 / org456`
- `customer1 / cust123`

## Cómo correr el proyecto

recomendado: Python 3.11 para arriba

En la terminal, estando en la carpeta del proyecto ejecutar:

- Una única vez para inicializar el proyecto

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

- Cada vez que levanten el proyecto:

```bash
.\.venv\Scripts\activate
python main.py
```

Luego abrir:

- Frontend: `http://127.0.0.1:8000/`
- Swagger: `http://127.0.0.1:8000/docs`

## Ejecucion de tests:

```bash
pytest
```

## Qué se puede hacer desde el frontend

- registrarse como cliente
- iniciar sesión
- listar eventos
- comprar entradas
- ver órdenes
- cancelar órdenes
- crear eventos si el usuario es `admin` u `organizer`

---

## Documentación del Proyecto

A continuación se detallan los entregables correspondientes a los distintos Sprints de la materia:

- [Sprint 1 - Requerimientos Refinados](REQUIREMENTS.md)
