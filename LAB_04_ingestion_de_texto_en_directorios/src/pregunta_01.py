from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    root = Path(__file__).resolve().parents[1]
    output = root / "submission"
    output.mkdir(exist_ok=True)
    tables = {}
    for split in ("train", "test"):
        records = []
        split_dir = root / "data" / split
        if not split_dir.exists():
            raise FileNotFoundError(f"Falta la carpeta de entrada: {split_dir}")
        for category_dir in sorted(p for p in split_dir.iterdir() if p.is_dir()):
            for path in sorted(category_dir.glob("*.txt")):
                phrase = path.read_text(encoding="utf-8-sig").strip()
                records.append({"phrase": phrase, "target": category_dir.name})
        table = pd.DataFrame(records, columns=["phrase", "target"])
        table.to_csv(output / f"{split}_dataset.csv", index=False, encoding="utf-8")
        tables[split] = table
    return tables["train"], tables["test"]

if __name__ == "__main__":
    pregunta_01()


pregunta_01()
