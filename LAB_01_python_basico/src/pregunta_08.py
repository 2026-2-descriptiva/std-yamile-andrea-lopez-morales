import pandas as pd

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)
    
    # Agrupación por la segunda columna, agregación de letras únicas y ordenamiento alfabético
    letras_por_valor = df.groupby(1)[0].agg(lambda x: sorted(set(x)))

    # Creación de la lista de tuplas (valor, letras) ordenada por el valor
    resultado = [(int(valor), letras) for valor, letras in letras_por_valor.items()]

    #print(resultado)
    return resultado

pregunta_08()
