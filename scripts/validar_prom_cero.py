"""
Luego de la limpieza y transformación de los datos, dí cuenta que aún aparecían
registros con un promedio general de 0.
Por lo tanto, se creó un nuevo script para validar estos registros y analizar
su distribución.
El resultado nota que son alumnos agrupados en la categoria de "Enseñanza Especial",
lo que es comunicado en la documentación del dataset por el Mineduc (página 5).
"""

import pandas as pd

# Carga el nuevo dataset limpio
df = pd.read_csv('data/rendimiento_limpio_2024.csv', sep=';')

# Filtra el DataFrame para encontrar las filas con promedio 0
df_prom_cero = df[df['PROM_GRAL'] == 0]

print(f"Total de registros con Promedio General = 0: {len(df_prom_cero):,}")

# Analiza la distribución del tipo de enseñanza para esos registros
print("\nDistribución de Tipo de Enseñanza para registros con Promedio Cero:")
print(df_prom_cero['TIPO_ENSENANZA'].value_counts())