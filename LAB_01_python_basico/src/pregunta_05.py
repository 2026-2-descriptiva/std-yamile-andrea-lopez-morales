import pandas as pd

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Agrupación por letra y cálculo del valor máximo y mínimo de la segunda columna
    max_min_letra = df.groupby(0)[1].agg(['max', 'min'])
    
    resultado = [(letra, int(fila["max"]), int(fila["min"])) for letra, fila in max_min_letra.iterrows()]

    #print(resultado)
    return resultado

pregunta_05()