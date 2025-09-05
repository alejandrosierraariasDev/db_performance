import psycopg2
import time
import json
import pandas as pd
import os
import sys
import datetime
from scripts.config import DB_CONFIG


def connect_db():
    """Establece la conexión con la base de datos."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def read_query_from_file(filepath):
    """Lee una consulta SQL desde un archivo."""
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Archivo de consulta no encontrado en {filepath}")
        return None


def run_test(phase):
    """Ejecuta las pruebas de rendimiento para una fase ('antes' o 'despues')."""
    conn = connect_db()
    if not conn:
        return None

    results = []

    with open('data/query_map.json', 'r') as f:
        query_map = json.load(f)

    test_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for query_pair in query_map:
        test_name = query_pair['test_name']
        description = query_pair['description']
        # La clave para el archivo de la consulta ahora depende del argumento 'phase'
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
        results.append({
            'test_name': test_name,
            'description': description,
            'execution_time_seconds': execution_time,
            'rows_processed': rows_processed,
            'timestamp': test_timestamp
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
            df_before.to_csv('output/before_results.csv', index=False)
            print("Resultados de la fase 'antes' guardados en output/before_results.csv")
    elif phase_to_run == 'despues':
        print("--- Ejecutando tests para la fase 'despues' ---")
        df_after = run_test('despues')
        if df_after is not None:
            df_after.to_csv('output/after_results.csv', index=False)
            print("Resultados de la fase 'despues' guardados en output/after_results.csv")
    else:
        print(f"Argumento inválido: {phase_to_run}. Use 'antes' o 'despues'.")
        sys.exit(1)