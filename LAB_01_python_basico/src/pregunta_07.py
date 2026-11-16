import pandas as pd

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Agrupación por la segunda columna y construcción de la lista de letras correspondientes
    letras_por_valor = df.groupby(1)[0].agg(list)

    # Creación de la lista de tuplas (valor, letras) ordenada por el valor
    resultado = [(int(valor), letras) for valor, letras in letras_por_valor.items()]
    
    #print(resultado)
    return resultado

pregunta_07()
