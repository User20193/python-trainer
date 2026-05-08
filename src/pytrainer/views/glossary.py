"""Словарь терминов с поиском."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..content import GlossaryEntry, all_glossary
from ..progress import ProgressStore
from ..theme import DARK, Palette
from ..widgets.markdown_view import MarkdownView


class GlossaryView(QWidget):
    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(8)

        title = QLabel("Словарь терминов")
        title.setObjectName("title")
        outer.addWidget(title)
        sub = QLabel("Простыми словами — что значит каждое слово в Python и в наших уроках.")
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        outer.addWidget(sub)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск термина...")
        self.search.textChanged.connect(self._refilter)
        outer.addWidget(self.search)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        outer.addWidget(splitter, stretch=1)

        self.list = QListWidget()
        self.list.itemClicked.connect(self._on_item)
        splitter.addWidget(self.list)

        self.view = MarkdownView()
        splitter.addWidget(self.view)
        splitter.setSizes([280, 700])

        self._populate()

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale
        cur = self.list.currentItem()
        if cur is not None:
            self._show(cur.data(Qt.ItemDataRole.UserRole))

    def on_show(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    def focus_term(self, term: str) -> None:
        for i in range(self.list.count()):
            item = self.list.item(i)
            entry = item.data(Qt.ItemDataRole.UserRole)
            if entry.term.lower() == term.lower():
                self.list.setCurrentRow(i)
                self._show(entry)
                return

    def _populate(self) -> None:
        self.list.clear()
        for entry in sorted(all_glossary(), key=lambda e: e.term.lower()):
            item = QListWidgetItem(entry.term)
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.list.addItem(item)
        if self.list.count():
            self.list.setCurrentRow(0)
            self._show(self.list.item(0).data(Qt.ItemDataRole.UserRole))

    def _on_item(self, item: QListWidgetItem) -> None:
        entry = item.data(Qt.ItemDataRole.UserRole)
        if entry:
            self._show(entry)

    def _refilter(self, text: str) -> None:
        text = text.strip().lower()
        for i in range(self.list.count()):
            item = self.list.item(i)
            entry: GlossaryEntry = item.data(Qt.ItemDataRole.UserRole)
            visible = (
                not text
                or text in entry.term.lower()
                or text in entry.definition_md.lower()
            )
            item.setHidden(not visible)

    def _show(self, entry: GlossaryEntry) -> None:
        body = f"# {entry.term}\n\n{entry.definition_md}"
        self.view.set_markdown(body, self._palette, self._font_scale)
