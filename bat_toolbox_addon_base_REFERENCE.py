"""
Bat Innovations Toolbox - Addon Base Class (Referenz)
---------------------------------------------------------
Dies ist eine REFERENZ-KOPIE der BatAddon-Basisklasse zum lokalen
Testen dieses Addons OHNE laufende Toolbox.

Innerhalb der echten Toolbox wird stattdessen automatisch
core/addon_base.py aus dem Hauptprojekt verwendet (siehe main.py:
dort wird zuerst "from core.addon_base import BatAddon" versucht und
nur bei einem ImportError auf diese Datei hier zurückgefallen).

Ihr müsst diese Datei NICHT anpassen - sie muss lediglich mit der
echten Schnittstelle synchron bleiben.
"""

from abc import ABC


class BatAddon(ABC):
    """Basisklasse, von der jede Addon-Hauptklasse erben muss."""

    id: str = "unbekanntes-addon"
    name: str = "Unbekanntes Addon"
    version: str = "0.0.1"

    def __init__(self, toolbox_context: dict = None):
        self.toolbox_context = toolbox_context or {}

    # ------------------------------------------------------------
    # Lifecycle-Hooks - vom Addon zu überschreiben
    # ------------------------------------------------------------
    def on_load(self) -> None:
        """Wird beim Aktivieren des Addons aufgerufen."""
        pass

    def on_unload(self) -> None:
        """Wird beim Deaktivieren/Entfernen des Addons aufgerufen."""
        pass

    def get_widget(self):
        """Muss ein QWidget zurückgeben, das die Toolbox anzeigt,
        oder None, wenn das Addon kein eigenes UI-Fenster braucht."""
        return None

    def get_settings_widget(self):
        """Optional: eigene Einstellungs-Oberfläche für dieses Addon."""
        return None

    # ------------------------------------------------------------
    def log(self, message: str) -> None:
        logger = self.toolbox_context.get("logger")
        if logger:
            logger.info("[%s] %s", self.id, message)
        else:
            print(f"[{self.id}] {message}")
