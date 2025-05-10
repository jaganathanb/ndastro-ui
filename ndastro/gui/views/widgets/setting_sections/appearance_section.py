from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class AppearanceSection(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # UI Elements
        self.label_theme = QLabel("Theme:")
        self.radio_light = QRadioButton("Light")
        self.radio_dark = QRadioButton("Dark")
        self.theme_group = QButtonGroup()
        self.theme_group.addButton(self.radio_light)
        self.theme_group.addButton(self.radio_dark)

        self.label_accent = QLabel("Accent Color:")
        self.accent_combo = QComboBox()
        self.accent_combo.addItems(["Blue", "Red", "Green", "Purple", "Orange"])

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.label_theme)
        layout.addWidget(self.radio_light)
        layout.addWidget(self.radio_dark)
        layout.addSpacing(10)
        layout.addWidget(self.label_accent)
        layout.addWidget(self.accent_combo)

        self._load()

        # Connect signals
        self.radio_light.toggled.connect(self._update)
        self.radio_dark.toggled.connect(self._update)
        self.accent_combo.currentTextChanged.connect(self._update)

    def _load(self):
        theme = self.view_model.get("Appearance", "theme", "Light")
        if theme.lower() == "dark":
            self.radio_dark.setChecked(True)
        else:
            self.radio_light.setChecked(True)

        accent = self.view_model.get("Appearance", "accent_color", "Blue")
        index = self.accent_combo.findText(accent)
        if index != -1:
            self.accent_combo.setCurrentIndex(index)

    def _update(self):
        theme = "Dark" if self.radio_dark.isChecked() else "Light"
        accent = self.accent_combo.currentText()

        self.view_model.set("Appearance", "theme", theme)
        self.view_model.set("Appearance", "accent_color", accent)
