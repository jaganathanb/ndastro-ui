"""ND Astro module."""

from i18n.translator import t
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from qt_material_icons import MaterialIcon

from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel
from ndastro.gui.views.settings_ui import SettingsWindow
from ndastro.libs.resizable_chart import ResizableAstroChart


class NDAstroMainWindow(QMainWindow):
    """Module providing a function printing python version."""

    def __init__(self, view_model: NDAstroViewModel) -> None:
        """Initialize the app."""
        super().__init__()
        self._view_model = view_model

        self._view_model.language_changed.connect(self._set_language)
        self._view_model.theme_changed.connect(self._set_theme)

        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI."""
        self._setup_window()
        self._setup_layout()
        self._setup_toolbar()
        self._setup_central_widget()
        self.show()

    def _setup_window(self) -> None:
        """Set up the main window properties."""
        self._create_actions()
        self._create_menus()

        self.setWindowTitle(self._view_model.title)

    def _setup_layout(self) -> None:
        """Set up the main layout."""
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.vl_left_frame = QVBoxLayout()

        self.left_frame = QFrame()
        self.h_layout.addWidget(self.left_frame)

        self.h_layout.setStretchFactor(self.left_frame, 10)

        self.left_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_frame.setLayout(self.vl_left_frame)

        self.vl_left_frame.addWidget(ResizableAstroChart(self._view_model))

    def _setup_toolbar(self) -> None:
        """Set up the toolbar."""
        toolbar = QToolBar("ND Astro toolbar", self)
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add a spacer to push the next item to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        l_selector = self._create_language_selector()
        t_selector = self._create_theme_selector()

        toolbar.addWidget(l_selector)
        toolbar.addWidget(t_selector)

    def _setup_central_widget(self) -> None:
        """Set up the central widget."""
        container = QWidget()
        container.setLayout(self.h_layout)

        self.setCentralWidget(container)

        self.show()

    def _create_language_selector(self) -> QComboBox:
        """Create language selector."""
        combo = QComboBox()
        options = self._view_model.locales
        for _, (text, _) in enumerate(options):
            combo.addItem(text)

        combo.currentIndexChanged.connect(self._view_model.set_language)

        return combo

    def _create_theme_selector(self) -> QComboBox:
        """Create theme selector."""
        combo = QComboBox()
        options = self._view_model.themes
        for _, (text, _) in enumerate(options):
            combo.addItem(text)

        combo.currentIndexChanged.connect(self._view_model.set_theme)

        return combo

    def _set_language(self) -> None:
        self._retranslate_ui()

    def _set_theme(self) -> None:
        self._apply_theme()

    def _apply_theme(self) -> None:
        pass

    def _retranslate_ui(self) -> None:
        self.setWindowTitle(t("common.appTitle"))

    def _create_menus(self) -> None:
        """Create the application menus."""
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_tools_menu()
        self._create_help_menu()

    def _create_file_menu(self) -> None:
        """Create the File menu."""
        self.file_menu = self.menuBar().addMenu(t("common.menus.file.title"))
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

    def _create_edit_menu(self) -> None:
        """Create the Edit menu."""
        self.edit_menu = self.menuBar().addMenu(t("common.menus.edit.title"))
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addAction(self.delete_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_all_action)

    def _create_view_menu(self) -> None:
        """Create the View menu."""
        self.view_menu = self.menuBar().addMenu(t("common.menus.view.title"))
        self.view_menu.addAction(self.zoom_in_action)
        self.view_menu.addAction(self.zoom_out_action)
        self.view_menu.addAction(self.reset_zoom_action)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.fullscreen_action)

    def _create_tools_menu(self) -> None:
        """Create the Tools menu."""
        self.tools_menu = self.menuBar().addMenu(t("common.menus.tools.title"))
        self.tools_menu.addAction(self.settings_action)
        self.tools_menu.addAction(self.preferences_action)
        self.tools_menu.addAction(self.extensions_action)
        self.tools_menu.addAction(self.plugins_action)

    def _create_help_menu(self) -> None:
        """Create the Help menu."""
        self.help_menu = self.menuBar().addMenu(t("common.menus.help.title"))
        self.help_menu.addAction(self.documentation_action)
        self.help_menu.addAction(self.support_action)
        self.help_menu.addAction(self.check_for_updates_action)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.about_action)

    def _create_actions(self) -> None:
        """Create the actions for the menus."""
        self._create_file_actions()
        self._create_edit_actions()
        self._create_view_actions()
        self._create_tools_actions()
        self._create_help_actions()

    def _create_file_actions(self) -> None:
        """Create file-related actions."""
        self.new_action = QAction(QIcon(MaterialIcon("add")), t("common.menus.file.new"), self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self._new_file)

        self.open_action = QAction(QIcon(MaterialIcon("folder_open")), t("common.menus.file.open"), self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self._open_file)

        self.save_action = QAction(QIcon(MaterialIcon("save")), t("common.menus.file.save"), self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self._save_file)

        self.save_as_action = QAction(QIcon(MaterialIcon("save_as")), t("common.menus.file.saveAs"), self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self._save_as_file)

        self.exit_action = QAction(QIcon(MaterialIcon("exit_to_app")), t("common.menus.file.exit"), self)
        self.exit_action.setShortcut("Ctrl+X")
        self.exit_action.triggered.connect(self.close)

    def _create_edit_actions(self) -> None:
        """Create edit-related actions."""
        self.undo_action = QAction(QIcon(MaterialIcon("undo")), t("common.menus.edit.undo"), self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self._undo)

        self.redo_action = QAction(QIcon(MaterialIcon("redo")), t("common.menus.edit.redo"), self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(self._redo)

        self.cut_action = QAction(QIcon(MaterialIcon("content_cut")), t("common.menus.edit.cut"), self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self._cut)

        self.copy_action = QAction(QIcon(MaterialIcon("content_copy")), t("common.menus.edit.copy"), self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self._copy)

        self.paste_action = QAction(QIcon(MaterialIcon("content_paste")), t("common.menus.edit.paste"), self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self._paste)

        self.delete_action = QAction(QIcon(MaterialIcon("delete")), t("common.menus.edit.delete"), self)
        self.delete_action.triggered.connect(self._delete)

        self.select_all_action = QAction(QIcon(MaterialIcon("select_all")), t("common.menus.edit.selectAll"), self)
        self.select_all_action.setShortcut("Ctrl+A")
        self.select_all_action.triggered.connect(self._select_all)

    def _create_view_actions(self) -> None:
        """Create view-related actions."""
        self.zoom_in_action = QAction(QIcon(MaterialIcon("zoom_in")), t("common.menus.view.zoomIn"), self)
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_in_action.triggered.connect(self._zoom_in)

        self.zoom_out_action = QAction(QIcon(MaterialIcon("zoom_out")), t("common.menus.view.zoomOut"), self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.triggered.connect(self._zoom_out)

        self.reset_zoom_action = QAction(QIcon(MaterialIcon("zoom_out_map")), t("common.menus.view.resetZoom"), self)
        self.reset_zoom_action.setShortcut("Ctrl+0")
        self.reset_zoom_action.triggered.connect(self._reset_zoom)

        self.fullscreen_action = QAction(QIcon(MaterialIcon("fullscreen")), t("common.menus.view.fullscreen"), self)
        self.fullscreen_action.setShortcut("F11")
        self.fullscreen_action.triggered.connect(self._toggle_fullscreen)

    def _create_tools_actions(self) -> None:
        """Create tools-related actions."""
        self.settings_action = QAction(QIcon(MaterialIcon("settings")), t("common.menus.tools.settings"), self)
        self.settings_action.triggered.connect(self._open_settings)

        self.preferences_action = QAction(QIcon(MaterialIcon("tune")), t("common.menus.tools.preferences"), self)
        self.preferences_action.triggered.connect(self._open_preferences)

        self.extensions_action = QAction(QIcon(MaterialIcon("extension")), t("common.menus.tools.extensions"), self)
        self.extensions_action.triggered.connect(self._manage_extensions)

        self.plugins_action = QAction(QIcon(MaterialIcon("widgets")), t("common.menus.tools.plugins"), self)
        self.plugins_action.triggered.connect(self._manage_plugins)

    def _create_help_actions(self) -> None:
        """Create help-related actions."""
        self.documentation_action = QAction(t("common.menus.help.documentation"), self)
        self.documentation_action.triggered.connect(self._open_documentation)

        self.support_action = QAction(t("common.menus.help.support"), self)
        self.support_action.triggered.connect(self._open_support)

        self.check_for_updates_action = QAction(t("common.menus.help.checkForUpdates"), self)
        self.check_for_updates_action.triggered.connect(self._check_for_updates)

        self.about_action = QAction(t("common.menus.help.about"), self)
        self.about_action.setShortcut("F1")
        self.about_action.triggered.connect(self._about)

    # Handlers for actions
    def _new_file(self) -> None:
        pass

    def _open_file(self) -> None:
        pass

    def _save_file(self) -> None:
        pass

    def _save_as_file(self) -> None:
        pass

    def _undo(self) -> None:
        pass

    def _redo(self) -> None:
        pass

    def _cut(self) -> None:
        pass

    def _copy(self) -> None:
        pass

    def _paste(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _select_all(self) -> None:
        pass

    def _zoom_in(self) -> None:
        pass

    def _zoom_out(self) -> None:
        pass

    def _reset_zoom(self) -> None:
        pass

    def _toggle_fullscreen(self) -> None:
        pass

    def _open_settings(self) -> None:
        s = SettingsWindow(self._view_model.settings)
        s.show()

    def _open_preferences(self) -> None:
        pass

    def _manage_extensions(self) -> None:
        pass

    def _manage_plugins(self) -> None:
        pass

    def _open_documentation(self) -> None:
        pass

    def _open_support(self) -> None:
        pass

    def _check_for_updates(self) -> None:
        pass

    @Slot()
    def _about(self) -> None:
        QMessageBox.about(
            self,
            "About Settings Editor",
            "The <b>Settings Editor</b> example shows how to access application settings using Qt.",
        )
