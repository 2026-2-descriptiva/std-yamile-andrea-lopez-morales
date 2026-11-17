import pandas as pd
from pathlib import Path
import json
import numpy as np


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
# Definición de rutas de archivos
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "insurance.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = submission_dir / "privacy_report.json"
    published_path = submission_dir / "insurance_published.csv"
    
    # Lectura del archivo CSV comprimido
    df = pd.read_csv(data_path)
    k_minimo = 5
    
    # Creación de las columnas de grupos para los cuasi-identificadores, Edad
    df['age_group'] = pd.cut(
        df['age'], 
        bins=[18, 30, 40, 50, 65], 
        labels=['18-29', '30-39', '40-49', '50-64'], 
        right=False
    ).astype(str)
    
    # creación de las columnas de grupos para los cuasi-identificadores, IMC
    df['bmi_group'] = pd.cut(
        df['bmi'], 
        bins=[0, 18.5, 25, 30, float('inf')], 
        labels=['bajo peso', 'normal', 'sobrepeso', 'obesidad'], 
        right=False
    ).astype(str)
    
    # creación de las columnas de grupos para los cuasi-identificadores, Número de hijos
    df['children_group'] = pd.cut(
        df['children'], 
        bins=[0, 1, 3, float('inf')], 
        labels=['0', '1-2', '3+'], 
        right=False
    ).astype(str)

    # Cálculo de k-anonimato y registros únicos con los cuasi-identificadores originales
    qi_originales = ['age', 'sex', 'bmi', 'children', 'region']
    conteo_original = df.groupby(qi_originales).size()
    original_k = int(conteo_original.min())
    original_unique_records = int((conteo_original == 1).sum())

    # Creación de esquemas de generalización
    esquemas = {
        'with_children': ['age_group', 'sex', 'bmi_group', 'children_group', 'region'],
        'without_children': ['age_group', 'sex', 'bmi_group', 'region']
    }
    
    reporte_esquemas = {}
    mejores_datos_publicados = None
    mejor_esquema_nombre = None
    max_registros_publicados = -1

    # Evaluación de cada esquema
    for nombre_esquema, qi_esquema in esquemas.items():
        tamanos_clase = df.groupby(qi_esquema).size().reset_index(name='class_size')
        
        # Uninión de los tamaños de clase con el DataFrame original para evaluar k-anonimato
        df_eval = df.merge(tamanos_clase, on=qi_esquema, how='left')
        
        # Filtrado de registros que cumplen con k-anonimato
        df_publicado = df_eval[df_eval['class_size'] >= k_minimo].copy()
        
        # Cálculo de la diversidad de fumadores en las clases publicadas
        diversidad_clases = df_publicado.groupby(qi_esquema)['smoker'].nunique().reset_index(name='smoker_diversity')
        clases_sin_diversidad = diversidad_clases[diversidad_clases['smoker_diversity'] == 1]
        
        # Filtrado de registros que pertenecen a clases sin diversidad de fumadores
        df_sin_div = df_publicado.merge(clases_sin_diversidad, on=qi_esquema, how='inner')
        
        reporte_esquemas[nombre_esquema] = {
            "quasi_identifiers": qi_esquema,
            "equivalence_classes": int(len(tamanos_clase[tamanos_clase['class_size'] > 0])),
            "k_before_suppression": int(tamanos_clase[tamanos_clase['class_size'] > 0]['class_size'].min()),
            "suppressed_records": int(len(df) - len(df_publicado)),
            "published_records": int(len(df_publicado)),
            "published_classes": int(len(df_publicado.groupby(qi_esquema))),
            "classes_without_smoker_diversity": int(len(clases_sin_diversidad)),
            "records_without_smoker_diversity": int(len(df_sin_div))
        }
        
        # Selección del esquema con más registros publicados
        if reporte_esquemas[nombre_esquema]["published_records"] > max_registros_publicados:
            max_registros_publicados = reporte_esquemas[nombre_esquema]["published_records"]
            mejor_esquema_nombre = nombre_esquema
            mejores_datos_publicados = df_publicado

    # Cálculo de estadísticas adicionales
    mean_charges_original = float(df['charges'].mean())
    mean_charges_published = float(mejores_datos_publicados['charges'].mean())
    
    smoker_rate_original = float((df['smoker'] == 'yes').mean())
    smoker_rate_published = float((mejores_datos_publicados['smoker'] == 'yes').mean())

    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": reporte_esquemas,
        "selected_scheme": mejor_esquema_nombre,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published
    }

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
        
    columnas_finales = esquemas[mejor_esquema_nombre] + ['smoker', 'charges']
    mejores_datos_publicados[columnas_finales].to_csv(published_path, index=False)

    return report


pregunta_01()
