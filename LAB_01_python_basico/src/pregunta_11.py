import pandas as pd

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Expansión de la cuarta columna (codes) en filas individuales
    df[3] = df[3].str.split(",")
    df_expandido = df.explode(3)

    # Suma de los valores de la segunda columna (value) para cada letra
    suma_letras = df_expandido.groupby(3)[1].sum()
    suma_letras = suma_letras.sort_index()
    

    # Conversión del resultado a un diccionario
    resultado = suma_letras.to_dict()

    #print(resultado)
    return resultado

pregunta_11()
