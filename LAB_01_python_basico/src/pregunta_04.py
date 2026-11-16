import pandas as pd

def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    # Lectura del archivo CSV comprimido sin encabezado y con separador de tabulación
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Transformación de la tercera columna a tipo datetime para extraer el mes
    meses = df[2].str.split('-').str[1]

    # Conteo registros por mes en la tercera columna y ordenamiento por mes 
    conteo = meses.value_counts().sort_index()
    resultado = list(conteo.items())
    #print(resultado)
    return resultado

pregunta_04()
