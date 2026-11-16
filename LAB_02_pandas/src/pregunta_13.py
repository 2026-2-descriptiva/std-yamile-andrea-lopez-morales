from pathlib import Path
import pandas as pd

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    # Ruta al archivo de datos
    DATA = Path(__file__).resolve().parents[1] / "data"

    # Lectura de los archivos tbl0.tsv y tbl2.tsv
    df_tbl0 = pd.read_csv(DATA / "tbl0.tsv", sep="\t")
    df_tbl2 = pd.read_csv(DATA / "tbl2.tsv", sep="\t")

    # Combinación de las tablas usando la columna 'c0'
    df_combinado = pd.merge(df_tbl0, df_tbl2, on='c0')

    # Suma de los valores de la columna 'c5b' para cada categoría de la columna 'c1'
    resultado = df_combinado.groupby('c1')['c5b'].sum()

    return resultado

pregunta_13()
