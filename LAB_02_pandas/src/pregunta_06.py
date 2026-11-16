from turtle import pd
from pathlib import Path
import pandas as pd

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    DATA = Path(__file__).resolve().parents[1] / "data"

    df = pd.read_csv(DATA / "tbl1.tsv", sep="\t")
    valores_distintos = sorted(df['c4'].str.upper().unique())

    return valores_distintos

pregunta_06()
