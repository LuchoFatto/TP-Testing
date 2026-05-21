# Sprint 1: Requerimientos Refinados

Este documento detalla las especificaciones funcionales, historias de usuario con sus respectivos criterios de aceptación (escenarios de testing) y los riesgos técnicos identificados durante la fase de análisis del **Sprint 1**.

---

## Historias de Usuario y Criterios de Aceptación

### 1. Modificación de Capacidad de un Evento `[PATCH /events/{event_id}/capacity]`

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

### 2. Eliminación Lógica de un Evento `[DELETE /events/{event_id}]`

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

## Riesgo Técnico Identificado

> **Fuera de Alcance Funcional - Sprint 1**
>
> Debido a la persistencia en archivos JSON crudos sin control de concurrencia (_locks_), existen riesgos de condiciones de carrera (_race conditions_) si operaciones de compra simultáneas coinciden con la eliminación lógica (`DELETE`) o cambio de capacidad (`PATCH`). Se documenta como un riesgo crítico de arquitectura para ser evaluado en las pruebas de carga no funcionales (JMeter, Sprint 4).

---

## Enlaces del Proyecto

- **Tablero de Trello (Backlog):** [Backlog de Testing - Sprint 1](https://trello.com/invite/b/6a0e6424b3a6819f46f74f5d/ATTI4e536083702ebe06ec89a9f84fe2041160428DFA/backlog-testing)
