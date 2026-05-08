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



# 12. Карточка профиля — print с sep
T_PRINT_CARD = Task(
    id="t-print-card",
    title="Карточка профиля",
    description_md="""\
Выведи **одной строкой** информацию о пользователе через ` | ` (пробел, вертикальная
черта, пробел):

```
Кирилл | 19 | Москва | Python
```

Используй один `print(...)` с параметром `sep`.
""",
    starter_code='# один print с четырьмя аргументами и sep=" | "\n',
    solution_code='print("Кирилл", 19, "Москва", "Python", sep=" | ")\n',
    solution_explanation_md="""\
- `sep=" | "` — между каждой парой аргументов будет ` | `.
- Числа в кавычки оборачивать не нужно — `print` сам их отформатирует.
""",
    hints=(
        "Используй sep=' | ' (пробел, |, пробел).",
        "Передай 4 аргумента подряд через запятую.",
    ),
    tests=(
        TaskTest(
            kind="stdio",
            name="вывод карточки",
            stdin="",
            expected_stdout="Кирилл | 19 | Москва | Python\n",
        ),
    ),
    xp=8,
)


# 13. ASCII-разделитель
T_PRINT_ASCII = Task(
    id="t-print-ascii",
    title="ASCII-разделитель",
    description_md="""\
Выведи строку из **40** знаков `=`. Без пробелов, в одну строку.

Подсказка: строку можно умножать на число.

```python
print("ab" * 3)  # ababab
```
""",
    starter_code='# один print со строкой "=" * 40\n',
    solution_code='print("=" * 40)\n',
    solution_explanation_md="""\
- В Python строку можно «умножить» на число — это повторение.
- `"=" * 40` создаст строку из 40 символов `=`.
- `print` выведет результат.
""",
    hints=(
        "Строку можно умножить на число: \"-\" * 5 → \"-----\".",
        "Один print, без циклов.",
    ),
    tests=(
        TaskTest(
            kind="stdio",
            name="40 знаков равно",
            stdin="",
            expected_stdout="========================================\n",
        ),
    ),
    xp=6,
)


# 14. Сумма двух чисел из ввода
T_SUM_INPUTS = Task(
    id="t-sum-inputs",
    title="Сумма двух чисел",
    description_md="""\
Прочитай **два целых числа** через `input()` (каждое — отдельной строкой) и выведи
их сумму.

Пример:

```
вход:
3
5

выход:
8
```
""",
    starter_code='a = int(input())\nb = int(input())\n# выведи a + b\n',
    solution_code='a = int(input())\nb = int(input())\nprint(a + b)\n',
    solution_explanation_md="""\
- `int(input())` читает строку и сразу превращает в число.
- Сумму выводим обычным `print(a + b)`.
- Без `int()` строки бы склеивались, не складывались: `"3" + "5"` дало бы `"35"`.
""",
    hints=(
        "Каждый input в отдельной строке, обёрнут в int(...).",
        "Сложить и просто print.",
    ),
    tests=(
        TaskTest(kind="stdio", name="3+5", stdin="3\n5\n", expected_stdout="8\n"),
        TaskTest(kind="stdio", name="0+0", stdin="0\n0\n", expected_stdout="0\n"),
        TaskTest(
            kind="stdio", name="-7+10", stdin="-7\n10\n", expected_stdout="3\n"
        ),
    ),
    xp=8,
)


# 15. Целое и дробное деление
T_DIVMOD = Task(
    id="t-divmod",
    title="Деление: частное и остаток",
    description_md="""\
Прочитай два положительных целых числа: `a` и `b` (через `input()`, каждое в своей
строке). Выведи **частное** и **остаток** от деления `a` на `b`, каждый —
отдельной строкой.

Пример:

```
вход:
17
5

выход:
3
2
```
""",
    starter_code='a = int(input())\nb = int(input())\n# выведи a // b и a % b\n',
    solution_code='a = int(input())\nb = int(input())\nprint(a // b)\nprint(a % b)\n',
    solution_explanation_md="""\
- `//` — целочисленное деление (без остатка).
- `%` — остаток от деления.
- Эти два оператора идут рядом, потому что вместе дают полную картину деления.
""",
    hints=(
        "// — целочисленное деление, % — остаток.",
        "Два print подряд: сначала частное, потом остаток.",
    ),
    tests=(
        TaskTest(
            kind="stdio", name="17 / 5", stdin="17\n5\n", expected_stdout="3\n2\n"
        ),
        TaskTest(
            kind="stdio", name="100 / 7", stdin="100\n7\n", expected_stdout="14\n2\n"
        ),
        TaskTest(
            kind="stdio", name="9 / 3", stdin="9\n3\n", expected_stdout="3\n0\n"
        ),
    ),
    xp=10,
)


