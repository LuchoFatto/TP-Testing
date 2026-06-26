# Informe de Cierre y Retrospectiva - Sprint 4

## 1. Evidencia de Correcciones y Regresión

Durante el desarrollo del Sprint 4, el equipo de desarrollo se enfocó en la resolución de los defectos documentados durante las pruebas del Sprint 2.

**Proceso de Corrección:**
Los defectos registrados previamente en [InformeTesting_Sprint2.md](InformeTesting_Sprint2.md) fueron revisados sobre el código fuente y ajustados para alinearlos con los requerimientos establecidos del proyecto.

**Verificación y Regresión:**
Se verificó que los cambios aplicados no alteraran el comportamiento esperado de las funcionalidades ya existentes ni de las nuevas implementaciones incorporadas durante el Sprint. La validación se apoyó en las pruebas disponibles del proyecto y en la revisión del funcionamiento de los módulos involucrados.

**Conclusión de la Fase de Regresión:**
Se concluye que los ajustes realizados no introdujeron impactos negativos en el resto del sistema. La evidencia gráfica disponible del proyecto se encuentra en la carpeta [Evidencias_CP](Evidencias_CP/), donde están documentadas las ejecuciones `CP_01.mkv` a `CP_15.mkv`.

---

## 2. Pruebas No Funcionales (JMeter)

En cumplimiento del punto del TP vinculado a pruebas no funcionales, se ejecutaron evidencias con Apache JMeter sobre el backend local expuesto en `127.0.0.1:8001`, utilizando una Mac M4 como equipo de ejecución.

**Configuración general del plan:**
Se utilizó un `Thread Group` con 10 usuarios, rampa de 30 segundos y duración total de 120 segundos, enviando el header `Content-Type: application/json`. El plan incluyó dos requests sobre endpoints relevantes del sistema: `POST /auth/login` y `GET /events`.

**Evidencia observada en los gráficos y tablas:**
- La imagen [graficos_JMeter/login_load_test_grafico.jpeg](graficos_JMeter/login_load_test_grafico.jpeg) muestra el comportamiento de latencia del login bajo carga, con tiempos bajos y una curva estable al avanzar la ejecución.
- La tabla [graficos_JMeter/tabla_consultar_eventos.jpeg](graficos_JMeter/tabla_consultar_eventos.jpeg) refleja una corrida con `Login` y `Consultar Eventos` en la que ambos requests mantuvieron un promedio de `3 ms`, `0.00%` de error y un throughput elevado, lo que indica que el backend respondió de forma consistente en ese escenario.
- En escenarios de mayor tráfico, la evidencia muestra que los tiempos de respuesta del servidor pueden llegar a triplicarse respecto de la corrida estable anterior, lo que deja en claro una degradación medible del rendimiento cuando aumenta la carga.

**Conclusión de la prueba no funcional:**
La evidencia disponible permite documentar que se ejecutó JMeter sobre endpoints reales del sistema desde una Mac M4 y que al menos una corrida tuvo resultados estables. Además, en un escenario de alto tráfico se observa una degradación clara del rendimiento, ya que los tiempos de respuesta del servidor pueden llegar a triplicarse respecto de la corrida base. En consecuencia, la prueba no funcional deja evidencia concreta de estabilidad en condiciones controladas y de sensibilidad del sistema frente al aumento de carga.

---

## 3. Retrospectiva del Equipo

La experiencia de trabajo en este TP mostró que fue importante arrancar por lo más concreto: entender el proyecto base, leer los requerimientos refinados de [REQUIREMENTS.md](REQUIREMENTS.md) y usar el plan de pruebas de [QA.md](QA.md) como guía para ordenar el resto del trabajo. A partir de eso, los escenarios y casos de [InformeTesting_Sprint2.md](InformeTesting_Sprint2.md) sirvieron para traducir las reglas de negocio en pruebas verificables y trazables.

Durante la ejecución, lo que más ayudó fue mantener una relación directa entre cada caso de prueba y el comportamiento real del sistema. Eso permitió detectar con claridad cuándo un resultado no coincidía con lo esperado, como pasó con los defectos documentados en el Sprint 2, y también facilitó revisar después si los ajustes realmente resolvían el problema sin romper otras partes del sistema.

Otro punto importante fue comprobar que el proyecto no se trataba de desarrollar mucho desde cero, sino de probar bien una base ya existente, con endpoints, persistencia en JSON, usuarios precargados y un frontend mínimo. En ese contexto, el trabajo de testing tuvo más valor cuando se apoyó en evidencia real, en la matriz de trazabilidad y en la comparación entre lo esperado en los documentos y lo observado en la ejecución.

Como aprendizaje general, quedó la idea de que redactar bien también forma parte del testing. No alcanza con decir que algo funciona: hay que poder mostrar por qué funciona, qué se corrigió y qué evidencia lo respalda. Esa fue la parte más útil del proceso, porque obligó a revisar el proyecto con criterio, a escribir y documentar de una manera completa cada fase del mismo.

También se aprendió a usar Trello como apoyo para ordenar el trabajo y seguir el avance del backlog, ya que formó parte de la planificación inicial definida en los requerimientos del proyecto.

---

## 4. Conclusiones Finales del Proyecto

El trabajo realizado durante el TP permitió cerrar una base de validación bastante completa sobre el sistema provisto. A partir de los requerimientos refinados, el plan de pruebas y los casos definidos en el Sprint 2, se pudieron revisar los flujos principales del proyecto y validar el comportamiento de las funcionalidades más importantes del backend.

En particular, el trabajo sobre los dos endpoints incorporados por el equipo permitió comprobar reglas de negocio concretas, registrar defectos, corregirlos y luego verificar que los ajustes no afectaran el resto del sistema. Eso deja una evidencia clara de que el proyecto no se trabajó solo desde la implementación puntual, sino también desde la trazabilidad entre requerimientos, pruebas y resultados.

Con la información disponible hasta este punto, el estado funcional del sistema es consistente con lo esperado para el parcial: los flujos base están documentados, los escenarios críticos tienen casos de prueba definidos y la regresión fue considerada en la validación. Además, se apoyó la revisión en los tests unitarios y de integración disponibles en el proyecto, que sirvieron como referencia para medir la cobertura de los flujos más importantes.

En la parte no funcional, la evidencia de JMeter deja una lectura clara: una corrida de carga con comportamiento estable sobre login y consulta de eventos, ejecutada desde una Mac M4, y una degradación visible cuando el tráfico aumenta, con tiempos de respuesta que pueden triplicarse. Eso aporta evidencia concreta sobre el comportamiento del sistema bajo carga y sobre cómo responde ante escenarios de mayor demanda. Si el sistema va a enfrentarse a un escenario de alta concurrencia, se recomienda aplicar un Load Balancer para distribuir la carga y mejorar la estabilidad del servicio.
