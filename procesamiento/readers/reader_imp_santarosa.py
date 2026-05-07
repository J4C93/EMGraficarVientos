from pathlib import Path
import pandas as pd

from ..config import COLUMNAS_ESTANDAR


def reader_imp_santarosa(path_carpeta: Path) -> pd.DataFrame:

    archivos = sorted(path_carpeta.glob("ReportEMASantaRosa*.csv"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos SantaRosa en {path_carpeta}"
        )

    dfs = []

    # =========================
    # 1. Leer viento estación
    # =========================

    for f in archivos:

        print(f"Leyendo {f.name}")

        df = pd.read_csv(
            f,
            sep=None,
            engine="python",
            encoding="latin1"
        )

        df_out = pd.DataFrame({
            "datetime": df.iloc[:, 0],
            "direccion": df.iloc[:, 5],
            "velocidad": df.iloc[:, 6],
        })

        df_out["datetime"] = pd.to_datetime(df_out["datetime"], errors="coerce")

        for c in ["direccion", "velocidad"]:
            df_out[c] = pd.to_numeric(df_out[c], errors="coerce")

        dfs.append(df_out)

    df_wind = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset=["datetime"])
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    # =========================
    # 2. Leer TSM diaria
    # =========================

    base_dir = Path(__file__).resolve().parents[2]
    archivo_tsm = base_dir / "raw" / "TSM_ATSM_diario_230226.xlsx"

    df_tsm = pd.read_excel(archivo_tsm)

    df_tsm = df_tsm.rename(
        columns={
            "AÑO": "year",
            "MES": "month",
            "DIA": "day",
            "SAN JOSE": "tsm"
        }
    )

    df_tsm["date"] = pd.to_datetime(
        dict(year=df_tsm.year, month=df_tsm.month, day=df_tsm.day),
        errors="coerce"
    )

    # asignar hora fija
    df_tsm["datetime"] = df_tsm["date"] + pd.Timedelta(hours=12)

    df_tsm = df_tsm[["datetime", "tsm"]]

    # =========================
    # 3. Merge viento + TSM
    # =========================

    # Crear columna auxiliar para el merge diario
    df_wind["date"] = df_wind["datetime"].dt.floor("D")
    df_tsm["date"] = df_tsm["datetime"].dt.floor("D")

    # merge solo con TSM
    df_final = df_wind.merge(
        df_tsm[["date", "tsm"]],
        on="date",
        how="left"
    )

    # eliminar columna auxiliar
    df_final = df_final.drop(columns="date", errors="ignore")

    # dejar TSM solo a las 12:00
    mask_1200 = (
        (df_final["datetime"].dt.hour == 12) &
        (df_final["datetime"].dt.minute == 0) &
        (df_final["datetime"].dt.second == 0)
    )

    df_final.loc[~mask_1200, "tsm"] = pd.NA

    df_final["estacion"] = "IMP SantaRosa"

    df_final = df_final[COLUMNAS_ESTANDAR]

    # =========================
    # 4. Exportar por año
    # =========================

    from ..export.export_por_anio import exportar_por_anio

    OUT_DIR = Path(__file__).resolve().parents[2] / "dataprocesada" / "IMP SantaRosa"

    exportar_por_anio(df_final, OUT_DIR)

    return df_final