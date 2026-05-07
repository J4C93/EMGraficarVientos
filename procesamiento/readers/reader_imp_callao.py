from pathlib import Path
import pandas as pd
import numpy as np
import re

# Ajusta el import según tu estructura real
from ..config import COLUMNAS_ESTANDAR


def reader_imp_callao(path_carpeta: Path) -> pd.DataFrame:
    """
    Lee todos los archivos ReportEMACallaoXXXX.csv dentro de la carpeta,
    los unifica y devuelve un DataFrame estandarizado.
    """

    # Buscar archivos válidos
    archivos = sorted(path_carpeta.glob("ReportEMACallao*.csv"))

    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos Callao en {path_carpeta}")

    dfs = []

    for f in archivos:
        print(f"Leyendo {f.name}")

        df = pd.read_csv(
            f,
            sep=None,          # autodetecta separador
            engine="python",
            encoding="latin1"
        )

        # Validación defensiva
        if df.shape[1] < 13:
            raise ValueError(
                f"{f.name} tiene solo {df.shape[1]} columnas. "
                "El separador no se interpretó correctamente."
            )

        # Extraer columnas por posición (según clean_ema.py)
        df_out = pd.DataFrame({
            "datetime": df.iloc[:, 0],
            "tsm": df.iloc[:, 2],
            "direccion": df.iloc[:, 11],
            "velocidad": df.iloc[:, 12],
        })

        # Conversión de tipos
        df_out["datetime"] = pd.to_datetime(df_out["datetime"], errors="coerce")

        for col in ["tsm", "direccion", "velocidad"]:
            df_out[col] = pd.to_numeric(df_out[col], errors="coerce")

        dfs.append(df_out)

    # Unir todos los años
    df_final = (
        pd.concat(dfs, ignore_index=True)
          .dropna(subset=["datetime"])
          .sort_values("datetime")
          .reset_index(drop=True)
    )

    # Asegurar unidades (si ya está en m/s no hacer nada)
    # Si estuviera en km/h descomentar:
    # df_final["velocidad"] = df_final["velocidad"] / 3.6

    # Agregar columna estación
    df_final["estacion"] = "IMP Callao"

    # Reordenar según contrato estándar
    df_final = df_final[COLUMNAS_ESTANDAR]

    from ..export.export_por_anio import exportar_por_anio
    OUT_DIR = Path(__file__).resolve().parents[2] / "dataprocesada" / "IMP Callao"
    exportar_por_anio(df_final, OUT_DIR)


    return df_final