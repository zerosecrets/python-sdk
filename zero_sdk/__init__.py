# flake8: noqa
import importlib.metadata
from .zero import *

__version__ = importlib.metadata.version(__package__ or __name__)
