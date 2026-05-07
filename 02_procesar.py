from pathlib import Path
import pandas as pd

from procesamiento.pipeline.clean_ema import clean_ema
from procesamiento.pipeline.extraer_semana import extraer_semana
from procesamiento.pipeline.promedios_semanales import promedios_semanales


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "dataprocesada"
OUT_DIR = BASE_DIR / "outputs"

OUT_DIR.mkdir(exist_ok=True)


def seleccionar_estaciones():

    estaciones = sorted([p for p in DATA_DIR.iterdir() if p.is_dir()])

    print("\nEstaciones disponibles:\n")

    for i, est in enumerate(estaciones, 1):
        print(f"{i}. {est.name}")

    seleccion = input("\nSeleccione estaciones (ej: 1 o 1,3): ")

    indices = [int(x.strip()) - 1 for x in seleccion.split(",")]

    return [estaciones[i] for i in indices]


def seleccionar_semana(df):

    df = df.copy()

    df["year"] = df["datetime"].dt.year
    df["week"] = df["datetime"].dt.isocalendar().week

    semanas = (
        df[["year","week"]]
        .drop_duplicates()
        .sort_values(["year","week"], ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    print("\nÚltimas semanas disponibles:\n")

    for i,row in semanas.iterrows():
        print(f"{i+1}. {row.year}-{row.week}")

    sel = int(input("\nSeleccione semana: ")) - 1

    return int(semanas.iloc[sel].year), int(semanas.iloc[sel].week)


def procesar_estaciones():

    estaciones = seleccionar_estaciones()

    for est_path in estaciones:

        print(f"\nProcesando estación: {est_path.name}")

        out_est = OUT_DIR / est_path.name
        out_est.mkdir(parents=True, exist_ok=True)

        df_clean = clean_ema(est_path)

        if df_clean.empty:
            print("Sin datos")
            continue

        year_sel, week_sel = seleccionar_semana(df_clean)

        df_semana = extraer_semana(df_clean, year_sel, week_sel)

        path_semana = out_est / "viento_ultimos_7_dias.csv"

        df_semana.to_csv(path_semana, index=False)

        print(f"Archivo generado: {path_semana}")

        prom = promedios_semanales(df_clean, year_sel, week_sel)

        path_prom = out_est / "Promedios_Semanales_Viento_TSM.csv"

        prom.to_csv(path_prom, index=False)

        print(f"Archivo generado: {path_prom}")


if __name__ == "__main__":
    procesar_estaciones()