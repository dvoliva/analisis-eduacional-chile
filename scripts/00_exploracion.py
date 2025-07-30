# -*- coding: utf-8 -*-

"""
Fase 0: Exploración de Datos de Rendimiento Escolar
==================================================
Este script implementa una estrategia de lectura por trozos (chunks) para manejar
el gran volumen de datos de forma eficiente en memoria.
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

FILE_PATH = "rendimiento_2024.csv" # Ruta del archivo CSV
CHUNK_SIZE = 100000  # Número de filas por chunk
SEPARATOR = ";"  # Separador utilizado en el archivo CSV
OUTPUT_DIR = "output" # Directorio para guardar los gráficos

# Verificar si el directorio de salida existe, si no, crearlo
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Directorio '{OUTPUT_DIR}' creado para guardar los gráficos.")


#Funcion de perfilamiento para analizar el archivo CSV en chunks
def perfilamiento():
    """
    Perfilamiento del archivo CSV para obtener total de filas 
    y estudiantes únicos.
    """
    #inicializar variables para almacenar información recolectada
    total_rows = 0
    unique_students = set()
    
    try:
        #crear iterador con pandas para leer el archivo en chunks(trozos de archivo)
        chunk_iterator = pd.read_csv(
            FILE_PATH,
            sep=SEPARATOR,
            chunksize=CHUNK_SIZE,
            low_memory=False,
            encoding='utf-8'
        )

        for chunk in chunk_iterator:
            #actualizar el conteo total de filas
            total_rows += len(chunk)

            #actualiza el set de estudiantes únicos
            unique_students.update(chunk['MRUN'].unique())

        #imprimir resultados
        print("\n-- Perfilamiento Finalizado --")
        print(f"Total de filas procesadas: {total_rows}")
        print(f"Total de estudiantes únicos: {len(unique_students)}")
            
    except FileNotFoundError:
        print(f"Error: El archivo {FILE_PATH} no se encuentra en la ruta especificada.")
    except Exception as e:
        print(f"Error inesperado: {e}")
perfilamiento()

#leer solo el primer chunk para analizar a modo de muestra
def analizar_muestra():

    print("\n-- Análisis de Muestra --")
    try: 
        muestra = pd.read_csv(FILE_PATH, sep=SEPARATOR, nrows=CHUNK_SIZE, low_memory=False, encoding='utf-8')

        columnas_numericas = ['PROM_GRAL', 'ASISTENCIA']
        for col in columnas_numericas:
            # Primero aseguramos que la columna sea tipo string
            muestra[col] = muestra[col].astype(str)
            # Luego realizamos la conversión a numérico
            muestra[col] = pd.to_numeric(
                muestra[col].str.replace(',', '.'),
                errors='coerce'
            )

        print(muestra[columnas_numericas].dtypes)
    
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
        plt.savefig('output/distribucion_promedio_general.png', dpi=300)
        print("Gráfico de distribución de promedio general guardado en 'output/distribucion_promedio_general.png'.")

    except FileNotFoundError:
        print(f"Error: El archivo {FILE_PATH} no se encuentra en la ruta especificada.")
    except Exception as e:
        print(f"Error inesperado al procesar la muestra: {e}")
#analizar_muestra()
