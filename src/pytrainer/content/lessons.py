"""Контент уроков. Все строки — Markdown."""
from __future__ import annotations

from . import Lesson

# ----- Раздел 0: Знакомство -----

S0 = ("00-intro", "0. Знакомство")

L_00_what = Lesson(
    id="00-what-is-python",
    section_id=S0[0],
    section_title=S0[1],
    title="Что такое Python и зачем он",
    body_md="""\
Python — это **язык программирования**. Тебя интересуют боты — отлично, на Python пишут
очень много ботов. Но не только: и сайты, и игры, и автоматизацию рутины, и анализ данных.

В жизни программа — это **текст**, который объясняет компьютеру, что нужно сделать. Этот
текст называют **кодом**. Код пишется по правилам — их и есть «синтаксис языка».

### Что нужно знать на старте

- Программа состоит из **инструкций** — это команды, идущие сверху вниз.
- Самая простая команда — **вывести что-то на экран**: `print("Привет!")`.
- Все «ужасы» из IT-фильмов — это просто текст. Никакой магии нет.

### Как читать наши уроки

1. Сверху — теория небольшими кусочками.
2. Потом — блок «Попробуй сам»: код можно сразу запустить и посмотреть, что получится.
3. После урока — задачи. Решаешь — получаешь XP и идёшь дальше.

> Совет: открывай «Песочницу» (в боковом меню) и пробуй там всё, что хочется. Сломать
> компьютер ты не сможешь — код выполняется в безопасном окружении.
""",
    try_it_code='print("Hello, world!")\nprint("Я учу Python")\n',
    task_ids=(),
    xp=3,
)

L_00_print = Lesson(
    id="00-first-print",
    section_id=S0[0],
    section_title=S0[1],
    title="Первая команда: print",
    body_md="""\
**`print`** — встроенная функция. «Функция» — это команда с именем, которой можно
что-то передать в скобках. У `print` задача простая: показать на экране то, что ей
передали.

```python
print("Привет!")
print("Меня зовут Кирилл")
```

### Несколько штук в одном `print`

Можно передать через запятую — Python поставит между ними пробел:

```python
print("2 + 2 =", 2 + 2)
```

### Параметр `sep`

Пробел между аргументами — это «разделитель». Его можно поменять параметром `sep`:

```python
print("a", "b", "c", sep="-")
# выведет: a-b-c
```

Так у `print` много мелких настроек: `sep`, `end`, `file` — но 99% времени
используется без них.

### Зачем это всё

Когда мы будем писать программу — `print` помогает посмотреть, что внутри нашего кода
происходит. Это самый простой инструмент **отладки** (от слова «debug» — «выгнать
ошибку»).
""",
    try_it_code='print("Меня зовут Python")\nprint("Сегодня", "хороший", "день", sep=" — ")\nprint("Конец строки", end="!\\n")\n',
    task_ids=("t-print-intro",),
    xp=4,
)

L_00_errors = Lesson(
    id="00-errors-comments",
    section_id=S0[0],
    section_title=S0[1],
    title="Комментарии и первые ошибки",
    body_md="""\
**Комментарий** — текст, который Python игнорирует. Нужен, чтобы оставить заметку
себе или другому человеку (часто — себе через месяц).

```python
# Это комментарий, Python его не выполняет
print("А вот это — выполнит")  # и это после кода — тоже комментарий
```

### Если ошибся

Python вместо паники пишет, **где** и **что** не так. Это называется **traceback** —
буквально «обратный след». Главное — смотреть на **последнюю строку**: там и
причина.

Например, если забыть закрыть кавычки:

```python
print("Привет)
```

Получим что-то вроде:

```
SyntaxError: unterminated string literal
```

`SyntaxError` = «ошибка синтаксиса», `unterminated string literal` = «незакрытая
строка». Перевели — нашли — поправили.

### Как читать сообщение об ошибке

1. Посмотри **последнюю строку** — там тип ошибки и краткое описание.
2. Посмотри **строку выше** — там номер строки и сам файл.
3. Гугли формулировку — это нормально.

> Не бойся ошибок. Программисты получают их сотни в день. Это не «провал» — это
> подсказка от компилятора, что и где поправить.
""",
    try_it_code='# попробуй убрать решётку и посмотри, что выведется\nprint("Без комментария")\n# print("С комментарием")\n',
    task_ids=(),
    xp=3,
)


# ----- Раздел 1: Переменные и типы -----

S1 = ("01-vars", "1. Переменные и типы")

