# -*- coding: utf-8 -*-

"""
# -*- coding: utf-8 -*-
02_analisis_de_brechas.py
Script para analizar y visualizar las brechas educacionales a partir de los
datos
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import numpy as np

INPUT_FILE = os.path.join("data/rendimiento_limpio_2024.csv")  # Ruta del archivo CSV de entrada
OUTPUT_DIR = os.path.join("output")  # Directorio de salida para gráficos

# configuración para manejar caracteres UTF-8
sys.stdout.reconfigure(encoding='utf-8')

#configuración de estilo de gráficos
sns.set_theme(style="whitegrid", palette="viridis")

#carga final de datos
df = pd.read_csv(INPUT_FILE, sep=';')
#filtrar por tipo de enseñanza para eliminar promedios 0,0
df_analisis = df[df['TIPO_ENSENANZA'] != 'Especial'].copy()
print(f"Datos cargados: {df_analisis.shape[0]} filas, {df_analisis.shape[1]} columnas")

print(f"Filas con PROM_GRAL faltante (NaN): {df_analisis['PROM_GRAL'].isna().sum():,}")


#ANÁLISIS POR TIPO DE ESTABLECIEMIENTO
def analisis_por_tipo_establecimiento():
    """
    Analiza las brechas de rendimiento escolar por tipo de establecimiento.
    """

    #agrupar por tipo de establecimiento y calcular promedios
    brecha_depe = df_analisis.groupby('TIPO_ESTABLECIMIENTO')['PROM_GRAL'].agg(['mean', 'count']).sort_values(by='mean', ascending=False)
    brecha_depe['mean'] = brecha_depe['mean'].round(2)

    print("Brechas por tipo de establecimiento:")
    print(brecha_depe)

    # Visualización
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(x=brecha_depe.index, y=brecha_depe['mean'], palette="magma", width=0.6)

    ax.set_title('Promedio General de Notas por Tipo de Establecimiento (2024)', fontsize=16, weight='bold')
    ax.set_xlabel('Tipo de Establecimiento', fontsize=12)
    ax.set_ylabel('Promedio General de Notas', fontsize=12)

    y_min = brecha_depe['mean'].min() - 0.2  # Un poco por debajo del mínimo
    y_max = brecha_depe['mean'].max() + 0.2  # Un poco por encima del máximo
    ax.set_ylim(y_min, y_max)

    # Establecer ticks cada 0.1 (décimas)
    y_ticks = np.arange(np.floor(y_min * 10) / 10, np.ceil(y_max * 10) / 10 + 0.1, 0.1)
    ax.set_yticks(y_ticks)

    # Agregar valores en las barras para mayor claridad
    for i, v in enumerate(brecha_depe['mean']):
        ax.text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.xticks(rotation=15) # Rotamos las etiquetas para que no se superpongan

    output_path = os.path.join(OUTPUT_DIR, 'brecha_por_dependencia.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nGráfico guardado en: {output_path}")
analisis_por_tipo_establecimiento()

def analisis_por_zona():
    """
    Analiza las brechas de rendimiento escolar por zona (urbana/rural).
    """
    print("\n--- Analizando Brecha por Zona Geográfica (Urbano/Rural) ---")
    brecha_zona = df_analisis.groupby('ZONA')['PROM_GRAL'].agg(['mean', 'count']).round(2)
    print(brecha_zona)

    # Analisis de brecha por región
    print("\n--- Analizando Brecha por Región ---")
    brecha_region = df_analisis.groupby('REGION')['PROM_GRAL'].agg(['mean', 'count']).sort_values(by='mean', ascending=False)
    brecha_region['mean'] = brecha_region['mean'].round(2)
    print(brecha_region)

    #visualización de brecha por región
    plt.figure(figsize=(14, 9))
    ax = sns.barplot(y=brecha_region.index, x=brecha_region['mean'], orient='h', 
                     width=0.6, palette="viridis")  # Barras más delgadas y paleta
    
    ax.set_title('Promedio General de Notas por Región (2024)', fontsize=16, weight='bold')
    ax.set_xlabel('Promedio General de Notas', fontsize=12)
    ax.set_ylabel('Región', fontsize=12)

    # Configurar escala X (horizontal) con décimas
    x_min = brecha_region['mean'].min() - 0.2
    x_max = brecha_region['mean'].max() + 0.2
    ax.set_xlim(x_min, x_max)

    # Establecer ticks cada 0.1 (décimas) en el eje X
    x_ticks = np.arange(np.floor(x_min * 10) / 10, np.ceil(x_max * 10) / 10 + 0.1, 0.1)
    ax.set_xticks(x_ticks)

    # Agregar valores al final de las barras
    for i, v in enumerate(brecha_region['mean']):
        ax.text(v + 0.02, i, f'{v:.2f}', ha='left', va='center', fontweight='bold', fontsize=9)

    # Agregar grid solo en X para mejor legibilidad
    ax.grid(axis='x', alpha=0.3)

    output_path = os.path.join(OUTPUT_DIR, 'brecha_por_region.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {output_path}")
analisis_por_zona()

def analisis_por_genero():
    """
    Analiza las brechas de rendimiento escolar por género.
    """
    print("\n--- Analizando Brecha por Género ---")
    
    # Verificar datos disponibles
    print(f"Total de estudiantes para análisis: {len(df_analisis):,}")
    print(f"Estudiantes con PROM_GRAL válido: {df_analisis['PROM_GRAL'].notna().sum():,}")
    
    # Análisis estadístico por género
    brecha_genero = df_analisis.groupby('GENERO')['PROM_GRAL'].agg(['mean', 'count', 'std', 'median']).round(2)
    
    print("\n📊 Estadísticas detalladas por género:")
    print("Género     | Promedio | Estudiantes | Desv.Est | Mediana")
    print("-" * 58)
    for genero in brecha_genero.index:
        promedio = brecha_genero.loc[genero, 'mean']
        estudiantes = brecha_genero.loc[genero, 'count']
        desv_est = brecha_genero.loc[genero, 'std']
        mediana = brecha_genero.loc[genero, 'median']
        print(f"{genero:<10} | {promedio:>6.2f} | {estudiantes:>10,} | {desv_est:>6.2f} | {mediana:>6.2f}")
    
    # Calcular la brecha de género
    if len(brecha_genero) == 2:
        prom_femenino = brecha_genero.loc['Femenino', 'mean'] if 'Femenino' in brecha_genero.index else 0
        prom_masculino = brecha_genero.loc['Masculino', 'mean'] if 'Masculino' in brecha_genero.index else 0
        brecha = abs(prom_femenino - prom_masculino)
        mejor_genero = 'Femenino' if prom_femenino > prom_masculino else 'Masculino'
        
        print(f"\n🔍 Análisis de brecha:")
        print(f"Diferencia entre géneros: {brecha:.2f} puntos")
        print(f"Género con mejor rendimiento: {mejor_genero}")
        print(f"Porcentaje de diferencia: {(brecha/min(prom_femenino, prom_masculino))*100:.1f}%")
    
    # Análisis por percentiles
    print(f"\n📈 Distribución por percentiles:")
    percentiles = df_analisis.groupby('GENERO')['PROM_GRAL'].quantile([0.25, 0.5, 0.75]).unstack()
    percentiles.columns = ['P25', 'P50 (Mediana)', 'P75']
    percentiles = percentiles.round(2)
    print(percentiles)
    
    # Visualización principal
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Gráfico de barras comparativo
    plt.subplot(2, 2, 1)
    ax1 = sns.barplot(x=brecha_genero.index, y=brecha_genero['mean'], 
                      palette=["#E74C3C", "#3498DB"], width=0.6)
    
    ax1.set_title('Promedio General por Género', fontsize=14, weight='bold')
    ax1.set_xlabel('Género', fontsize=11)
    ax1.set_ylabel('Promedio General', fontsize=11)
    
    # Configurar escala Y con décimas
    y_min = brecha_genero['mean'].min() - 0.15
    y_max = brecha_genero['mean'].max() + 0.15
    ax1.set_ylim(y_min, y_max)
    
    y_ticks = np.arange(np.floor(y_min * 10) / 10, np.ceil(y_max * 10) / 10 + 0.1, 0.1)
    ax1.set_yticks(y_ticks)
    
    # Agregar valores en las barras
    for i, genero in enumerate(brecha_genero.index):
        promedio = brecha_genero.loc[genero, 'mean']
        estudiantes = brecha_genero.loc[genero, 'count']
        ax1.text(i, promedio + 0.02, f'{promedio:.2f}\n({estudiantes:,})', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Subplot 2: Histograma comparativo
    plt.subplot(2, 2, 2)
    for genero in df_analisis['GENERO'].unique():
        if pd.notna(genero):
            datos_genero = df_analisis[df_analisis['GENERO'] == genero]['PROM_GRAL'].dropna()
            plt.hist(datos_genero, bins=30, alpha=0.7, label=genero, density=True)
    
    plt.title('Distribución de Promedios por Género', fontsize=14, weight='bold')
    plt.xlabel('Promedio General', fontsize=11)
    plt.ylabel('Densidad', fontsize=11)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 3: Box plot comparativo
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df_analisis, x='GENERO', y='PROM_GRAL', palette=["#E74C3C", "#3498DB"])
    plt.title('Distribución de Notas por Género', fontsize=14, weight='bold')
    plt.xlabel('Género', fontsize=11)
    plt.ylabel('Promedio General', fontsize=11)
    
    # Subplot 4: Análisis de asistencia por género
    plt.subplot(2, 2, 4)
    brecha_asistencia = df_analisis.groupby('GENERO')['ASISTENCIA'].agg(['mean']).round(1)
    ax4 = sns.barplot(x=brecha_asistencia.index, y=brecha_asistencia['mean'], 
                      palette=["#E74C3C", "#3498DB"], width=0.6)
    
    ax4.set_title('Promedio de Asistencia por Género', fontsize=14, weight='bold')
    ax4.set_xlabel('Género', fontsize=11)
    ax4.set_ylabel('Asistencia (%)', fontsize=11)
    
    # Agregar valores en las barras de asistencia
    for i, genero in enumerate(brecha_asistencia.index):
        asistencia = brecha_asistencia.loc[genero, 'mean']
        ax4.text(i, asistencia + 0.5, f'{asistencia:.1f}%', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    
    # Guardar la visualización
    output_path = os.path.join(OUTPUT_DIR, 'brecha_por_genero.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    print(f"\n💾 Gráfico guardado en: {output_path}")
    
    # Resumen final
    total_validos = brecha_genero['count'].sum()
    print(f"\n📋 Resumen del análisis:")
    print(f"Total de estudiantes analizados: {total_validos:,}")
    print(f"Representatividad: {(total_validos/len(df_analisis))*100:.1f}% de los datos cargados")
    
    if len(brecha_genero) == 2:
        print(f"La brecha de género es de {brecha:.2f} puntos, favorable al género {mejor_genero}")

analisis_por_genero()
