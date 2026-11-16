from pathlib import Path
import pandas as pd

def pregunta_11():
    """
    En `data/tbl1.tsv`, cada valor de la columna `c0` aparece en varias
    filas, una por cada letra de la columna `c4`. Construya un DataFrame con
    una fila por cada valor de `c0`, en orden ascendente, y las columnas `c0`
    y `c4`. En `c4`, escriba las letras de ese `c0` ordenadas alfabéticamente
    y separadas por comas.

    Ejemplo del formato de la respuesta:

            c0       c4
        0    0    b,f,g
        1    1    a,c,f
        2    2  a,c,e,f
        ...
    """

    # Ruta al archivo de datos
    DATA = Path(__file__).resolve().parents[1] / "data"

    # Lectura del archivo tbl1.tsv
    df = pd.read_csv(DATA / "tbl1.tsv", sep="\t")

    # Agrupación por la columna 'c0' y construcción de la lista de letras correspondientes
    letras_por_c0 = df.groupby('c0')['c4'].apply(lambda x: ','.join(sorted(x)))

    # Creación del DataFrame resultante con las columnas 'c0' y 'c4'
    resultado = pd.DataFrame({'c0': letras_por_c0.index, 'c4': letras_por_c0.values})

    # Ordenamiento por la columna 'c0'
    resultado = resultado.sort_values(by='c0').reset_index(drop=True)

    #print(resultado)
    return resultado

pregunta_11()
