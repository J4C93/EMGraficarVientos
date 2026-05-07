from pathlib import Path
import pandas as pd


def clean_ema(path_estacion: Path) -> pd.DataFrame:

    archivos = sorted(path_estacion.glob("*.csv"))

    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos en {path_estacion}")

    dfs = []

    for f in archivos:

        print(f"Leyendo {f.name}")

        df = pd.read_csv(f)

        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df["velocidad"] = pd.to_numeric(df["velocidad"], errors="coerce")
        df["direccion"] = pd.to_numeric(df["direccion"], errors="coerce")
        df["tsm"] = pd.to_numeric(df["tsm"], errors="coerce")

        dfs.append(df)

    df_final = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset=["datetime"])
        .drop_duplicates(subset="datetime")
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    return df_final