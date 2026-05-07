from pathlib import Path
import pandas as pd
import numpy as np

from ..config import COLUMNAS_ESTANDAR
from ..export.export_por_anio import exportar_por_anio


def reader_senamhi(path_carpeta: Path) -> pd.DataFrame:

    archivos = sorted(path_carpeta.glob("*.csv"))

    if not archivos:
        raise FileNotFoundError(f"No se encontraron CSV en {path_carpeta}")

    dfs = []

    for f in archivos:

        print(f"Leyendo {f.name}")

        df = pd.read_csv(
            f,
            skiprows=5,
            encoding="latin1",
            engine="python"
        )

        # Verificación básica de columnas
        if df.shape[1] < 7:
            raise ValueError(
                f"{f.name} no tiene suficientes columnas. "
                f"Columnas detectadas: {df.shape[1]}"
            )

        # Construir datetime (col0 = fecha, col1 = hora)
        datetime = pd.to_datetime(
            df.iloc[:, 0].astype(str) + " " + df.iloc[:, 1].astype(str),
            dayfirst=True,
            errors="coerce"
        )

        direccion = pd.to_numeric(df.iloc[:, 5], errors="coerce")
        velocidad = pd.to_numeric(df.iloc[:, 6], errors="coerce")

        df_out = pd.DataFrame({
            "datetime": datetime,
            "velocidad": velocidad,
            "direccion": direccion,
            "tsm": np.nan,
            "estacion": path_carpeta.name
        })

        dfs.append(df_out)

    df_final = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset=["datetime"])
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    # Exportar por año
    base_dir = Path(__file__).resolve().parents[2]
    OUT_DIR = base_dir / "dataprocesada" / path_carpeta.name

    exportar_por_anio(df_final, OUT_DIR)

    return df_final