# 16. Существует ли треугольник
T_TRI = Task(
    id="t-triangle",
    title="Существует ли треугольник?",
    description_md="""\
Напиши функцию `is_triangle(a, b, c)`, которая возвращает `True`, если из отрезков
с длинами `a`, `b`, `c` можно сложить треугольник, и `False` — иначе.

**Условие**: треугольник существует, если **сумма любых двух сторон строго больше
третьей**. Стороны должны быть положительными.

```python
is_triangle(3, 4, 5)   # True
is_triangle(1, 1, 5)   # False — 1 + 1 < 5
is_triangle(0, 4, 5)   # False — нулевая сторона
```
""",
    starter_code='def is_triangle(a, b, c):\n    pass\n',
    solution_code=(
        'def is_triangle(a, b, c):\n'
        '    if a <= 0 or b <= 0 or c <= 0:\n'
        '        return False\n'
        '    return a + b > c and a + c > b and b + c > a\n'
    ),
    solution_explanation_md="""\
- Сначала отсекаем некорректные данные: нулевые или отрицательные стороны.
- Дальше — три неравенства треугольника, объединённые `and`.
- Возвращаем результат сравнений напрямую — это уже `True` или `False`.
""",
    hints=(
        "Сначала проверь, что все стороны > 0.",
        "Условие треугольника: сумма любых двух больше третьей.",
        "Можешь вернуть результат `and` напрямую — это уже True/False.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="3-4-5",
            function="is_triangle",
            args=(3, 4, 5),
            expected=True,
        ),
        TaskTest(
            kind="functional",
            name="1-1-5",
            function="is_triangle",
            args=(1, 1, 5),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="вырожденный",
            function="is_triangle",
            args=(2, 3, 5),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="ноль стороны",
            function="is_triangle",
            args=(0, 4, 5),
            expected=False,
        ),
        TaskTest(
            kind="functional",
            name="равносторонний",
            function="is_triangle",
            args=(7, 7, 7),
            expected=True,
        ),
    ),
    xp=14,
)


# 17. FizzBuzz
T_FIZZBUZZ = Task(
    id="t-fizzbuzz",
    title="FizzBuzz",
    description_md="""\
Классическая задача: для каждого числа от **1 до n** включительно выведи строку:

- `Fizz` — если число делится на 3,
- `Buzz` — если число делится на 5,
- `FizzBuzz` — если делится на 3 **и** на 5,
- иначе — просто число.

Каждый ответ — на отдельной строке.

Пример вывода для `n = 5`:

```
1
2
Fizz
4
Buzz
```

Прочитай `n` через `input()`.
""",
    starter_code='n = int(input())\nfor i in range(1, n + 1):\n    # реши, что выводить\n    pass\n',
    solution_code=(
        'n = int(input())\n'
        'for i in range(1, n + 1):\n'
        '    if i % 15 == 0:\n'
        '        print("FizzBuzz")\n'
        '    elif i % 3 == 0:\n'
        '        print("Fizz")\n'
        '    elif i % 5 == 0:\n'
        '        print("Buzz")\n'
        '    else:\n'
        '        print(i)\n'
    ),
    solution_explanation_md="""\
- Сначала проверяй **самое узкое** условие — кратность 15 (это И на 3, И на 5).
  Если поставить эту проверку после `% 3` или `% 5`, она никогда не сработает.
- `% 15 == 0` эквивалентно `% 3 == 0 and % 5 == 0`, но короче.
- В `else` выводим само число — `print(i)`, число будет автоматически приведено к строке.
""",
    hints=(
        "Иди от самого узкого случая (15) к самому широкому (просто число).",
        "Внутри цикла используй if/elif/elif/else.",
        "% 15 == 0 — это и на 3, и на 5.",
    ),
    tests=(
        TaskTest(
            kind="stdio",
            name="до 5",
            stdin="5\n",
            expected_stdout="1\n2\nFizz\n4\nBuzz\n",
        ),
        TaskTest(
            kind="stdio",
            name="до 15",
            stdin="15\n",
            expected_stdout=(
                "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n"
                "11\nFizz\n13\n14\nFizzBuzz\n"
            ),
        ),
        TaskTest(kind="stdio", name="n=1", stdin="1\n", expected_stdout="1\n"),
    ),
    xp=15,
)


