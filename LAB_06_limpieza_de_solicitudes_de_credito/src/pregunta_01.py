from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    # Definición de rutas
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "solicitudes_de_credito.csv.gz"
    submission_dir = base_dir / "submission"

    submission_dir.mkdir(parents=True, exist_ok=True)
    report_path = submission_dir / "solicitudes_de_credito.csv"

    # Lectura del archivo CSV
    df = pd.read_csv(data_path, sep=";", index_col=0)

    # Ordenamiento de las columnas requeridas
    columnas_ordenadas = [
        'sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'estrato',
        'comuna_ciudadano', 'fecha_de_beneficio', 'monto_del_credito', 'línea_credito'
    ]
    df = df[columnas_ordenadas]

    # Limpieza de columnas de texto
    columnas_texto = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].str.lower()
            df[col] = df[col].str.replace(r'[-_]', ' ', regex=True)
            df[col] = df[col].apply(lambda x: ' '.join(str(x).split()) if pd.notnull(x) else x)
    
    # Limpieza del Monto del Crédito
    if 'monto_del_credito' in df.columns:
        df['monto_del_credito'] = df['monto_del_credito'].astype(str)
        df['monto_del_credito'] = df['monto_del_credito'].str.replace('$', '', regex=False)
        df['monto_del_credito'] = df['monto_del_credito'].str.replace(',', '', regex=False)
        df['monto_del_credito'] = df['monto_del_credito'].str.split('.').str[0]
        df['monto_del_credito'] = df['monto_del_credito'].astype(int)
        
    # Limpieza del Estrato
    if 'estrato' in df.columns:
        df['estrato'] = df['estrato'].astype(int)
        
    # Normalización de la fecha
    # 7. Normalización de la fecha (CON SOPORTE PARA FORMATOS MEZCLADOS)
    if 'fecha_de_beneficio' in df.columns:
        df['fecha_de_beneficio'] = pd.to_datetime(
            df['fecha_de_beneficio'], 
            dayfirst=True, 
            format='mixed' # <--- ESTA ES LA CLAVE MÁGICA
        )
        df['fecha_de_beneficio'] = df['fecha_de_beneficio'].dt.strftime('%Y-%m-%d')
        
    # Eliminación de filas con nulos (excepto comuna)
    subset_nulos = [col for col in df.columns if col != 'comuna_ciudadano']
    df = df.dropna(subset=subset_nulos)
    
    # Eliminación de duplicados
    df = df.drop_duplicates()
    
    # Exportar resultados
    df.to_csv(report_path, sep=';', index=False, encoding='utf-8')
    
    return df

pregunta_01()
