import pandas as pd
import numpy as np

def promedios_mensual(df):

    df = df.copy()
    df = df.sort_values("datetime")

    # Variables
    V = pd.to_numeric(df["velocidad"], errors="coerce")
    Dir = pd.to_numeric(df["direccion"], errors="coerce")
    TSM = pd.to_numeric(df["tsm"], errors="coerce")

    theta = np.deg2rad(Dir)

    df["u"] = -V * np.sin(theta)
    df["v"] = -V * np.cos(theta)
    df["TSM"] = TSM

    # Agrupar por día
    df["date"] = df["datetime"].dt.floor("D")

    diarios = (
        df.groupby("date")
        .agg(
            u_mean=("u", "mean"),
            v_mean=("v", "mean"),
            TSM_mean=("TSM", "mean")
        )
        .reset_index()
    )

    # Reconstrucción vectorial
    diarios["Vel_mean_mps"] = np.sqrt(
        diarios["u_mean"]**2 + diarios["v_mean"]**2
    )

    diarios["Dir_mean_deg"] = (
        np.rad2deg(
            np.arctan2(-diarios["u_mean"], -diarios["v_mean"])
        ) % 360
    )

    diarios["year"] = diarios["date"].dt.year
    diarios["month"] = diarios["date"].dt.month
    diarios["day"] = diarios["date"].dt.day

    # Tomar últimos 52 días
    resultado = diarios.sort_values("date").tail(52)

    return resultado