import psycopg2
import time
import json
import pandas as pd
import os
import sys
import datetime
from scripts.config import DB_CONFIG
from collections import defaultdict


def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def read_query_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Archivo de consulta no encontrado en {filepath}")
        return None


def get_index_usage(conn, query):
    """Obtiene información sobre los índices utilizados en una consulta"""
    try:
        with conn.cursor() as cur:
            # Ejecutar EXPLAIN ANALYZE para obtener el plan de ejecución
            cur.execute(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}")
            plan = cur.fetchone()[0][0]
            
            # Extraer información de índices usados
            used_indexes = set()
            
            def extract_indexes(node):
                if 'Index Name' in node and node['Index Name']:
                    used_indexes.add(node['Index Name'])
                if 'Plans' in node:
                    for plan in node['Plans']:
                        extract_indexes(plan)
            
            if 'Plan' in plan:
                extract_indexes(plan['Plan'])
            
            return list(used_indexes) if used_indexes else []
    except Exception as e:
        print(f"Error al obtener información de índices: {e}")
        return []

def load_historical_data():
    """Carga datos históricos para análisis de tendencias"""
    historical_data = defaultdict(list)
    try:
        if os.path.exists('output/historical_results.csv'):
            hist_df = pd.read_csv('output/historical_results.csv')
            for _, row in hist_df.iterrows():
                historical_data[row['test_name']].append({
                    'timestamp': row['timestamp'],
                    'execution_time_seconds': row['execution_time_seconds'],
                    'rows_processed': row['rows_processed']
                })
    except Exception as e:
        print(f"Error al cargar datos históricos: {e}")
    return historical_data

def calculate_trends(test_name, current_execution_time, historical_data):
    """Calcula tendencias basadas en datos históricos"""
    if test_name not in historical_data or len(historical_data[test_name]) < 2:
        return None, None, None
    
    history = historical_data[test_name]
    # Tomar las últimas 5 ejecuciones para la tendencia
    recent_runs = sorted(history, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    if len(recent_runs) < 2:
        return None, None, None
    
    # Calcular tiempo promedio histórico
    avg_time = sum(r['execution_time_seconds'] for r in recent_runs) / len(recent_runs)
    
    # Calcular tendencia (regresión lineal simple)
    times = [r['execution_time_seconds'] for r in recent_runs]
    x = range(len(times))
    n = len(times)
    if n > 1:
        x_mean = sum(x) / n
        y_mean = sum(times) / n
        numerator = sum((x[i] - x_mean) * (times[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        trend = numerator / denominator if denominator != 0 else 0
    else:
        trend = 0
    
    # Comparar con la ejecución actual
    if current_execution_time > avg_time * 1.2:
        performance = 'worse_than_average'
    elif current_execution_time < avg_time * 0.8:
        performance = 'better_than_average'
    else:
        performance = 'normal'
    
    return avg_time, trend, performance

def run_test(phase):
    conn = connect_db()
    if not conn:
        return None

    results = []
    historical_data = load_historical_data()
    
    with open('data/query_map.json', 'r') as f:
        query_map = json.load(f)

    test_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for query_pair in query_map:
        test_name = query_pair['test_name']
        description = query_pair['description']
        query_file_key = 'before' if phase == 'antes' else 'after'
        query_file = query_pair[query_file_key]
        query_path = os.path.join('queries', phase, query_file)

        query = read_query_from_file(query_path)
        if not query:
            continue

        print(f"Ejecutando '{test_name}' para la fase '{phase}'...")
        start_time = time.time()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                rows_processed = cur.rowcount
        except Exception as e:
            print(f"Fallo de ejecución para '{test_name}': {e}")
            rows_processed = "N/A"
            continue

        end_time = time.time()
        execution_time = end_time - start_time
        # Obtener información de índices
        used_indexes = get_index_usage(conn, query)
        
        # Calcular tendencias
        avg_time, trend, performance = calculate_trends(test_name, execution_time, historical_data)
        
        results.append({
            'test_name': test_name,
            'description': description,
            'execution_time_seconds': execution_time,
            'rows_processed': rows_processed,
            'timestamp': test_timestamp,
            'used_indexes': ', '.join(used_indexes) if used_indexes else 'Ninguno',
            'avg_execution_time': avg_time if avg_time is not None else 'N/A',
            'trend': f"{trend:.4f}" if trend is not None else 'N/A',
            'performance': performance if performance is not None else 'N/A'
        })
        print(f"'{test_name}' completada en {execution_time:.4f} segundos.\n")

    conn.close()
    return pd.DataFrame(results)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.performance_test [antes|despues]")
        sys.exit(1)

    phase_to_run = sys.argv[1].lower()

    if phase_to_run == 'antes':
        print("--- Ejecutando tests para la fase 'antes' ---")
        df_before = run_test('antes')
        if df_before is not None:
            # Guardar en el archivo histórico
            if os.path.exists('output/historical_results.csv'):
                df_hist = pd.read_csv('output/historical_results.csv')
                df_hist = pd.concat([df_hist, df_before], ignore_index=True)
            else:
                df_hist = df_before
            df_hist.to_csv('output/historical_results.csv', index=False)
            
            df_before.to_csv('output/before_results.csv', index=False)
            print("Resultados de la fase 'antes' guardados en output/before_results.csv")
            print("Datos históricos actualizados en output/historical_results.csv")
    elif phase_to_run == 'despues':
        print("--- Ejecutando tests para la fase 'despues' ---")
        df_after = run_test('despues')
        if df_after is not None:
            # Guardar en el archivo histórico
            if os.path.exists('output/historical_results.csv'):
                df_hist = pd.read_csv('output/historical_results.csv')
                df_hist = pd.concat([df_hist, df_after], ignore_index=True)
            else:
                df_hist = df_after
            df_hist.to_csv('output/historical_results.csv', index=False)
            
            df_after.to_csv('output/after_results.csv', index=False)
            print("Resultados de la fase 'despues' guardados en output/after_results.csv")
            print("Datos históricos actualizados en output/historical_results.csv")
    else:
        print(f"Argumento inválido: {phase_to_run}. Use 'antes' o 'despues'.")
        sys.exit(1)