L_01_vars = Lesson(
    id="01-variables",
    section_id=S1[0],
    section_title=S1[1],
    title="Переменные — коробки для данных",
    body_md="""\
**Переменная** — это имя для значения. Делается через знак `=`:

```python
name = "Кирилл"
age = 19
```

Слева от `=` — имя. Справа — то, что в нём лежит. После этого имя можно использовать
вместо значения:

```python
print(name)
print("Мне", age, "лет")
```

### Имена

- Латинскими буквами и цифрами, начинаются с буквы или `_`.
- Не должны совпадать с ключевыми словами (`if`, `for`, `def` и т.п.).
- Принято писать через `_`: `user_name`, `total_price`.
- Чем понятнее имя — тем лучше. `x = 1500` — плохо, `monthly_income = 1500` — хорошо.

### Менять можно

Имя переменной — это «коробка». Можно положить туда другое значение в любой момент:

```python
score = 0
score = score + 10
print(score)  # 10
```

`score = score + 10` читается так: «возьми текущий `score`, прибавь 10, запиши обратно
в `score`». Можно короче:

```python
score += 10  # то же самое
```
""",
    try_it_code='''name = "Кирилл"
age = 19
print("Привет,", name)
print("Мне", age, "лет")

age = age + 1
print("А теперь мне", age)
''',
    task_ids=(),
    xp=4,
)

L_01_types = Lesson(
    id="01-types",
    section_id=S1[0],
    section_title=S1[1],
    title="Типы: число, строка, булево",
    body_md="""\
У каждого значения в Python есть **тип** — что это вообще такое.

| Тип | Что это | Пример |
|---|---|---|
| `int` | целое число | `42`, `-3`, `0` |
| `float` | дробное число | `3.14`, `-0.5` |
| `str` | строка (текст) | `"привет"`, `'42'` |
| `bool` | булево (логика) | `True`, `False` |
| `None` | «ничего» | `None` |

Узнать тип можно функцией `type`:

```python
print(type(42))      # <class 'int'>
print(type("42"))    # <class 'str'>
print(type(True))    # <class 'bool'>
```

### Числа

С числами всё понятно: `+`, `-`, `*`, `/`, `**` (степень), `//` (целочисленное деление),
`%` (остаток):

```python
print(7 // 2)   # 3
print(7 % 2)    # 1
print(2 ** 10)  # 1024
```

### Строки

Строка — текст в кавычках. Кавычки можно использовать любые: `"..."` или `'...'`. Для
многострочного текста есть тройные кавычки:

```python
greeting = "Привет!"
multiline = \"\"\"
строка 1
строка 2
\"\"\"
```

Строки можно **складывать** (склеивать):

```python
first = "Кирилл"
last = "Иванов"
full = first + " " + last
print(full)
```

И умножать на число (повторение):

```python
print("=" * 20)  # ====================
```

### f-строки (форматирование)

Удобный способ собрать строку с переменными — поставить `f` перед открывающей кавычкой
и писать переменные в фигурных скобках:

```python
name = "Кирилл"
age = 19
print(f"Привет, {name}! Тебе {age}.")
```

### Преобразование типов

```python
x = "42"        # это строка
n = int(x)      # стало 42 (число)
print(n + 1)    # 43
```

Если попытаться `int("abc")` — будет ошибка `ValueError`. Не страшно: пока что мы
будем знать, что в строке точно цифры.
""",
    try_it_code='''x = 7
y = 3
print("целое:", x // y)
print("остаток:", x % y)
print("дробное:", x / y)

s = "42"
print("это строка:", s + s)
print("это число:", int(s) + int(s))
''',
    task_ids=(),
    xp=5,
)

L_01_input = Lesson(
    id="01-input",
    section_id=S1[0],
    section_title=S1[1],
    title="Считаем ввод от пользователя — input",
    body_md="""\
**`input`** — встроенная функция, которая ждёт, пока пользователь что-нибудь введёт
с клавиатуры и нажмёт Enter. Возвращает то, что ввели — **строкой**.

```python
name = input("Как тебя зовут? ")
print(f"Привет, {name}!")
```

> В нашей «Песочнице» и в задачах ввод подаётся в специальное поле «stdin». В
> задачах — задаётся автоматически из теста.

### Если ждём число

`input` всегда возвращает строку — если нужно число, конвертируем:

```python
age = int(input("Сколько тебе лет? "))
print(f"Через 10 лет тебе будет {age + 10}")
```

### Опечатки и проверки

Если пользователь ввёл «двадцать», `int(...)` упадёт с ошибкой. Это нормально.
Защищаться от ошибок ввода мы научимся позже (когда дойдём до `try/except`).
""",
    try_it_code='''name = input("Как тебя зовут? ")
print(f"Здравствуй, {name}!")
''',
    task_ids=("t-greeting", "t-magic-8"),
    xp=5,
)


# ----- Раздел 2: Условия -----

S2 = ("02-cond", "2. Условия")

