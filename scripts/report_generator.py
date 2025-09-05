import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report():
    """Genera un informe de comparación de rendimiento con gráficos."""
    try:
        # Intenta cargar los resultados de ambas fases
        df_before = pd.read_csv('output/before_results.csv')
        df_after = pd.read_csv('output/after_results.csv')
    except FileNotFoundError as e:
        print(f"Error: No se encontraron los archivos de resultados necesarios. Asegúrate de que 'performance_test.py' se ejecutó correctamente y generó 'before_results.csv' y 'after_results.csv'.")
        print(f"Detalle del error: {e}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer los archivos de resultados: {e}")
        return

    # Une los DataFrames para una comparación lado a lado
    df_comparison = pd.merge(df_before, df_after, on='test_name', suffixes=('_before', '_after'))

    # Calcula la mejora de rendimiento en porcentaje
    # Maneja el caso donde el tiempo antes podría ser cero (aunque improbable con datos reales)
    df_comparison['performance_gain_%'] = 0.0 # Inicializa en 0

    # Calcula solo donde el tiempo antes no es cero para evitar división por cero
    valid_rows = df_comparison['execution_time_seconds_before'] > 0
    df_comparison.loc[valid_rows, 'performance_gain_%'] = (
        (df_comparison.loc[valid_rows, 'execution_time_seconds_before'] - df_comparison.loc[valid_rows, 'execution_time_seconds_after']) /
        df_comparison.loc[valid_rows, 'execution_time_seconds_before']
    ) * 100

    # Redondea para una mejor legibilidad
    df_comparison['performance_gain_%'] = df_comparison['performance_gain_%'].round(2)

    # Ordena el DataFrame por tiempo de ejecución antes de la optimización (opcional, para un gráfico más claro)
    df_comparison = df_comparison.sort_values(by='execution_time_seconds_before', ascending=False)

    # Imprime los resultados en consola
    print("\n--- Informe Final de Rendimiento ---")
    print(df_comparison.to_string()) # to_string para mostrar todas las filas y columnas

    # --- Genera y guarda el gráfico de barras ---
    fig, ax = plt.subplots(figsize=(12, 8)) # Tamaño de la figura

    # Selecciona las columnas para el gráfico
    df_comparison.set_index('test_name')[['execution_time_seconds_before', 'execution_time_seconds_after']].plot(
        kind='bar',
        ax=ax,
        color=['#1f77b4', '#2ca02c'], # Colores azul y verde
        title='Comparación de Rendimiento de Consultas: Antes vs. Después de Optimización'
    )

    ax.set_ylabel('Tiempo de Ejecución (segundos)')
    ax.set_xlabel('Nombre de la Prueba de Consulta')
    ax.legend(['Antes de la Optimización', 'Después de la Optimización'])
    plt.xticks(rotation=45, ha='right') # Rota las etiquetas del eje X para mejor legibilidad
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Añade una rejilla horizontal suave
    plt.tight_layout() # Ajusta automáticamente los parámetros de la trama para dar un relleno ajustado

    # Guarda el gráfico en la carpeta 'output'
    output_filename = 'output/performance_comparison.png'
    plt.savefig(output_filename)
    print(f"\nGráfico de comparación guardado en: {output_filename}")
    plt.show() # Muestra el gráfico en una ventana

if __name__ == "__main__":
    generate_report()