# 18. Сумма цифр
T_DIGIT_SUM = Task(
    id="t-digit-sum",
    title="Сумма цифр числа",
    description_md="""\
Напиши функцию `digit_sum(n)`, которая возвращает сумму цифр **неотрицательного**
целого числа `n`.

```python
digit_sum(123)   # 6  (1 + 2 + 3)
digit_sum(0)     # 0
digit_sum(9999)  # 36
```
""",
    starter_code='def digit_sum(n):\n    pass\n',
    solution_code=(
        'def digit_sum(n):\n'
        '    total = 0\n'
        '    for ch in str(n):\n'
        '        total += int(ch)\n'
        '    return total\n'
    ),
    solution_explanation_md="""\
- Самый простой способ — превратить число в строку: `str(n)` даёт `"123"`.
- По строке мы можем итерироваться `for ch in ...` — символ за символом.
- Каждый символ превращаем обратно в число `int(ch)` и складываем.
- Альтернатива через `%` и `//` тоже работает, но для новичка строковый способ чище.
""",
    hints=(
        "Преврати число в строку через str(...).",
        "Перебери каждый символ и сложи int(символ).",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="123",
            function="digit_sum",
            args=(123,),
            expected=6,
        ),
        TaskTest(
            kind="functional",
            name="0",
            function="digit_sum",
            args=(0,),
            expected=0,
        ),
        TaskTest(
            kind="functional",
            name="9999",
            function="digit_sum",
            args=(9999,),
            expected=36,
        ),
        TaskTest(
            kind="functional",
            name="одна цифра",
            function="digit_sum",
            args=(7,),
            expected=7,
        ),
    ),
    xp=12,
)


# 19. Развернуть строку
T_REVERSE = Task(
    id="t-reverse",
    title="Развернуть строку",
    description_md="""\
Напиши функцию `reverse(s)`, которая возвращает строку, развёрнутую задом наперёд.

```python
reverse("Python")  # "nohtyP"
reverse("a")       # "a"
reverse("")        # ""
```

Способов несколько — выбери любой удобный.
""",
    starter_code='def reverse(s):\n    pass\n',
    solution_code='def reverse(s):\n    return s[::-1]\n',
    solution_explanation_md="""\
- В Python есть **срезы со шагом**: `s[start:stop:step]`. Если `step` отрицательный,
  идём с конца к началу.
- `s[::-1]` — «вся строка задом наперёд».
- Срезы работают и для списков: `[1, 2, 3][::-1]` → `[3, 2, 1]`.
""",
    hints=(
        "Самый короткий способ — срез s[::-1].",
        "Альтернатива — собирать символы в обратном порядке через цикл.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="Python",
            function="reverse",
            args=("Python",),
            expected="nohtyP",
        ),
        TaskTest(
            kind="functional",
            name="один символ",
            function="reverse",
            args=("a",),
            expected="a",
        ),
        TaskTest(
            kind="functional",
            name="пустая",
            function="reverse",
            args=("",),
            expected="",
        ),
        TaskTest(
            kind="functional",
            name="палиндром",
            function="reverse",
            args=("шалаш",),
            expected="шалаш",
        ),
    ),
    xp=10,
)


