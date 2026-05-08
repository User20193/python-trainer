"""Подсветка синтаксиса Python в редакторе кода через Pygments."""
from __future__ import annotations

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextDocument,
)
from PySide6.QtWidgets import QPlainTextEdit, QWidget


class PythonHighlighter(QSyntaxHighlighter):
    """Простой регексп-подсветчик Python — без зависимостей от Pygments в рантайме UI."""

    KEYWORDS = (
        "and as assert async await break class continue def del elif else except finally "
        "for from global if import in is lambda nonlocal not or pass raise return try "
        "while with yield"
    ).split()
    BUILTINS = (
        "True False None print input len range str int float list dict tuple set "
        "type isinstance open enumerate zip sorted reversed map filter sum max min abs "
        "round any all"
    ).split()

    def __init__(self, document: QTextDocument, dark: bool = True) -> None:
        super().__init__(document)
        self._rules: list[tuple[QRegularExpression, QTextCharFormat]] = []
        self._build(dark)

    def _fmt(self, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        f = QTextCharFormat()
        f.setForeground(QColor(color))
        if bold:
            f.setFontWeight(QFont.Weight.Bold)
        if italic:
            f.setFontItalic(True)
        return f

    def _build(self, dark: bool) -> None:
        if dark:
            kw = "#c792ea"
            builtin = "#82aaff"
            string = "#c3e88d"
            number = "#f78c6c"
            comment = "#5c6370"
            decorator = "#ffcb6b"
            funcdef = "#82aaff"
        else:
            kw = "#7c3aed"
            builtin = "#1d4ed8"
            string = "#15803d"
            number = "#b45309"
            comment = "#6b7280"
            decorator = "#a16207"
            funcdef = "#1d4ed8"

        self._rules.clear()

        for w in self.KEYWORDS:
            self._rules.append(
                (QRegularExpression(rf"\b{w}\b"), self._fmt(kw, bold=True)),
            )
        for w in self.BUILTINS:
            self._rules.append(
                (QRegularExpression(rf"\b{w}\b"), self._fmt(builtin)),
            )

        self._rules.append(
            (QRegularExpression(r"\bdef\s+(\w+)"), self._fmt(funcdef, bold=True))
        )
        self._rules.append(
            (QRegularExpression(r"\bclass\s+(\w+)"), self._fmt(funcdef, bold=True))
        )
        self._rules.append(
            (QRegularExpression(r"@\w+"), self._fmt(decorator)),
        )
        self._rules.append(
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), self._fmt(number)),
        )
        self._rules.append(
            (QRegularExpression(r"#[^\n]*"), self._fmt(comment, italic=True)),
        )
        # строки
        self._rules.append(
            (
                QRegularExpression(r"f?\"([^\"\\]|\\.)*\""),
                self._fmt(string),
            ),
        )
        self._rules.append(
            (
                QRegularExpression(r"f?'([^'\\]|\\.)*'"),
                self._fmt(string),
            ),
        )

    def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt API)
        for regex, fmt in self._rules:
            it = regex.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)


class LineNumberArea(QWidget):
    def __init__(self, editor: CodeEditor) -> None:
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):  # noqa: N802
        return self.editor.line_number_area_size()

    def paintEvent(self, event):  # noqa: N802
        self.editor.line_number_area_paint(event)


class CodeEditor(QPlainTextEdit):
    """Редактор Python-кода с подсветкой и нумерацией строк."""

    def __init__(self, parent=None, dark: bool = True) -> None:
        super().__init__(parent)
        self.setObjectName("code")
        font = QFont("JetBrains Mono")
        if not font.exactMatch():
            font = QFont("Cascadia Mono")
        if not font.exactMatch():
            font = QFont("Consolas")
        if not font.exactMatch():
            font = QFont("Menlo")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(11)
        self.setFont(font)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        self._highlighter = PythonHighlighter(self.document(), dark=dark)

        self._line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_area_width)
        self.updateRequest.connect(self._update_line_area)
        self._update_line_area_width()
        self._dark = dark

    def set_theme_dark(self, dark: bool) -> None:
        self._dark = dark
        self._highlighter = PythonHighlighter(self.document(), dark=dark)
        self._highlighter.rehighlight()
        self._line_area.update()

    def line_number_area_width(self) -> int:
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 10 + self.fontMetrics().horizontalAdvance("9") * digits

    def line_number_area_size(self):
        from PySide6.QtCore import QSize

        return QSize(self.line_number_area_width(), 0)

    def _update_line_area_width(self) -> None:
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _update_line_area(self, rect, dy) -> None:
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_area_width()

    def resizeEvent(self, e):  # noqa: N802
        super().resizeEvent(e)
        cr = self.contentsRect()
        self._line_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())

    def line_number_area_paint(self, event) -> None:
        painter = QPainter(self._line_area)
        bg = QColor("#0c0f17" if self._dark else "#eaeef6")
        fg = QColor("#5b6072" if self._dark else "#7a8095")
        painter.fillRect(event.rect(), bg)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        painter.setPen(fg)
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0,
                    int(top),
                    self._line_area.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
