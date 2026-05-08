"""Главное окно приложения PyTrainer."""
from __future__ import annotations

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from . import APP_NAME, __version__
from .progress import ProgressStore, level_from_xp, xp_to_next_level
from .theme import build_qss, get_palette
from .views.achievements import AchievementsView
from .views.flashcards import FlashcardsView
from .views.glossary import GlossaryView
from .views.home import HomeView
from .views.lessons import LessonsView
from .views.notes import NotesView
from .views.sandbox import SandboxView
from .views.settings import SettingsView

NAV_ITEMS = [
    ("home", "Главная", "🏠"),
    ("course", "Курс", "📚"),
    ("sandbox", "Песочница", "🧪"),
    ("flashcards", "Карточки", "🃏"),
    ("notes", "Заметки", "📝"),
    ("glossary", "Словарь", "📖"),
    ("achievements", "Достижения", "🏆"),
    ("settings", "Настройки", "⚙️"),
]


class Toast(QFrame):
    """Уведомление, всплывающее в правом верхнем углу окна."""

    def __init__(self, parent, palette) -> None:
        super().__init__(parent)
        self.setObjectName("statusInfo")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self._label = QLabel("", self)
        self._label.setWordWrap(True)
        self._label.setStyleSheet("padding: 10px 14px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)
        self.hide()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)
        self._palette = palette

    def set_palette(self, palette) -> None:
        self._palette = palette

    def show_message(self, text: str, kind: str = "info", ms: int = 3500) -> None:
        if kind == "ok":
            self.setObjectName("statusOk")
        elif kind == "bad":
            self.setObjectName("statusBad")
        else:
            self.setObjectName("statusInfo")
        # перезапросить qss
        self.style().unpolish(self)
        self.style().polish(self)
        self._label.setText(text)
        parent = self.parentWidget()
        if parent is not None:
            self.adjustSize()
            self.setMinimumWidth(min(420, max(260, self.sizeHint().width() + 40)))
            self.adjustSize()
            x = parent.width() - self.width() - 24
            y = 24
            self.move(x, y)
        self.show()
        self.raise_()
        self._timer.start(ms)