# 20. Считалка слов
T_WORD_COUNT = Task(
    id="t-word-count",
    title="Сколько слов в строке",
    description_md="""\
Напиши функцию `word_count(s)`, которая возвращает **количество слов** в строке.
Слова разделены любыми пробельными символами (один или несколько пробелов, табы,
переводы строки). Пустая строка — это 0 слов.

```python
word_count("hello world")        # 2
word_count("  один   два три ")  # 3
word_count("")                   # 0
```
""",
    starter_code='def word_count(s):\n    pass\n',
    solution_code='def word_count(s):\n    return len(s.split())\n',
    solution_explanation_md="""\
- Метод строки `.split()` без аргументов разбивает строку по любым пробелам.
- Хорошее свойство `.split()` без аргументов: **схлопывает несколько пробелов
  подряд в один** и игнорирует пробелы по краям. Если бы мы передали
  `s.split(" ")` — пустые строки попадали бы в результат.
- `len(...)` — длина списка = количество слов.
""",
    hints=(
        "s.split() без аргументов сделает всю работу.",
        "Не путай с s.split(' '), который оставляет пустые элементы.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="hello world",
            function="word_count",
            args=("hello world",),
            expected=2,
        ),
        TaskTest(
            kind="functional",
            name="много пробелов",
            function="word_count",
            args=("  один   два три ",),
            expected=3,
        ),
        TaskTest(
            kind="functional",
            name="пустая",
            function="word_count",
            args=("",),
            expected=0,
        ),
        TaskTest(
            kind="functional",
            name="одно слово",
            function="word_count",
            args=("привет",),
            expected=1,
        ),
        TaskTest(
            kind="functional",
            name="только пробелы",
            function="word_count",
            args=("    ",),
            expected=0,
        ),
    ),
    xp=12,
)


# 21. Уникальные элементы
T_UNIQUE = Task(
    id="t-unique",
    title="Уникальные элементы списка",
    description_md="""\
Напиши функцию `unique(items)`, которая возвращает **новый список** уникальных
элементов в том порядке, в каком они впервые встретились.

```python
unique([1, 2, 1, 3, 2, 4])      # [1, 2, 3, 4]
unique(["a", "b", "a", "c"])    # ["a", "b", "c"]
unique([])                      # []
```

Не используй `set()` — он не сохраняет порядок (и в этой задаче нужно сохранить
**первое появление** элемента).
""",
    starter_code='def unique(items):\n    pass\n',
    solution_code=(
        'def unique(items):\n'
        '    seen = set()\n'
        '    result = []\n'
        '    for item in items:\n'
        '        if item not in seen:\n'
        '            seen.add(item)\n'
        '            result.append(item)\n'
        '    return result\n'
    ),
    solution_explanation_md="""\
- Идея: помнить, что уже видели, и пропускать повторы.
- `seen` — это **множество** (`set`). Проверка `item in seen` работает очень быстро
  (быстрее, чем `item in result` для длинных списков).
- В `result` собираем элементы в порядке их первого появления.
""",
    hints=(
        "Заведи set() для уже виденных и list для результата.",
        "Перебирай items, пропускай тех, кто уже в set.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="числа",
            function="unique",
            args=([1, 2, 1, 3, 2, 4],),
            expected=[1, 2, 3, 4],
        ),
        TaskTest(
            kind="functional",
            name="строки",
            function="unique",
            args=(["a", "b", "a", "c"],),
            expected=["a", "b", "c"],
        ),
        TaskTest(
            kind="functional",
            name="пустой",
            function="unique",
            args=([],),
            expected=[],
        ),
        TaskTest(
            kind="functional",
            name="без повторов",
            function="unique",
            args=([1, 2, 3],),
            expected=[1, 2, 3],
        ),
    ),
    xp=14,
)


