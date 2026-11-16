import pandas as pd

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Expansión de la quinta columna (metrics) en filas individuales
    df[4] = df[4].str.split(",")
    df_expandido = df.explode(4)

    # Separación de los pares clave:valor en columnas separadas
    df_expandido["valor_numerico"] = df_expandido[4].str.split(":").str[1].astype(int)

    # Suma de los valores para cada letra de la primera columna
    suma_letras = df_expandido.groupby(0)['valor_numerico'].sum()
    
    # Ordenamiento de las letras en orden alfabético
    suma_letras = suma_letras.sort_index()

    # Conversión del resultado a un diccionario
    resultado = suma_letras.to_dict()

    #print(resultado)
    return resultado

pregunta_12()
