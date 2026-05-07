from pathlib import Path

from procesamiento.readers.reader_imp_callao import reader_imp_callao
from procesamiento.readers.reader_senamhi import reader_senamhi
from procesamiento.readers.reader_imp_santarosa import reader_imp_santarosa
from procesamiento.readers.reader_imp_camana import reader_imp_camana

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

# Callao
reader_imp_callao(RAW_DIR / "IMP Callao")

# Santa Rosa
reader_imp_santarosa(RAW_DIR / "IMP SantaRosa")

# Camana
#reader_imp_camana(RAW_DIR / "IMP Camana")

# SENAMHI
#reader_senamhi(RAW_DIR / "SNM Camana")
#reader_senamhi(RAW_DIR / "SNM Casma")
#reader_senamhi(RAW_DIR / "SNM Cañete")