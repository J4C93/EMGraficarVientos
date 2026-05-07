from pathlib import Path

<<<<<<< HEAD
=======
from procesamiento.pipeline.serie import graficar_serie
from procesamiento.pipeline.rosa import rosa_viento


>>>>>>> 333f3684b66026bd01c250ad19476edf8a53beaa
BASE_DIR = Path(__file__).resolve().parent

OUT_DIR = BASE_DIR / "outputs"
PLOT_DIR = BASE_DIR / "plots"


<<<<<<< HEAD
# -------------------------------
# Selección de modo
# -------------------------------
def seleccionar_modo():

    print("\nModo de gráficos:\n")
    print("1. Semanal")
    print("2. Diario (serie diaria + rosa mensual)")

    opcion = input("\nSeleccione opción: ").strip()

    if opcion == "1":
        from procesamiento.pipeline.serie import graficar_serie
        from procesamiento.pipeline.rosa import rosa_viento

        return graficar_serie, rosa_viento

    elif opcion == "2":
        from procesamiento.pipeline.serie_diaria import graficar_serie
        from procesamiento.pipeline.rosa_mensual import rosa_viento

        return graficar_serie, rosa_viento

    else:
        raise ValueError("Opción inválida")


# -------------------------------
# Selección estaciones
# -------------------------------
=======
>>>>>>> 333f3684b66026bd01c250ad19476edf8a53beaa
def seleccionar_estaciones():

    estaciones = sorted([p for p in OUT_DIR.iterdir() if p.is_dir()])

    print("\nEstaciones disponibles:\n")

    for i, est in enumerate(estaciones, 1):
        print(f"{i}. {est.name}")

    seleccion = input("\nSeleccione estaciones (ej: 1 o 1,3): ")
<<<<<<< HEAD
=======

>>>>>>> 333f3684b66026bd01c250ad19476edf8a53beaa
    idx = [int(x.strip()) - 1 for x in seleccion.split(",")]

    return [estaciones[i] for i in idx]


<<<<<<< HEAD
# -------------------------------
# Runner principal
# -------------------------------
def run_graficos():

    graficar_serie, rosa_viento = seleccionar_modo()
=======
def run_graficos():

>>>>>>> 333f3684b66026bd01c250ad19476edf8a53beaa
    estaciones = seleccionar_estaciones()

    for est in estaciones:

        print(f"\nGenerando gráficos: {est.name}")

        plot_est = PLOT_DIR / est.name

        rosa_viento(est, plot_est)
<<<<<<< HEAD
=======

>>>>>>> 333f3684b66026bd01c250ad19476edf8a53beaa
        graficar_serie(est, plot_est)


if __name__ == "__main__":
    run_graficos()