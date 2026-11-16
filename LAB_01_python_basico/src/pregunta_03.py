import pandas as pd

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    # Lectura del archivo CSV comprimido
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    
    # Agrupación por letra y suma de los valores de la segunda columna
    suma_por_letra = df.groupby(0)[1].sum().sort_index()
    resultado = list(suma_por_letra.items())
    #print(resultado)
    return resultado

pregunta_03()