L_02_if = Lesson(
    id="02-if-else",
    section_id=S2[0],
    section_title=S2[1],
    title="if / else: первое решение",
    body_md="""\
**Условие** — точка, где программа решает: «делать одно или другое».

```python
age = 17
if age >= 18:
    print("Можно голосовать")
else:
    print("Подожди ещё")
```

### Главное

- После `if` пишется **условие** — выражение, которое даёт `True` или `False`.
- После двоеточия `:` идёт **тело** — что делать, если условие истинно. Тело сдвинуто
  пробелами вправо. **Этот сдвиг (отступ) — обязателен.** Пиши 4 пробела или один Tab,
  но не смешивай.
- `else` — что делать, если условие ложно. У `else` тоже свой блок.

### Сравнения

```text
==  равно
!=  не равно
>   больше
<   меньше
>=  больше или равно
<=  меньше или равно
```

`=` это «положить значение», `==` это «сравнить». Не путай.

```python
if name == "Python":
    print("Это твой друг")
```

### Один if без else

`else` не обязателен. Можно просто:

```python
balance = 1000
if balance < 0:
    print("Долг!")
print("Конец проверки")
```
""",
    try_it_code='''age = int(input("Возраст: "))
if age >= 18:
    print("Совершеннолетний")
else:
    print("Ещё нет")
''',
    task_ids=("t-even-odd",),
    xp=5,
)

L_02_elif = Lesson(
    id="02-elif",
    section_id=S2[0],
    section_title=S2[1],
    title="elif: цепочка условий",
    body_md="""\
Когда вариантов больше двух, появляется `elif` — «иначе если»:

```python
score = 73
if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
elif score >= 50:
    print("Удовлетворительно")
else:
    print("Не сдал")
```

### Как читать

Python проверяет условия **по порядку сверху вниз**. Первое подошедшее — выполняется,
остальные пропускаются.

### Цепочка `elif` — это не несколько `if`

Сравни:

```python
# 1. Цепочка — выполнится одно
if x > 0:
    print("плюс")
elif x == 0:
    print("ноль")
elif x < 0:
    print("минус")

# 2. Несколько отдельных if — могут сработать несколько
if x > 0:
    print("плюс")
if x == 0:
    print("ноль")
if x < 0:
    print("минус")
```

Тут оба варианта дают одинаковый результат, потому что только одно условие может быть
истинным. Но в общем случае — **`elif` это часть одной цепочки, отдельный `if` — это
независимая проверка.**
""",
    try_it_code='''score = int(input("Балл: "))
if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
elif score >= 50:
    print("Удовлетворительно")
else:
    print("Не сдал")
''',
    task_ids=("t-grade",),
    xp=5,
)

L_02_bool = Lesson(
    id="02-bool-ops",
    section_id=S2[0],
    section_title=S2[1],
    title="Логика: and, or, not",
    body_md="""\
Условия можно объединять.

- **`and`** (и) — истинно, если **оба** истинны.
- **`or`** (или) — истинно, если **хотя бы одно** истинно.
- **`not`** (не) — переворачивает.

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("Пускаем")

if age < 18 or not has_id:
    print("Не пускаем")
```

### Скобки

Если условий много — лучше с скобками, чтобы не путаться:

```python
if (age >= 18 and has_id) or is_admin:
    ...
```

### True и False — это значения

Их можно сохранить в переменную:

```python
is_active = age >= 18
print(is_active)  # True или False
```
""",
    try_it_code='''age = 20
has_id = True
print(age >= 18 and has_id)  # True
print(age < 18 or not has_id)  # False
''',
    task_ids=("t-password",),
    xp=4,
)


# ----- Раздел 3: Списки и словари -----

S3 = ("03-collections", "3. Списки и словари")

L_03_lists = Lesson(
    id="03-lists",
    section_id=S3[0],
    section_title=S3[1],
    title="Списки: упорядоченные коллекции",
    body_md="""\
**Список** (`list`) — упорядоченный набор значений. Записывается в квадратных скобках,
элементы через запятую. Может содержать что угодно.

```python
fruits = ["яблоко", "груша", "банан"]
print(fruits)
print(len(fruits))  # 3 — длина списка
```

### Доступ по индексу

Индекс — номер элемента. **Считаем с 0!**

```python
fruits = ["яблоко", "груша", "банан"]
print(fruits[0])   # яблоко
print(fruits[1])   # груша
print(fruits[-1])  # банан — отрицательный индекс = с конца
```

### Менять и добавлять

```python
fruits[0] = "ананас"      # заменили
fruits.append("персик")   # добавили в конец
fruits.remove("груша")    # удалили по значению
print(fruits)
```

### Срезы

`spisok[начало:конец]` — берём подсписок:

```python
nums = [1, 2, 3, 4, 5]
print(nums[1:4])   # [2, 3, 4]
print(nums[:3])    # [1, 2, 3]
print(nums[::-1])  # [5, 4, 3, 2, 1] — наоборот
```

### Полезные функции

```python
nums = [3, 1, 4, 1, 5]
print(min(nums), max(nums), sum(nums))  # 1 5 14
nums.sort()
print(nums)  # [1, 1, 3, 4, 5]
```
""",
    try_it_code='''fruits = ["яблоко", "груша", "банан"]
fruits.append("персик")
print(fruits)
print("Первый:", fruits[0])
print("Последний:", fruits[-1])
print("Длина:", len(fruits))
''',
    task_ids=("t-shopping-list",),
    xp=6,
)

