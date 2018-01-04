__all__ = ["BaseTests"]

try:
	from .BaseTests import BaseTests
except ImportError:
	print("WARNING: PyVISA is not installed. Equipment tests may not work!")