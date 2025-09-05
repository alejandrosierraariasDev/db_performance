# 🚀 Proyecto de Optimización de Rendimiento de Bases de Datos

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✓-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 📌 Resumen
Este proyecto presenta una **metodología práctica** para evaluar y optimizar el rendimiento de una base de datos **PostgreSQL**.  
Se utilizan **Python, psycopg2, pandas y matplotlib** para medir el tiempo de ejecución de consultas críticas **antes y después** de aplicar mejoras.  

👉 El resultado final es un **informe comparativo** con métricas y visualizaciones que validan la ganancia de rendimiento.

---

## ✨ Características
- 🔍 **Evaluación Previa**: mide las consultas en el estado original de la base de datos.  
- ⚡ **Evaluación Posterior**: compara el rendimiento tras aplicar optimizaciones.  
- 📂 **Código Reutilizable**: consultas almacenadas en archivos `.sql` para fácil mantenimiento.  
- 📊 **Reporte Automático**: genera tabla y gráfico de barras con las mejoras.  
- 🗄️ **Metodología Probada**: utiliza la base de datos de ejemplo **Pagila**.  

---

## 📂 Estructura del Proyecto
```
/proyecto_db_performance
├── requirements.txt
├── scripts/
│   ├── config.py              # Configuración de conexión a la BD
│   ├── performance_test.py    # Script principal de medición
│   └── report_generator.py    # Script para generar informe final
├── queries/
│   ├── antes/                 # Consultas originales
│   └── despues/               # Consultas optimizadas
├── data/
│   └── query_map.json         # Mapeo de consultas para comparativa
└── output/
    ├── before_results.csv
    ├── after_results.csv
    └── performance_comparison.png

```
## ▶️ Ejecución del Script de Pruebas para medir el rendimiento de las consultas (fase **antes/después**)
**🟢 Paso 1: Analisis inicial**
```
python -m scripts.performance_test antes
```
**🛠 ️Paso 2
Fase de Desarrollo y Optimización (N meses) este es el periodo donde se optimiza la BBDD**
```
Progreso: 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ 40%
```

**⚙️ Paso 3: Desarrollo finalizado la optimizacion y empezamos la verificacion posterior**

```
python -m scripts.performance_test despues
```
**📊 Paso 4: Generar el Informe Final**
Cuando ya tengas los dos archivos CSV (before_results.csv y after_results.csv), puedes generar el informe final para visualizar los resultados.

```
python -m scripts.report_generator
```