L_03_dicts = Lesson(
    id="03-dicts",
    section_id=S3[0],
    section_title=S3[1],
    title="Словари: ключ → значение",
    body_md="""\
**Словарь** (`dict`) — пары «ключ — значение». Записывается в фигурных скобках:

```python
user = {
    "name": "Кирилл",
    "age": 19,
    "is_admin": False,
}

print(user["name"])      # Кирилл
print(user["age"] + 1)   # 20
```

### Зачем

Список хорош, когда у тебя **последовательность одинаковых вещей** (фрукты,
покупки). Словарь — когда **разные данные с понятными именами** (профиль, настройки).

### Менять и добавлять

```python
user["age"] = 20            # поменяли
user["email"] = "k@e.com"   # добавили новый ключ
del user["is_admin"]        # удалили
```

### Перебор

```python
for key, value in user.items():
    print(key, "→", value)
```

### Что можно положить в ключ

Текст, число, кортеж. **Список нельзя.** Звучит странно, но запомни.

### Безопасный доступ

Если ключа нет — Python кинет `KeyError`. Чтобы не ловить — `get`:

```python
print(user.get("phone"))             # None
print(user.get("phone", "не задан")) # 'не задан'
```
""",
    try_it_code='''user = {"name": "Кирилл", "age": 19}
print(user["name"], user["age"])
user["email"] = "k@example.com"
print(user)
print("Профессии нет:", user.get("job", "—"))
''',
    task_ids=(),
    xp=5,
)


# ----- Раздел 4: Циклы -----

S4 = ("04-loops", "4. Циклы")

L_04_for = Lesson(
    id="04-for-loop",
    section_id=S4[0],
    section_title=S4[1],
    title="for: пройти по элементам",
    body_md="""\
**Цикл `for`** — берёт по одному элементу из коллекции и выполняет код. По-русски:
«для каждого X в Y делай Z».

```python
fruits = ["яблоко", "груша", "банан"]
for fruit in fruits:
    print("Купил", fruit)
```

`fruit` — это **переменная цикла**. Имя любое — Python будет брать в неё каждый
элемент.

### range — последовательность чисел

`range(n)` даёт числа от `0` до `n-1`:

```python
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

`range(start, stop)`:

```python
for i in range(2, 7):
    print(i)  # 2, 3, 4, 5, 6
```

`range(start, stop, step)`:

```python
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
```

### Зачем нужен i

Если нужно одновременно знать **номер** элемента и сам элемент — `enumerate`:

```python
fruits = ["яблоко", "груша"]
for i, name in enumerate(fruits, start=1):
    print(i, name)  # 1 яблоко / 2 груша
```

### break и continue

- `break` — выйти из цикла досрочно.
- `continue` — пропустить остаток текущей итерации и перейти к следующей.

```python
for n in range(10):
    if n == 5:
        break        # дойдёт до 5 и остановится
    if n % 2 == 0:
        continue     # чётные пропустит
    print(n)
```
""",
    try_it_code='''for i in range(1, 11):
    print(i, end=" ")
print()  # перевод строки
total = 0
for n in [1, 2, 3, 4, 5]:
    total += n
print("Сумма:", total)
''',
    task_ids=(),
    xp=6,
)

L_04_while = Lesson(
    id="04-while",
    section_id=S4[0],
    section_title=S4[1],
    title="while: пока условие истинно",
    body_md="""\
**Цикл `while`** — выполняй блок, **пока условие истинно**.

```python
n = 5
while n > 0:
    print(n)
    n = n - 1
print("Поехали!")
```

### Чем `while` отличается от `for`

- `for` — когда заранее знаешь, **по чему** идти (по списку, по `range`).
- `while` — когда заранее не знаешь, **сколько раз** надо.

Например, угадайка: «спрашивай, пока не угадает» — это `while`.

### Берегись бесконечных циклов

```python
n = 5
while n > 0:
    print(n)
# забыли уменьшить n — это бесконечный цикл!
```

В нашем тренажёре сработает таймаут (5 сек) и он остановится. На реальной машине —
программа повиснет.

### Совет

В большинстве случаев `for` понятнее, чем `while`. Используй `while`, когда условие
выхода **зависит от пользователя или от внешних данных**.
""",
    try_it_code='''import random
secret = random.randint(1, 5)
guess = 0
attempts = 0
while guess != secret:
    attempts += 1
    guess = random.randint(1, 5)
print("Угадали число", secret, "за", attempts, "попыток")
''',
    task_ids=("t-guess-number",),
    xp=6,
)

