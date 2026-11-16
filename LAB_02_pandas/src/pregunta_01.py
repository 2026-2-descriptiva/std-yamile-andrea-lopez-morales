from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    DATA = Path(__file__).resolve().parents[1] / "data"

    return int(len(pd.read_csv(DATA / "tbl0.tsv", sep="\t")))
pregunta_01()


