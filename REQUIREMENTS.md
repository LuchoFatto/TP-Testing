# Sprint 1: Requerimientos Refinados

Este documento detalla las especificaciones funcionales, historias de usuario con sus respectivos criterios de aceptación (escenarios de testing) y los riesgos técnicos identificados durante la fase de análisis del **Sprint 1**.

---

## Historias de Usuario y Criterios de Aceptación

### 1. Modificación de Capacidad de un Evento `[PATCH /events/{event_id}/capacity]` (REQ_01)

> **Como** Organizador del evento o Administrador del sistema,
> **Quiero** modificar la capacidad total de un evento,
> **Para** ajustar la disponibilidad de entradas según las necesidades del negocio.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Incremento o reducción válida**
  - **Dado** que existe un evento con ID `123`, cuya capacidad actual es `100` y tiene `40` entradas vendidas.
  - **Y** estoy autenticado con un token válido.
  - **Cuando** envío una petición `PATCH /events/123/capacity` con una nueva capacidad de `80`.
  - **Entonces** el sistema debe actualizar la capacidad en el archivo JSON.
  - **Y** debe responder con un código de estado `200 OK` junto con el evento modificado.

- **Escenario 2: Error de Negocio - Reducción por debajo de lo vendido (Caso de Borde)**
  - **Dado** que existe un evento con ID `123`, con `60` entradas ya vendidas.
  - **Cuando** intento modificar la capacidad a `50`.
  - **Entonces** el sistema **NO** debe aplicar el cambio.
  - **Y** debe responder un código de estado `400 Bad Request` con el mensaje:
    ```json
    { "detail": "La nueva capacidad no puede ser menor a las entradas vendidas." }
    ```

- **Escenario 3: Error de Validación - Capacidad igual o menor a cero**
  - **Cuando** intento modificar la capacidad de un evento a `0` o a un número negativo (ej. `-10`).
  - **Entonces** el sistema debe rechazar la solicitud con un código de estado `400 Bad Request` o `422 Unprocessable Entity`.

- **Escenario 4: Error de Ciclo de Vida - Evento Eliminado Lógicamente**
  - **Dado** que el evento con ID `123` fue marcado previamente como eliminado (`deleted: true` o `active: false` según corresponda).
  - **Cuando** intento modificar su capacidad.
  - **Entonces** el sistema debe denegar la acción y responder con un `400 Bad Request` indicando que el evento está inactivo o borrado.

- **Escenario 5: Error de Autorización - Usuario común intenta modificar un evento ajeno**
  - **Dado** que existe un evento con ID `3` cuyo `owner_username` es `"organizer1"`.
  - **Y** estoy autenticado como el usuario `"organizer2"` (rol usuario común).
  - **Cuando** envío una petición `PATCH /events/3/capacity` con una nueva capacidad de `60`.
  - **Entonces** el sistema **NO** debe aplicar el cambio.
  - **Y** debe responder un código de estado `403 Forbidden` con el mensaje:
    ```json
    { "detail": "No tiene permisos para modificar este evento." }
    ```

---

### 2. Eliminación Lógica de un Evento `[DELETE /events/{event_id}]` (REQ_02)

> **Como** Usuario Administrador o Dueño del evento,
> **Quiero** eliminar un evento del sistema,
> **Para** darlo de baja de la oferta pública cuando sea necesario.


#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Admin elimina cualquier evento**
  - **Dado** que existe un evento con ID `3` y tiene órdenes registradas en `orders.json`.
  - **Y** estoy autenticado con un token de administrador (`token-admin1`).
  - **Cuando** envío una petición `DELETE /events/3`.
  - **Entonces** el sistema debe cambiar el atributo `deleted` a `true` en el archivo JSON.
  - **Y** debe responder con un código de estado `200 OK` (o `204 No Content`).