L_04_nested = Lesson(
    id="04-nested-loops",
    section_id=S4[0],
    section_title=S4[1],
    title="Вложенные циклы",
    body_md="""\
В цикл можно положить ещё один цикл. Получим **вложение**.

```python
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}*{j}={i*j}", end="\\t")
    print()  # перенос строки в конце ряда
```

Получится таблица умножения 3 на 3.

### Когда нужны

- Перебор пар «всё со всем» (карты в колоде, точки на сетке).
- Обработка вложенных списков (список списков).

### Сложность

Вложенный цикл «работает» **столько раз, сколько произведение длин**. Два цикла по
1000 элементов = миллион итераций. Это уже заметно — будь аккуратен.

### Как НЕ запутаться

- Имена переменных циклов разные (`i`, `j`, `row`, `col`).
- Внутренний `break` ломает только внутренний цикл, не оба.
""",
    try_it_code='''for row in range(1, 6):
    for col in range(1, 6):
        print(row * col, end="\\t")
    print()
''',
    task_ids=("t-multi-table",),
    xp=5,
)


# ----- Раздел 5: Функции -----

S5 = ("05-funcs", "5. Функции")

L_05_def = Lesson(
    id="05-def-return",
    section_id=S5[0],
    section_title=S5[1],
    title="Функции: def, return, print vs return",
    body_md="""\
Функция — кусок кода с именем. Ты её **определяешь** один раз и **вызываешь** сколько
угодно.

```python
def greet(name):
    print(f"Привет, {name}!")

greet("Кирилл")
greet("Аня")
```

- `def` — ключевое слово, начинаем определение функции.
- `greet` — **имя** функции.
- В скобках — **параметры** (входы).
- Тело — со сдвигом (4 пробела).

### return vs print

Это разные вещи!

- `print(x)` **показывает** `x` пользователю на экране. Возвращает `None`.
- `return x` **возвращает** значение туда, откуда вызвали. Снаружи можно его поймать
  в переменную.

```python
def double(n):
    return n * 2

result = double(5)   # вернётся 10
print(result)        # выведет 10
```

Если перепутать:

```python
def double_bad(n):
    print(n * 2)   # просто печатает на экран
    # return нет! значит, вернётся None

x = double_bad(5)  # на экран попадёт 10
print(x)           # выведет None
```

**Запомни**: пользователю — `print`. Дальше по коду — `return`.

### Параметры по умолчанию

```python
def greet(name, greeting="Привет"):
    print(f"{greeting}, {name}!")

greet("Кирилл")              # Привет, Кирилл!
greet("Кирилл", "Здарова")   # Здарова, Кирилл!
```
""",
    try_it_code='''def double(n):
    return n * 2

print(double(5))
print(double(7))

def greet(name, greeting="Привет"):
    print(f"{greeting}, {name}!")

greet("Кирилл")
greet("Аня", "Здарова")
''',
    task_ids=("t-area",),
    xp=7,
)

L_05_args = Lesson(
    id="05-args-kwargs",
    section_id=S5[0],
    section_title=S5[1],
    title="*args и **kwargs",
    body_md="""\
Бывает, что хочется передать **сколько угодно** аргументов.

### `*args` — много позиционных

```python
def my_sum(*nums):
    total = 0
    for n in nums:
        total += n
    return total

print(my_sum(1, 2, 3))           # 6
print(my_sum(10, 20, 30, 40))    # 100
```

`*nums` означает «сложи все позиционные аргументы в кортеж под именем `nums`». Имя
любое, но по соглашению пишут `args`.

### `**kwargs` — много именованных

```python
def show_user(**fields):
    for key, value in fields.items():
        print(f"{key}: {value}")

show_user(name="Кирилл", age=19)
# name: Кирилл
# age: 19
```

`**fields` означает «собери все именованные аргументы в словарь». Имя любое,
по соглашению — `kwargs`.

### Обратное распаковывание

`*` и `**` работают и в обратную сторону — **распаковывают**:

```python
nums = [1, 2, 3]
print(my_sum(*nums))   # как my_sum(1, 2, 3)

opts = {"name": "Аня", "age": 20}
show_user(**opts)      # как show_user(name="Аня", age=20)
```

### Зачем тебе это

Когда дойдём до Telegram-бота — увидишь, что библиотеки часто принимают `**kwargs`,
чтобы не ломаться от новых параметров. Знать имена `args/kwargs` — must.
""",
    try_it_code='''def my_sum(*nums):
    return sum(nums)

print(my_sum(1, 2, 3))
print(my_sum(10, 20, 30, 40))

def show_user(**fields):
    for k, v in fields.items():
        print(f"{k}: {v}")

show_user(name="Кирилл", age=19)
''',
    task_ids=(),
    xp=6,
)

