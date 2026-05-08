"""Главный экран — приветствие, статистика, "что делать дальше"."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from ..content import all_achievements, all_lessons, all_tasks
from ..progress import ProgressStore, xp_to_next_level
from ..theme import DARK, Palette


class _Card(QFrame):
    def __init__(self, title: str, value: str, sub: str = "") -> None:
        super().__init__()
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(2)
        self.title_l = QLabel(title)
        self.title_l.setObjectName("subtitle")
        self.value_l = QLabel(value)
        self.value_l.setObjectName("stat")
        self.sub_l = QLabel(sub)
        self.sub_l.setObjectName("subtitle")
        layout.addWidget(self.title_l)
        layout.addWidget(self.value_l)
        layout.addWidget(self.sub_l)

    def set_value(self, value: str, sub: str = "") -> None:
        self.value_l.setText(value)
        self.sub_l.setText(sub)


class HomeView(QWidget):
    """Дашборд со статистикой и кнопкой «Продолжить»."""

    go_to = Signal(str)
    open_lesson = Signal(str)

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        self.greeting = QLabel("Привет!")
        self.greeting.setObjectName("title")
        layout.addWidget(self.greeting)

        self.subtitle = QLabel("Учим Python с нуля — мини-проект за мини-проектом.")
        self.subtitle.setObjectName("subtitle")
        layout.addWidget(self.subtitle)

        # карточки статистики
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)

        self.card_xp = _Card("Опыт (XP)", "0")
        self.card_level = _Card("Уровень", "1")
        self.card_streak = _Card("Стрик", "0 дн.")
        self.card_lessons = _Card("Пройдено уроков", "0/0")
        self.card_tasks = _Card("Решено задач", "0/0")
        self.card_ach = _Card("Достижений", "0/0")

        for c in (
            self.card_xp,
            self.card_level,
            self.card_streak,
            self.card_lessons,
            self.card_tasks,
            self.card_ach,
        ):
            cards_row.addWidget(c, stretch=1)
        layout.addLayout(cards_row)

        # прогресс по уровню
        self.level_progress = QProgressBar()
        self.level_progress.setRange(0, 100)
        self.level_progress.setFormat("%v / %m XP до следующего уровня")
        self.level_progress.setMinimumHeight(18)
        layout.addWidget(self.level_progress)

        # секция "Продолжить"
        cont_card = QFrame()
        cont_card.setObjectName("card")
        cont_layout = QVBoxLayout(cont_card)
        cont_layout.setContentsMargins(20, 18, 20, 18)
        cont_layout.setSpacing(10)

        h = QLabel("Что делать дальше")
        h.setObjectName("h2")
        cont_layout.addWidget(h)

        self.next_text = QLabel("Открой первый урок и поехали 🚀")
        self.next_text.setWordWrap(True)
        cont_layout.addWidget(self.next_text)

        cont_buttons = QHBoxLayout()
        cont_buttons.setSpacing(8)
        self.btn_continue = QPushButton("Продолжить")
        self.btn_continue.setObjectName("primary")
        self.btn_continue.clicked.connect(self._on_continue)
        self.btn_open_course = QPushButton("Открыть курс")
        self.btn_open_course.clicked.connect(lambda: self.go_to.emit("course"))
        self.btn_sandbox = QPushButton("Песочница")
        self.btn_sandbox.clicked.connect(lambda: self.go_to.emit("sandbox"))
        for b in (self.btn_continue, self.btn_open_course, self.btn_sandbox):
            cont_buttons.addWidget(b)
        cont_buttons.addStretch(1)
        cont_layout.addLayout(cont_buttons)

        layout.addWidget(cont_card)

        layout.addItem(
            QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # tip под низом
        tip = QLabel(
            "💡 Совет: ничего не понятно? Открой «Словарь» — там простые объяснения "
            "терминов. Или попробуй код в «Песочнице» — это безопасно."
        )
        tip.setWordWrap(True)
        tip.setObjectName("subtitle")
        layout.addWidget(tip)

        self.refresh()

    def on_show(self) -> None:
        self.refresh()

    def set_theme(self, palette: Palette, _font_scale: float) -> None:
        self._palette = palette
        # стили подхватятся из QApplication — переопределять нечего

    def refresh(self) -> None:
        p = self.store.progress
        s = p.settings
        if s.user_name.strip():
            self.greeting.setText(f"Привет, {s.user_name.strip()}!")
        else:
            self.greeting.setText("Привет!")

        # карточки
        all_l = all_lessons()
        all_t = all_tasks()
        all_a = all_achievements()
        self.card_xp.set_value(str(p.xp))
        self.card_level.set_value(str(p.level))
        self.card_streak.set_value(f"{p.streak_days} дн.")
        self.card_lessons.set_value(f"{len(p.completed_lessons)}/{len(all_l)}")
        self.card_tasks.set_value(f"{len(p.completed_tasks)}/{len(all_t)}")
        self.card_ach.set_value(f"{len(p.achievements)}/{len(all_a)}")

        cur, total = xp_to_next_level(p.xp)
        if total == 0:
            self.level_progress.setRange(0, 1)
            self.level_progress.setValue(1)
            self.level_progress.setFormat("Максимальный уровень")
        else:
            self.level_progress.setRange(0, total)
            self.level_progress.setValue(cur)
            self.level_progress.setFormat(f"{cur} / {total} XP до следующего уровня")

        # «что делать дальше»
        next_lesson = self._next_lesson()
        if next_lesson is None:
            self.next_text.setText("Все уроки пройдены 🎉 Загляни в «Карточки» или «Песочницу».")
            self.btn_continue.setEnabled(False)
        else:
            self.next_text.setText(
                f"📚 <b>{next_lesson.section_title}</b> → "
                f"<b>{next_lesson.title}</b>"
            )
            self.next_text.setTextFormat(Qt.TextFormat.RichText)
            self.btn_continue.setEnabled(True)
            self._next_lesson_id = next_lesson.id

    def _next_lesson(self):
        p = self.store.progress
        for lesson in all_lessons():
            if lesson.id not in p.completed_lessons:
                return lesson
        return None

    def _on_continue(self) -> None:
        nxt = self._next_lesson()
        if nxt:
            self.open_lesson.emit(nxt.id)
