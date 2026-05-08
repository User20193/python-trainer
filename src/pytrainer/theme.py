"""Темы (тёмная/светлая) и масштабирование шрифта.

Стили формируются из палитры, чтобы можно было переключаться без перезапуска.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    name: str
    bg: str
    bg_panel: str
    bg_card: str
    bg_code: str
    bg_output: str
    border: str
    border_strong: str
    text: str
    text_muted: str
    text_dim: str
    accent: str
    accent_text: str
    success: str
    success_bg: str
    success_text: str
    danger: str
    danger_bg: str
    danger_text: str
    info_bg: str
    info_text: str
    selection: str


DARK = Palette(
    name="dark",
    bg="#0f1117",
    bg_panel="#161922",
    bg_card="#161922",
    bg_code="#0c0f17",
    bg_output="#080a11",
    border="#1f2330",
    border_strong="#2a3142",
    text="#e6e6e6",
    text_muted="#c8ccd6",
    text_dim="#6c7180",
    accent="#5a8dee",
    accent_text="#0a0d14",
    success="#2bb673",
    success_bg="#133b29",
    success_text="#bff5d8",
    danger="#d96565",
    danger_bg="#3b1f1f",
    danger_text="#ffd2d2",
    info_bg="#1d2840",
    info_text="#cfdcf6",
    selection="#2c5dbf",
)


LIGHT = Palette(
    name="light",
    bg="#f4f6fb",
    bg_panel="#ffffff",
    bg_card="#ffffff",
    bg_code="#f1f3f9",
    bg_output="#fafbfd",
    border="#dde2eb",
    border_strong="#c7cdd9",
    text="#1c2030",
    text_muted="#3a4258",
    text_dim="#7a8095",
    accent="#3b6fd6",
    accent_text="#ffffff",
    success="#1f8a55",
    success_bg="#dff5e8",
    success_text="#0c4a2c",
    danger="#c43d3d",
    danger_bg="#fde0e0",
    danger_text="#5a1a1a",
    info_bg="#e1ecff",
    info_text="#1f3b6e",
    selection="#a4c2f4",
)


def get_palette(name: str) -> Palette:
    return LIGHT if name == "light" else DARK


def build_qss(palette: Palette, font_scale: float = 1.0) -> str:
    base = max(11, int(round(13 * font_scale)))
    code = max(11, int(round(13 * font_scale)))
    title = max(16, int(round(22 * font_scale)))
    subtitle = max(11, int(round(13 * font_scale)))
    section = max(10, int(round(11 * font_scale)))
    stat = max(20, int(round(28 * font_scale)))
    p = palette
    return f"""
* {{
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: {base}px;
    color: {p.text};
}}

QMainWindow, QWidget#root {{
    background-color: {p.bg};
}}

QWidget#sidebar {{
    background-color: {p.bg_panel};
    border-right: 1px solid {p.border};
}}

QListWidget#nav {{
    background-color: transparent;
    border: none;
    outline: 0;
    padding: 8px 0;
    font-size: {base}px;
}}

QListWidget#nav::item {{
    padding: 10px 18px;
    border-left: 3px solid transparent;
    color: {p.text_muted};
}}

QListWidget#nav::item:hover {{
    background-color: {p.border};
}}

QListWidget#nav::item:selected {{
    background-color: {p.border};
    color: {p.text};
    border-left: 3px solid {p.accent};
}}

QLabel#brand {{
    color: {p.text};
    font-size: {max(15, int(round(18 * font_scale)))}px;
    font-weight: 600;
    padding: 18px 18px 6px 18px;
}}

QLabel#brandSub {{
    color: {p.text_dim};
    font-size: {section}px;
    padding: 0 18px 18px 18px;
}}

QLabel.section, QLabel#section {{
    color: {p.text_dim};
    font-size: {section}px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12px 18px 4px 18px;
}}

QPushButton {{
    background-color: {p.border_strong};
    color: {p.text};
    border: 1px solid {p.border_strong};
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 500;
    font-size: {base}px;
}}

QPushButton:hover {{
    background-color: {p.border};
}}

QPushButton:disabled {{
    background-color: {p.border};
    color: {p.text_dim};
    border: 1px solid {p.border};
}}

