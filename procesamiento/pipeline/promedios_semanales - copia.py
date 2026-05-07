import pandas as pd
import numpy as np


def promedios_semanales(df, year_sel, week_sel):

    df = df.copy()
    df = df.sort_values("datetime")

    V = pd.to_numeric(df["velocidad"], errors="coerce")
    Dir = pd.to_numeric(df["direccion"], errors="coerce")
    TSM = pd.to_numeric(df["tsm"], errors="coerce")

    theta = np.deg2rad(Dir)

    df["u"] = -V * np.sin(theta)
    df["v"] = -V * np.cos(theta)
    df["TSM"] = TSM

    df["year"] = df["datetime"].dt.year
    df["doy"] = df["datetime"].dt.dayofyear
    df["week"] = ((df["doy"] - 1) // 7) + 1

    weekly = (
        df.groupby(["year", "week"])
        .agg(
            u_mean=("u", "mean"),
            v_mean=("v", "mean"),
            TSM_mean=("TSM", "mean"),
            date_start=("datetime", "min")
        )
        .reset_index()
    )

    weekly["date_rep"] = weekly["date_start"] + pd.Timedelta(days=6)

    weekly["Vel_mean_mps"] = np.sqrt(
        weekly["u_mean"]**2 + weekly["v_mean"]**2
    )

    weekly["Dir_mean_deg"] = (
        np.rad2deg(
            np.arctan2(-weekly["u_mean"], -weekly["v_mean"])
        ) % 360
    )

    weekly["day"] = weekly["date_rep"].dt.day
    weekly["month"] = weekly["date_rep"].dt.month
    weekly["year"] = weekly["date_rep"].dt.year

    month_letters = {
        1:"E",2:"F",3:"M",4:"A",5:"M",6:"J",
        7:"J",8:"A",9:"S",10:"O",11:"N",12:"D"
    }

    weekly["month_letter"] = weekly["month"].map(month_letters)

    resultado = weekly[
        [
            "year","week","date_rep","day","month",
            "month_letter","Vel_mean_mps","Dir_mean_deg","TSM_mean"
        ]
    ]

    resultado = resultado.sort_values("date_rep")

    idx = resultado[
        (resultado["year"] == year_sel) &
        (resultado["week"] == week_sel)
    ].index

    if len(idx) == 0:
        return resultado.tail(52)

    end_idx = idx[0]

    resultado = resultado.loc[max(0, end_idx-51):end_idx]

    return resultado