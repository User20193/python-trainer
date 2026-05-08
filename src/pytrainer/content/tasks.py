"""Задачи с автопроверкой."""
from __future__ import annotations

from . import Task, TaskTest

# 1. Карточка знакомства
T_PRINT_INTRO = Task(
    id="t-print-intro",
    title="Карточка знакомства",
    description_md="""\
Напиши программу, которая выводит **одной строкой** через ` — ` (тире с пробелами):

```
Кирилл — 19 — Москва
```

Подсказка: у `print` есть параметр `sep`. Например:

```python
print("a", "b", sep="-")
# выведет: a-b
```

Используй `sep=" — "` (пробел, длинное тире, пробел).
""",
    starter_code='# Напиши print(...) с тремя аргументами и параметром sep\n',
    solution_code='print("Кирилл", 19, "Москва", sep=" — ")\n',
    solution_explanation_md="""\
- Передаём в `print` три аргумента — строку, число и строку. Число `print` сам
  превратит в строку.
- Параметр `sep` отвечает за разделитель между аргументами. По умолчанию там пробел,
  мы заменили на `" — "`.
- В `print` каждое значение между запятыми передаётся как отдельный аргумент — это
  ключевое отличие от ручного склеивания через `+`.
""",
    hints=(
        "У print есть параметр sep, который ставится между аргументами.",
        "Передавай три аргумента через запятую и одним именованным аргументом sep=...",
    ),
    tests=(
        TaskTest(
            kind="stdio",
            name="вывод одной строкой через ' — '",
            stdin="",
            expected_stdout="Кирилл — 19 — Москва\n",
        ),
    ),
    xp=8,
)


# 2. Приветствие
T_GREETING = Task(
    id="t-greeting",
    title="Приветствие по имени",
    description_md="""\
Прочитай имя пользователя через `input()` и выведи:

```
Здравствуй, <имя>!
```

Например, если ввели `Кирилл`, программа должна вывести:

```
Здравствуй, Кирилл!
```
""",
    starter_code='name = input("Как тебя зовут? ")\n# напиши тут print(...)\n',
    solution_code='name = input("Как тебя зовут? ")\nprint(f"Здравствуй, {name}!")\n',
    solution_explanation_md="""\
- `input(...)` получает строку с клавиатуры. То, что в скобках — это
  «приглашение», его видит пользователь до ввода. На авто-проверку приглашение
  не влияет.
- `f"..."` — это **f-строка**: внутри `{}` можно писать переменную, и Python
  подставит её значение. Удобнее, чем `+`.
""",
    hints=(
        "Сначала input() в переменную name, потом print(f\"...\").",
        "В f-строке имя переменной пишут в фигурных скобках: f\"Привет, {name}!\".",
    ),
    tests=(
        TaskTest(
            kind="stdio",
            name="имя Кирилл",
            stdin="Кирилл\n",
            expected_stdout="Здравствуй, Кирилл!\n",
        ),
        TaskTest(
            kind="stdio",
            name="имя Аня",
            stdin="Аня\n",
            expected_stdout="Здравствуй, Аня!\n",
        ),
    ),
    xp=10,
)


# 3. Магический шар
T_MAGIC = Task(
    id="t-magic-8",
    title="Магический шар",
    description_md="""\
Напиши функцию `answer(question)`. Она получает **строку-вопрос** и возвращает
ответ:

- если длина вопроса **чётная** — возвращает `"Да"`;
- если длина вопроса **нечётная** — возвращает `"Нет"`.

```python
answer("Я выучу Python?")  # длина 15 — нечётная → "Нет"
answer("Будет ли дождь?")  # длина 14 — чётная → "Да"
```

> Это упрощённая версия. В настоящем «шаре» ответ был бы случайным.
""",
    starter_code='def answer(question):\n    # верни "Да" или "Нет"\n    pass\n',
    solution_code='def answer(question):\n    if len(question) % 2 == 0:\n        return "Да"\n    return "Нет"\n',
    solution_explanation_md="""\
- `len(question)` — количество символов в строке.
- Оператор `%` — остаток от деления. `len % 2 == 0` означает «чётное».
- В функции с `return` после `if` `else` можно не писать — если ушли в `return`,
  выполнение прервётся.
""",
    hints=(
        "len() даёт длину строки.",
        "Чётность проверяй через `% 2 == 0`.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="чётная длина → Да",
            function="answer",
            args=("Будет ли дождь?",),
            expected="Да",
        ),
        TaskTest(
            kind="functional",
            name="нечётная длина → Нет",
            function="answer",
            args=("Я выучу Python?",),
            expected="Нет",
        ),
        TaskTest(
            kind="functional",
            name="пустая строка → Да",
            function="answer",
            args=("",),
            expected="Да",
        ),
    ),
    xp=12,
)


