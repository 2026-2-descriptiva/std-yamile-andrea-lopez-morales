from pathlib import Path
import re
import pandas as pd


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    path = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    header = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.+)$")
    records = []
    current = None
    for line in lines:
        match = header.match(line)
        if match:
            if current is not None:
                records.append(current)
            current = [int(match.group(1)), int(match.group(2)),
                       float(match.group(3).replace(",", ".")), [match.group(4)]]
        elif current is not None and line.strip() and not line.lstrip().startswith("-"):
            current[3].append(line.strip())
    if current is not None:
        records.append(current)
    rows = []
    for num, count, percent, parts in records:
        text = re.sub(r"\s+", " ", " ".join(parts)).strip().rstrip(".")
        keywords = ", ".join(item.strip() for item in text.split(","))
        rows.append((num, count, percent, keywords))
    return pd.DataFrame(rows, columns=["cluster", "cantidad_de_palabras_clave",
                                       "porcentaje_de_palabras_clave", "principales_palabras_clave"])


pregunta_01()
