import pandas as pd

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    
    # Lectura del archivo CSV comprimido con separador de tabulación y sin encabezado
    df = pd.read_csv("data/data.csv.gz", sep="\t", header=None)

    # Separación de los pares clave:valor en la quinta columna y creación de un DataFrame
    metrics_df = df[4].str.split(',', expand=True).stack().str.split(':', expand=True)
    metrics_df.columns = ['clave', 'valor']
    metrics_df['valor'] = metrics_df['valor'].astype(int)

    # Agrupación por clave y cálculo del valor mínimo y máximo
    min_max_metrics = metrics_df.groupby('clave')['valor'].agg(['min', 'max']).sort_index()

    resultado = [(clave, fila['min'], fila['max']) for clave, fila in min_max_metrics.iterrows()]

    #print(resultado)
    return resultado
pregunta_06()