- **Escenario 2: Camino Feliz (Happy Path) - Dueño elimina evento SIN órdenes**
  - **Dado** que existe un evento con ID `5` cuyo `owner_username` es `"organizer1"`.
  - **Y** el evento **NO** tiene ninguna orden asociada en `orders.json` (ni activas ni canceladas).
  - **Y** estoy autenticado como `"organizer1"`.
  - **Cuando** envío una petición `DELETE /events/5`.
  - **Entonces** el sistema debe realizar el borrado lógico del evento.
  - **Y** debe responder con un código de estado `200 OK`.

- **Escenario 3: Error de Negocio - Dueño intenta eliminar evento CON órdenes históricas**
  - **Dado** que existe un evento con ID `3` cuyo `owner_username` es `"organizer1"`.
  - **Y** el evento tiene al menos una orden en `orders.json` con estado `"cancelled"`.
  - **Y** estoy autenticado como `"organizer1"`.
  - **Cuando** envío una petición `DELETE /events/3`.
  - **Entonces** el sistema **NO** debe aplicar el cambio.
  - **Y** debe responder un código de estado `400 Bad Request` con el mensaje:
    ```json
    { "detail": "El dueño no puede eliminar un evento que ya registra órdenes." }
    ```

- **Escenario 4: Error de Autorización - Organizador no dueño intenta eliminar**
  - **Dado** que existe un evento con ID `3` cuyo `owner_username` es `"organizer1"`.
  - **Y** estoy autenticado como el usuario `"organizer2"` (rol usuario común).
  - **Cuando** envío una petición `DELETE /events/3`.
  - **Entonces** el sistema debe denegar la acción.
  - **Y** debe responder un código de estado `403 Forbidden` con el mensaje:
    ```json
    { "detail": "No tiene permisos para eliminar este evento." }
    ```

- **Escenario 5: Error de Existencia - ID no encontrado**
  - **Cuando** un usuario (Admin o no) envía una petición `DELETE /events/9999` (ID inexistente).
  - **Entonces** el sistema debe responder un código de estado `404 Not Found` con el mensaje:
    ```json
    { "detail": "Evento no encontrado." }
    ```

---

### 3. Registro de un Cliente Nuevo `[POST /auth/register]` (REQ_03)

> **Como** Visitante anónimo,
> **Quiero** registrarme en el sistema ingresando un nombre de usuario, contraseña y rol,
> **Para** crear una cuenta que me permita acceder a las funciones comerciales de la plataforma.


#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Registro exitoso de un nuevo cliente**
  - **Dado** que el `username` `"nuevo_cliente"` no existe dentro del archivo `users.json`.
  - **Cuando** envío una petición `POST /auth/register` con los datos obligatorios del esquema y el rol `"customer"`.
  - **Entonces** el sistema debe añadir el nuevo registro de usuario en el archivo JSON.
  - **Y** debe responder con un código de estado `200 OK` confirmando la creación.

- **Escenario 2: Error de Negocio - Intento de registro con un usuario ya existente**
  - **Dado** que el `username` `"admin1"` ya se encuentra registrado previamente en el archivo `users.json`.
  - **Cuando** envío una petición `POST /auth/register` intentando duplicar el identificador `"admin1"`.
  - **Entonces** el sistema **NO** debe modificar el estado del archivo de persistencia.
  - **Y** debe responder con un código de estado `400 Bad Request` indicando que el usuario ya existe.


### 4. Inicio de Sesión `[POST /auth/login]` (REQ_04)

> **Como** Usuario registrado en el sistema,
> **Quiero** ingresar mis credenciales de autenticación,
> **Para** obtener un token de acceso temporal que valide mi identidad en peticiones posteriores.


#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Inicio de sesión correcto**
  - **Dado** que el usuario `"organizer1"` y su contraseña coinciden estrictamente con los registros de `users.json`.
  - **Cuando** envío una petición `POST /auth/login` incluyendo las credenciales en el cuerpo de la solicitud.
  - **Entonces** el sistema debe validar los datos de acceso contra la persistencia local.
  - **Y** debe responder con un código de estado `200 OK` devolviendo la estructura del `access_token`.

