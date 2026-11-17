from pathlib import Path
import pandas as pd
import json
import re

def main():

    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

import pandas as pd
import json
import re
from pathlib import Path

def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    # Definición de rutas de archivos
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "ventas.csv.gz"
    submission_dir = base_dir / "submission"
    
    # Creación del directorio de salida si no existe
    submission_dir.mkdir(parents=True, exist_ok=True)
    report_path = submission_dir / "data_quality_report.json"
    
    # Lectura del archivo CSV comprimido con separador de coma y sin conversión automática de NA
    df = pd.read_csv(data_path, sep=",", dtype=str, keep_default_na=False)
    
    # Normalización de los nombres de las columnas
    df.columns = (
        df.columns
        .str.replace('\ufeff', '')
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
    )
    
    # Análisis de columnas requeridas y no requeridas
    columnas_requeridas = {
        'supplier_id', 'supplier', 'country', 'city', 'purchase_date', 
        'amount', 'discount', 'weight', 'units', 'unit_price', 'contact_email'
    }
    columnas_actuales = set(df.columns)
    
    row_count = int(len(df))
    column_count = int(len(df.columns))
    
    missing_required_columns = sorted(list(columnas_requeridas - columnas_actuales))
    unexpected_columns = sorted(list(columnas_actuales - columnas_requeridas))
    
    # Detección de filas duplicadas y duplicados por supplier_id
    duplicate_row_count = int(df.duplicated().sum())
    
    if 'supplier_id' in df.columns:
        # keep=False cuenta TODOS los registros de un proveedor si aparece repetido
        dup_supplier_count = int(df.duplicated(subset=['supplier_id'], keep=False).sum())
    else:
        dup_supplier_count = 0
        
    # Conteo de valores faltantes por columna (vacíos o 'N/A')
    is_missing = (df == '') | (df == 'N/A')
    missing_value_count_by_column = {col: int(is_missing[col].sum()) for col in df.columns}
    
    # Validación de correos electrónicos
    invalid_email_count = 0
    if 'contact_email' in df.columns:
        
        present_emails = df['contact_email'][~is_missing['contact_email']]
        for email in present_emails:
            email_str = str(email).strip()
            
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email_str):
                invalid_email_count += 1
                
    # Validación de unidades
    invalid_unit_count = 0
    if 'units' in df.columns:
        
        present_units = df['units'][~is_missing['units']]
        for unit in present_units:
            unit_str = str(unit).strip()
            if unit_str.isdigit():
                if int(unit_str) <= 0:
                    invalid_unit_count += 1
            else:
                invalid_unit_count += 1 # Si tiene letras, decimales o símbolos es inválido
                
    # Obtención de valores distintos de la columna 'country'
    country_values = []
    if 'country' in df.columns:
        country_values = sorted(list(df['country'].unique()))
        
    # Construcción del reporte final
    report = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": dup_supplier_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values
    }
    
    # Escritura del reporte en formato JSON
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    return report