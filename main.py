"""
Weltzeit-Anzeige Addon
--------------------------
Zeigt die aktuelle Uhrzeit in mehreren Zeitzonen gleichzeitig an.
Nutzt ausschließlich die Python-Standardbibliothek (zoneinfo, ab
Python 3.9), keine externen Abhängigkeiten notwendig.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from core.addon_base import BatAddon

# Voreingestellte Staedte/Zeitzonen, die beim ersten Start angezeigt werden.
DEFAULT_CITIES = [
    ("Berlin", "Europe/Berlin"),
    ("London", "Europe/London"),
    ("New York", "America/New_York"),
    ("Los Angeles", "America/Los_Angeles"),
    ("Tokio", "Asia/Tokyo"),
    ("Sydney", "Australia/Sydney"),
]


class WeltzeitAddon(BatAddon):
    id = "weltzeit_anzeige"
    name = "Weltzeit-Anzeige"
    version = "1.0.0"

    def __init__(self, toolbox_context=None):
        super().__init__(toolbox_context)
        self.cities = list(DEFAULT_CITIES)

    def on_load(self) -> None:
        self.log("Weltzeit-Anzeige aktiviert.")

    def on_unload(self) -> None:
        self.log("Weltzeit-Anzeige deaktiviert.")

    def get_widget(self):
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
            QComboBox, QGridLayout, QFrame, QMessageBox
        )

        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Weltzeit-Anzeige")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        # --- Bereich: Uhren-Grid --------------------------------------
        clocks_grid = QGridLayout()
        layout.addLayout(clocks_grid)

        # Merkt sich pro Stadt die Labels, damit wir sie beim Timer-Tick
        # nur aktualisieren statt das Layout jedes Mal neu zu bauen.
        clock_rows = []  # Liste von (name, tz_name, time_label, date_label, row_frame)

        def rebuild_clock_rows():
            # Alte Zeilen entfernen (sauber, kein deleteLater-Timing-Problem:
            # sofort verstecken + Parent entfernen)
            while clocks_grid.count():
                item = clocks_grid.takeAt(0)
                w = item.widget()
                if w:
                    w.hide()
                    w.setParent(None)
                    w.deleteLater()
            clock_rows.clear()

            for row, (city_name, tz_name) in enumerate(self.cities):
                name_label = QLabel(city_name)
                name_label.setStyleSheet("font-weight: 600;")
                clocks_grid.addWidget(name_label, row, 0)

                time_label = QLabel("--:--:--")
                time_label.setStyleSheet("font-size: 20px; font-weight: 700;")
                clocks_grid.addWidget(time_label, row, 1)

                date_label = QLabel("")
                date_label.setStyleSheet("color: #8B98A8; font-size: 11px;")
                clocks_grid.addWidget(date_label, row, 2)

                remove_btn = QPushButton("✕")
                remove_btn.setFixedWidth(28)
                remove_btn.setToolTip(f"{city_name} entfernen")
                remove_btn.clicked.connect(lambda checked, tz=tz_name: remove_city(tz))
                clocks_grid.addWidget(remove_btn, row, 3)

                clock_rows.append((city_name, tz_name, time_label, date_label))

        def update_clocks():
            for city_name, tz_name, time_label, date_label in clock_rows:
                try:
                    now = datetime.now(ZoneInfo(tz_name))
                    time_label.setText(now.strftime("%H:%M:%S"))
                    date_label.setText(now.strftime("%a, %d.%m.%Y"))
                except Exception:
                    time_label.setText("Fehler")

        def remove_city(tz_name):
            self.cities = [c for c in self.cities if c[1] != tz_name]
            rebuild_clock_rows()
            update_clocks()

        rebuild_clock_rows()
        update_clocks()

        timer = QTimer(widget)
        timer.timeout.connect(update_clocks)
        timer.start(1000)
        widget._keep_timer_alive = timer  # verhindert Garbage Collection des Timers

        # --- Trennlinie ---------------------------------------------------
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #1E3550;")
        layout.addWidget(separator)

        # --- Bereich: Zeitzone hinzufügen ----------------------------------
        add_row = QHBoxLayout()
        add_row.addWidget(QLabel("Zeitzone hinzufügen:"))

        tz_combo = QComboBox()
        common_zones = sorted(
            tz for tz in available_timezones()
            if "/" in tz and not tz.startswith("Etc/")
        )
        tz_combo.addItems(common_zones)
        add_row.addWidget(tz_combo, 1)

        add_btn = QPushButton("+ Hinzufügen")
        add_row.addWidget(add_btn)
        layout.addLayout(add_row)

        def add_city():
            tz_name = tz_combo.currentText()
            if any(c[1] == tz_name for c in self.cities):
                QMessageBox.information(widget, "Bereits vorhanden", f"'{tz_name}' ist schon in der Liste.")
                return
            display_name = tz_name.split("/")[-1].replace("_", " ")
            self.cities.append((display_name, tz_name))
            rebuild_clock_rows()
            update_clocks()

        add_btn.clicked.connect(add_city)

        layout.addStretch(1)
        return widget