# 22. Минимум-максимум вручную
T_MIN_MAX = Task(
    id="t-min-max",
    title="Минимум и максимум вручную",
    description_md="""\
Напиши функцию `min_max(numbers)`, которая возвращает **кортеж** `(минимум,
максимум)` списка чисел.

**Условие**: реализуй сам, не используя встроенные `min()` и `max()`.

```python
min_max([3, 1, 4, 1, 5, 9])   # (1, 9)
min_max([7])                  # (7, 7)
```

Гарантируется, что список не пуст.
""",
    starter_code='def min_max(numbers):\n    pass\n',
    solution_code=(
        'def min_max(numbers):\n'
        '    cur_min = numbers[0]\n'
        '    cur_max = numbers[0]\n'
        '    for n in numbers[1:]:\n'
        '        if n < cur_min:\n'
        '            cur_min = n\n'
        '        if n > cur_max:\n'
        '            cur_max = n\n'
        '    return (cur_min, cur_max)\n'
    ),
    solution_explanation_md="""\
- Идея: пройти по всем элементам и держать «текущий минимум» и «текущий максимум».
- Начальные значения — первый элемент списка. Дальше идём со второго.
- Возвращаем **кортеж** `(min, max)` — это скобки с запятой, как и `(1, 2)`.
""",
    hints=(
        "Запоминай текущий минимум и максимум, начиная с первого элемента.",
        "Проходи по списку и обновляй, если нашёл меньше/больше.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="разные",
            function="min_max",
            args=([3, 1, 4, 1, 5, 9],),
            expected=(1, 9),
        ),
        TaskTest(
            kind="functional",
            name="один элемент",
            function="min_max",
            args=([7],),
            expected=(7, 7),
        ),
        TaskTest(
            kind="functional",
            name="отрицательные",
            function="min_max",
            args=([-3, -1, -7, -2],),
            expected=(-7, -1),
        ),
    ),
    xp=12,
)


# 23. Среднее
T_AVERAGE = Task(
    id="t-average",
    title="Среднее арифметическое",
    description_md="""\
Напиши функцию `average(numbers)`, которая возвращает среднее арифметическое
чисел в списке. Если список пустой — возвращай `0`.

Округлять не нужно — результат может быть дробью.

```python
average([1, 2, 3, 4])   # 2.5
average([10])           # 10.0
average([])             # 0
```
""",
    starter_code='def average(numbers):\n    pass\n',
    solution_code=(
        'def average(numbers):\n'
        '    if not numbers:\n'
        '        return 0\n'
        '    return sum(numbers) / len(numbers)\n'
    ),
    solution_explanation_md="""\
- Сначала проверка на пустой список — `if not numbers` истинно, если список пустой.
- `sum(numbers) / len(numbers)` — стандартная формула среднего.
- Деление через `/` всегда даёт `float`, даже если числа целые.
""",
    hints=(
        "sum() и len() из коробки.",
        "Не забудь обработать пустой список (иначе деление на 0).",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="1..4",
            function="average",
            args=([1, 2, 3, 4],),
            expected=2.5,
        ),
        TaskTest(
            kind="functional",
            name="один",
            function="average",
            args=([10],),
            expected=10.0,
        ),
        TaskTest(
            kind="functional",
            name="пустой",
            function="average",
            args=([],),
            expected=0,
        ),
    ),
    xp=10,
)


# 24. Подсчёт буквы
T_COUNT_CHAR = Task(
    id="t-count-char",
    title="Сколько раз встречается символ",
    description_md="""\
Напиши функцию `count_char(s, ch)`, которая считает, сколько раз символ `ch`
встречается в строке `s`. Регистр **игнорируем** (большие и маленькие буквы
считаются одним символом).

```python
count_char("Hello", "l")     # 2
count_char("Hello", "H")     # 1  (находит и H)
count_char("Hello", "h")     # 1  (то же самое — регистр не важен)
count_char("Привет", "е")    # 1
```
""",
    starter_code='def count_char(s, ch):\n    pass\n',
    solution_code=(
        'def count_char(s, ch):\n'
        '    return s.lower().count(ch.lower())\n'
    ),
    solution_explanation_md="""\
- `.lower()` приводит строку к нижнему регистру. Применяем и к строке, и к символу.
- `.count(...)` у строки сразу возвращает количество вхождений.
- Альтернатива — цикл с `+= 1`, но `.count` короче и быстрее.
""",
    hints=(
        ".lower() уберёт разницу в регистре.",
        "У строки есть метод .count(подстрока).",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="ll",
            function="count_char",
            args=("Hello", "l"),
            expected=2,
        ),
        TaskTest(
            kind="functional",
            name="регистр H",
            function="count_char",
            args=("Hello", "h"),
            expected=1,
        ),
        TaskTest(
            kind="functional",
            name="нет вхождений",
            function="count_char",
            args=("Hello", "z"),
            expected=0,
        ),
        TaskTest(
            kind="functional",
            name="пустая строка",
            function="count_char",
            args=("", "a"),
            expected=0,
        ),
        TaskTest(
            kind="functional",
            name="русский",
            function="count_char",
            args=("Привет", "Е"),
            expected=1,
        ),
    ),
    xp=12,
)


