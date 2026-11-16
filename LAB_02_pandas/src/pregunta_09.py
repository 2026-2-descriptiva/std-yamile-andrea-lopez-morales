from pathlib import Path
import pandas as pd

def pregunta_09():
    """
    Retorne la tabla `data/tbl0.tsv` completa con una columna adicional
    llamada `year`, al final, que contenga el año de la fecha de la columna
    `c3` como un texto de cuatro caracteres.

    Ejemplo del formato de la respuesta:

            c0 c1  c2          c3  year
        0    0  E   1  1999-02-28  1999
        1    1  A   2  1999-10-28  1999
        2    2  B   5  1998-05-02  1998
        ...
    """
    
    # Ruta al archivo de datos
    DATA = Path(__file__).resolve().parents[1] / "data"

    # Lectura del archivo tbl0.tsv
    df = pd.read_csv(DATA / "tbl0.tsv", sep="\t")

    # Agregar la columna 'year' al DataFrame, que contiene el año de la fecha en la columna 'c3'
    df['year'] = df['c3'].str.split('-').str[0]

    #print(df)
    return df

pregunta_09()
