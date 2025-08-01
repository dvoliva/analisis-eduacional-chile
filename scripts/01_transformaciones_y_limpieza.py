# -*- coding: utf-8 -*-

"""
01_transformacion_y_limpieza.py
Script para limpiar, transformar y preparar los datos de rendimiento escolar 2024
para el análisis.
"""
import pandas as pd
import os
import sys
import time
import matplotlib.pyplot as plt

#configuración de la salida estándar para manejar caracteres UTF-8
sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = os.path.join("data/rendimiento_2024.csv")  # Ruta del archivo CSV de entrada
OUTPUT_FILE = os.path.join("data/rendimiento_limpio_2024.csv")  # Ruta del archivo CSV de salida
SEPARATOR = ";"  # Separador utilizado en el archivo CSV

#columnas relevantes para el análisis basadas en la exploración previa
# Estas columnas se seleccionan para mantener solo la información necesaria
COLUMNAS_RELEVANTES = [
    #métricas de rendimiento
    'PROM_GRAL', 'ASISTENCIA', 'SIT_FIN_R',
    #dimensiones
    'COD_DEPE2', 'RURAL_RBD', 'GEN_ALU', 'COD_REG_RBD',
    #columna para filtrar por establecimientos funcionando
    'ESTADO_ESTAB',
    #columna que contiene PROM_GRAL 0,0
    'COD_ENSE2'
    ]

#diccionario para mapear los códigos de las columnas a nombres más descriptivos
DEPE_MAP = {
    1: 'Municipal',
    2: 'Particular Subvencionado',
    3: 'Particular Pagado',
    4: 'Corp. de Adm. Delegada',
    5: 'Servicio Local de Educación'
}

RURAL_MAP = {0: 'Urbano',
              1: 'Rural'}

GENERO_MAP = {1: 'Masculino',
               2: 'Femenino'}

REGION_MAP = {
    1: 'Tarapacá', 2: 'Antofagasta', 3: 'Atacama', 4: 'Coquimbo',
    5: 'Valparaíso', 6: "O'Higgins", 7: 'Maule', 8: 'Biobío',
    9: 'La Araucanía', 10: 'Los Lagos', 11: 'Aysén', 12: 'Magallanes',
    13: 'Metropolitana', 14: 'Los Ríos', 15: 'Arica y Parinacota', 16: 'Ñuble'
} 

ENSE2_MAP = {
    2: 'Básica Niños',
    3: 'Básica Adultos',
    4: 'Especial',
    5: 'Media HC Jóvenes',
    6: 'Media HC Adultos',
    7: 'Media TP Jóvenes',
    8: 'Media TP Adultos'
}

start_time = time.time()  # Tiempo de inicio del script 

print("--- Fase 1: Configuración Inicial Completa ---")
print(f"Archivo de entrada: {INPUT_FILE}")
print(f"Se procesarán {len(COLUMNAS_RELEVANTES)} columnas.")

chunks_limpios = []

try:
    #iterador para leer el archivo CSV en chunks
    #esto permite manejar archivos grandes sin cargar todo en memoria
    chunk_iterator = pd.read_csv(
        INPUT_FILE,
        sep=SEPARATOR,
        chunksize=100000,
        usecols=COLUMNAS_RELEVANTES,
        low_memory=False,
        encoding='utf-8'
    )

    #procesar cada chunk
    for i, chunk in enumerate(chunk_iterator):
        if (i + 1) % 5 == 0:
            print(f"Procesando chunk {i+1}...")
        print(f"Chunk {i+1} tiene {len(chunk):,} filas.")

        # Verificar valores únicos antes de filtrar
        # if i == 0:  # Solo en el primer chunk
            # print(f"Valores únicos en ESTADO_ESTAB: {chunk['ESTADO_ESTAB'].unique()}")
            # print(f"Valores únicos en SIT_FIN_R: {chunk['SIT_FIN_R'].unique()}")
    
        #filtro 1: filtrar por establecimientos funcionando
        chunk_filtrado = chunk[chunk['ESTADO_ESTAB'] == 1 ].copy()
        # print(f"Después filtro ESTADO_ESTAB: {len(chunk_filtrado)} filas")
        #filtro 2: solo estudiantes promovidos o reprobados
        chunk_filtrado = chunk_filtrado[chunk_filtrado['SIT_FIN_R'].isin(['P', 'R'])].copy()
        # print(f"Después filtro SIT_FIN_R: {len(chunk_filtrado)} filas")

        #si el chunk está vacío después de los filtros, continuar con el siguiente
        if chunk_filtrado.empty:
            continue
        
        chunk_filtrado['PROM_GRAL'] = chunk_filtrado['PROM_GRAL'].astype(str).str.replace(',', '.')
        chunk_filtrado['ASISTENCIA'] = chunk_filtrado['ASISTENCIA'].astype(str).str.replace(',', '.')

        #convertir PROM_GRAL a numérico
        chunk_filtrado['PROM_GRAL'] = pd.to_numeric(
            chunk_filtrado['PROM_GRAL'],
            errors='coerce'
            )

        #convertir ASISTENCIA a numérico
        chunk_filtrado['ASISTENCIA'] = pd.to_numeric(
            chunk_filtrado['ASISTENCIA'],
            errors='coerce'
            )
        
        #decodificar las columnas categóricas
        chunk_filtrado['TIPO_ESTABLECIMIENTO'] = chunk_filtrado['COD_DEPE2'].map(DEPE_MAP)
        chunk_filtrado['ZONA'] = chunk_filtrado['RURAL_RBD'].map(RURAL_MAP)
        chunk_filtrado['GENERO'] = chunk_filtrado['GEN_ALU'].map(GENERO_MAP)
        chunk_filtrado['REGION'] = chunk_filtrado['COD_REG_RBD'].map(REGION_MAP)
        chunk_filtrado['TIPO_ENSENANZA'] = chunk_filtrado['COD_ENSE2'].map(ENSE2_MAP)


        #agregar el chunk limpio a la lista de chunks limpios
        chunks_limpios.append(chunk_filtrado)

    #concatenar todos los chunks limpios en un solo DataFrame
    if chunks_limpios:
        df_limpio = pd.concat(chunks_limpios, ignore_index=True)

        #eliminar columnas originales que ya no son necesarias
        df_limpio.drop(columns=['COD_DEPE2',
                                'RURAL_RBD',
                                'GEN_ALU',
                                'COD_REG_RBD',
                                'ESTADO_ESTAB',
                                'COD_ENSE2'], inplace=True)

        #reordenar las columnas
        col_ordenadas = ['REGION',
                    'TIPO_ESTABLECIMIENTO',
                    'ZONA',
                    'GENERO',
                    'PROM_GRAL',
                    'TIPO_ENSENANZA',
                    'ASISTENCIA',
                    'SIT_FIN_R']
        df_limpio = df_limpio[col_ordenadas]

        #guardar el DataFrame limpio en un nuevo archivo CSV
        df_limpio.to_csv(OUTPUT_FILE, sep=SEPARATOR, index=False)

        end_time = time.time()  # Tiempo de finalización del script
        total_time = end_time - start_time

        print(f"proceso completado en {total_time:.2f} segundos!")
        print(f"archivo limpio con {len(df_limpio):,} filas en: {OUTPUT_FILE}")
    else:
        print("No se encontraron datos válidos después del filtrado.")
    

except Exception as e:
    print(f"Error inesperado: {e}")
