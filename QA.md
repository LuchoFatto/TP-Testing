# Plan de Pruebas Inicial (Test Plan)
## Proyecto: Sistema de Gestión de Eventos (Testing de Aplicaciones)

**Roles QA / Testers:** Diseño de escenarios, ejecución de pruebas manuales y automatización.

---

## 1. Introducción y Objetivos
El objetivo de este plan es definir el enfoque, los recursos y los escenarios de validación para las nuevas funcionalidades solicitadas en el Sprint 1:
* **Eliminación lógica de eventos:** `DELETE /events/{event_id}`
* **Modificación de capacidad:** `PATCH /events/{event_id}/capacity`

El propósito es garantizar que ambas funcionalidades cumplan con las reglas de negocio refinadas y se integren correctamente con la arquitectura base del sistema, mitigando riesgos técnicos.

## 2. Alcance (Scope)

### 2.1. Funcionalidades a probar (In Scope)
* **Endpoints (API Testing):** Validación de reglas de negocio y contratos HTTP para las nuevas rutas:
    * *DELETE:* Verificación de restricciones por rol (Admin vs. Dueño) y bloqueo por existencia de órdenes históricas.
    * *PATCH:* Validación de límites inferiores frente a entradas ya vendidas y restricción de modificación sobre registros inactivos.
* **Persistencia de Datos:** Verificación de la consistencia de estados en los archivos `.json`.
* **Regresión Funcional:** Validación manual de caja negra sobre el circuito base heredado (Registro, Login, Compra y Cancelación).
* **Automatización Funcional (E2E):** Ejecución de flujos críticos automatizados mediante Selenium IDE en la interfaz web.
* **Pruebas No Funcionales (Rendimiento/Concurrencia):** Simulación de escenarios de carga utilizando Apache JMeter para estresar la persistencia local.

### 2.2. Elementos fuera del alcance (Out of Scope)
* Pruebas de seguridad e integridad criptográfica de tokens (ficticios en el código base).
* Pruebas de accesibilidad y compatibilidad en navegadores móviles.
* Tuning o configuración de infraestructura de servidores externos.

## 3. Estrategia de Pruebas
Se aplicará un enfoque primordialmente de **Caja Negra** (basado en la especificación de requerimientos) para las actividades de QA, evaluando particiones de equivalencia y valores límite. Esto se complementará con Verificación Estructural (**Caja Blanca**) ejecutada mediante cobertura de pruebas unitarias por parte de Desarrollo.

**Niveles de prueba aplicados (STLC):**
1. **Unitarias y de Integración:** Ejecutadas en el backend mediante el framework `pytest`.
2. **Pruebas de Sistema (Endpoints):** Validación de flujos de API y códigos HTTP (200, 400, 403, 404) utilizando Postman.
3. **Pruebas de Regresión:** Re-ejecución de suites manuales y automatizadas tras la integración de los nuevos endpoints.

## 4. Estrategia de Datos de Prueba (Semillas)
Para garantizar la independencia de los casos de prueba y evitar el estado corrupto del sistema, se utilizará un aislamiento total de datos:
* **Mecanismo:** Restauración de la base de datos local utilizando los archivos de la carpeta `tests/_baseline_data/` (`users.json`, `events.json`, `orders.json`).
* **Herramientas de QA:** Postman (API), Selenium IDE (UI), Apache JMeter (Carga).

## 5. Análisis de Riesgos
En base a lo analizado sobre la arquitectura del sistema, se detectan los siguientes riesgos que podrían presentarse en producción:

* **Riesgo 1: Condiciones de carrera y corrupción de datos.**
  * *¿Por qué es un riesgo?* La persistencia se basa en archivos JSON sin mecanismos de bloqueo transaccional (*locks*). 
  * *¿Qué podría salir mal en producción?* Si dos usuarios intentan comprar simultáneamente la última entrada de un evento, o si el administrador lo elimina en el exacto milisegundo de una compra, el último proceso en guardar el archivo sobreescribirá al anterior. Un cliente podría recibir confirmación de una entrada que jamás se guardó en el sistema.
* **Riesgo 2: Falsos positivos por fragilidad en la automatización UI.**
  * *¿Por qué es un riesgo?* Los scripts de Selenium IDE dependen de selectores estáticos (ID, clases CSS) de la interfaz web.
  * *¿Qué podría salir mal en producción?* Si el equipo de desarrollo altera estéticamente un botón o formulario sin romper la lógica de negocio, los scripts de prueba fallarán, generando falsas alarmas (falsos positivos) y demorando el proceso de validación final.

## 6. Criterios de Aprobación y Salida (Exit Criteria)
* Ejecución exitosa del 100% de los casos de prueba críticos diseñados para los nuevos endpoints (`PATCH` y `DELETE`).
* Ausencia de defectos de Severidad Alta o Bloqueante abiertos al momento de la entrega.
* Suite de pruebas unitarias en `pytest` ejecutándose sin fallos y con entornos JSON correctamente aislados.