from pathlib import Path
import pandas as pd

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """
    # Ruta al archivo de datos
    DATA = Path(__file__).resolve().parents[1] / "data"

    # Lectura del archivo tbl0.tsv
    df = pd.read_csv(DATA / "tbl0.tsv", sep="\t")

    # Agrupación por la columna 'c1' y concatenación de los valores de la columna 'c2' ordenados y separados por ':'
    concatenacion_categorias = df.groupby('c1')['c2'].apply(lambda x: ':'.join(map(str, sorted(x)))).reset_index()

    # Renombrar la columna resultante a 'c2'
    concatenacion_categorias.columns = ['c1', 'c2']

    # Establecer 'c1' como índice y ordenar alfabéticamente
    concatenacion_categorias.set_index('c1', inplace=True)
    concatenacion_categorias.sort_index(inplace=True)

    return concatenacion_categorias

pregunta_10()
