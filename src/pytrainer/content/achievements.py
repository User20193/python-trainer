"""Достижения."""
from __future__ import annotations

from . import Achievement


def _ach(progress, *, lessons: int = 0, tasks: int = 0, xp: int = 0, streak: int = 0,
         flashcards: int = 0) -> bool:
    return (
        len(progress.completed_lessons) >= lessons
        and len(progress.completed_tasks) >= tasks
        and progress.xp >= xp
        and progress.streak_days >= streak
        and sum(progress.flashcard_correct.values()) >= flashcards
    )


ACHIEVEMENTS: tuple[Achievement, ...] = (
    Achievement(
        id="first-step",
        title="Первый шаг",
        description="Прошёл свой первый урок.",
        icon="👣",
        check=lambda p: _ach(p, lessons=1),
    ),
    Achievement(
        id="first-task",
        title="Кодер",
        description="Решил первую задачу.",
        icon="⌨",
        check=lambda p: _ach(p, tasks=1),
    ),
    Achievement(
        id="five-lessons",
        title="Прогресс есть",
        description="Прошёл 5 уроков.",
        icon="📚",
        check=lambda p: _ach(p, lessons=5),
    ),
    Achievement(
        id="ten-lessons",
        title="На полпути",
        description="Прошёл 10 уроков.",
        icon="🚶",
        check=lambda p: _ach(p, lessons=10),
    ),
    Achievement(
        id="all-lessons",
        title="Знаток",
        description="Прошёл все уроки курса.",
        icon="🎓",
        check=lambda p: _ach(p, lessons=24),
    ),
    Achievement(
        id="five-tasks",
        title="Решатель",
        description="Решил 5 задач.",
        icon="🧩",
        check=lambda p: _ach(p, tasks=5),
    ),
    Achievement(
        id="all-tasks",
        title="Чемпион задач",
        description="Решил все задачи курса.",
        icon="🥇",
        check=lambda p: _ach(p, tasks=11),
    ),
    Achievement(
        id="xp-50",
        title="50 XP",
        description="Накопил 50 XP.",
        icon="⚡",
        check=lambda p: _ach(p, xp=50),
    ),
    Achievement(
        id="xp-200",
        title="200 XP",
        description="Накопил 200 XP.",
        icon="💎",
        check=lambda p: _ach(p, xp=200),
    ),
    Achievement(
        id="streak-3",
        title="3 дня подряд",
        description="Заходил 3 дня подряд.",
        icon="🔥",
        check=lambda p: _ach(p, streak=3),
    ),
    Achievement(
        id="streak-7",
        title="Неделя на огне",
        description="Заходил 7 дней подряд.",
        icon="🔥🔥",
        check=lambda p: _ach(p, streak=7),
    ),
    Achievement(
        id="quiz-10",
        title="Внимательный",
        description="Правильно ответил на 10 карточек.",
        icon="🧠",
        check=lambda p: _ach(p, flashcards=10),
    ),
    Achievement(
        id="bot-ready",
        title="Бот в кармане",
        description="Прошёл раздел про Telegram-бота.",
        icon="🤖",
        check=lambda p: (
            "08-bot-create" in p.completed_lessons
            and "08-bot-echo" in p.completed_lessons
            and "08-bot-commands" in p.completed_lessons
        ),
    ),
)