L_05_lambda = Lesson(
    id="05-lambda",
    section_id=S5[0],
    section_title=S5[1],
    title="lambda: короткие функции на лету",
    body_md="""\
`lambda` — короткая запись функции, у которой **одно выражение**.

```python
square = lambda x: x * x
print(square(5))   # 25
```

Это **то же самое**, что:

```python
def square(x):
    return x * x
```

### Где встретишь

Когда нужно передать **функцию как аргумент** — `lambda` сокращает запись:

```python
nums = [3, 1, 4, 1, 5, 9, 2]
sorted_nums = sorted(nums, key=lambda x: -x)  # сортируем по убыванию
print(sorted_nums)
```

Но если функция длинная или используется в нескольких местах — пиши обычный `def`.
`lambda` — для одноразовых.

### Совет

`lambda` пугает только из-за слова. Не бойся: «лямбда — это короткая безымянная
функция в одну строку». Всё.
""",
    try_it_code='''cube = lambda x: x ** 3
print(cube(2))
print(cube(3))

users = [{"name": "Аня", "age": 20}, {"name": "Боб", "age": 18}]
users.sort(key=lambda u: u["age"])
print(users)
''',
    task_ids=(),
    xp=4,
)


# ----- Раздел 6: Файлы и модули -----

S6 = ("06-files", "6. Файлы и модули")

L_06_modules = Lesson(
    id="06-modules",
    section_id=S6[0],
    section_title=S6[1],
    title="Модули: import",
    body_md="""\
**Модуль** — отдельный файл с кодом. Чтобы воспользоваться чужим (или своим в другом
файле) — пишут `import`.

```python
import math

print(math.pi)            # 3.14159...
print(math.sqrt(16))      # 4.0
```

`math` — модуль из стандартной библиотеки Python. **Стандартная библиотека** — то,
что идёт «в комплекте» с Python: `math`, `random`, `json`, `datetime`, `os`...

### Разные формы import

```python
import math                  # math.sqrt
from math import sqrt        # просто sqrt
from math import sqrt as sq  # sq
import math as m              # m.sqrt
```

Любой вариант — рабочий. Выбирают по вкусу и читаемости.

### Свой модуль

Если у тебя в той же папке файл `helpers.py` с функцией `greet`, импортируешь так:

```python
from helpers import greet
greet("Кирилл")
```

Это и есть «разбить код по файлам».

### Полезные модули из стандартной библиотеки

| Модуль | Что внутри |
|---|---|
| `math` | синусы, корни, число π |
| `random` | случайные числа, перемешивание |
| `datetime` | даты и время |
| `json` | сохранять/читать JSON |
| `os`, `pathlib` | файлы и папки |
""",
    try_it_code='''import random

names = ["Аня", "Боб", "Веня"]
print("Случайный:", random.choice(names))

import math
print("Пи:", math.pi)
print("Корень из 81:", math.sqrt(81))
''',
    task_ids=(),
    xp=5,
)

L_06_files = Lesson(
    id="06-files-json",
    section_id=S6[0],
    section_title=S6[1],
    title="Файлы и JSON",
    body_md="""\
Чтобы записать что-то на диск или прочесть — используют `open` с конструкцией `with`.

### Запись

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Привет, файл!\\n")
```

`"w"` означает «write» (запись, перезаписать). После выхода из `with` файл
автоматически закроется. **Всегда** используй `with` — иначе можно забыть `close`.

### Чтение

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()
print(text)
```

Хочешь по строкам?

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
```

### JSON

JSON — стандартный формат данных. Похож на Python-словарь и список. Любой бот,
любой API — это JSON.

```python
import json

user = {"name": "Кирилл", "age": 19, "skills": ["python"]}
text = json.dumps(user, ensure_ascii=False, indent=2)
print(text)

restored = json.loads(text)
print(restored["name"])
```

`json.dumps` — словарь → строка. `json.loads` — строка → словарь.

`json.dump` / `json.load` — то же, но сразу с файлом.

```python
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=2)

with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```
""",
    try_it_code='''import json

user = {"name": "Кирилл", "age": 19}
text = json.dumps(user, ensure_ascii=False, indent=2)
print(text)

back = json.loads(text)
print("Имя:", back["name"])
''',
    task_ids=(),
    xp=6,
)


# ----- Раздел 7: pip / venv / API -----

