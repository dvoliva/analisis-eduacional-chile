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

FILE_PATH = "data/rendimiento_2024.csv" # Ruta del archivo CSV
CHUNK_SIZE = 100000  # Número de filas por chunk
SEPARATOR = ";"  # Separador utilizado en el archivo CSV
OUTPUT_DIR = "output" # Directorio para guardar los gráficos

# Diccionarios de mapeo para traducir códigos a etiquetas descriptivas
MAPEOS = {
    'COD_DEPE2': {
        1: 'Municipal',
        2: 'Particular Subvencionado',
        3: 'Particular Pagado',
        4: 'Corporación de Administración Delegada',
        5: 'Servicio Local de Educación'
    },
    'RURAL_RBD': {
        0: 'Urbano',
        1: 'Rural'
    },
    'GEN_ALU': {
        0: 'Sin información',
        1: 'Masculino',
        2: 'Femenino'
    },
    'SIT_FIN_R': {
        'P': 'Promovido',
        'T': 'Trasladado',
        'Y': 'Retirado',
        'R': 'Reprobado',
        '': 'Sin información'
    },
    'COD_REG_RBD': {
        1: 'Tarapacá',
        2: 'Antofagasta',
        3: 'Atacama',
        4: 'Coquimbo',
        5: 'Valparaíso',
        6: 'Libertador General Bernardo O\'Higgins',
        7: 'Maule',
        8: 'Biobío',
        9: 'La Araucanía',
        10: 'Los Lagos',
        11: 'Aysén del General Carlos Ibáñez del Campo',
        12: 'Magallanes y de la Antártica Chilena',
        13: 'Metropolitana de Santiago',
        14: 'Los Ríos',
        15: 'Arica y Parinacota',
        16: 'Ñuble'
    }
}

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
        
        print("\n-- Iniciando Perfilamiento --")

        for chunk in chunk_iterator:
            #actualizar el conteo total de filas
            total_rows += len(chunk)

            #actualiza el set de estudiantes únicos
            unique_students.update(chunk['MRUN'].unique())

        #imprimir resultados
        print(f"Total de filas procesadas: {total_rows}")
        print(f"Total de estudiantes únicos: {len(unique_students)}")    
        print("\n-- Perfilamiento Finalizado --")

    except FileNotFoundError:
        print(f"Error: El archivo {FILE_PATH} no se encuentra en la ruta especificada.")
    except Exception as e:
        print(f"Error inesperado: {e}")
perfilamiento()

def analizar_columnas_claves():
    """
    Analiza las columnas categoricas y de métricas seleccionadas
    para el análisis posterior.
    """
    #definir columnas categoricas
    columnas_categoricas = ['COD_DEPE2', 'RURAL_RBD', 'GEN_ALU', 'SIT_FIN_R', 'COD_REG_RBD']
    #diccionario para guardar los conteos de cada columna
    conteos_columnas_categoricas = {col: {} for col in columnas_categoricas}
    print("\n--- Iniciando Análisis de Columnas Clave ---")

    try:
        chunk_iterator = pd.read_csv(
                FILE_PATH,
                sep=SEPARATOR,
                chunksize=CHUNK_SIZE,
                low_memory=False,
                encoding='utf-8'
            )
                
        #Procesando distribuciones de columnas categóricas
        for chunk in chunk_iterator:
            for col in columnas_categoricas:
                count = chunk[col].value_counts().to_dict()
                for value, count in count.items():
                    conteos_columnas_categoricas[col][value] = conteos_columnas_categoricas[col].get(value, 0) + count

        print("\n--- Distribución de Columnas Clave (Total) ---")
        for col, counts in conteos_columnas_categoricas.items():
            print(f'\nDistribución de {col}:')
            
            # Crear DataFrame y mapear valores si existe mapeo
            df_counts = pd.DataFrame(list(counts.items()), columns=['Valor', 'Frecuencia'])
            
            if col in MAPEOS:
                # Agregar columna con descripción
                df_counts['Descripción'] = df_counts['Valor'].map(MAPEOS[col]).fillna('Valor desconocido')
                # Reordenar columnas para mejor visualización
                df_counts = df_counts[['Valor', 'Descripción', 'Frecuencia']]
            
            print(df_counts)

        #Procesando muestra para columnas númericas
        print("\n--- Procesando muestra para columnas numéricas ---")
        muestra = pd.read_csv(
            FILE_PATH, 
            sep=SEPARATOR, 
            nrows=500000,  # Leer una muestra de 500,000 filas
            low_memory=False, 
            encoding='utf-8'
            )

        print("\n--- Estadísticas descriptivas de la muestra ---")
        print(muestra[[]].describe())

        columnas_numericas = ['PROM_GRAL', 'ASISTENCIA']
        for col in columnas_numericas:
            # Primero aseguramos que las columna sean tipo string
            muestra[col] = muestra[col].astype(str)
            # Luego realizamos la conversión a numérico
            muestra[col] = pd.to_numeric(
                muestra[col].str.replace(',', '.'),
                errors='coerce'
            )

            plt.figure(figsize=(12, 7))
            muestra[col].plot(kind='hist', bins=50, edgecolor='black')
            plt.title(f'Distribución de {col} (Muestra de 500,000 registros)')
            plt.xlabel(col)
            plt.ylabel('Frecuencia')
            plt.grid(axis='y', alpha=0.75)
            
            output_path = os.path.join(OUTPUT_DIR, f'distribucion_{col.lower()}.png')
            plt.savefig(output_path, dpi=300)
            print(f"Gráfico de distribución para '{col}' guardado en: '{output_path}'")

        print("\n--- Información detallada de la muestra ---")
        muestra.info()

    except Exception as e:
        print(f"Error al procesar las columnas categóricas: {e}")
analizar_columnas_claves()
