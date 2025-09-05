Resumen de Resultados
Las optimizaciones implementadas resultaron en una reducción significativa del tiempo de ejecución de ambas consultas, superando las expectativas iniciales. La ganancia de rendimiento más notable se observó en la consulta de inventario, con una mejora de más del 97%.

Consulta	Tiempo Antes de la Optimización	Tiempo Después de la Optimización	Ganancia de Rendimiento
Reporte de Ventas	0.056 segundos	0.003 segundos	94.64%
Inventario de Películas	0.186 segundos	0.002 segundos	98.92%

Exportar a Hojas de cálculo
Análisis de los Datos
Fase "Antes" de la Optimización
El análisis inicial de las consultas reveló tiempos de ejecución elevados, indicativos de ineficiencias en la lógica o en el diseño de la base de datos.

Reporte de Ventas Mensual: La consulta tardó 0.056 segundos en ejecutarse, procesando un volumen de 16 filas. Este tiempo era considerable para un reporte con un volumen de datos tan bajo.

Inventario de Películas: Esta consulta fue la de peor rendimiento, con un tiempo de ejecución de 0.186 segundos. Su estructura original, que probablemente utilizaba subconsultas anidadas, la hacía particularmente lenta.

Fase "Después" de la Optimización
Después de reescribir y optimizar las consultas, los resultados mejoraron drásticamente, lo que demuestra la efectividad de las técnicas aplicadas, como el reemplazo de subconsultas por JOINs y el ajuste de índices.

Reporte de Ventas Mensual: El tiempo de ejecución se redujo a solo 0.003 segundos, una mejora de casi 20 veces.

Inventario de Películas: El tiempo de ejecución se desplomó a 0.002 segundos, un aumento en la eficiencia de casi 100 veces.

El siguiente gráfico de barras ilustra visualmente la reducción en el tiempo de ejecución.

Conclusiones y Recomendaciones
Las optimizaciones realizadas han demostrado un impacto directo y positivo en el rendimiento del sistema, reduciendo el consumo de recursos y acelerando la generación de reportes clave. La mejora es significativa y justifica la inversión de tiempo en este tipo de proyectos.

Se recomienda continuar con esta metodología de análisis en otras áreas de la base de datos para identificar y resolver cuellos de botella adicionales, asegurando así la escalabilidad y el rendimiento a largo plazo de la plataforma.