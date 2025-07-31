# -*- coding: utf-8 -*-

"""
01_transformacion_y_limpieza.py
Script para limpiar, transformar y preparar los datos de rendimiento escolar 2024
para el análisis.
"""
import pandas as pd
import os
import sys

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
    'ESTADO_ESTAB'
    ]

print("--- Fase 1: Configuración Inicial Completa ---")
print(f"Archivo de entrada: {INPUT_FILE}")
print(f"Se procesarán {len(COLUMNAS_RELEVANTES)} columnas.")

clean_chunks = []

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
    
        #filtro 1: filtrar por establecimientos funcionando
        chunk_filtrado = chunk[chunk['ESTADO_ESTAB'] == '1'].copy()

        #filtro 2: solo estudiantes promovidos o reprobados
        chunk_filtrado = chunk_filtrado[chunk_filtrado['SIT_FIN_R'].isin(['P', 'R'])].copy()

        #si el chunk está vacío después de los filtros, continuar con el siguiente
        if chunk_filtrado.empty:
            continue
        
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
        
        #agregar el chunk limpio a la lista de chunks limpios
        clean_chunks.append(chunk_filtrado)

    print(f"Se procesaron {len(clean_chunks)} chunks.")

except Exception as e:
    print(f"Error inesperado: {e}")
