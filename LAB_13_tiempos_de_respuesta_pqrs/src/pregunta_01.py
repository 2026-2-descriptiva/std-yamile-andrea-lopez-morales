from pathlib import Path
import pandas as pd
import numpy as np

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    # Definición de rutas de archivos
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    
    # Lectura de los archivos CSV
    df_web = pd.read_csv(data_dir / "historical_requests_web.csv.gz")
    df_letter = pd.read_csv(data_dir / "historical_requests_letter.csv.gz")

    df_web['channel'] = 'web'
    df_letter['channel'] = 'letter'
    
    df_web = df_web.drop_duplicates()
    df_letter = df_letter.drop_duplicates()
    
    df = pd.concat([df_web, df_letter], ignore_index=True)
    
    # Conversión de fechas y cálculo de días hábiles y calendario
    df['in_date'] = pd.to_datetime(df['in_date'])
    df['out_date'] = pd.to_datetime(df['out_date'])
    df['year'] = df['in_date'].dt.year
    
    # Cálculo de días calendario y hábiles
    respondidas = df['out_date'].notna()
    
    # Días calendario
    df.loc[respondidas, 'calendar_days'] = (df.loc[respondidas, 'out_date'] - df.loc[respondidas, 'in_date']).dt.days
    
    # Días hábiles (usando np.busday_count)
    in_dates_shifted = (df.loc[respondidas, 'in_date'] + pd.Timedelta(days=1)).values.astype('datetime64[D]')
    out_dates_shifted = (df.loc[respondidas, 'out_date'] + pd.Timedelta(days=1)).values.astype('datetime64[D]')
    df.loc[respondidas, 'business_days'] = np.busday_count(in_dates_shifted, out_dates_shifted)
    
    # Cálculo de cumplimiento del plazo
    df['on_time'] = False
    df.loc[respondidas & (df['business_days'] <= 15), 'on_time'] = True
    df['pending_flag'] = df['out_date'].isna()
    
    
    # tabla 1: RESUMEN POR CANAL
    channel_summary = df.groupby('channel').agg(
        requests=('in_date', 'count'),
        pending=('pending_flag', 'sum'),
        on_time_count=('on_time', 'sum'),
        median_business_days=('business_days', 'median')
    ).reset_index()
    
    channel_summary['answered'] = channel_summary['requests'] - channel_summary['pending']
    channel_summary['on_time_rate'] = channel_summary['on_time_count'] / channel_summary['requests']
    
    channel_summary = channel_summary.sort_values('channel')
    columnas_ch = ['channel', 'requests', 'answered', 'pending', 'median_business_days', 'on_time_rate']
    channel_summary = channel_summary[columnas_ch]
    
    
    # tabla 2: RESUMEN POR AÑO Y CANAL
    yearly_summary = df.groupby(['year', 'channel']).agg(
        requests=('in_date', 'count'),
        pending=('pending_flag', 'sum'),
        on_time_count=('on_time', 'sum')
    ).reset_index()
    
    yearly_summary['on_time_rate'] = yearly_summary['on_time_count'] / yearly_summary['requests']
    
    yearly_summary = yearly_summary.sort_values(['year', 'channel'])
    columnas_yr = ['year', 'channel', 'requests', 'pending', 'on_time_rate']
    yearly_summary = yearly_summary[columnas_yr]
    
    
    # Tabla 3: RESUMEN POR DÍA DE ENTRADA
    entry_day_summary = df.groupby('day_name').agg(
        requests=('in_date', 'count'),
        median_calendar_days=('calendar_days', 'median'),
        median_business_days=('business_days', 'median')
    ).reset_index()
    
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    entry_day_summary['day_name'] = pd.Categorical(entry_day_summary['day_name'], categories=orden_dias, ordered=True)
    entry_day_summary = entry_day_summary.sort_values('day_name')
    
    
    # Exportación
    channel_summary.to_csv(submission_dir / "channel_summary.csv", index=False)
    yearly_summary.to_csv(submission_dir / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(submission_dir / "entry_day_summary.csv", index=False)
    
    return channel_summary, yearly_summary, entry_day_summary
    
       
pregunta_01()

