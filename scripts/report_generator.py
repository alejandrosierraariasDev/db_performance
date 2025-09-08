import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report():
    try:
        df_before = pd.read_csv('output/before_results.csv')
        df_after = pd.read_csv('output/after_results.csv')
    except FileNotFoundError as e:
        print(f"Error: No se encontraron los archivos de resultados necesarios. Asegúrate de que 'performance_test.py' se ejecutó correctamente y generó 'before_results.csv' y 'after_results.csv'.")
        print(f"Detalle del error: {e}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer los archivos de resultados: {e}")
        return

    df_comparison = pd.merge(df_before, df_after, on='test_name', suffixes=('_before', '_after'))

    df_comparison['performance_gain_%'] = 0.0

    valid_rows = df_comparison['execution_time_seconds_before'] > 0
    df_comparison.loc[valid_rows, 'performance_gain_%'] = (
        (df_comparison.loc[valid_rows, 'execution_time_seconds_before'] - df_comparison.loc[valid_rows, 'execution_time_seconds_after']) /
        df_comparison.loc[valid_rows, 'execution_time_seconds_before']
    ) * 100

    df_comparison['performance_gain_%'] = df_comparison['performance_gain_%'].round(2)
    df_comparison = df_comparison.sort_values(by='execution_time_seconds_before', ascending=False)

    print("\n--- Informe Final de Rendimiento ---")
    print(df_comparison.to_string())

    plt.style.use('ggplot')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [2, 1]})
    
    # Gráfico superior: Tiempos de ejecución
    x = range(len(df_comparison))
    width = 0.35
    
    rects1 = ax1.bar([i - width/2 for i in x], 
                    df_comparison['execution_time_seconds_before'], 
                    width, 
                    label='Antes',
                    color='#3498db',
                    edgecolor='#2980b9',
                    alpha=0.9)
                    
    rects2 = ax1.bar([i + width/2 for i in x], 
                    df_comparison['execution_time_seconds_after'], 
                    width, 
                    label='Después',
                    color='#2ecc71',
                    edgecolor='#27ae60',
                    alpha=0.9)
    
    ax1.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
    ax1.set_title('Comparación de Rendimiento: Tiempos de Ejecución', fontsize=14, pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_comparison['test_name'], rotation=45, ha='right')
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Añadir etiquetas a las barras
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f'{height:.2f}s',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    
    autolabel(rects1)
    autolabel(rects2)
    
    # Gráfico inferior: Registros procesados
    width = 0.4
    ax2.bar([i - width/2 for i in x], 
            df_comparison['rows_processed_before'], 
            width, 
            label='Antes',
            color='#e74c3c',
            alpha=0.7)
            
    ax2.bar([i + width/2 for i in x], 
            df_comparison['rows_processed_after'], 
            width, 
            label='Después',
            color='#f39c12',
            alpha=0.7)
    
    ax2.set_ylabel('Registros Procesados', fontsize=12)
    ax2.set_title('Volumen de Datos Procesados', fontsize=14, pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_comparison['test_name'], rotation=45, ha='right')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Ajustar el espaciado
    plt.subplots_adjust(hspace=0.4)
    plt.tight_layout()
    
    # Añadir título general
    plt.suptitle('Análisis de Rendimiento: Antes vs. Después de la Optimización', 
                fontsize=16, y=1.02)
    
    # Ajustar el diseño para que no se corten las etiquetas
    plt.tight_layout(rect=[0, 0, 1, 0.98])

    output_filename = 'output/performance_comparison.png'
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    print(f"\nGráfico de comparación guardado en: {output_filename}")
    
    # Cerrar la figura para liberar memoria
    plt.close()

if __name__ == "__main__":
    generate_report()