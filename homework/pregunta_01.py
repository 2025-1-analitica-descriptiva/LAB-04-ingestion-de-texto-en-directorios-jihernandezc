# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```

    """
    import os
    import zipfile
    import pandas as pd
    from pathlib import Path

    # Crear directorio output si no existe
    output_dir = Path("files/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Verificar si el archivo zip existe
    zip_path = Path("files/input.zip")
    if not zip_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {zip_path}")

    # Descomprimir el archivo zip
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("files/input")

    def process_directory(base_dir, dataset_type):
        data = []
        base_path = Path(f"files/input/{dataset_type}")

        if not base_path.exists():
            raise FileNotFoundError(f"No se encontró el directorio {base_path}")

        # Procesar cada carpeta de sentimiento
        for sentiment in ["positive", "negative", "neutral"]:
            sentiment_dir = base_path / sentiment
            if sentiment_dir.exists():
                # Leer cada archivo de texto
                for txt_file in sentiment_dir.glob("*.txt"):
                    try:
                        with open(txt_file, "r", encoding="utf-8") as f:
                            phrase = f.read().strip()
                            if phrase:  # Solo agregar si hay contenido
                                data.append({"phrase": phrase, "target": sentiment})
                    except Exception as e:
                        print(f"Error al procesar {txt_file}: {str(e)}")

        if not data:
            raise ValueError(f"No se encontraron datos en {base_path}")

        # Crear DataFrame y guardar como CSV
        df = pd.DataFrame(data)
        output_file = output_dir / f"{dataset_type}_dataset.csv"
        df.to_csv(output_file, index=False)
        return df

    try:
        # Procesar directorios train y test
        train_df = process_directory("files/input", "train")
        test_df = process_directory("files/input", "test")

        # Verificar que los archivos se crearon correctamente
        if not (output_dir / "train_dataset.csv").exists():
            raise FileNotFoundError("No se pudo crear train_dataset.csv")
        if not (output_dir / "test_dataset.csv").exists():
            raise FileNotFoundError("No se pudo crear test_dataset.csv")

        return train_df, test_df

    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        raise