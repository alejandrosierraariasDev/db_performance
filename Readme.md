# 🚀 Análisis de Rendimiento de Bases de Datos - Antes y Después de Mejoras

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✓-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 📌 Propósito
Este proyecto permite realizar un **análisis comparativo** del rendimiento de una base de datos **PostgreSQL** antes y después de implementar mejoras. Está diseñado para:

- Medir el impacto de las optimizaciones en consultas críticas
- Identificar cuellos de botella en el rendimiento
- Validar la efectividad de los cambios realizados
- Generar informes detallados para la toma de decisiones

## 📋 Resumen Técnico
El proyecto utiliza **Python, psycopg2, pandas y matplotlib** para:
1. Ejecutar consultas SQL almacenadas en archivos
2. Medir tiempos de ejecución y uso de recursos
3. Analizar índices utilizados en cada consulta
4. Generar informes comparativos con visualizaciones
5. Seguir tendencias de rendimiento a lo largo del tiempo

👉 El resultado es un **informe detallado** que cuantifica la mejora de rendimiento y proporciona información valiosa para optimizaciones futuras.

---

## ✨ Características Clave

### 🔍 Análisis de Consultas
- Ejecución de consultas SQL almacenadas en archivos
- Medición precisa de tiempos de ejecución
- Conteo de filas procesadas
- Identificación de índices utilizados

### 📈 Análisis Comparativo
- Comparación lado a lado de métricas antes/después
- Cálculo de porcentajes de mejora
- Generación de gráficos comparativos
- Seguimiento de tendencias temporales

### 📊 Reportes Avanzados
- Informe detallado en formato Markdown
- Gráficos de rendimiento comparativo
- Análisis de uso de índices
- Tendencias de rendimiento a lo largo del tiempo

### 🛠️ Facilidad de Uso
- Configuración centralizada
- Estructura de proyecto clara
- Código modular y documentado
- Fácil integración con flujos de trabajo existentes

---

## 📂 Estructura del Proyecto

```
/proyecto_db_performance
├── requirements.txt             # Dependencias de Python
├── scripts/
│   ├── config.py               # Configuración de conexión a la BD
│   ├── performance_test.py     # Script principal de medición
│   └── report_generator.py     # Generador de informes
├── queries/                    # Consultas SQL organizadas
│   ├── antes/                  # Consultas originales (antes de mejoras)
│   └── despues/                # Consultas optimizadas (después de mejoras)
├── data/
│   └── query_map.json          # Mapeo de consultas para comparativa
└── output/                     # Resultados e informes
    ├── before_results.csv      # Resultados iniciales
    ├── after_results.csv       # Resultados posteriores
    ├── historical_results.csv  # Historial de ejecuciones
    └── performance_comparison.png  # Gráfico comparativo
```

### Descripción de Archivos Importantes

- **`scripts/performance_test.py`**: 
  - Ejecuta las consultas SQL y mide su rendimiento
  - Registra métricas de tiempo, filas procesadas y uso de índices
  - Almacena resultados en archivos CSV

- **`scripts/report_generator.py`**:
  - Genera informes comparativos en formato Markdown
  - Crea visualizaciones de rendimiento
  - Analiza tendencias a lo largo del tiempo

- **`data/query_map.json`**:
  - Define las consultas a ejecutar y sus metadatos
  - Mapea consultas "antes" con sus equivalentes "después"

## 🚀 Guía de Uso Rápido

### 🔧 Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 10 o superior
- Dependencias del proyecto: `pip install -r requirements.txt`

### 🔄 Flujo de Trabajo

#### 1️⃣ Fase Inicial: Análisis de Línea Base
```bash
# Ejecutar pruebas en el estado actual (antes de mejoras)
python -m scripts.performance_test antes
```

#### 2️⃣ Fase de Optimización
- Implementar mejoras en la base de datos
- Optimizar consultas, índices y configuración
- Documentar cambios realizados

#### 3️⃣ Fase de Validación
```bash
# Ejecutar pruebas después de las mejoras
python -m scripts.performance_test despues
```

#### 4️⃣ Generación de Informe
```bash
# Generar informe comparativo
python -m scripts.report_generator
```

### 📊 Interpretación de Resultados

El informe generado incluirá:
- Comparación de tiempos de ejecución
- Análisis de uso de índices
- Tendencias de rendimiento
- Recomendaciones de optimización

### 🔄 Ejecuciones Posteriores
Cada vez que ejecutes las pruebas, los resultados se agregarán al historial, permitiendo:
- Seguimiento de tendencias a largo plazo
- Análisis del impacto de optimizaciones incrementales
- Identificación de regresiones de rendimiento