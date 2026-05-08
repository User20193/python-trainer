"""Словарь терминов."""
from __future__ import annotations

from . import GlossaryEntry

GLOSSARY: tuple[GlossaryEntry, ...] = (
    GlossaryEntry(
        term="print",
        definition_md=(
            "Встроенная функция, которая выводит значения на экран.\n\n"
            "```python\nprint(\"Привет\", \"мир\", sep=\"-\")\n```\n\n"
            "Параметры: `sep` (разделитель между аргументами), `end` (что в конце; "
            "по умолчанию перевод строки)."
        ),
    ),
    GlossaryEntry(
        term="input",
        definition_md=(
            "Встроенная функция: ждёт, пока пользователь введёт строку с клавиатуры, "
            "и возвращает её. Всегда возвращает **строку**.\n\n"
            "```python\nname = input(\"Имя: \")\nage = int(input(\"Возраст: \"))\n```\n"
        ),
    ),
    GlossaryEntry(
        term="Переменная",
        definition_md=(
            "Имя для значения. Создаётся через `=`. Чем понятнее имя — тем "
            "лучше для тебя через месяц.\n\n"
            "```python\nuser_name = \"Кирилл\"\n```"
        ),
    ),
    GlossaryEntry(
        term="int",
        definition_md=(
            "Целое число. Может быть положительным, отрицательным, нулём.\n\n"
            "```python\nn = 42\nn = int(\"42\")  # из строки\n```"
        ),
    ),
    GlossaryEntry(
        term="float",
        definition_md=(
            "Дробное число (с десятичной точкой).\n\n"
            "```python\npi = 3.14\n```"
        ),
    ),
    GlossaryEntry(
        term="str",
        definition_md=(
            "Строка — текст в кавычках. Можно складывать, умножать на число, "
            "брать срезы.\n\n"
            "```python\nname = \"Аня\"\nfull = \"Привет, \" + name\n```"
        ),
    ),
    GlossaryEntry(
        term="bool",
        definition_md=(
            "Булево значение: `True` или `False`. Получается из условий "
            "(`age >= 18`) и логических операций (`and`, `or`, `not`)."
        ),
    ),
    GlossaryEntry(
        term="None",
        definition_md=(
            "Специальное значение «ничего». Возвращается функциями без `return`. "
            "Не равно ни `0`, ни пустой строке. Сравнивается через `is`: `if x is None`."
        ),
    ),
    GlossaryEntry(
        term="f-строка",
        definition_md=(
            "Строка с подстановкой переменных. Обозначается префиксом `f`:\n\n"
            "```python\nname = \"Аня\"\nprint(f\"Привет, {name}!\")\n```"
        ),
    ),
    GlossaryEntry(
        term="if / else / elif",
        definition_md=(
            "Условный оператор. `if` — если истинно, `elif` — иначе если, "
            "`else` — иначе.\n\n"
            "```python\nif x > 0:\n    print(\"плюс\")\nelif x == 0:\n    "
            "print(\"ноль\")\nelse:\n    print(\"минус\")\n```"
        ),
    ),
    GlossaryEntry(
        term="and / or / not",
        definition_md=(
            "Логические операторы. `and` — оба истинны, `or` — хотя бы один, "
            "`not` — переворачивает True/False."
        ),
    ),
    GlossaryEntry(
        term="list",
        definition_md=(
            "Список — упорядоченный набор значений в квадратных скобках.\n\n"
            "```python\nfruits = [\"яблоко\", \"груша\"]\nfruits.append(\"банан\")\n"
            "print(fruits[0])  # яблоко\n```"
        ),
    ),
    GlossaryEntry(
        term="dict",
        definition_md=(
            "Словарь — пары ключ-значение в фигурных скобках.\n\n"
            "```python\nuser = {\"name\": \"Аня\", \"age\": 20}\nprint(user[\"name\"])\n```"
        ),
    ),
    GlossaryEntry(
        term="tuple",
        definition_md=(
            "Кортеж — как список, но **неизменяемый**. Запись в круглых скобках.\n\n"
            "```python\npoint = (3, 5)\nx, y = point  # распаковка\n```"
        ),
    ),
    GlossaryEntry(
        term="set",
        definition_md=(
            "Множество — набор **уникальных** элементов без порядка.\n\n"
            "```python\ntags = {\"python\", \"linux\"}\ntags.add(\"git\")\n```"
        ),
    ),
    GlossaryEntry(
        term="for",
        definition_md=(
            "Цикл по элементам. «Для каждого X в Y делай Z».\n\n"
            "```python\nfor i in range(5):\n    print(i)\n```"
        ),
    ),
    GlossaryEntry(
        term="while",
        definition_md=(
            "Цикл «пока условие истинно». Используй, когда не знаешь заранее, "
            "сколько итераций будет.\n\n"
            "```python\nn = 5\nwhile n > 0:\n    print(n)\n    n -= 1\n```"
        ),
    ),
    GlossaryEntry(
        term="break",
        definition_md=(
            "Досрочно выйти из цикла."
        ),
    ),
    GlossaryEntry(
        term="continue",
        definition_md=(
            "Пропустить остаток текущей итерации и перейти к следующей."
        ),
    ),
    GlossaryEntry(
        term="range",
        definition_md=(
            "Встроенная функция, которая возвращает последовательность чисел.\n\n"
            "```python\nrange(5)        # 0,1,2,3,4\nrange(2, 7)     # 2,3,4,5,6\n"
            "range(0, 10, 2) # 0,2,4,6,8\n```"
        ),
    ),
    GlossaryEntry(
        term="def",
        definition_md=(
            "Ключевое слово для определения функции.\n\n"
            "```python\ndef double(n):\n    return n * 2\n```"
        ),
    ),
    GlossaryEntry(
        term="return",
        definition_md=(
            "Возвращает значение из функции. Не путай с `print`: `print` выводит на "
            "экран, `return` отдаёт значение коду, который вызвал функцию."
        ),
    ),
    GlossaryEntry(
        term="*args",
        definition_md=(
            "Параметр функции, в который собираются **все позиционные** аргументы "
            "в виде кортежа.\n\n"
            "```python\ndef sum_all(*nums):\n    return sum(nums)\n\nsum_all(1, 2, 3)\n```"
        ),
    ),
    GlossaryEntry(
        term="**kwargs",
        definition_md=(
            "Параметр функции, в который собираются **все именованные** аргументы "
            "в виде словаря.\n\n"
            "```python\ndef show(**fields):\n    for k, v in fields.items():\n        print(k, v)\n"
            "show(name=\"Аня\", age=20)\n```"
        ),
    ),
    GlossaryEntry(
        term="lambda",
        definition_md=(
            "Короткая безымянная функция в одну строку.\n\n"
            "```python\nsquare = lambda x: x * x\n```"
        ),
    ),
    GlossaryEntry(
        term="import",
        definition_md=(
            "Подключает модуль (другой файл с кодом).\n\n"
            "```python\nimport math\nfrom random import choice\n```"
        ),
    ),
    GlossaryEntry(
        term="модуль",
        definition_md=(
            "Файл с Python-кодом, который можно импортировать в другой файл. "
            "Стандартная библиотека (math, random, json, datetime, os, pathlib) идёт "
            "вместе с Python."
        ),
    ),
    GlossaryEntry(
        term="JSON",
        definition_md=(
            "Текстовый формат для обмена данными. Очень похож на Python-словари и "
            "списки. Для перевода — модуль `json`:\n\n"
            "```python\nimport json\ntext = json.dumps({\"a\": 1})\n"
            "data = json.loads(text)\n```"
        ),
    ),
    GlossaryEntry(
        term="open",
        definition_md=(
            "Встроенная функция для открытия файла. Используй с `with`:\n\n"
            "```python\nwith open(\"a.txt\", \"r\", encoding=\"utf-8\") as f:\n    "
            "text = f.read()\n```"
        ),
    ),
    GlossaryEntry(
        term="with",
        definition_md=(
            "Контекстный менеджер. Гарантирует, что ресурс (например, файл) будет "
            "корректно закрыт после выхода из блока."
        ),
    ),
    GlossaryEntry(
        term="pip",
        definition_md=(
            "Менеджер пакетов Python. Командой `pip install имя` ставит библиотеку "
            "из репозитория [PyPI](https://pypi.org). Список зависимостей хранят в "
            "`requirements.txt`."
        ),
    ),
    GlossaryEntry(
        term="venv",
        definition_md=(
            "Виртуальное окружение — изолированная папка с локальными пакетами для "
            "конкретного проекта. Создаётся командой `python -m venv .venv`. "
            "Активируется `source .venv/bin/activate` (Linux/Mac) или "
            "`.venv\\Scripts\\activate` (Windows)."
        ),
    ),
    GlossaryEntry(
        term="API",
        definition_md=(
            "Application Programming Interface — способ программам общаться. В вебе "
            "обычно по HTTP. Запросы делают через библиотеку `requests`, ответы "
            "приходят в JSON."
        ),
    ),
    GlossaryEntry(
        term="async / await",
        definition_md=(
            "Способ писать код, который **может ждать** (например, ответ от сервера) "
            "и при этом не блокировать программу.\n\n"
            "```python\nasync def fetch():\n    data = await client.get(...)\n    return data\n```\n"
            "Используется в `aiogram`, `asyncio`, `aiohttp`."
        ),
    ),
    GlossaryEntry(
        term="aiogram",
        definition_md=(
            "Популярная Python-библиотека для Telegram-ботов. Под капотом — `asyncio`. "
            "Ставится через `pip install aiogram`."
        ),
    ),
    GlossaryEntry(
        term="BotFather",
        definition_md=(
            "Специальный бот в Telegram (`@BotFather`), через которого создаются "
            "новые боты. После `/newbot` он выдаст **токен** — пароль твоего бота. "
            "Береги его, не клади в репозиторий."
        ),
    ),
    GlossaryEntry(
        term="токен",
        definition_md=(
            "Длинная случайная строка-пароль для доступа к API. Для Telegram-бота — "
            "выдаёт `@BotFather`. Хранится в переменной окружения, не в коде."
        ),
    ),
    GlossaryEntry(
        term="traceback",
        definition_md=(
            "След ошибки — то, что Python печатает, когда что-то пошло не так. Читай "
            "**снизу вверх**: внизу — что именно сломалось, выше — где это случилось."
        ),
    ),
    GlossaryEntry(
        term="отступ (indent)",
        definition_md=(
            "Пробелы или табы в начале строки. В Python они **обязательны** — "
            "обозначают вложенность блоков. Стандарт — 4 пробела."
        ),
    ),
    GlossaryEntry(
        term="REPL",
        definition_md=(
            "Read-Eval-Print Loop — режим, в котором Python читает по одной команде, "
            "выполняет, печатает результат. Это наша «Песочница» в приложении."
        ),
    ),
)
