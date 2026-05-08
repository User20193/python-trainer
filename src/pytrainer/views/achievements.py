"""Стена достижений."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..content import all_achievements
from ..progress import ProgressStore
from ..theme import DARK, Palette


class AchievementsView(QWidget):
    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(8)

        title = QLabel("Достижения")
        title.setObjectName("title")
        outer.addWidget(title)
        self.sub = QLabel("")
        self.sub.setObjectName("subtitle")
        outer.addWidget(self.sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll, stretch=1)

        self.host = QWidget()
        scroll.setWidget(self.host)
        self.grid = QGridLayout(self.host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(14)
        self.grid.setVerticalSpacing(14)

        self.refresh()

    def on_show(self) -> None:
        self.refresh()

    def set_theme(self, palette: Palette, _font_scale: float) -> None:
        self._palette = palette
        self.refresh()

    def refresh(self) -> None:
        # очистим текущие
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        unlocked = self.store.progress.achievements
        all_a = all_achievements()
        self.sub.setText(f"Получено {len(unlocked)} из {len(all_a)}.")
        per_row = 3
        for i, ach in enumerate(all_a):
            row = i // per_row
            col = i % per_row
            self.grid.addWidget(self._make_card(ach, ach.id in unlocked), row, col)

    def _make_card(self, ach, unlocked: bool) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setContentsMargins(16, 14, 16, 14)
        v.setSpacing(4)

        head = QHBoxLayout()
        icon = QLabel(ach.icon)
        icon.setStyleSheet("font-size: 28px;")
        head.addWidget(icon)
        title = QLabel(ach.title)
        title.setObjectName("h2")
        head.addWidget(title, stretch=1)
        if unlocked:
            tag = QLabel("✓ получено")
            tag.setStyleSheet(
                f"color: {self._palette.success}; font-weight: 600;"
            )
            head.addWidget(tag)
        else:
            tag = QLabel("закрыто")
            tag.setStyleSheet(
                f"color: {self._palette.text_dim}; font-weight: 500;"
            )
            head.addWidget(tag)
        v.addLayout(head)

        desc = QLabel(ach.description)
        desc.setWordWrap(True)
        desc.setObjectName("subtitle")
        v.addWidget(desc)

        if not unlocked:
            card.setStyleSheet("QFrame#card { opacity: 0.65; }")
        return card
