from pathlib import Path
import pandas as pd

from procesamiento.pipeline.clean_ema import clean_ema
from procesamiento.pipeline.extraer_semana import extraer_semana
from procesamiento.pipeline.promedios_semanales import promedios_semanales


# --------------------------------
# Rutas base
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "dataprocesada"
OUT_DIR = BASE_DIR / "outputs"

OUT_DIR.mkdir(exist_ok=True)


# --------------------------------
# Selector de estaciones
# --------------------------------

def seleccionar_estaciones():

    estaciones = sorted([p for p in DATA_DIR.iterdir() if p.is_dir()])

    print("\nEstaciones disponibles:\n")

    for i, est in enumerate(estaciones, 1):
        print(f"{i}. {est.name}")

    seleccion = input("\nSeleccione estaciones (ej: 1 o 1,3): ")

    indices = [int(x.strip()) - 1 for x in seleccion.split(",")]

    estaciones_seleccionadas = [estaciones[i] for i in indices]

    return estaciones_seleccionadas


# --------------------------------
# Pipeline principal
# --------------------------------

def procesar_estaciones():

    estaciones = seleccionar_estaciones()

    for est_path in estaciones:

        print(f"\nProcesando estación: {est_path.name}")

        # carpeta de salida
        out_est = OUT_DIR / est_path.name
        out_est.mkdir(parents=True, exist_ok=True)

        # --------------------------------
        # 1. limpiar dataset completo
        # --------------------------------

        df_clean = clean_ema(est_path)

        if df_clean.empty:
            print("Sin datos")
            continue

        # --------------------------------
        # 2. últimos 7 días (para rosa)
        # --------------------------------

        df_semana = extraer_semana(df_clean)

        path_semana = out_est / "viento_ultimos_7_dias.csv"

        df_semana.to_csv(path_semana, index=False)

        print(f"Archivo generado: {path_semana}")

        # --------------------------------
        # 3. promedios semanales históricos
        # --------------------------------

        prom = promedios_semanales(df_clean)

        path_prom = out_est / "Promedios_Semanales_Viento_TSM.csv"

        prom.to_csv(path_prom, index=False)

        print(f"Archivo generado: {path_prom}")


# --------------------------------
# Main
# --------------------------------

if __name__ == "__main__":

    procesar_estaciones()