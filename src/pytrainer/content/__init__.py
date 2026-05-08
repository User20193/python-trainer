"""Модели контента (уроки, задачи, словарь, карточки, достижения).

Контент хранится прямо как Python-объекты — это удобно для добавления новых
уроков и для статической проверки структуры. Данные собираются в реестры
в соседних модулях (``lessons``, ``tasks`` и т.п.).
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

# --- Уроки и задачи ---


@dataclass(frozen=True)
class TaskTest:
    """Один автотест для задачи."""

    kind: str  # 'stdio' | 'functional'
    name: str  # человекочитаемое имя
    # для stdio:
    stdin: str = ""
    expected_stdout: str = ""
    # для functional:
    function: str = ""
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    expected: object = None


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description_md: str
    starter_code: str
    solution_code: str
    solution_explanation_md: str
    hints: tuple[str, ...] = ()
    tests: tuple[TaskTest, ...] = ()
    xp: int = 10


@dataclass(frozen=True)
class Lesson:
    id: str
    section_id: str  # например, "01-basics"
    section_title: str  # для отображения в дереве
    title: str
    body_md: str
    try_it_code: str | None = None
    task_ids: tuple[str, ...] = ()
    xp: int = 5


# --- Словарь терминов ---


@dataclass(frozen=True)
class GlossaryEntry:
    term: str
    definition_md: str
    related_lesson_ids: tuple[str, ...] = ()


# --- Карточки/квиз ---


@dataclass(frozen=True)
class Flashcard:
    id: str
    section_id: str
    question: str
    options: tuple[str, ...]
    correct_index: int
    explanation_md: str = ""


# --- Достижения ---


@dataclass(frozen=True)
class Achievement:
    """Достижение.

    ``check`` принимает текущий ``Progress`` и возвращает True, если получено.
    """

    id: str
    title: str
    description: str
    icon: str  # эмодзи
    check: Callable[[object], bool] = field(repr=False)


def all_lessons() -> tuple[Lesson, ...]:
    from .lessons import LESSONS

    return LESSONS


def all_tasks() -> tuple[Task, ...]:
    from .tasks import TASKS

    return TASKS


def all_glossary() -> tuple[GlossaryEntry, ...]:
    from .glossary import GLOSSARY

    return GLOSSARY


def all_flashcards() -> tuple[Flashcard, ...]:
    from .flashcards import FLASHCARDS

    return FLASHCARDS


def all_achievements() -> tuple[Achievement, ...]:
    from .achievements import ACHIEVEMENTS

    return ACHIEVEMENTS


def task_by_id(task_id: str) -> Task | None:
    for t in all_tasks():
        if t.id == task_id:
            return t
    return None


def lesson_by_id(lesson_id: str) -> Lesson | None:
    for lesson in all_lessons():
        if lesson.id == lesson_id:
            return lesson
    return None


def lessons_by_section() -> list[tuple[str, str, list[Lesson]]]:
    """Список (section_id, section_title, [lessons]) в порядке появления."""
    seen: dict[str, tuple[str, list[Lesson]]] = {}
    order: list[str] = []
    for lesson in all_lessons():
        if lesson.section_id not in seen:
            seen[lesson.section_id] = (lesson.section_title, [])
            order.append(lesson.section_id)
        seen[lesson.section_id][1].append(lesson)
    return [(sid, seen[sid][0], seen[sid][1]) for sid in order]


def lessons_in_section(section_id: str) -> Sequence[Lesson]:
    return [lesson for lesson in all_lessons() if lesson.section_id == section_id]
