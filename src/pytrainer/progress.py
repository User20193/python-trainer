"""Сохранение прогресса и настроек пользователя в JSON.

Хранятся:
- завершённые уроки/задачи
- XP, уровень, стрик дней
- разблокированные достижения
- последние сохранённые решения задач
- личные заметки по урокам
- настройки (тема, размер шрифта, имя)

Файл: ``%APPDATA%/PyTrainer/progress.json`` на Windows,
``~/.local/share/PyTrainer/progress.json`` на Linux,
``~/Library/Application Support/PyTrainer/progress.json`` на macOS.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path


def app_data_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = str(Path.home() / "Library" / "Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    p = Path(base) / "PyTrainer"
    p.mkdir(parents=True, exist_ok=True)
    return p


# Уровни: индекс = уровень - 1, значение = минимальный XP, нужный, чтобы туда попасть.
LEVEL_THRESHOLDS = [0, 50, 120, 220, 360, 540, 770, 1050, 1380, 1760, 2200]


def level_from_xp(xp: int) -> int:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
        else:
            break
    return level


def xp_to_next_level(xp: int) -> tuple[int, int]:
    """Возвращает (xp_в_текущем_уровне, xp_до_следующего_уровня).

    Если уровень максимальный — возвращает (xp_в_текущем, 0).
    """
    lvl = level_from_xp(xp)
    if lvl >= len(LEVEL_THRESHOLDS):
        return (xp - LEVEL_THRESHOLDS[-1], 0)
    cur = LEVEL_THRESHOLDS[lvl - 1]
    nxt = LEVEL_THRESHOLDS[lvl]
    return (xp - cur, nxt - cur)


@dataclass
class Settings:
    theme: str = "dark"  # dark / light
    font_scale: float = 1.0  # 0.85 / 1.0 / 1.15 / 1.3
    user_name: str = ""

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "font_scale": self.font_scale,
            "user_name": self.user_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Settings:
        return cls(
            theme=data.get("theme", "dark"),
            font_scale=float(data.get("font_scale", 1.0)),
            user_name=data.get("user_name", ""),
        )


@dataclass
class Progress:
    completed_lessons: set[str] = field(default_factory=set)
    completed_tasks: set[str] = field(default_factory=set)
    flashcard_correct: dict[str, int] = field(default_factory=dict)
    last_saved_code: dict[str, str] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)  # lesson_id -> текст
    sandbox_code: str = ""
    xp: int = 0
    streak_days: int = 0
    last_active_iso: str = ""  # YYYY-MM-DD
    achievements: set[str] = field(default_factory=set)
    settings: Settings = field(default_factory=Settings)

    def to_dict(self) -> dict:
        return {
            "completed_lessons": sorted(self.completed_lessons),
            "completed_tasks": sorted(self.completed_tasks),
            "flashcard_correct": self.flashcard_correct,
            "last_saved_code": self.last_saved_code,
            "notes": self.notes,
            "sandbox_code": self.sandbox_code,
            "xp": self.xp,
            "streak_days": self.streak_days,
            "last_active_iso": self.last_active_iso,
            "achievements": sorted(self.achievements),
            "settings": self.settings.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Progress:
        return cls(
            completed_lessons=set(data.get("completed_lessons", [])),
            completed_tasks=set(data.get("completed_tasks", [])),
            flashcard_correct=dict(data.get("flashcard_correct", {})),
            last_saved_code=dict(data.get("last_saved_code", {})),
            notes=dict(data.get("notes", {})),
            sandbox_code=data.get("sandbox_code", ""),
            xp=int(data.get("xp", 0)),
            streak_days=int(data.get("streak_days", 0)),
            last_active_iso=data.get("last_active_iso", ""),
            achievements=set(data.get("achievements", [])),
            settings=Settings.from_dict(data.get("settings", {})),
        )

    @property
    def level(self) -> int:
        return level_from_xp(self.xp)


class ProgressStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (app_data_dir() / "progress.json")
        self._progress = self._load()

    def _load(self) -> Progress:
        if not self.path.exists():
            return Progress()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return Progress()
        return Progress.from_dict(data)

    def save(self) -> None:
        self.path.write_text(
            json.dumps(self._progress.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @property
    def progress(self) -> Progress:
        return self._progress

    # --- удобные операции ---

    def touch_today(self) -> int:
        """Зафиксировать активность сегодня. Возвращает текущий стрик."""
        today = date.today().isoformat()
        if self._progress.last_active_iso == today:
            return self._progress.streak_days

        prev: date | None = None
        if self._progress.last_active_iso:
            try:
                prev = date.fromisoformat(self._progress.last_active_iso)
            except ValueError:
                prev = None

        if prev and (date.today() - prev) == timedelta(days=1):
            self._progress.streak_days += 1
        else:
            self._progress.streak_days = 1
        self._progress.last_active_iso = today
        self.save()
        return self._progress.streak_days

    def add_xp(self, amount: int) -> tuple[int, bool]:
        """Добавить XP. Возвращает (новый_xp, повышен_ли_уровень)."""
        prev_level = self._progress.level
        self._progress.xp += amount
        new_level = self._progress.level
        self.save()
        return self._progress.xp, new_level > prev_level

    def mark_lesson_done(self, lesson_id: str) -> bool:
        """Отметить урок пройденным. True, если впервые."""
        if lesson_id in self._progress.completed_lessons:
            return False
        self._progress.completed_lessons.add(lesson_id)
        self.save()
        return True

    def mark_task_done(self, task_id: str) -> bool:
        if task_id in self._progress.completed_tasks:
            return False
        self._progress.completed_tasks.add(task_id)
        self.save()
        return True

    def save_task_code(self, task_id: str, code: str) -> None:
        self._progress.last_saved_code[task_id] = code
        self.save()

    def get_task_code(self, task_id: str) -> str | None:
        return self._progress.last_saved_code.get(task_id)

    def save_note(self, lesson_id: str, text: str) -> None:
        if text.strip():
            self._progress.notes[lesson_id] = text
        else:
            self._progress.notes.pop(lesson_id, None)
        self.save()

    def get_note(self, lesson_id: str) -> str:
        return self._progress.notes.get(lesson_id, "")

    def save_sandbox(self, code: str) -> None:
        self._progress.sandbox_code = code
        self.save()

    def add_flashcard_correct(self, card_id: str) -> None:
        self._progress.flashcard_correct[card_id] = (
            self._progress.flashcard_correct.get(card_id, 0) + 1
        )
        self.save()

    def unlock_achievement(self, ach_id: str) -> bool:
        if ach_id in self._progress.achievements:
            return False
        self._progress.achievements.add(ach_id)
        self.save()
        return True

    def update_settings(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self._progress.settings, k):
                setattr(self._progress.settings, k, v)
        self.save()

    def reset(self) -> None:
        kept_settings = self._progress.settings
        self._progress = Progress(settings=kept_settings)
        self.save()
