from pathlib import Path
import pandas as pd

def pregunta_04():
    """
    Usando `data/tbl0.tsv`, calcule el promedio de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son los promedios.

    Ejemplo del formato de la respuesta:

        c1
        A    4.6250
        B    5.1429
        C    5.4000
        ...
    """

    DATA = Path(__file__).resolve().parents[1] / "data"

    df = pd.read_csv(DATA / "tbl0.tsv", sep="\t")
    promedios_categorias = df.groupby('c1')['c2'].mean().sort_index()

    return promedios_categorias

pregunta_04()
