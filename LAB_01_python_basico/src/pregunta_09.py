import pandas as pd

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    #print(df.head())
    
    # Conteo de apariciones de cada clave en la quinta columna
    pares = df[4].str.split(",").explode()
    claves = pares.str.split(":").str[0]
    conteo = claves.value_counts().sort_index()
    
    resultado = conteo.to_dict()

    #print(resultado)
    return resultado

pregunta_09()
