import pandas as pd

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    # Lectura del archivo CSV comprimido
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Conteo de registros por letra en la primera columna y ordenamiento alfabético
    conteo_letras = df[0].value_counts().sort_index()
    resultado = list(conteo_letras.items())
    #print(resultado)
    return resultado
pregunta_02()