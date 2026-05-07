import pandas as pd
import numpy as np


def extraer_semana(df, year_sel, week_sel):

    df = df.copy()
    df["year"] = df["datetime"].dt.year
    df["week"] = df["datetime"].dt.isocalendar().week

    df_week = df[
        (df["year"] == year_sel) &
        (df["week"] == week_sel)
    ]

    print(f"Semana usada: {year_sel}-S{week_sel}")
    print(f"N° registros originales: {len(df_week)}")

    fecha = pd.to_datetime(df_week["datetime"], errors="coerce")
    direccion = pd.to_numeric(df_week["direccion"], errors="coerce")
    velocidad = pd.to_numeric(df_week["velocidad"], errors="coerce")

    mask = (
        fecha.notna()
        & np.isfinite(direccion)
        & np.isfinite(velocidad)
        & (velocidad >= 0)
    )

    df_out = pd.DataFrame({
        "Fecha": fecha[mask].values,
        "DV": direccion[mask].values,
        "VV": velocidad[mask].values
    })

    print(f"N° registros filtrados: {len(df_out)}")

    return df_out