- **Escenario 2: Error de Autenticación - Intento de login con credenciales inválidas**
  - **Dado** que el usuario `"organizer1"` existe pero se proporciona una contraseña incorrecta.
  - **Cuando** envío una petición `POST /auth/login` con la clave errónea.
  - **Entonces** el sistema debe bloquear el flujo de autenticación de la ruta.
  - **Y** debe responder con un código de estado `401 Unauthorized` denegando el token.


### 5. Creación de un Evento `[POST /events]` (REQ_05)

> **Como** Usuario Administrador o Dueño del evento,
> **Quiero** registrar un nuevo evento especificando sus datos de configuración base,
> **Para** habilitar la venta de entradas al público general dentro de la cartelera.


#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Creación exitosa de un evento**
  - **Dado** que estoy autenticado en el sistema con un token válido que me asocia al usuario `"organizer1"`.
  - **Cuando** envío una petición `POST /events` con datos válidos de nombre, fecha futura, capacidad entera superior a cero y precio positivo.
  - **Entonces** el sistema debe insertar el evento en `events.json`, configurando los valores por defecto de inicialización y enlazando el parámetro `"owner_username": "organizer1"`.
  - **Y** debe responder con un código de estado `200 OK` adjuntando la entidad del evento creada.

- **Escenario 2: Error de Validación - Datos inconsistentes según esquema estructural**
  - **Dado** que estoy autenticado con un token de acceso autorizado en los headers.
  - **Cuando** envío una petición `POST /events` con un valor de capacidad inválido para el modelo, tal como un número decimal o negativo.
  - **Entonces** la capa de validación de datos interceptores debe detener la ejecución de la lógica del servicio de manera reactiva.
  - **Y** debe responder con un código de estado `422 Unprocessable Content`.

### 6. Consulta de Eventos [GET /events] (REQ_06)

> **Como** Usuario del sistema,
> **Quiero** consultar el listado de eventos disponibles,
> **Para** conocer la oferta vigente y poder adquirir entradas.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Consulta exitosa de eventos activos**

  - Dado que existen múltiples eventos activos registrados en el archivo events.json.

  - Cuando envío una petición GET /events.

  - Entonces el sistema debe recuperar los eventos disponibles.

  - Y debe responder con un código de estado 200 OK devolviendo una colección de eventos.

- **Escenario 2: Filtro de Negocio - Eventos eliminados lógicamente no visibles**

  - Dado que existen eventos marcados con deleted: true.

  - Cuando realizo una consulta GET /events.

  - Entonces el sistema no debe incluir dichos eventos en la respuesta.

  - Y debe responder con un código de estado 200 OK.

- **Escenario 3: Caso de Borde - No existen eventos activos**

  - Dado que no existen eventos activos registrados.

  - Cuando envío una petición GET /events.

  - Entonces el sistema debe responder correctamente.

  - Y debe devolver una lista vacía junto con un código de estado 200 OK.

### 7. Consulta de Detalle de Evento [GET /events/{event_id}] (REQ_07)

> **Como** Usuario del sistema,
>
> **Quiero** consultar la información detallada de un evento específico,
>
> **Para** visualizar sus características y disponibilidad.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Consulta exitosa**

  - Dado que existe un evento con ID 123.

  - Cuando envío una petición `GET /events/123.`

  - Entonces el sistema debe recuperar los datos completos del evento.

  - Y debe responder con un código de estado 200 OK devolviendo la entidad correspondiente.

- **Escenario 2: Error de Existencia - Evento inexistente**
- Cuando envío una petición `GET /events/9999.`
  
- Entonces el sistema debe responder con un código de estado 404 Not Found.
  
- Y debe devolver el mensaje:

```
{"detail": "Event not found"}
```

