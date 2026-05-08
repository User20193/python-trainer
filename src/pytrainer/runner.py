"""Запуск пользовательского кода в отдельном процессе с таймаутом.

Используется тот же исполняемый файл (включая собранный PyInstaller `.exe`)
в режиме worker — чтобы не зависеть от наличия отдельного интерпретатора Python
на машине пользователя.
"""
from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass


@dataclass
class RunResult:
    stdout: str
    stderr: str
    return_code: int
    timed_out: bool


def _python_command() -> list[str]:
    """Команда для запуска worker.

    Если запущены под PyInstaller — используем тот же exe c флагом ``--pytrainer-worker``.
    Иначе — текущий интерпретатор Python с пакетом ``pytrainer``.
    """
    if getattr(sys, "frozen", False):
        return [sys.executable, "--pytrainer-worker"]
    return [sys.executable, "-m", "pytrainer", "--pytrainer-worker"]


def run_user_code(code: str, stdin: str = "", timeout: float = 5.0) -> RunResult:
    """Запустить произвольный пользовательский код.

    Записываем код во временный файл, запускаем worker (он его выполнит),
    возвращаем stdout/stderr. На вход — stdin как строку.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        path = f.name

    try:
        cmd = _python_command() + [path]
        try:
            proc = subprocess.run(
                cmd,
                input=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout if isinstance(e.stdout, str) else (
                e.stdout.decode("utf-8", "replace") if e.stdout else ""
            )
            stderr = e.stderr if isinstance(e.stderr, str) else (
                e.stderr.decode("utf-8", "replace") if e.stderr else ""
            )
            return RunResult(
                stdout=stdout,
                stderr=stderr + f"\n[Превышен таймаут {timeout:.0f}с — код вышел из времени]",
                return_code=-1,
                timed_out=True,
            )
        return RunResult(
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
            return_code=proc.returncode,
            timed_out=False,
        )
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def run_functional_check(
    user_code: str,
    function_name: str,
    cases: list[tuple[tuple, dict, object]],
    timeout: float = 5.0,
) -> tuple[bool, str]:
    """Проверить функциональным тестом.

    Импортируется ``function_name`` из user_code и вызывается с каждым набором
    аргументов из ``cases`` (``(args, kwargs, expected)``). Возвращает ``(ok, message)``.
    """
    wrapper = textwrap.dedent(
        f"""
        import json, sys, traceback
        _ns = {{}}
        try:
            exec(compile({user_code!r}, '<решение>', 'exec'), _ns)
        except Exception:
            traceback.print_exc()
            sys.exit(2)

        if {function_name!r} not in _ns:
            print('Не найдена функция {function_name}', file=sys.stderr)
            sys.exit(3)
        _f = _ns[{function_name!r}]

        cases = json.loads(sys.stdin.read())
        for args, kwargs, expected in cases:
            try:
                got = _f(*args, **kwargs)
            except Exception as exc:
                print('FAIL: вызов ' + repr({function_name!r}) + '(*' + repr(args) +
                      ', **' + repr(kwargs) + ') кинул исключение: ' +
                      type(exc).__name__ + ': ' + str(exc))
                sys.exit(4)
            if got != expected:
                print('FAIL: ' + {function_name!r} + '(*' + repr(args) +
                      ', **' + repr(kwargs) + ') вернула ' + repr(got) +
                      ', ожидалось ' + repr(expected))
                sys.exit(5)
        print('OK')
        """
    )
    payload = json.dumps([[list(a), k, e] for a, k, e in cases])
    res = run_user_code(wrapper, stdin=payload, timeout=timeout)
    if res.timed_out:
        return False, "Превышен таймаут — возможно, бесконечный цикл."
    if res.return_code == 0 and "OK" in res.stdout:
        return True, "OK"
    msg = (res.stdout or "").strip()
    if res.stderr.strip():
        msg = (msg + "\n" + res.stderr.strip()).strip()
    if not msg:
        msg = "Тест не пройден."
    return False, msg


def run_worker(args: list[str]) -> int:
    """Worker: выполнить указанный py-файл, имитируя обычный запуск ``python file.py``."""
    if not args:
        sys.stderr.write("worker: ожидается путь до py-файла\n")
        return 64
    path = args[0]
    sys.argv = [path] + list(args[1:])
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 0
    except Exception:
        import traceback

        traceback.print_exc()
        return 1
    return 0


def normalize_text(s: str) -> str:
    """Нормализовать вывод: убрать концы строк, пробелы по краям, привести к единому стилю."""
    return "\n".join(line.rstrip() for line in s.replace("\r\n", "\n").splitlines()).strip()