class MainWindow(QMainWindow):
    palette_changed = Signal()

    def __init__(self, store: ProgressStore) -> None:
        super().__init__()
        self.store = store
        self.setWindowTitle(f"{APP_NAME} — учим Python с нуля")
        self.resize(1200, 760)
        self.setMinimumSize(1024, 640)
        self.setWindowIcon(_default_icon())

        root = QWidget()
        root.setObjectName("root")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)

        brand = QLabel(APP_NAME)
        brand.setObjectName("brand")
        sb_layout.addWidget(brand)
        brand_sub = QLabel(f"v{__version__} · учим Python с нуля")
        brand_sub.setObjectName("brandSub")
        sb_layout.addWidget(brand_sub)

        nav_section = QLabel("Навигация")
        nav_section.setObjectName("section")
        sb_layout.addWidget(nav_section)

        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        self.nav.setSpacing(0)
        self.nav.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        for key, label, emoji in NAV_ITEMS:
            item = QListWidgetItem(f"{emoji}  {label}")
            item.setData(Qt.ItemDataRole.UserRole, key)
            item.setSizeHint(QSize(0, 38))
            self.nav.addItem(item)
        sb_layout.addWidget(self.nav, stretch=1)

        # XP/level summary в нижней части сайдбара
        self.xp_summary = QLabel("")
        self.xp_summary.setObjectName("brandSub")
        self.xp_summary.setWordWrap(True)
        self.xp_summary.setMargin(0)
        self.xp_summary.setStyleSheet("padding: 8px 18px 16px 18px;")
        sb_layout.addWidget(self.xp_summary)

        root_layout.addWidget(sidebar)

        # Stack of views
        self.stack = QStackedWidget()
        self.stack.setObjectName("stack")
        root_layout.addWidget(self.stack, stretch=1)

        self.setCentralWidget(root)

        # Создание представлений
        self.home_view = HomeView(self.store, self)
        self.lessons_view = LessonsView(self.store, self)
        self.sandbox_view = SandboxView(self.store, self)
        self.flashcards_view = FlashcardsView(self.store, self)
        self.notes_view = NotesView(self.store, self)
        self.glossary_view = GlossaryView(self.store, self)
        self.achievements_view = AchievementsView(self.store, self)
        self.settings_view = SettingsView(self.store, self)

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.lessons_view)
        self.stack.addWidget(self.sandbox_view)
        self.stack.addWidget(self.flashcards_view)
        self.stack.addWidget(self.notes_view)
        self.stack.addWidget(self.glossary_view)
        self.stack.addWidget(self.achievements_view)
        self.stack.addWidget(self.settings_view)

        self._views_by_key = {
            "home": self.home_view,
            "course": self.lessons_view,
            "sandbox": self.sandbox_view,
            "flashcards": self.flashcards_view,
            "notes": self.notes_view,
            "glossary": self.glossary_view,
            "achievements": self.achievements_view,
            "settings": self.settings_view,
        }

        self.nav.currentItemChanged.connect(self._on_nav_changed)
        self.nav.setCurrentRow(0)

        # сигналы
        self.home_view.go_to.connect(self.go_to)
        self.home_view.open_lesson.connect(self.open_lesson)
        self.lessons_view.requested_xp.connect(self._on_xp_event)
        self.lessons_view.requested_lesson_xp.connect(self._on_lesson_xp_event)
        self.lessons_view.requested_open_term.connect(self._open_glossary_term)
        self.flashcards_view.requested_xp.connect(self._on_xp_event)
        self.settings_view.theme_changed.connect(self._apply_theme)
        self.settings_view.font_scale_changed.connect(self._apply_theme)
        self.settings_view.user_name_changed.connect(self._on_user_name_changed)
        self.settings_view.progress_reset.connect(self._on_progress_reset)

        self.toast = Toast(self, get_palette(self.store.progress.settings.theme))

        # Стрик дня (фиксируем активность)
        self.store.touch_today()
        self._check_achievements()
        self._update_xp_summary()
        self._apply_theme()

    # --- public ---

    def go_to(self, key: str) -> None:
        idx = next((i for i, (k, _, _) in enumerate(NAV_ITEMS) if k == key), 0)
        self.nav.setCurrentRow(idx)

    def open_lesson(self, lesson_id: str) -> None:
        self.go_to("course")
        self.lessons_view.open_lesson(lesson_id)

    def show_toast(self, text: str, kind: str = "info") -> None:
        self.toast.show_message(text, kind)

    def resizeEvent(self, e):  # noqa: N802
        super().resizeEvent(e)
        if self.toast.isVisible():
            x = self.width() - self.toast.width() - 24
            self.toast.move(x, 24)

    # --- internal ---

    def _on_nav_changed(self, current, _previous) -> None:
        if current is None:
            return
        key = current.data(Qt.ItemDataRole.UserRole)
        view = self._views_by_key.get(key)
        if view:
            self.stack.setCurrentWidget(view)
            if hasattr(view, "on_show"):
                view.on_show()

    def _on_xp_event(self, amount: int, message: str) -> None:
        new_xp, level_up = self.store.add_xp(amount)
        msg = f"+{amount} XP — {message}"
        if level_up:
            msg += f" 🎉 уровень {level_from_xp(new_xp)}!"
        self.show_toast(msg, "ok")
        self._check_achievements()
        self._update_xp_summary()
        self.home_view.refresh()
        self.achievements_view.refresh()

    def _on_lesson_xp_event(self, amount: int, lesson_id: str) -> None:
        self._on_xp_event(amount, f"урок «{lesson_id}» пройден")

    def _on_user_name_changed(self, _name: str) -> None:
        self.home_view.refresh()

    def _on_progress_reset(self) -> None:
        self._update_xp_summary()
        self.home_view.refresh()
        self.lessons_view.refresh()
        self.flashcards_view.refresh()
        self.achievements_view.refresh()
        self.notes_view.refresh()
        self.show_toast("Прогресс сброшен. Начинаем заново!", "info")

    def _open_glossary_term(self, term: str) -> None:
        self.go_to("glossary")
        self.glossary_view.focus_term(term)

    def _apply_theme(self) -> None:
        s = self.store.progress.settings
        palette = get_palette(s.theme)
        QApplication.instance().setStyleSheet(build_qss(palette, s.font_scale))
        self.toast.set_palette(palette)
        for view in self._views_by_key.values():
            if hasattr(view, "set_theme"):
                view.set_theme(palette, s.font_scale)
        self.palette_changed.emit()

    def _update_xp_summary(self) -> None:
        p = self.store.progress
        cur, total = xp_to_next_level(p.xp)
        if total == 0:
            line = f"⚡ {p.xp} XP · уровень {p.level} (макс)"
        else:
            line = f"⚡ {p.xp} XP · уровень {p.level} ({cur}/{total} до {p.level + 1})"
        line += f"\n🔥 стрик: {p.streak_days} дн."
        self.xp_summary.setText(line)

    def _check_achievements(self) -> None:
        from .content import all_achievements

        p = self.store.progress
        for ach in all_achievements():
            try:
                if ach.id not in p.achievements and ach.check(p):
                    if self.store.unlock_achievement(ach.id):
                        self.show_toast(f"{ach.icon} Получено: «{ach.title}»", "ok")
            except Exception:  # noqa: BLE001
                continue


def _default_icon() -> QIcon:
    pix = QPixmap(64, 64)
    pix.fill(QColor("#5a8dee"))
    from PySide6.QtGui import QPainter

    painter = QPainter(pix)
    painter.setPen(QColor("#0a0d14"))
    f = QFont("Segoe UI")
    f.setBold(True)
    f.setPointSize(28)
    painter.setFont(f)
    painter.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, "Py")
    painter.end()
    return QIcon(pix)


def run_app(argv: list[str]) -> int:
    app = QApplication.instance() or QApplication(argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_NAME)

    store = ProgressStore()
    win = MainWindow(store)
    win.show()
    return app.exec()
