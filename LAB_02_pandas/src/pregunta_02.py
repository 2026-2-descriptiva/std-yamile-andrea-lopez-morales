from pathlib import Path
import pandas as pd
def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    DATA = Path(__file__).resolve().parents[1] / "data"


    return int(pd.read_csv(DATA / "tbl0.tsv", sep="\t").shape[1])
pregunta_02()
