# myqr/__init__.py

# Package version
__version__ = "0.1.0"

# Author
__author__  = "Sara Carrasquillo"

# Contact email
__email__   = "SaraCarrasquillo007@gmail.com"

# Exposes these classes at the package level
from .gui import QRApp
from .util import qr_size

__all__ = [
    "QRApp",
    "qr_size",
]