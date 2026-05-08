"""Настройки: тема, размер шрифта, имя, сброс прогресса."""
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..progress import ProgressStore, app_data_dir
from ..theme import DARK, Palette

FONT_SCALES = [
    ("Меньше (0.85)", 0.85),
    ("Обычный (1.0)", 1.0),
    ("Крупнее (1.15)", 1.15),
    ("Крупный (1.3)", 1.3),
]


class SettingsView(QWidget):
    theme_changed = Signal()
    font_scale_changed = Signal()
    user_name_changed = Signal(str)
    progress_reset = Signal()

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(14)

        title = QLabel("Настройки")
        title.setObjectName("title")
        outer.addWidget(title)

        # тема
        outer.addWidget(self._row("Тема", self._theme_widget()))
        # шрифт
        outer.addWidget(self._row("Размер шрифта", self._font_widget()))
        # имя
        outer.addWidget(self._row("Имя для приветствия", self._name_widget()))

        # сброс
        outer.addWidget(self._row("Сбросить прогресс", self._reset_widget()))

        # инфо
        info = QFrame()
        info.setObjectName("statusInfo")
        iv = QVBoxLayout(info)
        iv.setContentsMargins(14, 10, 14, 10)
        path = app_data_dir() / "progress.json"
        info_label = QLabel(f"Прогресс хранится локально в:\n{path}")
        info_label.setWordWrap(True)
        iv.addWidget(info_label)
        outer.addWidget(info)

        outer.addStretch(1)

    def set_theme(self, palette: Palette, _font_scale: float) -> None:
        self._palette = palette

    def on_show(self) -> None:
        self.user_name_input.setText(self.store.progress.settings.user_name)

    def _row(self, label_text: str, widget: QWidget) -> QFrame:
        frame = QFrame()
        frame.setObjectName("card")
        h = QHBoxLayout(frame)
        h.setContentsMargins(16, 12, 16, 12)
        h.setSpacing(14)
        label = QLabel(label_text)
        label.setObjectName("h2")
        label.setMinimumWidth(220)
        h.addWidget(label)
        h.addWidget(widget, stretch=1)
        return frame

    def _theme_widget(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Тёмная", "dark")
        self.theme_combo.addItem("Светлая", "light")
        idx = 0 if self.store.progress.settings.theme != "light" else 1
        self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        h.addWidget(self.theme_combo)
        h.addStretch(1)
        return w

    def _font_widget(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        self.font_combo = QComboBox()
        for label, scale in FONT_SCALES:
            self.font_combo.addItem(label, scale)
        cur_scale = self.store.progress.settings.font_scale
        target_idx = 1
        for i, (_, scale) in enumerate(FONT_SCALES):
            if abs(scale - cur_scale) < 0.01:
                target_idx = i
                break
        self.font_combo.setCurrentIndex(target_idx)
        self.font_combo.currentIndexChanged.connect(self._on_font_changed)
        h.addWidget(self.font_combo)
        h.addStretch(1)
        return w

    def _name_widget(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        self.user_name_input = QLineEdit(self.store.progress.settings.user_name)
        self.user_name_input.setPlaceholderText("Например, Кирилл")
        self.user_name_input.editingFinished.connect(self._on_name_changed)
        h.addWidget(self.user_name_input)
        return w

    def _reset_widget(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        self.btn_reset = QPushButton("Сбросить весь прогресс")
        self.btn_reset.setObjectName("danger")
        self.btn_reset.clicked.connect(self._on_reset)
        h.addWidget(self.btn_reset)
        h.addStretch(1)
        return w

    def _on_theme_changed(self) -> None:
        theme = self.theme_combo.currentData()
        self.store.update_settings(theme=theme)
        self.theme_changed.emit()

    def _on_font_changed(self) -> None:
        scale = float(self.font_combo.currentData())
        self.store.update_settings(font_scale=scale)
        self.font_scale_changed.emit()

    def _on_name_changed(self) -> None:
        name = self.user_name_input.text().strip()
        self.store.update_settings(user_name=name)
        self.user_name_changed.emit(name)

    def _on_reset(self) -> None:
        ans = QMessageBox.question(
            self,
            "Сбросить прогресс",
            "Точно сбросить весь прогресс? Уроки, задачи, XP, стрик — всё обнулится.\n"
            "Настройки темы и шрифта останутся.",
        )
        if ans == QMessageBox.StandardButton.Yes:
            self.store.reset()
            self.progress_reset.emit()