# 4. Чёт/нечёт
T_EVEN_ODD = Task(
    id="t-even-odd",
    title="Чёт или нечёт",
    description_md="""\
Прочитай **целое число** через `input()` и выведи:

- `чётное` — если число делится на 2 без остатка;
- `нечётное` — иначе.

Примеры:

```
вход:  4
выход: чётное

вход:  7
выход: нечётное
```
""",
    starter_code='n = int(input("Введи число: "))\n# выведи "чётное" или "нечётное"\n',
    solution_code='n = int(input("Введи число: "))\nif n % 2 == 0:\n    print("чётное")\nelse:\n    print("нечётное")\n',
    solution_explanation_md="""\
- `int(input(...))` — сначала читаем строку, потом превращаем в число.
- Чётность — `% 2 == 0`. Если делится на 2 без остатка — чётное.
- Тут как раз нужен `else`: вариантов ровно два, не три.
""",
    hints=(
        "int(input(...)) сразу даст число.",
        "Проверка чётности — оператор `%`.",
    ),
    tests=(
        TaskTest(kind="stdio", name="4", stdin="4\n", expected_stdout="чётное\n"),
        TaskTest(kind="stdio", name="7", stdin="7\n", expected_stdout="нечётное\n"),
        TaskTest(kind="stdio", name="0", stdin="0\n", expected_stdout="чётное\n"),
        TaskTest(kind="stdio", name="-3", stdin="-3\n", expected_stdout="нечётное\n"),
    ),
    xp=10,
)


# 5. Оценка
T_GRADE = Task(
    id="t-grade",
    title="Оценка по баллу",
    description_md="""\
Прочитай балл (целое число от 0 до 100) и выведи оценку по таблице:

| Балл | Текст |
|---|---|
| 90 и выше | `Отлично` |
| 70-89 | `Хорошо` |
| 50-69 | `Удовлетворительно` |
| меньше 50 | `Не сдал` |

Используй `if / elif / else`.
""",
    starter_code='score = int(input("Балл: "))\n# напиши цепочку if/elif/else\n',
    solution_code='''score = int(input("Балл: "))
if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
elif score >= 50:
    print("Удовлетворительно")
else:
    print("Не сдал")
''',
    solution_explanation_md="""\
- Цепочка `if / elif / else` проверяет условия по порядку. Первое подходящее —
  выполняется, остальные пропускаются.
- Важно идти **сверху вниз** от большего к меньшему. Если бы мы начали с `if score
  >= 50`, то и 95 бы попал в «удовлетворительно».
""",
    hints=(
        "Начинай с самой высокой границы (>=90), иди вниз.",
        "Каждое следующее `elif` уже не нужно проверять верхнюю границу — Python сам пропустил предыдущие.",
    ),
    tests=(
        TaskTest(kind="stdio", name="95", stdin="95\n", expected_stdout="Отлично\n"),
        TaskTest(kind="stdio", name="73", stdin="73\n", expected_stdout="Хорошо\n"),
        TaskTest(
            kind="stdio", name="55", stdin="55\n", expected_stdout="Удовлетворительно\n"
        ),
        TaskTest(kind="stdio", name="40", stdin="40\n", expected_stdout="Не сдал\n"),
        TaskTest(kind="stdio", name="90", stdin="90\n", expected_stdout="Отлично\n"),
    ),
    xp=12,
)


