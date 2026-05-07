from pathlib import Path
import pandas as pd

from ..config import COLUMNAS_ESTANDAR


def reader_imp_camana(path_carpeta: Path) -> pd.DataFrame:

    archivos = sorted(path_carpeta.glob("Weathercloud Est  Camana *.csv"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos Camana en {path_carpeta}"
        )

    dfs = []

    for f in archivos:

        print(f"Leyendo {f.name}")

        df = pd.read_csv(
            f,
            sep=",",
            encoding="latin1",
            engine="python",
            on_bad_lines="skip"
        )

        # normalizar nombres
        cols = [c.lower() for c in df.columns]

        # detectar columnas
        col_time = None
        col_vel = None
        col_dir = None

        for c in df.columns:

            cl = c.lower()

            if "date" in cl:
                col_time = c

            if "average wind speed" in cl:
                col_vel = c

            if "average wind direction" in cl:
                col_dir = c

        if col_time is None or col_vel is None or col_dir is None:
            raise ValueError(
                f"No se detectaron columnas necesarias en {f.name}\n"
                f"Columnas disponibles: {list(df.columns)}"
            )

        df_out = pd.DataFrame({
            "datetime": df[col_time],
            "velocidad": df[col_vel],
            "direccion": df[col_dir],
        })

        df_out["datetime"] = pd.to_datetime(
            df_out["datetime"],
            errors="coerce"
        )

        for c in ["direccion", "velocidad"]:
            df_out[c] = pd.to_numeric(df_out[c], errors="coerce")

        df_out["tsm"] = pd.NA

        dfs.append(df_out)

    df_final = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset=["datetime"])
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    df_final["estacion"] = "IMP Camana"

    df_final = df_final[COLUMNAS_ESTANDAR]

    from ..export.export_por_anio import exportar_por_anio

    OUT_DIR = Path(__file__).resolve().parents[2] / "dataprocesada" / "IMP Camana"

    exportar_por_anio(df_final, OUT_DIR)

    return df_final