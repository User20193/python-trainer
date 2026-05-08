"""Карточки/квиз: маленькие вопросы с вариантами и пояснениями."""
from __future__ import annotations

import random

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..content import all_flashcards
from ..progress import ProgressStore
from ..theme import DARK, Palette
from ..widgets.markdown_view import MarkdownView


class FlashcardsView(QWidget):
    requested_xp = Signal(int, str)

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0
        self._cards = list(all_flashcards())
        self._index = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(10)

        title = QLabel("Карточки")
        title.setObjectName("title")
        outer.addWidget(title)
        sub = QLabel("Маленькие вопросы по пройденному. Если правильно — +2 XP.")
        sub.setObjectName("subtitle")
        outer.addWidget(sub)

        card = QFrame()
        card.setObjectName("card")
        cv = QVBoxLayout(card)
        cv.setContentsMargins(20, 18, 20, 18)
        cv.setSpacing(10)

        self.progress_label = QLabel("")
        self.progress_label.setObjectName("subtitle")
        cv.addWidget(self.progress_label)

        self.question_label = QLabel("")
        self.question_label.setObjectName("h2")
        self.question_label.setWordWrap(True)
        cv.addWidget(self.question_label)

        self.options_box = QVBoxLayout()
        self.options_box.setSpacing(6)
        cv.addLayout(self.options_box)
        self._group = QButtonGroup(self)

        self.expl_view = MarkdownView()
        self.expl_view.setMaximumHeight(180)
        self.expl_view.hide()
        cv.addWidget(self.expl_view)

        btn_row = QHBoxLayout()
        self.btn_check = QPushButton("Проверить")
        self.btn_check.setObjectName("primary")
        self.btn_check.clicked.connect(self._on_check)
        btn_row.addWidget(self.btn_check)
        self.btn_next = QPushButton("Дальше →")
        self.btn_next.setObjectName("ghost")
        self.btn_next.clicked.connect(self._on_next)
        self.btn_next.hide()
        btn_row.addWidget(self.btn_next)
        btn_row.addStretch(1)
        cv.addLayout(btn_row)

        outer.addWidget(card)
        outer.addStretch(1)

        self._reset_order()
        self._show()

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale

    def on_show(self) -> None:
        pass

    def refresh(self) -> None:
        self._reset_order()
        self._show()

    def _reset_order(self) -> None:
        self._index = 0
        self._cards = list(all_flashcards())
        random.shuffle(self._cards)

    def _show(self) -> None:
        if not self._cards:
            self.question_label.setText("Карточек пока нет — добавятся с уроками.")
            self.progress_label.setText("")
            self.btn_check.hide()
            self.btn_next.hide()
            self._clear_options()
            return
        if self._index >= len(self._cards):
            self.question_label.setText(
                "🎉 Все карточки на сегодня закончились. Можно перетасовать."
            )
            self.progress_label.setText("")
            self._clear_options()
            self.btn_check.setText("Перетасовать")
            self.btn_check.show()
            self.btn_check.clicked.disconnect()
            self.btn_check.clicked.connect(self.refresh)
            self.btn_next.hide()
            self.expl_view.hide()
            return

        card = self._cards[self._index]
        self.progress_label.setText(f"Карточка {self._index + 1} из {len(self._cards)}")
        self.question_label.setText(card.question)
        self._clear_options()
        for i, option in enumerate(card.options):
            rb = QRadioButton(option)
            self.options_box.addWidget(rb)
            self._group.addButton(rb, i)
        self.btn_check.setText("Проверить")
        try:
            self.btn_check.clicked.disconnect()
        except RuntimeError:
            pass
        self.btn_check.clicked.connect(self._on_check)
        self.btn_check.show()
        self.btn_next.hide()
        self.expl_view.hide()

    def _clear_options(self) -> None:
        for btn in list(self._group.buttons()):
            self._group.removeButton(btn)
            btn.setParent(None)
            btn.deleteLater()
        while self.options_box.count():
            item = self.options_box.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _on_check(self) -> None:
        if self._index >= len(self._cards):
            return
        chosen = self._group.checkedId()
        if chosen == -1:
            return
        card = self._cards[self._index]
        ok = chosen == card.correct_index
        text = "## ✓ Правильно!\n\n" if ok else "## ✗ Не совсем\n\n"
        if not ok:
            text += f"Правильный ответ: **{card.options[card.correct_index]}**\n\n"
        if card.explanation_md:
            text += card.explanation_md
        self.expl_view.set_markdown(text, self._palette, self._font_scale)
        self.expl_view.show()
        if ok:
            self.store.add_flashcard_correct(card.id)
            self.requested_xp.emit(2, "верный ответ карточки")
        self.btn_check.hide()
        self.btn_next.show()

    def _on_next(self) -> None:
        self._index += 1
        self._show()


_ = Qt
