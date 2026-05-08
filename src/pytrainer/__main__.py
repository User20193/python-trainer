"""Точка входа.

Особенность: тот же исполняемый файл (включая собранный PyInstaller `.exe`)
умеет работать как worker — для безопасного запуска пользовательского кода
из задач в отдельном процессе. См. ``runner.py``.
"""
from __future__ import annotations

import sys


def _is_worker_invocation(argv: list[str]) -> bool:
    return len(argv) >= 2 and argv[1] == "--pytrainer-worker"


def main() -> int:
    argv = sys.argv

    if _is_worker_invocation(argv):
        from pytrainer.runner import run_worker

        return run_worker(argv[2:])

    # multiprocessing-style freeze support — на всякий случай
    try:
        from multiprocessing import freeze_support

        freeze_support()
    except Exception:  # noqa: BLE001
        pass

    from pytrainer.app import run_app

    return run_app(argv)


if __name__ == "__main__":
    raise SystemExit(main())