S7 = ("07-pip-api", "7. pip, виртуальное окружение, API")

L_07_pip = Lesson(
    id="07-pip-venv",
    section_id=S7[0],
    section_title=S7[1],
    title="pip и виртуальное окружение",
    body_md="""\
Кроме стандартной библиотеки, в Python есть **тысячи внешних** — в репозитории
[PyPI](https://pypi.org). Их ставят командой `pip`.

```text
pip install requests
```

После этого в коде:

```python
import requests
r = requests.get("https://example.com")
print(r.status_code)
```

### Виртуальное окружение (venv)

Если ты ставишь библиотеки прямо в систему — со временем будет «суп» из несовместимых
версий. Поэтому делают **виртуальное окружение** — папку с локальными библиотеками
для конкретного проекта.

В терминале (Windows):

```text
python -m venv .venv
.venv\\Scripts\\activate
pip install requests
```

(на Linux/macOS вместо `.venv\\Scripts\\activate` — `source .venv/bin/activate`)

Активировано — все `pip install` пойдут только в этот проект. Удалил папку — нет
больше зависимостей.

### requirements.txt

Чтобы коллега (или ты сам через год) мог поставить **тот же** набор библиотек —
сохраняют список:

```text
pip freeze > requirements.txt
```

И ставят:

```text
pip install -r requirements.txt
```

Внутри файла — построчно `имя==версия`:

```text
requests==2.31.0
aiogram==3.4.1
```

### Зачем тебе это

В разделе про Telegram-бота поставим `aiogram`. Без `pip` его взять негде.

> ⚠ В нашем тренажёре нельзя устанавливать пакеты напрямую — это бы нарушило
> песочницу. Поэтому код с внешними библиотеками здесь **не запустится**, но
> понимать команды надо: ты будешь применять их у себя в терминале/IDE.
""",
    try_it_code='print("pip и venv можно потренировать только в реальном терминале — но эти команды теперь тебе знакомы.")\n',
    task_ids=(),
    xp=5,
)

L_07_api = Lesson(
    id="07-http-api",
    section_id=S7[0],
    section_title=S7[1],
    title="HTTP-запросы и API",
    body_md="""\
**API** (Application Programming Interface) — способ одной программы попросить что-то
у другой. Большинство современных API работают через HTTP — те же URL, что и у
сайтов, только в ответ приходит обычно **JSON**, а не HTML.

### Простой пример с requests

```python
import requests

r = requests.get("https://api.thecatapi.com/v1/images/search")
data = r.json()
print(data[0]["url"])
```

Что произошло:

1. `requests.get(url)` — отправили GET-запрос.
2. `r.json()` — Python сам распарсил JSON-ответ в список словарей.
3. Достали `[0]["url"]` — ссылку на картинку котика.

### GET, POST и параметры

- `GET` — «дай мне данные».
- `POST` — «прими от меня данные».

Параметры:

```python
requests.get("https://api.example.com/search", params={"q": "python"})
# превратится в https://api.example.com/search?q=python
```

POST с JSON:

```python
requests.post("https://api.example.com/users",
              json={"name": "Кирилл"})
```

### Зачем тебе это

Telegram-бот — это, по сути, программа, которая ходит в Telegram API за новыми
сообщениями и шлёт ответы туда же. Только для удобства — есть готовая библиотека
`aiogram`, которая прячет HTTP-детали.

> ⚠ В нашем тренажёре нет интернета внутри песочницы, но в реальной IDE этот код
> заработает с пакетом `requests`.
""",
    try_it_code='print("Здесь обычно требуется requests — у нас в песочнице его нет, но команда тебе уже знакома.")\n',
    task_ids=(),
    xp=5,
)


# ----- Раздел 8: Telegram-бот -----

S8 = ("08-bot", "8. Первый Telegram-бот")

L_08_create = Lesson(
    id="08-bot-create",
    section_id=S8[0],
    section_title=S8[1],
    title="Регистрируем бота у BotFather",
    body_md="""\
Бот в Telegram — это аккаунт, которым управляет программа, а не человек. Чтобы его
создать, не надо ничего изобретать — есть **специальный бот** `@BotFather`.

### Шаги

1. Откройте Telegram, найдите [@BotFather](https://t.me/BotFather), нажмите **Start**.
2. Отправьте команду `/newbot`.
3. Введите **имя** бота (любое, можно по-русски).
4. Введите **username** бота — должно заканчиваться на `bot`, например `my_first_pytrainer_bot`.
5. BotFather пришлёт **токен** — длинная строка вида `123456:ABC-DEF...`. Это **пароль**
   твоего бота.

### Береги токен

- Никогда не показывай его в репозитории, в скриншотах, в чате.
- Если случайно показал — `/revoke` у BotFather и сделай новый.

### Куда положить токен в коде

В рабочем проекте — в **переменную окружения** или в `.env`-файл, не зашивай прямо
в код:

```python
import os
TOKEN = os.environ["BOT_TOKEN"]
```

Или, если только для пробы:

```python
TOKEN = "СЮДА_ТОКЕН"
```

(потом не забыть сменить).

### Что мы сделаем дальше

Поставим библиотеку `aiogram`, напишем бота, который отвечает на любое сообщение тем
же текстом — это «эхо-бот». Минимум кода — максимум радости.
""",
    try_it_code='print("На этом уроке кода нет — нужно зайти в Telegram и поговорить с @BotFather.")\n',
    task_ids=(),
    xp=4,
)

