# IMP - EMA Gráficos V2

Pipeline en Python para lectura, procesamiento y generación automática de gráficos meteorológicos y oceanográficos a partir de datos de estaciones EMA/SENAMHI e información de TSM.

## Descripción

Este proyecto permite:

- Leer datos meteorológicos provenientes de diferentes estaciones.
- Estandarizar y limpiar registros EMA/SENAMHI.
- Calcular promedios semanales.
- Integrar información de Temperatura Superficial del Mar (TSM).
- Generar gráficos automáticos:
  - Series temporales Viento–TSM.
  - Rosas de viento.
- Exportar productos procesados en formato CSV.

El flujo está orientado a automatizar la generación operativa de productos gráficos semanales.

---

# Estructura del proyecto

```text
.
├── 01_run_readers.py
├── 02_procesar.py
├── 03_graficar.py
│
├── raw/                # Datos originales
├── dataprocesada/      # Datos limpios/procesados
├── outputs/            # Tablas exportadas
├── plots/              # Figuras generadas
│
└── procesamiento/
    ├── readers/
    ├── pipeline/
    └── export/
```

---

# Flujo de trabajo

## 1. Lectura de datos

Ejecuta los readers para convertir y organizar los datos crudos:

```bash
python 01_run_readers.py
```

---

## 2. Procesamiento

Limpieza, extracción semanal y generación de estadísticas:

```bash
python 02_procesar.py
```

---

## 3. Generación de gráficos

Produce figuras semanales automáticamente:

```bash
python 03_graficar.py
```

---

# Productos generados

## Series temporales

- Velocidad del viento
- Dirección del viento
- Temperatura Superficial del Mar (TSM)

Ejemplo:

```text
SerieVientoTSM-2026-S19.png
```

---

## Rosas de viento

Ejemplo:

```text
RosaViento-2026-S19.png
```

---

# Estaciones soportadas

Actualmente el proyecto incluye procesamiento para:

- IMP Callao
- IMP Santa Rosa
- IMP Camaná
- SENAMHI Casma
- SENAMHI Cañete
- SENAMHI Chincha
- SENAMHI Casa Grande
- SENAMHI Huaura
- SENAMHI Puerto Pizarro

---

# Dependencias

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Dependencias principales:

- pandas
- numpy
- matplotlib
- windrose
- openpyxl

---

# Organización del código

## `procesamiento/readers`

Lectores específicos para cada formato de estación.

## `procesamiento/pipeline`

Rutinas principales de procesamiento:

- limpieza
- extracción semanal
- promedios
- generación de rosas
- generación de series

## `procesamiento/export`

Exportación de productos CSV.

---

# Datos de entrada

Los datos originales deben colocarse en:

```text
raw/
```

El proyecto admite múltiples formatos CSV/XLSX dependiendo de la estación.

---

# Outputs

## Datos procesados

```text
dataprocesada/
```

## Tablas exportadas

```text
outputs/
```

## Gráficos

```text
plots/
```

---

# Estado del proyecto

Proyecto en desarrollo operativo para automatización de productos meteorológicos y oceanográficos.

---

# Autor

Jaime Aquino