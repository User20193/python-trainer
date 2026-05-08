"""Песочница: запусти любой Python-код и посмотри вывод."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..progress import ProgressStore
from ..runner import run_user_code
from ..theme import DARK, Palette
from ..widgets.code_editor import CodeEditor

SANDBOX_DEFAULT = '''# Песочница: пиши любой Python и нажимай «Запустить».
# Можно использовать input() — просто вбей значения в поле «stdin».

name = input("Как тебя зовут? ")
print(f"Привет, {name}!")
print("Сумма 2+2 =", 2 + 2)
'''


class SandboxView(QWidget):
    """Простая REPL-вью: редактор → кнопка → вывод."""

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(8)

        title = QLabel("Песочница")
        title.setObjectName("title")
        outer.addWidget(title)
        sub = QLabel(
            "Здесь можно запускать любой Python-код. Все ошибки безопасны — "
            "код выполняется в отдельном процессе."
        )
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        outer.addWidget(sub)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        outer.addWidget(splitter, stretch=1)

        # left: editor
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(6)
        lv.addWidget(QLabel("Код:"))
        self.editor = CodeEditor()
        self.editor.textChanged.connect(self._on_editor_changed)
        lv.addWidget(self.editor, stretch=1)

        lv.addWidget(QLabel("stdin (по строке на input):"))
        self.stdin_edit = QPlainTextEdit()
        self.stdin_edit.setMaximumHeight(80)
        lv.addWidget(self.stdin_edit)

        btn_row = QHBoxLayout()
        self.btn_run = QPushButton("▶ Запустить")
        self.btn_run.setObjectName("primary")
        self.btn_run.clicked.connect(self._on_run)
        btn_row.addWidget(self.btn_run)
        self.btn_clear = QPushButton("Очистить вывод")
        self.btn_clear.setObjectName("ghost")
        self.btn_clear.clicked.connect(lambda: self.output.clear())
        btn_row.addWidget(self.btn_clear)
        self.btn_reset = QPushButton("Сбросить код")
        self.btn_reset.setObjectName("ghost")
        self.btn_reset.clicked.connect(self._on_reset)
        btn_row.addWidget(self.btn_reset)
        btn_row.addStretch(1)
        lv.addLayout(btn_row)

        splitter.addWidget(left)

        # right: output
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(6)
        rv.addWidget(QLabel("Вывод:"))
        self.output = QPlainTextEdit()
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        rv.addWidget(self.output, stretch=1)

        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusInfo")
        sf = QHBoxLayout(self.status_frame)
        sf.setContentsMargins(10, 6, 10, 6)
        self.status_label = QLabel("Готова к запуску.")
        sf.addWidget(self.status_label)
        rv.addWidget(self.status_frame)

        splitter.addWidget(right)
        splitter.setSizes([520, 520])

        # начальный код
        saved = self.store.progress.sandbox_code or SANDBOX_DEFAULT
        self.editor.setPlainText(saved)

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale
        self.editor.set_theme_dark(palette.name == "dark")

    def on_show(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    def _on_run(self) -> None:
        code = self.editor.toPlainText()
        stdin = self.stdin_edit.toPlainText()
        result = run_user_code(code, stdin=stdin, timeout=10.0)
        text = result.stdout
        if result.stderr:
            text = (text + ("\n" if text and not text.endswith("\n") else "") + result.stderr)
        if result.timed_out:
            self._set_status("⚠ Таймаут — код не уложился в 10 секунд.", "bad")
        elif result.return_code == 0:
            self._set_status("✓ Готово.", "ok")
        else:
            self._set_status("⚠ Программа завершилась с ошибкой.", "bad")
        if not text.strip():
            text = "(пустой вывод)"
        self.output.setPlainText(text)

    def _on_reset(self) -> None:
        self.editor.setPlainText(SANDBOX_DEFAULT)

    def _on_editor_changed(self) -> None:
        self.store.save_sandbox(self.editor.toPlainText())

    def _set_status(self, text: str, kind: str) -> None:
        if kind == "ok":
            self.status_frame.setObjectName("statusOk")
        elif kind == "bad":
            self.status_frame.setObjectName("statusBad")
        else:
            self.status_frame.setObjectName("statusInfo")
        self.status_frame.style().unpolish(self.status_frame)
        self.status_frame.style().polish(self.status_frame)
        self.status_label.setText(text)
