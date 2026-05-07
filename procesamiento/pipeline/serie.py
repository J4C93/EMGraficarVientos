import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from pathlib import Path


def graficar_serie(est_dir: Path, plot_dir: Path):

    IN_FILE = est_dir / "Promedios_Semanales_Viento_TSM.csv"

    df = pd.read_csv(IN_FILE)
    df["date_rep"] = pd.to_datetime(df["date_rep"])

    vel = df["Vel_mean_mps"].values
    direction = df["Dir_mean_deg"].values
    tsm = df["TSM_mean"].values

    day = df["day"].astype(str).values
    month_letter = df["month_letter"].values
    year = df["year"].values

    theta = np.deg2rad(direction)
    u = -vel * np.sin(theta)
    v = -vel * np.cos(theta)

    x = np.arange(len(df))
    y0 = np.zeros_like(x)

    n_extra = 6

    xticks = np.arange(1, len(df), 2)

    fig, (ax_tsm, ax_wind) = plt.subplots(
        2, 1,
        figsize=(9, 6),
        sharex=True,
        gridspec_kw={"height_ratios": [1.2, 2.2]}
    )

    # -----------------------------
    # TSM
    # -----------------------------
    ax_tsm.plot(x, tsm, color="tab:red", linewidth=2)

    ax_tsm.set_ylabel("TSM (°C)")
    ax_tsm.set_ylim(12, 30)
    ax_tsm.set_yticks(np.arange(12, 31, 2))
    ax_tsm.grid(True, axis="y", linestyle=":", color="0.7")
    ax_tsm.grid(True, axis="x", linestyle=":", color="0.7")

    # -----------------------------
    # VIENTO
    # -----------------------------
    ax_wind.axhline(0, color="0.6", linewidth=0.8)

    cmap = plt.cm.jet
    norm = plt.Normalize(0, 12)

    q = ax_wind.quiver(
        x, y0,
        u, v,
        vel,
        angles="uv",
        scale_units="xy",
        scale=1.5,
        cmap=cmap,
        norm=norm,
        width=0.0018,
        headlength=10,
        headwidth=5,
        headaxislength=4,
        pivot="tail",
        zorder=2.5
    )

    ax_wind.set_ylim(-12, 12)
    ax_wind.set_yticks(np.arange(-12, 13, 2))
    ax_wind.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: f"{abs(int(y))}")
    )

    ax_wind.set_ylabel("Velocidad del viento (m/s)")
    ax_wind.grid(True, axis="y", linestyle=":", color="0.7")
    ax_wind.grid(True, axis="x", linestyle=":", color="0.7")

    ax_wind.set_xlim(-0.5, len(df) - 0.5 + n_extra)

    # -----------------------------
    # EJE MESES
    # -----------------------------
    ax_wind.set_xticks(xticks)
    ax_wind.set_xticklabels(month_letter[xticks], fontsize=9)
    ax_wind.tick_params(axis="x", length=0)

    # -----------------------------
    # EJE DÍAS
    # -----------------------------
    ax_top = ax_wind.twiny()
    ax_top.set_xlim(ax_wind.get_xlim())
    ax_top.set_xticks(xticks)
    ax_top.set_xticklabels(day[xticks], fontsize=8)

    ax_top.tick_params(axis="x", length=3, pad=-210)

    # -----------------------------
    # AÑOS
    # -----------------------------
    ax_wind.text(
        0.0, -0.15, str(year[0]),
        transform=ax_wind.transAxes,
        ha="left", va="top", fontsize=9
    )

    ax_wind.text(
        0.87, -0.15, str(year[-1]),
        transform=ax_wind.transAxes,
        ha="right", va="top", fontsize=9
    )

    # -----------------------------
    # COLORBAR
    # -----------------------------
    plt.tight_layout(rect=[0, 0.15, 1, 1])

    cax = fig.add_axes([0.2, 0.15, 0.6, 0.018])
    cbar = fig.colorbar(q, cax=cax, orientation="horizontal")
    cbar.set_ticks(np.arange(0, 13, 2))

    fecha_ref = df["date_rep"].max()
    year_iso, week_iso, _ = fecha_ref.isocalendar()

    week_iso = int(week_iso) - 1

    fname = f"SerieVientoTSM-{year_iso}-S{week_iso}.png"

    plot_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        plot_dir / fname,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Figura '{fname}' generada.")