# 6. Сильный пароль
T_PASSWORD = Task(
    id="t-password",
    title="Проверка пароля",
    description_md="""\
Напиши функцию `is_strong(password)`. Она возвращает `True`, если пароль:

- содержит **не меньше 8 символов**, **и**
- содержит хотя бы одну **цифру**, **и**
- содержит хотя бы одну **заглавную букву** (любую — английскую или русскую).

Иначе — `False`.

Подсказка: в строке можно проверить условие так:

```python
any(c.isdigit() for c in s)        # есть ли хотя бы одна цифра
any(c.isupper() for c in s)        # есть ли хотя бы одна заглавная
```
""",
    starter_code='def is_strong(password):\n    # верни True/False\n    pass\n',
    solution_code='''def is_strong(password):
    if len(password) < 8:
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c.isupper() for c in password):
        return False
    return True
''',
    solution_explanation_md="""\
- Каждое требование проверяем отдельным `if`. Если хоть одно не выполнено — `return
  False`. Дошли до конца — `return True`.
- Можно было одной строкой через `and`, но последовательные `if`-ранние-возвраты
  читаются яснее: видно, **какое именно** условие провалилось.
- `any(c.isdigit() for c in password)` — это «есть хотя бы один символ, у которого
  `isdigit()` возвращает True». Это **генератор**: проверяет лениво и сразу
  останавливается, как только нашлось.
""",
    hints=(
        "len(password) даст длину.",
        "any(c.isdigit() for c in password) — есть ли цифра.",
        "any(c.isupper() for c in password) — есть ли заглавная.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="хороший пароль",
            function="is_strong",
            args=("Hello123",),
            expected=True,
        ),
        TaskTest(
            kind="functional",
            name="короткий",
            function="is_strong",
            args=("Hi1",),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="без цифры",
            function="is_strong",
            args=("HelloWorld",),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="без заглавной",
            function="is_strong",
            args=("hello123",),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="пустой",
            function="is_strong",
            args=("",),
            expected=False,
        ),
    ),
    xp=15,
)


# 7. Список покупок
T_SHOPPING = Task(
    id="t-shopping-list",
    title="Список покупок",
    description_md="""\
Напиши функцию `add_item(items, item)`. Она получает:

- `items` — текущий список покупок (список строк),
- `item` — название продукта (строка).

Должна вернуть **новый отсортированный** список, в который добавлен `item`.
**Если такой продукт уже есть в списке, его добавлять не нужно.**

Не меняй переданный список — собери и верни новый.

```python
add_item(["хлеб"], "молоко")
# → ["молоко", "хлеб"]

add_item(["молоко", "хлеб"], "хлеб")
# → ["молоко", "хлеб"]
```
""",
    starter_code='def add_item(items, item):\n    # верни новый отсортированный список\n    pass\n',
    solution_code='''def add_item(items, item):
    if item in items:
        return sorted(items)
    return sorted(items + [item])
''',
    solution_explanation_md="""\
- `item in items` — есть ли уже такой элемент в списке. Если есть — просто
  возвращаем отсортированный список как есть.
- `items + [item]` — это **новый** список (старый не изменён).
- `sorted(...)` — возвращает новый отсортированный список. Не путай с методом
  `.sort()` — тот меняет на месте и ничего не возвращает.
""",
    hints=(
        "Проверь, есть ли item в items, через `in`.",
        "Чтобы вернуть новый список — используй `sorted(...)` (а не метод .sort()).",
        "Сложение списков: `[1, 2] + [3]` → `[1, 2, 3]`.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="новый продукт",
            function="add_item",
            args=(["хлеб"], "молоко"),
            expected=["молоко", "хлеб"],
        ),
        TaskTest(
            kind="functional",
            name="уже есть",
            function="add_item",
            args=(["молоко", "хлеб"], "хлеб"),
            expected=["молоко", "хлеб"],
        ),
        TaskTest(
            kind="functional",
            name="из пустого",
            function="add_item",
            args=([], "яблоко"),
            expected=["яблоко"],
        ),
        TaskTest(
            kind="functional",
            name="порядок",
            function="add_item",
            args=(["банан", "яблоко"], "арбуз"),
            expected=["арбуз", "банан", "яблоко"],
        ),
    ),
    xp=15,
)


