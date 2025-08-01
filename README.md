# Análisis de Brechas Educacionales en Chile 2024

## 📊 Análisis de Datos Educacionales a Gran Escala con Python

Este proyecto demuestra técnicas para el **procesamiento eficiente de archivos CSV masivos** (3.6M+ registros) utilizando Python y pandas, enfocándose en el análisis de brechas educacionales en el sistema escolar chileno.

## 🚀 Características Técnicas Principales

### **Procesamiento de Archivos Grandes**
- ✅ **Chunking Strategy**: Procesamiento por lotes de 100,000 registros
- ✅ **Memory Management**: Gestión eficiente de memoria para datasets de GB
- ✅ **Encoding Handling**: Manejo automático de UTF-8 y caracteres especiales

### **Pipeline de Datos**
1. **Exploración inicial** (`00_exploracion.py`)
2. **Transformación y limpieza** (`01_transformaciones_y_limpieza.py`)
3. **Análisis estadístico** (`02_analisis.py`)

## 🛠️ Ventajas del Enfoque con Python

### **¿Por qué Python para Archivos Grandes?**

#### **1. Procesamiento por Chunks**
```python
# Técnica clave: No cargar todo en memoria
chunk_iterator = pd.read_csv(
    archivo, 
    chunksize=100000,  # Procesar de 100k en 100k
    low_memory=False
)

for chunk in chunk_iterator:
    # Procesar cada bloque independientemente
    chunk_procesado = procesar_chunk(chunk)
    chunks_limpios.append(chunk_procesado)
```

#### **2. Manejo Inteligente de Encoding**
```python
# Solución a problemas de caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')
chunk['COLUMNA'] = chunk['COLUMNA'].astype(str).str.replace(',', '.')
```

#### **3. Filtrado Eficiente**
```python
# Filtros aplicados antes de cargar en memoria
chunk_filtrado = chunk[
    (chunk['ESTADO_ESTAB'] == 1) &  # Solo establecimientos activos
    (chunk['SIT_FIN_R'].isin(['P', 'R']))  # Solo promovidos/reprobados
].copy()
```

## 📈 Resultados del Análisis

### **Datos Procesados**
- **Total registros**: 3,568,930 → 3,076,190 válidos
- **Tiempo de procesamiento**: ~23 segundos
- **Memoria utilizada**: <2GB (vs 15GB+ sin chunking)

### **Brechas Identificadas**

#### **Por Tipo de Establecimiento**
| Tipo | Promedio | Estudiantes |
|------|----------|-------------|
| Particular Pagado | 6.37 | 300,629 |
| Particular Subvencionado | 6.00 | 1,606,172 |
| Municipal | 5.97 | 926,323 |
| Corp. Adm. Delegada | 5.64 | 42,969 |

#### **Por Género**
- **Femenino**: 6.10 (1,498,340 estudiantes)
- **Masculino**: 5.94 (1,577,842 estudiantes)
- **Brecha**: 0.16 puntos (2.7% diferencia)

#### **Por Zona Geográfica**
- **Rural**: 6.11 promedio
- **Urbano**: 6.01 promedio

## 🔧 Stack Tecnológico

### **Librerías Core**
```python
import pandas as pd        # Manipulación de datos
import numpy as np         # Operaciones numéricas
import matplotlib.pyplot as plt  # Visualización
import seaborn as sns      # Gráficos estadísticos
```

## 📊 Visualizaciones Generadas

El proyecto genera automáticamente:
- Histogramas de distribución
- Gráficos de barras comparativos
- Box plots para análisis de dispersión
- Visualizaciones multi-panel

## ⚡ Ventajas del Enfoque vs Alternativas

### **Python + Pandas vs Excel**
| Aspecto | Python | Excel |
|---------|--------|-------|
| **Tamaño máximo** | Ilimitado | 1M filas |
| **Velocidad** | ~23s para 3.6M | Crash |
| **Automatización** | 100% | Limitada |
| **Memoria** | Eficiente | Ineficiente |


## 🚀 Cómo Ejecutar

### **Prerequisitos**
```bash
pip install pandas numpy matplotlib seaborn
```

### **Ejecución**
```bash
# 1. Exploración inicial
python scripts/00_exploracion.py

# 2. Limpieza y transformación
python scripts/01_transformaciones_y_limpieza.py

# 3. Análisis de brechas
python scripts/02_analisis.py
```

## 📁 Estructura del Proyecto

```
analisis-educacional-chile/
├── data/
│   ├── rendimiento_2024.csv           # Dataset original (3.6M registros)
│   └── rendimiento_limpio_2024.csv    # Dataset procesado
├── scripts/
│   ├── 00_exploracion.py              # EDA inicial
│   ├── 01_transformaciones_y_limpieza.py  # Pipeline de limpieza
│   └── 02_analisis.py                 # Análisis estadístico
├── output/
│   ├── *.png                          # Visualizaciones
│   └── *.txt                          # Logs de ejecución
└── env/                               # Entorno virtual
```

## 🎯 Lecciones Técnicas Aprendidas

### **1. Problema de Encoding**
**Síntoma**: Caracteres especiales aparecían como símbolos extraños
**Solución**: `sys.stdout.reconfigure(encoding='utf-8')`

### **2. Problema de Decimales**
**Síntoma**: 90% de datos se convertían a NaN
**Solución**: Conversión de comas a puntos antes de `pd.to_numeric()`

### **3. Problema de Memoria**
**Síntoma**: Sistema se quedaba sin memoria
**Solución**: Procesamiento por chunks de 100k registros

### **4. Problema de Performance**
**Síntoma**: Procesamiento lento
**Solución**: Filtros aplicados antes de operaciones costosas

## 🔍 Casos de Uso

Este enfoque es ideal para:
- **Análisis gubernamentales** con millones de registros
- **Data Science** en datasets grandes
- **Business Intelligence** automatizada
- **Reportes** recurrentes con big data
- **Investigación académica** con datos masivos

## 📚 Conclusiones Técnicas

Python demuestra ser **superior** para análisis de archivos grandes debido a:

1. **Escalabilidad**: Maneja datasets de cualquier tamaño
2. **Flexibilidad**: Adaptable a cualquier formato de datos
3. **Automatización**: Scripts reutilizables y programables
4. **Performance**: Optimizado para operaciones vectorizadas
5. **Ecosystem**: Librerías especializadas para cada necesidad

---

**Dataset**: Datos del Ministerio de Educación de Chile 2024 
            https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/  
**Objetivo**: Demostrar capacidades de Python para análisis