# 25. Калькулятор
T_CALC = Task(
    id="t-calc",
    title="Простой калькулятор",
    description_md="""\
Напиши функцию `calc(a, op, b)`. Она получает два числа `a`, `b` и **строку с
операцией** `op` (`"+"`, `"-"`, `"*"`, `"/"`). Возвращает результат.

При делении на ноль — возвращай строку `"делить на ноль нельзя"`.
При неизвестной операции — возвращай строку `"неизвестная операция"`.

```python
calc(2, "+", 3)    # 5
calc(10, "/", 4)   # 2.5
calc(5, "/", 0)    # "делить на ноль нельзя"
calc(2, "%", 3)    # "неизвестная операция"
```
""",
    starter_code='def calc(a, op, b):\n    pass\n',
    solution_code=(
        'def calc(a, op, b):\n'
        '    if op == "+":\n'
        '        return a + b\n'
        '    if op == "-":\n'
        '        return a - b\n'
        '    if op == "*":\n'
        '        return a * b\n'
        '    if op == "/":\n'
        '        if b == 0:\n'
        '            return "делить на ноль нельзя"\n'
        '        return a / b\n'
        '    return "неизвестная операция"\n'
    ),
    solution_explanation_md="""\
- Цепочка отдельных `if ...: return ...` вместо `if/elif/else` — это **ранние
  возвраты**. Каждый `return` сразу выходит из функции.
- Деление на ноль обрабатываем отдельной проверкой.
- Дошли до конца функции — значит, ни одна операция не подошла, возвращаем
  «неизвестная операция».
""",
    hints=(
        "Используй цепочку if'ов с return.",
        "Перед делением проверь, не равен ли b нулю.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="плюс",
            function="calc",
            args=(2, "+", 3),
            expected=5,
        ),
        TaskTest(
            kind="functional",
            name="минус",
            function="calc",
            args=(10, "-", 4),
            expected=6,
        ),
        TaskTest(
            kind="functional",
            name="умножить",
            function="calc",
            args=(3, "*", 7),
            expected=21,
        ),
        TaskTest(
            kind="functional",
            name="деление",
            function="calc",
            args=(10, "/", 4),
            expected=2.5,
        ),
        TaskTest(
            kind="functional",
            name="деление на 0",
            function="calc",
            args=(5, "/", 0),
            expected="делить на ноль нельзя",
        ),
        TaskTest(
            kind="functional",
            name="неизвестная",
            function="calc",
            args=(2, "%", 3),
            expected="неизвестная операция",
        ),
    ),
    xp=15,
)


# 26. *args
T_ARGS_SUM = Task(
    id="t-args-sum",
    title="*args: сумма любого числа аргументов",
    description_md="""\
Напиши функцию `total(*nums)`, которая возвращает сумму **любого** количества
переданных чисел. Если ничего не передано — `0`.

```python
total(1, 2, 3)       # 6
total()              # 0
total(10)            # 10
total(1, 2, 3, 4, 5) # 15
```

Подсказка: `*args` в определении функции собирает все позиционные аргументы в
кортеж.
""",
    starter_code='def total(*nums):\n    pass\n',
    solution_code='def total(*nums):\n    return sum(nums)\n',
    solution_explanation_md="""\
- `*nums` в определении функции означает: «сюда соберутся все позиционные аргументы».
- Внутри функции `nums` — это **кортеж** (tuple), как `(1, 2, 3)`.
- `sum(nums)` суммирует элементы. Для пустого кортежа `sum` вернёт 0 — поэтому
  отдельная проверка не нужна.
""",
    hints=(
        "В определении функции пиши *nums — это собирает все аргументы.",
        "sum() работает и с кортежем, и с пустым кортежем (вернёт 0).",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="1+2+3",
            function="total",
            args=(1, 2, 3),
            expected=6,
        ),
        TaskTest(
            kind="functional",
            name="пусто",
            function="total",
            args=(),
            expected=0,
        ),
        TaskTest(
            kind="functional",
            name="один",
            function="total",
            args=(10,),
            expected=10,
        ),
        TaskTest(
            kind="functional",
            name="много",
            function="total",
            args=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            expected=55,
        ),
    ),
    xp=12,
)


