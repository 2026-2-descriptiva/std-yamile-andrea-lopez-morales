import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    # Definición de rutas de archivos
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "sales.csv.gz"
    submission_dir = base_dir / "submission"
    
    # Creación del directorio de salida si no existe
    submission_dir.mkdir(parents=True, exist_ok=True)
    
    # Lectura del archivo CSV comprimido
    df = pd.read_csv(data_path)
    
    # conversión de la columna 'OrderDate' a tipo datetime para poder extraer el mes
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    
    # Creación de la columna 'order_month' que contiene el mes de la orden en formato Period (AAAA-MM)
    df['order_month'] = df['OrderDate'].dt.to_period('M')
    
    # Identificación del mes de la primera compra para cada cliente
    cohortes_clientes = df.groupby('CustomerID')['order_month'].min().reset_index()
    cohortes_clientes.rename(columns={'order_month': 'cohort_month'}, inplace=True)
    
    # Concatenación de la información de cohorte con el DataFrame original
    df = df.merge(cohortes_clientes, on='CustomerID')
    
    # Cálculo del índice de período (meses transcurridos desde la cohorte)
    df['period_index'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)
    df['cohort_month'] = df['cohort_month'].astype(str)
    
    # Agrupación por cohorte y período para contar clientes activos
    cohort_data = df.groupby(['cohort_month', 'period_index'])['CustomerID'].nunique().reset_index()
    cohort_data.rename(columns={'CustomerID': 'active_customers'}, inplace=True)
    
    # Cálculo del tamaño de cada cohorte (clientes activos en el período 0)
    cohort_sizes = cohort_data[cohort_data['period_index'] == 0].set_index('cohort_month')['active_customers']
    
    # Adición de la columna 'cohort_size' al DataFrame principal usando el tamaño de cohorte correspondiente
    cohort_data['cohort_size'] = cohort_data['cohort_month'].map(cohort_sizes)
    
    # Cálculo de Tasa de Retención
    cohort_data['retention_rate'] = cohort_data['active_customers'] / cohort_data['cohort_size']
    
    # Ordenamiento de los datos por cohorte y período para la exportación
    cohort_data = cohort_data.sort_values(by=['cohort_month', 'period_index'])
    
    # Exportación del CSV
    csv_path = submission_dir / "cohort_retention.csv"
    cohort_data.to_csv(csv_path, index=False)
    
    # Creación del mapa de calor de retención
    cohort_pivot = cohort_data.pivot(index='cohort_month', columns='period_index', values='retention_rate')
    
    # Configuración del tamaño de la figura y título
    plt.figure(figsize=(12, 8))
    plt.title("Cohort Retention Rate")
    
    # Creación del mapa de calor con anotaciones y formato de porcentaje
    sns.heatmap(
        cohort_pivot, 
        annot=True, 
        fmt='.0%', 
        cmap='YlGnBu', 
        vmin=0.0, 
        vmax=1.0
    )
    
    plt.ylabel('Cohort Month')
    plt.xlabel('Period Index')
    
    # Ajuste del diseño para evitar superposición de elementos
    plt.tight_layout()
    
    # Exportación del mapa de calor como imagen PNG
    png_path = submission_dir / "cohort_retention_heatmap.png"
    plt.savefig(png_path)
    plt.close() 
    
    return cohort_data

    