- **Escenario 3: Error de Ciclo de Vida - Evento eliminado lógicamente**
- Dado que existe un evento con ID 123 marcado como eliminado.
  
- Cuando intento consultar su detalle.
  
- Entonces el sistema debe denegar la operación.
  
- Y debe responder con un código de estado 404 Not Found.

### 8. Modificación Completa de Evento [PUT /events/{event_id}] (REQ_08)

> **Como** Dueño del evento o Administrador,
>
> **Quiero** modificar la configuración completa de un evento,
>
> **Para** mantener actualizada su información.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Actualización exitosa**

  - Dado que existe un evento con ID 123.

  - Y estoy autenticado como dueño del evento o administrador.

  - Cuando envío una petición PUT /events/123 con datos válidos.

  - Entonces el sistema debe actualizar la información en events.json.

  - Y debe responder con un código de estado 200 OK devolviendo la entidad actualizada.

- **Escenario 2: Error de Autorización - Usuario sin permisos**

  - Dado que el evento pertenece a otro organizador.

  - Cuando intento modificarlo.

  - Entonces el sistema debe rechazar la solicitud.

  - Y debe responder con un código de estado 403 Forbidden.

- **Escenario 3: Error de Validación - Datos inválidos**

  - Cuando envío un nombre vacío, un precio negativo o una capacidad inválida.

  - Entonces el sistema debe rechazar la solicitud.

  - Y debe responder con un código de estado 422 Unprocessable Content.

- **Escenario 4: Error de Existencia - Evento inexistente**

  - Cuando intento modificar el evento con ID 9999.

  - Entonces el sistema debe responder con un código de estado 404 Not Found.

### 9. Desactivación de Evento [PATCH /events/{event_id}/deactivate] (REQ_09)

> **Como** Dueño del evento o Administrador,
>
> **Quiero** desactivar un evento,
>
> **Para** suspender su disponibilidad sin eliminarlo definitivamente.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Desactivación exitosa**

  - Dado que existe un evento activo con ID 123.

  - Y estoy autenticado como dueño o administrador.

  - Cuando envío una petición PATCH /events/123/deactivate.

  - Entonces el sistema debe marcar el evento como inactivo.

  - Y debe responder con un código de estado 200 OK.

- **Escenario 2: Error de Autorización - Usuario sin permisos**

  - Dado que el evento pertenece a otro organizador.

  - Cuando intento desactivarlo.

  - Entonces el sistema debe responder con un código de estado 403 Forbidden.

- **Escenario 3: Error de Existencia - Evento inexistente**

  - Cuando envío una petición PATCH /events/9999/deactivate.

  - Entonces el sistema debe responder con un código de estado 404 Not Found.

- **Escenario 4: Caso de Borde - Evento ya desactivado**

  - Dado que el evento ya se encuentra inactivo.

  - Cuando intento desactivarlo nuevamente.

  - Entonces el sistema debe responder informando que el recurso ya se encuentra desactivado.

  - Y debe devolver un código 400 Bad Request o 409 Conflict.

### 10. Consulta de Órdenes [GET /orders] (REQ_10)

> **Como** Usuario autenticado,
>
> **Quiero** consultar las órdenes registradas,
>
> **Para** visualizar el historial de compras.

#### **Criterios de Aceptación (Escenarios de Testing)**

- **Escenario 1: Camino Feliz (Happy Path) - Consulta exitosa**

  - Dado que existen órdenes registradas.

  - Y estoy autenticado correctamente.

  - Cuando envío una petición GET /orders.

  - Entonces el sistema debe devolver las órdenes permitidas según mi rol.

  - Y debe responder con un código de estado 200 OK.

- **Escenario 2: Error de Autenticación - Token inexistente**

  - Cuando realizo una petición sin token válido.

  - Entonces el sistema debe responder con un código de estado 401 Unauthorized.