# 27. List comprehension: верхний регистр
T_MAP_UPPER = Task(
    id="t-map-upper",
    title="Список в верхний регистр",
    description_md="""\
Напиши функцию `to_upper_list(words)`, которая получает список строк и возвращает
**новый** список с теми же строками, но в **верхнем регистре**.

```python
to_upper_list(["hi", "world"])   # ["HI", "WORLD"]
to_upper_list([])                # []
```

В решении используй **list comprehension** — это конструкция вида
`[выражение for x in список]`.
""",
    starter_code='def to_upper_list(words):\n    pass\n',
    solution_code='def to_upper_list(words):\n    return [w.upper() for w in words]\n',
    solution_explanation_md="""\
- **List comprehension** `[w.upper() for w in words]` — это компактная запись
  цикла, который собирает результат в список.
- Эквивалентный полный код:

```python
result = []
for w in words:
    result.append(w.upper())
return result
```

- Через `lambda` тот же результат: `list(map(lambda w: w.upper(), words))`. Но
  comprehension читается лучше.
""",
    hints=(
        "List comprehension: [выражение for элемент in список].",
        "У строки есть метод .upper().",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="hi/world",
            function="to_upper_list",
            args=(["hi", "world"],),
            expected=["HI", "WORLD"],
        ),
        TaskTest(
            kind="functional",
            name="пустой",
            function="to_upper_list",
            args=([],),
            expected=[],
        ),
        TaskTest(
            kind="functional",
            name="русский",
            function="to_upper_list",
            args=(["привет"],),
            expected=["ПРИВЕТ"],
        ),
    ),
    xp=12,
)


# 28. Фильтрация чётных
T_FILTER_EVEN = Task(
    id="t-filter-even",
    title="Только чётные",
    description_md="""\
Напиши функцию `only_even(numbers)`, которая возвращает **новый** список с
чётными числами из исходного, в том же порядке.

```python
only_even([1, 2, 3, 4, 5, 6])   # [2, 4, 6]
only_even([1, 3, 5])            # []
only_even([])                   # []
```

Сделай через **list comprehension с условием**.
""",
    starter_code='def only_even(numbers):\n    pass\n',
    solution_code='def only_even(numbers):\n    return [n for n in numbers if n % 2 == 0]\n',
    solution_explanation_md="""\
- В list comprehension можно добавить **фильтр** через `if ...`:
  `[n for n in numbers if n % 2 == 0]`.
- Это означает «возьми n из numbers, оставь только те, где n % 2 == 0».
- Эквивалент полным кодом — `for` + `if` + `append`.
""",
    hints=(
        "[n for n in numbers if условие].",
        "Чётность — n % 2 == 0.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="смешанный",
            function="only_even",
            args=([1, 2, 3, 4, 5, 6],),
            expected=[2, 4, 6],
        ),
        TaskTest(
            kind="functional",
            name="только нечётные",
            function="only_even",
            args=([1, 3, 5],),
            expected=[],
        ),
        TaskTest(
            kind="functional",
            name="пустой",
            function="only_even",
            args=([],),
            expected=[],
        ),
        TaskTest(
            kind="functional",
            name="нули",
            function="only_even",
            args=([0, 1, 2],),
            expected=[0, 2],
        ),
    ),
    xp=12,
)


