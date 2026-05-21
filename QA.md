# Plan de Pruebas (Test Plan)
## Proyecto: Sistema de Gestión de Eventos (Testing de Aplicaciones)

**QA / Testers:** Diseño de escenarios (positivos, negativos, alternativos) y automatización en `tests/`.

---

## 1. Introducción y Objetivos
El objetivo de este plan es definir el enfoque, los recursos y los escenarios de validación para las nuevas funcionalidades:
* **Eliminación de eventos:** `DELETE /events/{event_id}`
* **Modificación de capacidad:** `PATCH /events/{event_id}/capacity`

El propósito es garantizar que ambas funcionalidades cumplan con las reglas de negocio y se integren correctamente con la arquitectura existente.

## 2. Alcance (Scope)

### 2.1. Funcionalidades a probar (In Scope)
* **Endpoints:** Validación de reglas de negocio para los nuevos endpoints.
    * **Eliminación de eventos:**
        * Roles: Admin (puede borrar todo), Organizador/Dueño (solo propios y sin órdenes registradas), Usuario (sin permisos).
        * Validaciones: ID inexistente.
    * **Cambio de capacidad:**
        * Roles: Dueño y Administradores.
        * Validaciones: Capacidad > 0, Nueva capacidad >= Entradas vendidas, No modificar eventos eliminados.
* **Persistencia de Datos:** Verificación de integridad en archivos `.json`.
* **Interfaz de Usuario:** Validación de elementos (botones, campos, alertas) mediante automatización (Selenium o similar).
* **Flujos de la aplicación:** Pruebas E2E (login, registro, modificación, eliminación).

### 2.2. Elementos fuera del alcance (Out of Scope)
* Pruebas de estrés o carga (Performance).
* Pruebas de concurrencia sobre archivos `.json`.
* Seguridad criptográfica.
* Compatibilidad entre múltiples navegadores.
* Pruebas de accesibilidad.
* Pruebas de consumo de recursos.

## 3. Estrategia de Pruebas
Se emplearán técnicas de **Caja Blanca** (acceso a código) y **Caja Negra** (requisitos/APIs).

**Niveles de prueba (pytest):**
1. **Unitarias:** Funciones y métodos individuales.
2. **Integración:** Interacción entre módulos/APIs (Black-box).
3. **Sistema:** Comportamiento completo del sistema.
4. **Aceptación:** Alfa (interno) y Beta (profesor).
5. **Testing manual:** Postman, exploratorio y debug.
6. **Regresión:** Ejecución transversal tras cambios.

## 4. Estrategia de Datos de Prueba (Semillas)
* **Tecnologías:** Python 3.11+, FastAPI, `pytest`, `httpx` (TestClient), Postman, `monkeypatch`.
* **Herramientas:**
    * `pytest`: Estructura base.
    * `monkeypatch`: Testing de lógica (services) con dependencias externas.
    * `httpx`: Testing de rutas/API (integración).
    * `Postman`: Debug y prototipado rápido.
* **Base de Datos:** Se utiliza `tests/_baseline_data/` para restaurar `users.json`, `events.json` y `orders.json` a un estado controlado antes de cada ejecución (aislamiento total).

## 5. Matriz de Riesgos Inicial
* Sobrecarga del equipo de desarrollo.
* Riesgos de concurrencia en archivos JSON.

## 6. Criterios de Aprobación (Exit Criteria)
* **Entorno:** Restauración automática de datos controlados antes de cada ejecución.
* **Éxito:** Suite de pruebas en `pytest` con 0 fallos y 100% de cobertura de los casos definidos.
