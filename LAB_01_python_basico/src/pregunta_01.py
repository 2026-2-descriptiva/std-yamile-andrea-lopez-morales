import pandas as pd 

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """

    # Leectura del archivo CSV comprimido
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)
    
    #Visualización de los primeros registros del DataFrame
    #print(df.head())
#pregunta_01()

    #Cálculo de la suma de los valores de la segunda columna
    suma_total = int(df[1].sum())
    return suma_total
    #print(suma_total)
pregunta_01()
