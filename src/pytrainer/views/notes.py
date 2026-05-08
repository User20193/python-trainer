"""Заметки: ↔ для каждого урока — своя текстовая тетрадь."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..content import all_lessons, lessons_by_section
from ..progress import ProgressStore
from ..theme import DARK, Palette

GENERAL_KEY = "__general__"


class NotesView(QWidget):
    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._current_id = GENERAL_KEY

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(8)

        title = QLabel("Заметки / Тетрадь")
        title.setObjectName("title")
        outer.addWidget(title)
        sub = QLabel(
            "Здесь можно записывать что-то своё к каждому уроку. Полезно, когда "
            "хочется что-то уточнить или зафиксировать «открытие»."
        )
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        outer.addWidget(sub)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        outer.addWidget(splitter, stretch=1)

        self.list = QListWidget()
        self.list.itemClicked.connect(self._on_item)
        splitter.addWidget(self.list)

        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(6)
        self.label_for = QLabel("Общие заметки")
        self.label_for.setObjectName("h2")
        rv.addWidget(self.label_for)
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Пиши что хочешь...")
        self.editor.textChanged.connect(self._on_text_changed)
        rv.addWidget(self.editor, stretch=1)

        btn_row = QHBoxLayout()
        self.status = QLabel("Сохраняется автоматически.")
        self.status.setObjectName("subtitle")
        btn_row.addWidget(self.status)
        btn_row.addStretch(1)
        self.btn_clear = QPushButton("Очистить")
        self.btn_clear.setObjectName("ghost")
        self.btn_clear.clicked.connect(self._on_clear)
        btn_row.addWidget(self.btn_clear)
        rv.addLayout(btn_row)

        splitter.addWidget(right)
        splitter.setSizes([280, 700])

        self._populate()
        self._load_current()

    def on_show(self) -> None:
        self._populate()
        self._load_current()

    def refresh(self) -> None:
        self._populate()
        self._load_current()

    def set_theme(self, palette: Palette, _font_scale: float) -> None:
        self._palette = palette

    def _populate(self) -> None:
        self.list.clear()
        general_item = QListWidgetItem("📒 Общие заметки")
        general_item.setData(Qt.ItemDataRole.UserRole, GENERAL_KEY)
        self.list.addItem(general_item)
        for _, section_title, lessons in lessons_by_section():
            sep = QListWidgetItem(f"— {section_title} —")
            sep.setFlags(Qt.ItemFlag.NoItemFlags)
            self.list.addItem(sep)
            for lesson in lessons:
                has = bool(self.store.get_note(lesson.id))
                marker = "📝" if has else "  "
                item = QListWidgetItem(f"{marker}  {lesson.title}")
                item.setData(Qt.ItemDataRole.UserRole, lesson.id)
                self.list.addItem(item)

    def _load_current(self) -> None:
        # выбрать первый элемент, если ещё не выбрано
        if self._current_id == GENERAL_KEY:
            self.list.setCurrentRow(0)
            self.label_for.setText("Общие заметки")
        text = self.store.get_note(self._current_id)
        self.editor.blockSignals(True)
        self.editor.setPlainText(text)
        self.editor.blockSignals(False)

    def _on_item(self, item: QListWidgetItem) -> None:
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        self._current_id = data
        if data == GENERAL_KEY:
            self.label_for.setText("Общие заметки")
        else:
            from ..content import lesson_by_id

            lesson = lesson_by_id(data)
            if lesson:
                self.label_for.setText(f"Заметки к: {lesson.title}")
        text = self.store.get_note(self._current_id)
        self.editor.blockSignals(True)
        self.editor.setPlainText(text)
        self.editor.blockSignals(False)

    def _on_text_changed(self) -> None:
        self.store.save_note(self._current_id, self.editor.toPlainText())

    def _on_clear(self) -> None:
        self.editor.setPlainText("")


# подавим неиспользуемые
_ = all_lessons
_ = QFrame
