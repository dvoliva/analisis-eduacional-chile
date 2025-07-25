# -*- coding: utf-8 -*-

"""
Fase 1: Exploración de Datos de Rendimiento Escolar
==================================================
Este script implementa una estrategia de lectura por trozos (chunks) para manejar
el gran volumen de datos de forma eficiente en memoria.
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

FILE_PATH = "rendimiento_2024.csv"
CHUNK_SIZE = 100000  # Número de filas por chunk
SEPARATOR = ";"  # Separador utilizado en el archivo CSV



#inicializar variables para almacenar información recolectada
total_rows = 0
unique_students = set()
unique_years = set()
chunk_count = 0

#crear iterador con pandas para leer el archivo en chunks
def perfilamiento():
    try:
        chunk_iterator = pd.read_csv(FILE_PATH, sep=SEPARATOR ,chunksize=CHUNK_SIZE, low_memory=False, encoding='utf-8')

        for chunk in chunk_iterator:
            #actualizar el conteo total de filas
            chunk_count += 1

            #contar las filas
            total_rows += len(chunk)
            #extraer estudiantes unicos
            unique_students.update(chunk['MRUN'].unique())
            #extraer años unicos
            unique_years.update(chunk['AGNO'].unique())

            #imprimir resultados
            print("\n-- Perfilamiento Finalizado --")
            print(f"Total de filas procesadas: {total_rows}")
            print(f"Total de estudiantes únicos: {len(unique_students)}")
            print(f"Años presentes encontrados: {len(unique_years)}")

            if len(unique_students) > total_rows:
                print("hay estudiantes que se repiten a lo largo de los años.")
            else:
                print("El número de estudiantes únicos es consistente con el total de filas procesadas.")
            
    except FileNotFoundError:
        print(f"Error: El archivo {FILE_PATH} no se encuentra en la ruta especificada.")
    except Exception as e:
        print(f"Error inesperado: {e}")

#perfilamiento()

#leer solo el primer chunk para analizar a modo de muestra
print("\n-- Análisis de Muestra --")
try: 
    muestra = pd.read_csv(FILE_PATH, sep=SEPARATOR, nrows=CHUNK_SIZE, low_memory=False, encoding='utf-8')
    
    print('primeras filas de la muestra:')
    print(muestra.head())

    print("\nInformación de las columnas y uso de memoria: ")
    muestra.info(memory_usage='deep')

    print("\nEstadísticas descriptivas de las columnas:")
    print(muestra[['PROM_GRAL', 'ASISTENCIA']].describe())
    print(muestra['COD_DEPE2'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

    plt.figure(figsize=(10, 6))
    muestra['PROM_GRAL'].plot(kind='hist', bins=30, edgecolor='black', title='Distribución de Promedio General')
    plt.xlabel('Promedio General')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.savefig('distribucion_promedio_general.png', dpi=300)
    print("Gráfico de distribución de promedio general guardado como 'distribucion_promedio_general.png'.")

except FileNotFoundError:
    print(f"Error: El archivo {FILE_PATH} no se encuentra en la ruta especificada.")
except Exception as e:
    print(f"Error inesperado al procesar la muestra: {e}")


