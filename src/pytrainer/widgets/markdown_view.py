"""Рендер Markdown с подсветкой code-блоков через Pygments."""
from __future__ import annotations

import re

import markdown as md_lib
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import PythonLexer
from pygments.util import ClassNotFound
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QTextBrowser

from ..theme import LIGHT, Palette

CODE_BLOCK_RE = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)


def render_markdown(text: str, palette: Palette, font_scale: float = 1.0) -> str:
    """Превратить markdown-строку в HTML, подходящий для QTextBrowser.setHtml."""
    # Подсветим code-блоки сами, потом отдадим оставшееся в markdown library.
    pieces: list[str] = []
    last = 0
    formatter_style = "default" if palette is LIGHT else "monokai"
    formatter = HtmlFormatter(style=formatter_style, noclasses=True, nowrap=False)

    for m in CODE_BLOCK_RE.finditer(text):
        pieces.append(text[last : m.start()])
        lang = m.group(1).strip() or "python"
        body = m.group(2)
        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = PythonLexer()
        html_block = highlight(body, lexer, formatter)
        # markdown-движок не должен переваривать получившийся HTML
        pieces.append(f"\n\n<!--RAWCODE-->{html_block}<!--/RAWCODE-->\n\n")
        last = m.end()
    pieces.append(text[last:])
    intermediate = "".join(pieces)

    md = md_lib.Markdown(extensions=["extra", "sane_lists", "toc"])
    html_body = md.convert(intermediate)

    base = max(11, int(round(13 * font_scale)))
    h1 = max(16, int(round(22 * font_scale)))
    h2 = max(14, int(round(18 * font_scale)))
    h3 = max(13, int(round(15 * font_scale)))

    css = f"""
    <style>
    body {{
        color: {palette.text};
        background: transparent;
        font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
        font-size: {base}px;
        line-height: 1.55;
    }}
    h1 {{ font-size: {h1}px; color: {palette.text}; margin-top: 0; }}
    h2 {{ font-size: {h2}px; color: {palette.text}; margin-top: 18px; }}
    h3 {{ font-size: {h3}px; color: {palette.text}; margin-top: 14px; }}
    a {{ color: {palette.accent}; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    p, li {{ color: {palette.text}; }}
    code {{
        font-family: "JetBrains Mono", "Cascadia Mono", "Consolas", monospace;
        background: {palette.bg_code};
        color: {palette.text};
        padding: 1px 5px;
        border-radius: 4px;
    }}
    pre {{
        background: {palette.bg_code};
        border: 1px solid {palette.border};
        border-radius: 8px;
        padding: 10px 12px;
        overflow-x: auto;
        font-size: {base}px;
    }}
    blockquote {{
        margin: 8px 0;
        padding: 8px 12px;
        border-left: 3px solid {palette.accent};
        background: {palette.info_bg};
        color: {palette.text};
        border-radius: 4px;
    }}
    table {{ border-collapse: collapse; }}
    th, td {{
        border: 1px solid {palette.border};
        padding: 6px 10px;
    }}
    th {{ background: {palette.bg_card}; }}
    </style>
    """
    return css + html_body


class MarkdownView(QTextBrowser):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setOpenLinks(False)
        self.setOpenExternalLinks(False)
        self.anchorClicked.connect(self._on_anchor_clicked)
        self._on_link: callable | None = None

    def set_markdown(self, text: str, palette: Palette, font_scale: float = 1.0) -> None:
        self.setHtml(render_markdown(text, palette, font_scale))

    def set_link_handler(self, handler) -> None:
        self._on_link = handler

    def _on_anchor_clicked(self, url: QUrl) -> None:
        s = url.toString()
        # внутренние ссылки начинаются с "lesson:" / "term:" / "task:"
        if self._on_link and (
            s.startswith("lesson:") or s.startswith("term:") or s.startswith("task:")
        ):
            self._on_link(s)
            return
        QDesktopServices.openUrl(url)