QPushButton#primary {{
    background-color: {p.accent};
    border: 1px solid {p.accent};
    color: {p.accent_text};
    font-weight: 600;
}}

QPushButton#success {{
    background-color: {p.success};
    border: 1px solid {p.success};
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#danger {{
    background-color: {p.danger};
    border: 1px solid {p.danger};
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#ghost {{
    background-color: transparent;
    border: 1px solid {p.border_strong};
    color: {p.text};
}}

QTextBrowser, QPlainTextEdit, QTextEdit, QLineEdit {{
    background-color: {p.bg_panel};
    border: 1px solid {p.border};
    border-radius: 6px;
    selection-background-color: {p.selection};
    color: {p.text};
    padding: 6px;
    font-size: {base}px;
}}

QPlainTextEdit#code, QTextEdit#code {{
    font-family: "JetBrains Mono", "Cascadia Mono", "Consolas", "Menlo", monospace;
    font-size: {code}px;
    background-color: {p.bg_code};
    border: 1px solid {p.border};
    color: {p.text};
}}

QPlainTextEdit#output, QTextEdit#output {{
    font-family: "JetBrains Mono", "Cascadia Mono", "Consolas", "Menlo", monospace;
    font-size: {max(10, code - 1)}px;
    background-color: {p.bg_output};
    border: 1px solid {p.border};
}}

QSplitter::handle {{
    background-color: {p.border};
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {p.border_strong};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {p.border_strong};
    border-radius: 5px;
    min-width: 30px;
}}

QLabel#title {{
    font-size: {title}px;
    font-weight: 600;
    color: {p.text};
}}

QLabel#h2 {{
    font-size: {max(14, int(round(16 * font_scale)))}px;
    font-weight: 600;
    color: {p.text};
}}

QLabel#subtitle {{
    font-size: {subtitle}px;
    color: {p.text_dim};
}}

QLabel#stat {{
    font-size: {stat}px;
    font-weight: 700;
    color: {p.text};
}}

QFrame#card {{
    background-color: {p.bg_card};
    border: 1px solid {p.border};
    border-radius: 10px;
}}

QFrame#statusOk {{
    background-color: {p.success_bg};
    border: 1px solid {p.success};
    border-radius: 6px;
}}

QFrame#statusOk QLabel {{
    color: {p.success_text};
}}

QFrame#statusBad {{
    background-color: {p.danger_bg};
    border: 1px solid {p.danger};
    border-radius: 6px;
}}

QFrame#statusBad QLabel {{
    color: {p.danger_text};
}}

QFrame#statusInfo {{
    background-color: {p.info_bg};
    border: 1px solid {p.border_strong};
    border-radius: 6px;
}}

QFrame#statusInfo QLabel {{
    color: {p.info_text};
}}

QProgressBar {{
    background-color: {p.bg_card};
    border: 1px solid {p.border};
    border-radius: 6px;
    text-align: center;
    color: {p.text};
    height: {max(12, int(round(14 * font_scale)))}px;
    font-size: {section}px;
}}

QProgressBar::chunk {{
    background-color: {p.accent};
    border-radius: 5px;
}}

QComboBox {{
    background-color: {p.bg_card};
    border: 1px solid {p.border_strong};
    border-radius: 6px;
    padding: 6px 10px;
    color: {p.text};
    min-width: 140px;
}}

QComboBox QAbstractItemView {{
    background-color: {p.bg_card};
    color: {p.text};
    selection-background-color: {p.selection};
    border: 1px solid {p.border_strong};
}}

QToolTip {{
    color: {p.text};
    background-color: {p.bg_card};
    border: 1px solid {p.border_strong};
    padding: 6px;
}}

QListWidget {{
    background-color: {p.bg_panel};
    border: 1px solid {p.border};
    border-radius: 6px;
    color: {p.text};
}}

QListWidget::item {{
    padding: 6px 10px;
}}

QListWidget::item:selected {{
    background-color: {p.selection};
    color: {p.text};
}}

QTreeWidget {{
    background-color: {p.bg_panel};
    border: 1px solid {p.border};
    border-radius: 6px;
    color: {p.text};
}}

QTreeWidget::item {{
    padding: 4px 6px;
}}

QTreeWidget::item:selected {{
    background-color: {p.selection};
}}
"""
