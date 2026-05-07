import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from matplotlib.patches import Patch
from pathlib import Path


def rosa_viento(estacion_dir: Path, plot_dir: Path):

    csv_file = estacion_dir / "viento_ultimos_7_dias.csv"

    df = pd.read_csv(csv_file)

    fecha = pd.to_datetime(df["Fecha"], errors="coerce")
    direccion = pd.to_numeric(df["DV"], errors="coerce").to_numpy()
    velocidad = pd.to_numeric(df["VV"], errors="coerce").to_numpy()

    mask = (
        fecha.notna()
        & np.isfinite(direccion)
        & np.isfinite(velocidad)
        & (velocidad >= 0)
    )

    fecha = fecha[mask]
    direccion = direccion[mask]
    velocidad = velocidad[mask]

    bins_vel = [0.0, 0.7, 4.10, 6.8, 10.4]

    colors = [
        "#6BAFB0",
        "#1F6F78",
        "#6AA84F",
        "#F1C232",
        "#CC0000",
    ]

    labels_vel = [
        "< 0.70 m/s",
        "0.70–4.10 m/s",
        "4.10–6.80 m/s",
        "6.80–10.40 m/s",
        "≥ 10.40 m/s",
    ]

    dpi = 200
    fig = plt.figure(figsize=(12, 6.75), dpi=dpi)

    ax = WindroseAxes.from_ax(fig=fig)

    ax.bar(
        direccion,
        velocidad,
        bins=bins_vel,
        nsector=8,
        normed=True,
        opening=0.8,
        edgecolor="black",
        colors=colors
    )

    rgrids = np.arange(0, 100, 20)

    ax.set_rgrids(
        rgrids,
        labels=[f"{r}" for r in rgrids],
        angle=0
    )

    ax.set_ylim(0, 100)
    ax.set_rorigin(-10)

    handles = [
        Patch(facecolor=colors[i], edgecolor="black", label=labels_vel[i])
        for i in range(len(labels_vel))
    ]

    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=3,
        frameon=True,
        title="Velocidad del viento (m/s)",
        fontsize=12,
        title_fontsize=12
    )

    #legend.get_frame().set_linewidth(0.8)

    fecha_ref = fecha.max()
    year, week, _ = fecha_ref.isocalendar()

    fname = f"RosaViento-{year}-S{int(week)}.png"

    plot_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        plot_dir / fname,
        dpi=dpi,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Figura '{fname}' generada.")