# 8. Угадай число — счётчик попыток
T_GUESS = Task(
    id="t-guess-number",
    title="Угадайка: счётчик попыток",
    description_md="""\
Напиши функцию `attempts(secret, guesses)`. Она получает:

- `secret` — загаданное число,
- `guesses` — список попыток в порядке ввода.

Должна вернуть **номер первой удачной попытки** (считая с 1).
Если ни одна не угадала — вернуть `-1`.

```python
attempts(7, [3, 5, 7, 8])  # → 3
attempts(7, [1, 2, 3])     # → -1
```
""",
    starter_code='def attempts(secret, guesses):\n    # верни номер удачной попытки или -1\n    pass\n',
    solution_code='''def attempts(secret, guesses):
    for i, g in enumerate(guesses, start=1):
        if g == secret:
            return i
    return -1
''',
    solution_explanation_md="""\
- `enumerate(..., start=1)` даёт пары `(номер, элемент)`, где номера начинаются с 1.
- Как только нашли совпадение — `return i` сразу, дальше идти не надо.
- Если цикл прошёл целиком и ничего не вернули — возвращаем `-1`.
""",
    hints=(
        "Используй enumerate, чтобы знать номер попытки.",
        "Если нашли — выходи из функции через return.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="третья",
            function="attempts",
            args=(7, [3, 5, 7, 8]),
            expected=3,
        ),
        TaskTest(
            kind="functional",
            name="первая",
            function="attempts",
            args=(1, [1, 2, 3]),
            expected=1,
        ),
        TaskTest(
            kind="functional",
            name="не угадал",
            function="attempts",
            args=(10, [1, 2, 3]),
            expected=-1,
        ),
        TaskTest(
            kind="functional",
            name="пустой список",
            function="attempts",
            args=(5, []),
            expected=-1,
        ),
    ),
    xp=12,
)


# 9. Таблица умножения
T_MULTI = Task(
    id="t-multi-table",
    title="Таблица умножения N×N",
    description_md="""\
Напиши функцию `make_table(n)`. Она возвращает **строку** с таблицей умножения
N на N. Числа в строке разделены табуляцией (`\\t`), строки разделены `\\n`.

В **последнем элементе НЕ должно быть** ни табуляции, ни перевода строки в конце.

Для `n = 3`:

```
1\\t2\\t3
2\\t4\\t6
3\\t6\\t9
```
""",
    starter_code='def make_table(n):\n    # верни строку с таблицей\n    pass\n',
    solution_code='''def make_table(n):
    rows = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            row.append(str(i * j))
        rows.append("\\t".join(row))
    return "\\n".join(rows)
''',
    solution_explanation_md="""\
- Внешний цикл `for i` — строки.
- Внутренний `for j` — столбцы.
- Каждое число превращаем в строку (`str(...)`) и добавляем в список `row`.
- `"\\t".join(row)` склеивает элементы списка через табуляцию (без лишней в конце).
- `"\\n".join(rows)` склеивает строки через перевод (без лишнего перевода в конце).
- Это идиома — **сначала собираем в список, в конце склеиваем через `join`**.
  Так не появляются лишние разделители.
""",
    hints=(
        "Два вложенных цикла: внешний строки, внутренний столбцы.",
        "Используй list + join, чтобы не было лишних разделителей.",
        "Преобразуй числа в строки через str(...) перед join.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="3x3",
            function="make_table",
            args=(3,),
            expected="1\t2\t3\n2\t4\t6\n3\t6\t9",
        ),
        TaskTest(
            kind="functional",
            name="1x1",
            function="make_table",
            args=(1,),
            expected="1",
        ),
        TaskTest(
            kind="functional",
            name="2x2",
            function="make_table",
            args=(2,),
            expected="1\t2\n2\t4",
        ),
    ),
    xp=15,
)