L_08_echo = Lesson(
    id="08-bot-echo",
    section_id=S8[0],
    section_title=S8[1],
    title="Эхо-бот на aiogram",
    body_md="""\
**aiogram** — самая популярная Python-библиотека для Telegram-ботов. Под капотом —
`asyncio` (асинхронный код). Не пугайся слов: пока что просто увидим **работающий**
шаблон.

### Установка

```text
python -m venv .venv
.venv\\Scripts\\activate         # на Linux/Mac: source .venv/bin/activate
pip install aiogram
```

### Минимум кода

```python
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "СЮДА_ТОКЕН_ОТ_BOTFATHER"

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer("Привет! Я твой первый бот. Напиши что-нибудь — я повторю.")


@dp.message()
async def echo(message: Message) -> None:
    if message.text:
        await message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

### Что происходит

- `Bot(TOKEN)` — клиент, который умеет говорить с Telegram.
- `Dispatcher` — «маршрутизатор» сообщений.
- Декоратор `@dp.message(...)` — «эту функцию вызвать, когда придёт нужное сообщение».
- `CommandStart()` — фильтр на команду `/start`.
- `await message.answer(...)` — отвечаем тем же чатом.
- `dp.start_polling(bot)` — запускает «опрос» Telegram (каждые несколько секунд
  спрашиваем «есть новые сообщения?»).

### `async`/`await` — зачем

Бот может одновременно ждать ответы от Telegram и отвечать другим пользователям.
`async`/`await` — способ сказать «эта функция может ждать». Подробно — в продвинутых
уроках; пока что **достаточно скопировать** этот шаблон.

### Запуск

```text
python bot.py
```

Открой бота в Telegram, нажми Start — увидишь свою же программу в действии.
""",
    try_it_code='print("Этот код запускают в реальной системе — у нас в песочнице нет интернета и aiogram.")\n',
    task_ids=("t-bot-echo",),
    xp=8,
)

L_08_commands = Lesson(
    id="08-bot-commands",
    section_id=S8[0],
    section_title=S8[1],
    title="Команды и куда расти дальше",
    body_md="""\
К твоему боту легко добавлять команды. Каждая команда — отдельная функция:

```python
from aiogram.filters import Command


@dp.message(Command("help"))
async def on_help(message: Message) -> None:
    await message.answer(
        "Команды:\\n"
        "/start — приветствие\\n"
        "/help — этот список\\n"
        "/cat — случайный котик"
    )


@dp.message(Command("cat"))
async def on_cat(message: Message) -> None:
    import requests
    url = requests.get(
        "https://api.thecatapi.com/v1/images/search"
    ).json()[0]["url"]
    await message.answer_photo(url)
```

### Куда расти

- **Кнопки** (`InlineKeyboardMarkup`) — клавиатуры, которые появляются под сообщением.
- **Состояния FSM** — запоминать, на каком шаге диалога пользователь.
- **База данных** (`sqlite`) — чтобы пользователи и их данные «жили» между запусками.
- **Размещение бота на сервере** — чтобы он работал, когда твой ноут выключен.

### Где смотреть

- [Документация aiogram](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

### Что мы прошли

Поздравляю — ты прошёл от `print("Hello")` до запуска первого Telegram-бота.
Дальше — практика и собственные идеи. Возвращайся в «Песочницу», эксперементируй,
читай документацию. **Всё**, что мы видели в курсе, — реальные кирпичи реальных
проектов.
""",
    try_it_code=None,
    task_ids=(),
    xp=4,
)


LESSONS: tuple[Lesson, ...] = (
    L_00_what,
    L_00_print,
    L_00_errors,
    L_01_vars,
    L_01_types,
    L_01_input,
    L_02_if,
    L_02_elif,
    L_02_bool,
    L_03_lists,
    L_03_dicts,
    L_04_for,
    L_04_while,
    L_04_nested,
    L_05_def,
    L_05_args,
    L_05_lambda,
    L_06_modules,
    L_06_files,
    L_07_pip,
    L_07_api,
    L_08_create,
    L_08_echo,
    L_08_commands,
)
