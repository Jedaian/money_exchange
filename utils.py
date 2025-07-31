import sys
import os

def resource_path(relative_path):
    """
    Get the absolute path to a resource, whether running in dev or as a PyInstaller .exe.
    """
    try:
        # When bundled by PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in a regular Python environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