# 10. Площадь — функции
T_AREA = Task(
    id="t-area",
    title="Площади фигур",
    description_md="""\
Напиши **две функции**:

- `rect_area(a, b)` — площадь прямоугольника со сторонами `a` и `b`.
- `circle_area(r)` — площадь круга с радиусом `r`. Используй `math.pi`.

```python
rect_area(3, 4)   # 12
circle_area(1)    # 3.141592653589793
```

Не забудь `import math` сверху.
""",
    starter_code='import math\n\ndef rect_area(a, b):\n    pass\n\ndef circle_area(r):\n    pass\n',
    solution_code='import math\n\ndef rect_area(a, b):\n    return a * b\n\ndef circle_area(r):\n    return math.pi * r * r\n',
    solution_explanation_md="""\
- `rect_area` — просто `a * b`. Тут важно использовать `return`, **а не** `print`.
- `circle_area` — формула `π · r²`. `math.pi` — встроенная константа из модуля
  `math`.
- В Python `r ** 2` тоже работает как «r в квадрате» — это эквивалентная запись.
""",
    hints=(
        "Прямоугольник — это просто умножение сторон.",
        "Круг — math.pi * r * r или math.pi * r ** 2.",
        "Не забудь return, а не print.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="прямоугольник 3x4",
            function="rect_area",
            args=(3, 4),
            expected=12,
        ),
        TaskTest(
            kind="functional",
            name="круг радиуса 1",
            function="circle_area",
            args=(1,),
            expected=3.141592653589793,
        ),
        TaskTest(
            kind="functional",
            name="круг радиуса 2",
            function="circle_area",
            args=(2,),
            expected=12.566370614359172,
        ),
    ),
    xp=15,
)


# 11. Эхо-бот — концептуальная задача (показать решение)
T_BOT_ECHO = Task(
    id="t-bot-echo",
    title="Эхо-бот: вспомним шаблон",
    description_md="""\
В этой задаче проверим, что ты можешь воспроизвести минимальный «скелет» эхо-бота
на aiogram **без подсказок**.

Напиши функцию `bot_template(token)`, которая возвращает **строку** с готовым
шаблоном:

```text
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot("<TOKEN>")
dp = Dispatcher()

@dp.message()
async def echo(message: Message) -> None:
    if message.text:
        await message.answer(message.text)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

Только вместо `<TOKEN>` — подставь полученное значение `token`.

Тестов на работу бота нет (у нас нет интернета в песочнице) — просто собери строку.
""",
    starter_code='def bot_template(token):\n    # верни строку с шаблоном эхо-бота\n    pass\n',
    solution_code='''def bot_template(token):
    return (
        "import asyncio\\n"
        "from aiogram import Bot, Dispatcher\\n"
        "from aiogram.types import Message\\n"
        "\\n"
        f"bot = Bot(\\"{token}\\")\\n"
        "dp = Dispatcher()\\n"
        "\\n"
        "@dp.message()\\n"
        "async def echo(message: Message) -> None:\\n"
        "    if message.text:\\n"
        "        await message.answer(message.text)\\n"
        "\\n"
        "async def main() -> None:\\n"
        "    await dp.start_polling(bot)\\n"
        "\\n"
        "if __name__ == \\"__main__\\":\\n"
        "    asyncio.run(main())\\n"
    )
''',
    solution_explanation_md="""\
- Этот «шаблон» — **то самое**, что ты будешь копировать в новый файл `bot.py`,
  когда станешь делать своего реального бота.
- Здесь мы собираем его **строкой** в Python — это аналог того, как фреймворки
  иногда генерируют код для тебя.
- В `f`-строке `{token}` подставляется значение параметра.
- `\\\\n` внутри строки — это символ переноса строки. Когда ты сохранишь результат
  в файл — там будут реальные переносы.
""",
    hints=(
        "Используй несколько строк через '\\n' и склей их.",
        "Один кусок должен быть f-строкой — там подставляется token.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="токен есть в результате",
            function="bot_template",
            args=("MY_TOKEN_123",),
            expected=(
                "import asyncio\n"
                "from aiogram import Bot, Dispatcher\n"
                "from aiogram.types import Message\n"
                "\n"
                'bot = Bot("MY_TOKEN_123")\n'
                "dp = Dispatcher()\n"
                "\n"
                "@dp.message()\n"
                "async def echo(message: Message) -> None:\n"
                "    if message.text:\n"
                "        await message.answer(message.text)\n"
                "\n"
                "async def main() -> None:\n"
                "    await dp.start_polling(bot)\n"
                "\n"
                'if __name__ == "__main__":\n'
                "    asyncio.run(main())\n"
            ),
        ),
    ),
    xp=20,
)


TASKS: tuple[Task, ...] = (
    T_PRINT_INTRO,
    T_GREETING,
    T_MAGIC,
    T_EVEN_ODD,
    T_GRADE,
    T_PASSWORD,
    T_SHOPPING,
    T_GUESS,
    T_MULTI,
    T_AREA,
    T_BOT_ECHO,
)
