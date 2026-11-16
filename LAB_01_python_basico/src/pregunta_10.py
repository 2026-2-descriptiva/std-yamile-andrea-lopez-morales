import pandas as pd

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """
    
    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Guardando la letra de la primera columna
    letras = df[0]

    # Cálculo de la cantidad de elementos en la cuarta columna (codes)
    cant_codes = df[3].str.split(",").str.len()

    # Cálculo de la cantidad de pares en la quinta columna (metrics)
    cant_metrics = df[4].str.split(",").str.len()

    # Creación de la lista de tuplas (letter, cant_codes, cant_metrics)
    resultado = list(zip(letras, cant_codes, cant_metrics))

    #print(resultado)
    return resultado
pregunta_10()