# 29. Словарь: подсчёт частот
T_COUNT_WORDS = Task(
    id="t-count-words",
    title="Частота слов",
    description_md="""\
Напиши функцию `word_freq(s)`, которая получает строку и возвращает **словарь**
вида `{слово: количество}`. Слова разделены пробелами. Регистр игнорируем.

```python
word_freq("ab AB cd Ab")
# {"ab": 3, "cd": 1}

word_freq("")
# {}
```
""",
    starter_code='def word_freq(s):\n    pass\n',
    solution_code=(
        'def word_freq(s):\n'
        '    result = {}\n'
        '    for word in s.lower().split():\n'
        '        result[word] = result.get(word, 0) + 1\n'
        '    return result\n'
    ),
    solution_explanation_md="""\
- `s.lower()` приводит к нижнему регистру.
- `.split()` бьёт по пробелам, схлопывая повторы.
- `result.get(word, 0)` — получить значение по ключу, если нет — `0`. Удобно для
  «инкремента счётчика»: `result[word] = result.get(word, 0) + 1`.
- Альтернатива — `from collections import Counter` (уже встроено в Python).
""",
    hints=(
        "s.lower() и s.split() — твои друзья.",
        "Используй dict.get(ключ, 0), чтобы избежать KeyError.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="разные регистры",
            function="word_freq",
            args=("ab AB cd Ab",),
            expected={"ab": 3, "cd": 1},
        ),
        TaskTest(
            kind="functional",
            name="пустая",
            function="word_freq",
            args=("",),
            expected={},
        ),
        TaskTest(
            kind="functional",
            name="одно слово",
            function="word_freq",
            args=("привет",),
            expected={"привет": 1},
        ),
    ),
    xp=15,
)


# 30. JSON: профиль
T_JSON_PROFILE = Task(
    id="t-json-profile",
    title="Сборка профиля в JSON-строку",
    description_md="""\
Напиши функцию `to_json(name, age, hobbies)`. Она возвращает JSON-строку, которая
описывает пользователя:

```json
{"name": "Кирилл", "age": 19, "hobbies": ["python", "music"]}
```

Используй модуль `json` из стандартной библиотеки. Не забудь
`ensure_ascii=False`, иначе кириллица превратится в `\\uXXXX`.

```python
to_json("Кирилл", 19, ["python", "music"])
# '{"name": "Кирилл", "age": 19, "hobbies": ["python", "music"]}'
```
""",
    starter_code='import json\n\ndef to_json(name, age, hobbies):\n    pass\n',
    solution_code=(
        'import json\n'
        '\n'
        'def to_json(name, age, hobbies):\n'
        '    data = {"name": name, "age": age, "hobbies": hobbies}\n'
        '    return json.dumps(data, ensure_ascii=False)\n'
    ),
    solution_explanation_md="""\
- Сначала собираем словарь Python — это не JSON, это просто dict.
- `json.dumps(...)` превращает Python-структуру в **строку JSON**.
- `ensure_ascii=False` оставляет кириллицу как есть. По умолчанию `json` всё
  не-ASCII экранирует.
- Обратное — `json.loads("...")` принимает JSON-строку и даёт обратно dict.
""",
    hints=(
        "Соберите dict из аргументов.",
        "json.dumps(dict, ensure_ascii=False) даёт строку.",
    ),
    tests=(
        TaskTest(
            kind="functional",
            name="базовый",
            function="to_json",
            args=("Кирилл", 19, ["python", "music"]),
            expected='{"name": "Кирилл", "age": 19, "hobbies": ["python", "music"]}',
        ),
        TaskTest(
            kind="functional",
            name="без хобби",
            function="to_json",
            args=("Аня", 25, []),
            expected='{"name": "Аня", "age": 25, "hobbies": []}',
        ),
    ),
    xp=15,
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
    T_PRINT_CARD,
    T_PRINT_ASCII,
    T_SUM_INPUTS,
    T_DIVMOD,
    T_TRI,
    T_FIZZBUZZ,
    T_DIGIT_SUM,
    T_REVERSE,
    T_WORD_COUNT,
    T_UNIQUE,
    T_MIN_MAX,
    T_AVERAGE,
    T_COUNT_CHAR,
    T_CALC,
    T_ARGS_SUM,
    T_MAP_UPPER,
    T_FILTER_EVEN,
    T_COUNT_WORDS,
    T_JSON_PROFILE,
    T_BOT_ECHO,
)
