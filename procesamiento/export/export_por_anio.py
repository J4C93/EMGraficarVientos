from pathlib import Path
import pandas as pd


def exportar_por_anio(df: pd.DataFrame, out_dir: Path):

    if df.empty:
        raise ValueError("DataFrame vacío")

    # Crear carpeta si no existe
    out_dir.mkdir(parents=True, exist_ok=True)

    df["year"] = df["datetime"].dt.year

    for year, df_year in df.groupby("year"):

        estacion = df_year["estacion"].iloc[0]

        fname = f"{estacion}_{year}.csv"
        path_out = out_dir / fname

        df_year.drop(columns="year").to_csv(path_out, index=False)

        print(f"Archivo generado: {path_out}")