import pandas as pd
import numpy as np

def extraer_diario(df):

    df = df.copy()
    df = df.sort_values("datetime")

    # Última fecha disponible
    fecha_max = df["datetime"].max()

    # Obtener año y mes del último dato
    year = fecha_max.year
    month = fecha_max.month

    year_sel = fecha_max.year
    month_sel = fecha_max.month

    # Filtrar mes calendario completo
    df_mes = df[
        (df["datetime"].dt.year == year_sel) &
        (df["datetime"].dt.month == month_sel)
    ]

    print(f"Mes usado: {year_sel}-{month_sel:02d}")
    print(f"N° registros originales: {len(df_mes)}")

    fecha = pd.to_datetime(df_mes["datetime"], errors="coerce")
    direccion = pd.to_numeric(df_mes["direccion"], errors="coerce")
    velocidad = pd.to_numeric(df_mes["velocidad"], errors="coerce")

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