- **Escenario 3: Caso de Borde - Sin órdenes registradas**

  - Dado que no existen órdenes para el usuario.

  - Cuando consulto GET /orders.

  - Entonces el sistema debe responder con una lista vacía.

  - Y debe devolver un código de estado 200 OK.

### 11. Compra de Entradas [POST /orders] (REQ_11)

> **Como** Cliente autenticado,
>
> **Quiero** comprar entradas para un evento,
>
> **Para** asistir al mismo.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Compra exitosa**

  - Dado que existe un evento activo con disponibilidad suficiente.

  - Y estoy autenticado como cliente.

  - Cuando envío una petición POST /orders indicando una cantidad válida de entradas.

  - Entonces el sistema debe registrar la orden en orders.json.

  - Y debe responder con un código de estado 200 OK.

- **Escenario 2: Error de Negocio - Capacidad insuficiente**

  - Dado que el evento no posee entradas disponibles suficientes.

  - Cuando intento realizar la compra.

  - Entonces el sistema debe rechazar la operación.

  - Y debe responder con un código de estado 400 Bad Request.

- **Escenario 3: Error de Ciclo de Vida - Evento inactivo**

  - Dado que el evento se encuentra desactivado o eliminado.

  - Cuando intento comprar entradas.

  - Entonces el sistema debe responder con un código de estado 400 Bad Request.

- **Escenario 4: Error de Validación - Cantidad inválida**

  - Cuando intento comprar 0 o una cantidad negativa de entradas.

  - Entonces el sistema debe rechazar la solicitud.

  - Y debe responder con un código de estado 422 Unprocessable Content.

### 12. Cancelación de Orden [PATCH /orders/{order_id}/cancel] (REQ_12)

> **Como** Cliente propietario de una orden o Administrador,
>
> **Quiero** cancelar una orden existente,
>
> **Para** anular la compra realizada.

#### Criterios de Aceptación (Escenarios de Testing)

- **Escenario 1: Camino Feliz (Happy Path) - Cancelación exitosa**

  - Dado que existe una orden activa con ID 10.

  - Y estoy autenticado como propietario de la orden.

  - Cuando envío una petición PATCH /orders/10/cancel.

  - Entonces el sistema debe actualizar el estado de la orden a "cancelled".

  - Y debe responder con un código de estado 200 OK.

- **Escenario 2: Error de Autorización - Usuario ajeno a la orden**

  - Dado que la orden pertenece a otro usuario.

  - Cuando intento cancelarla.

  - Entonces el sistema debe responder con un código de estado 403 Forbidden.

- **Escenario 3: Error de Existencia - Orden inexistente**

  - Cuando envío una petición PATCH /orders/9999/cancel.

  - Entonces el sistema debe responder con un código de estado 404 Not Found.

  - Y debe devolver el mensaje:

```
{ "detail": "Orden no encontrada." }
```

- **Escenario 4: Caso de Borde - Orden ya cancelada**

  - Dado que la orden ya posee estado "cancelled".

  - Cuando intento cancelarla nuevamente.

  - Entonces el sistema debe rechazar la operación.

  - Y debe responder con un código de estado 400 Bad Request.

## Riesgo Técnico Identificado

> **Fuera de Alcance Funcional - Sprint 1**
>
> Debido a la persistencia en archivos JSON crudos sin control de concurrencia (_locks_), existen riesgos de condiciones de carrera (_race conditions_) si operaciones de compra simultáneas coinciden con la eliminación lógica (`DELETE`) o cambio de capacidad (`PATCH`). Se documenta como un riesgo crítico de arquitectura para ser evaluado en las pruebas de carga no funcionales (JMeter, Sprint 4).

---

## Enlaces del Proyecto

- **Tablero de Trello (Backlog):** [Backlog de Testing - Sprint 1](https://trello.com/invite/b/6a0e6424b3a6819f46f74f5d/ATTI4e536083702ebe06ec89a9f84fe2041160428DFA/backlog-testing)
