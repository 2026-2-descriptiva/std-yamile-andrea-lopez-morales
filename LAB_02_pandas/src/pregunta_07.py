from pathlib import Path
import pandas as pd

def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """
    # Ruta al archivo de datos
    DATA = Path(__file__).resolve().parents[1] / "data"

    # Lectura del archivo tbl0.tsv
    df = pd.read_csv(DATA / "tbl0.tsv", sep="\t")

    # Agrupación por la columna 'c1' y suma de los valores de la columna 'c2' y ordenamiento alfabético
    sumas_categorias = df.groupby('c1')['c2'].sum().sort_index()
    
    #print(sumas_categorias)
    return sumas_categorias

pregunta_07()
