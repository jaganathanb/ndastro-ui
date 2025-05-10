import pytz
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class GeneralSection(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.start_on_boot = QCheckBox("Start on system boot")

        self.label_locale = QLabel("Language / Locale:")
        self.combo_locale = QComboBox()
        self.combo_locale.addItems(
            [
                "en_US",
                "fr_FR",
                "de_DE",
                "es_ES",
                "hi_IN",
                "ja_JP",
                "zh_CN",
            ],
        )

        self.label_timezone = QLabel("Time Zone:")
        self.combo_timezone = QComboBox()
        self.combo_timezone.addItems(pytz.all_timezones)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.start_on_boot)
        layout.addSpacing(10)
        layout.addWidget(self.label_locale)
        layout.addWidget(self.combo_locale)
        layout.addSpacing(10)
        layout.addWidget(self.label_timezone)
        layout.addWidget(self.combo_timezone)

        self._load()

        self.start_on_boot.stateChanged.connect(self._update)
        self.combo_locale.currentTextChanged.connect(self._update)
        self.combo_timezone.currentTextChanged.connect(self._update)

    def _load(self):
        checked = self.view_model.get("General", "start_on_boot", "false") == "true"
        self.start_on_boot.setChecked(checked)

        saved_locale = self.view_model.get("General", "locale", "en_US")
        index = self.combo_locale.findText(saved_locale)
        if index != -1:
            self.combo_locale.setCurrentIndex(index)

        saved_tz = self.view_model.get("General", "timezone", "UTC")
        index = self.combo_timezone.findText(saved_tz)
        if index != -1:
            self.combo_timezone.setCurrentIndex(index)

    def _update(self):
        self.view_model.set("General", "start_on_boot", "true" if self.start_on_boot.isChecked() else "false")
        self.view_model.set("General", "locale", self.combo_locale.currentText())
        self.view_model.set("General", "timezone", self.combo_timezone.currentText())
