"""Курс: дерево разделов/уроков + просмотр урока + панель задач."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..content import (
    Lesson,
    Task,
    all_achievements,
    lesson_by_id,
    lessons_by_section,
    task_by_id,
)
from ..progress import ProgressStore
from ..runner import normalize_text, run_functional_check, run_user_code
from ..theme import DARK, Palette
from ..widgets.code_editor import CodeEditor
from ..widgets.markdown_view import MarkdownView


class LessonsView(QWidget):
    """Левая панель — дерево, правая — стек (приветствие / урок / задача)."""

    requested_xp = Signal(int, str)  # amount, message
    requested_lesson_xp = Signal(int, str)  # amount, lesson_id
    requested_open_term = Signal(str)

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # дерево
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumWidth(260)
        self.tree.setMaximumWidth(360)
        self.tree.itemClicked.connect(self._on_tree_clicked)

        # правая часть — стек: welcome / lesson / task
        self.right_stack = QStackedWidget()

        self.welcome_widget = self._build_welcome()
        self.lesson_widget = LessonWidget(self.store, self)
        self.task_widget = TaskWidget(self.store, self)

        self.lesson_widget.requested_open_term.connect(self.requested_open_term)
        self.lesson_widget.requested_open_task.connect(self._open_task_by_id)
        self.lesson_widget.lesson_completed.connect(self._on_lesson_done)
        self.task_widget.task_solved.connect(self._on_task_solved)
        self.task_widget.requested_open_lesson.connect(self.open_lesson)

        self.right_stack.addWidget(self.welcome_widget)
        self.right_stack.addWidget(self.lesson_widget)
        self.right_stack.addWidget(self.task_widget)

        splitter.addWidget(self.tree)
        splitter.addWidget(self.right_stack)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([280, 800])

        outer.addWidget(splitter)

        self.refresh()

    # --- public ---

    def on_show(self) -> None:
        self.refresh()

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale
        self.lesson_widget.set_theme(palette, font_scale)
        self.task_widget.set_theme(palette, font_scale)
        self.refresh_tree()

    def refresh(self) -> None:
        self.refresh_tree()
        if self.right_stack.currentWidget() is self.lesson_widget:
            self.lesson_widget.refresh()
        elif self.right_stack.currentWidget() is self.task_widget:
            self.task_widget.refresh()

    def open_lesson(self, lesson_id: str) -> None:
        lesson = lesson_by_id(lesson_id)
        if lesson is None:
            return
        self.lesson_widget.show_lesson(lesson)
        self.right_stack.setCurrentWidget(self.lesson_widget)
        self._select_tree_item(("lesson", lesson_id))

    def open_task(self, task_id: str) -> None:
        task = task_by_id(task_id)
        if task is None:
            return
        self.task_widget.show_task(task)
        self.right_stack.setCurrentWidget(self.task_widget)
        self._select_tree_item(("task", task_id))

    # --- private ---

    def _build_welcome(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(48, 48, 48, 48)
        v.setSpacing(10)
        title = QLabel("Курс «Python с нуля до Telegram-бота»")
        title.setObjectName("title")
        v.addWidget(title)
        sub = QLabel(
            "Слева — разделы. Жми на любой урок, чтобы открыть его. После уроков идут "
            "практические задачи: код запускается прямо здесь, проверка автоматическая."
        )
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        v.addWidget(sub)
        v.addStretch(1)
        return w

    def refresh_tree(self) -> None:
        self.tree.clear()
        p = self.store.progress
        for section_id, section_title, lessons in lessons_by_section():
            section_done = sum(
                1 for lesson in lessons if lesson.id in p.completed_lessons
            )
            section_label = f"{section_title}  · {section_done}/{len(lessons)}"
            section_item = QTreeWidgetItem([section_label])
            section_item.setData(0, Qt.ItemDataRole.UserRole, ("section", section_id))
            section_item.setExpanded(True)
            font = section_item.font(0)
            font.setBold(True)
            section_item.setFont(0, font)
            self.tree.addTopLevelItem(section_item)

            for lesson in lessons:
                done = "✓ " if lesson.id in p.completed_lessons else "·  "
                lesson_item = QTreeWidgetItem([f"{done}{lesson.title}"])
                lesson_item.setData(0, Qt.ItemDataRole.UserRole, ("lesson", lesson.id))
                section_item.addChild(lesson_item)

                for task_id in lesson.task_ids:
                    task = task_by_id(task_id)
                    if task is None:
                        continue
                    tdone = "✓ " if task.id in p.completed_tasks else "·  "
                    task_item = QTreeWidgetItem([f"   ⌨ {tdone}{task.title}"])
                    task_item.setData(0, Qt.ItemDataRole.UserRole, ("task", task.id))
                    lesson_item.addChild(task_item)

        for i in range(self.tree.topLevelItemCount()):
            self.tree.topLevelItem(i).setExpanded(True)

    def _select_tree_item(self, target) -> None:
        def visit(item: QTreeWidgetItem) -> bool:
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if data == target:
                self.tree.setCurrentItem(item)
                return True
            for i in range(item.childCount()):
                if visit(item.child(i)):
                    return True
            return False

        for i in range(self.tree.topLevelItemCount()):
            if visit(self.tree.topLevelItem(i)):
                return

    def _on_tree_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        kind, oid = data
        if kind == "lesson":
            self.open_lesson(oid)
        elif kind == "task":
            self.open_task(oid)
        elif kind == "section":
            item.setExpanded(not item.isExpanded())

    def _open_task_by_id(self, task_id: str) -> None:
        self.open_task(task_id)

    def _on_lesson_done(self, lesson_id: str) -> None:
        # отметим урок и наградим XP, если впервые
        if self.store.mark_lesson_done(lesson_id):
            lesson = lesson_by_id(lesson_id)
            xp = lesson.xp if lesson else 5
            self.requested_lesson_xp.emit(xp, lesson_id)
        self.refresh_tree()
        self.lesson_widget.refresh()

    def _on_task_solved(self, task_id: str) -> None:
        if self.store.mark_task_done(task_id):
            task = task_by_id(task_id)
            xp = task.xp if task else 10
            self.requested_xp.emit(xp, f"задача «{task.title}»")
        self.refresh_tree()
        self.task_widget.refresh()
        # автоматически отметим связанный урок, если все его задачи сделаны
        for lesson in self._lessons_with_task(task_id):
            if all(tid in self.store.progress.completed_tasks for tid in lesson.task_ids):
                self._on_lesson_done(lesson.id)

    def _lessons_with_task(self, task_id: str) -> list[Lesson]:
        from ..content import all_lessons

        return [lesson for lesson in all_lessons() if task_id in lesson.task_ids]


class LessonWidget(QWidget):
    """Просмотр одного урока: markdown + опц. "попробуй сам" + кнопка «Готово»."""

    lesson_completed = Signal(str)
    requested_open_term = Signal(str)
    requested_open_task = Signal(str)

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0
        self._lesson: Lesson | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(10)

        title_row = QHBoxLayout()
        self.section_label = QLabel("")
        self.section_label.setObjectName("section")
        self.section_label.setMargin(0)
        self.section_label.setStyleSheet("padding: 0 0 0 0;")
        title_row.addWidget(self.section_label)
        title_row.addStretch(1)
        outer.addLayout(title_row)

        self.title_label = QLabel("")
        self.title_label.setObjectName("title")
        outer.addWidget(self.title_label)

        self.md_view = MarkdownView()
        self.md_view.set_link_handler(self._on_link)
        outer.addWidget(self.md_view, stretch=2)

        # «Попробуй сам»
        self.try_card = QFrame()
        self.try_card.setObjectName("card")
        try_layout = QVBoxLayout(self.try_card)
        try_layout.setContentsMargins(14, 12, 14, 12)
        try_layout.setSpacing(6)
        self.try_label = QLabel("💡 Попробуй сам")
        self.try_label.setObjectName("h2")
        try_layout.addWidget(self.try_label)
        self.try_editor = CodeEditor()
        self.try_editor.setMinimumHeight(120)
        self.try_editor.setMaximumHeight(220)
        try_layout.addWidget(self.try_editor)
        try_btn_row = QHBoxLayout()
        self.try_run_btn = QPushButton("▶ Запустить")
        self.try_run_btn.setObjectName("primary")
        self.try_run_btn.clicked.connect(self._run_try_it)
        try_btn_row.addWidget(self.try_run_btn)
        try_btn_row.addStretch(1)
        try_layout.addLayout(try_btn_row)
        self.try_output = QPlainTextEdit()
        self.try_output.setObjectName("output")
        self.try_output.setReadOnly(True)
        self.try_output.setMaximumHeight(120)
        try_layout.addWidget(self.try_output)
        outer.addWidget(self.try_card)

        # tasks of this lesson
        self.tasks_card = QFrame()
        self.tasks_card.setObjectName("card")
        tasks_layout = QVBoxLayout(self.tasks_card)
        tasks_layout.setContentsMargins(14, 10, 14, 10)
        tasks_layout.setSpacing(6)
        tlabel = QLabel("⌨ Задачи к уроку")
        tlabel.setObjectName("h2")
        tasks_layout.addWidget(tlabel)
        self.tasks_box = QVBoxLayout()
        self.tasks_box.setSpacing(4)
        tasks_layout.addLayout(self.tasks_box)
        outer.addWidget(self.tasks_card)

        # bottom actions
        bottom = QHBoxLayout()
        bottom.addStretch(1)
        self.done_btn = QPushButton("Отметить пройденным ✓")
        self.done_btn.setObjectName("success")
        self.done_btn.clicked.connect(self._mark_done)
        bottom.addWidget(self.done_btn)
        outer.addLayout(bottom)

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale
        self.try_editor.set_theme_dark(palette.name == "dark")
        if self._lesson:
            self.md_view.set_markdown(self._lesson.body_md, palette, font_scale)

    def refresh(self) -> None:
        if self._lesson is None:
            return
        # обновим состояние кнопок задач
        self._render_tasks(self._lesson)
        self._update_done_btn()

    def show_lesson(self, lesson: Lesson) -> None:
        self._lesson = lesson
        self.section_label.setText(lesson.section_title)
        self.title_label.setText(lesson.title)
        self.md_view.set_markdown(lesson.body_md, self._palette, self._font_scale)
        if lesson.try_it_code:
            self.try_card.show()
            self.try_editor.setPlainText(lesson.try_it_code)
            self.try_output.clear()
        else:
            self.try_card.hide()

        if lesson.task_ids:
            self.tasks_card.show()
            self._render_tasks(lesson)
        else:
            self.tasks_card.hide()

        self._update_done_btn()

    def _render_tasks(self, lesson: Lesson) -> None:
        # очищаем старые
        while self.tasks_box.count():
            item = self.tasks_box.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        p = self.store.progress
        for task_id in lesson.task_ids:
            task = task_by_id(task_id)
            if task is None:
                continue
            row = QHBoxLayout()
            done = "✓ " if task.id in p.completed_tasks else "· "
            label = QLabel(f"{done}{task.title}")
            row.addWidget(label, stretch=1)
            btn = QPushButton("Открыть")
            btn.setObjectName("primary")
            btn.clicked.connect(lambda _=False, tid=task.id: self.requested_open_task.emit(tid))
            row.addWidget(btn)
            wrap = QWidget()
            wrap.setLayout(row)
            self.tasks_box.addWidget(wrap)

    def _update_done_btn(self) -> None:
        if self._lesson is None:
            return
        if self._lesson.id in self.store.progress.completed_lessons:
            self.done_btn.setText("✓ Урок пройден")
            self.done_btn.setEnabled(False)
        else:
            self.done_btn.setText("Отметить пройденным ✓")
            self.done_btn.setEnabled(True)

    def _mark_done(self) -> None:
        if self._lesson is None:
            return
        self.lesson_completed.emit(self._lesson.id)

    def _run_try_it(self) -> None:
        code = self.try_editor.toPlainText()
        result = run_user_code(code, timeout=5.0)
        out = result.stdout
        if result.stderr:
            out = (out + ("\n" if out and not out.endswith("\n") else "") + result.stderr)
        if not out.strip():
            out = "(пустой вывод)"
        self.try_output.setPlainText(out)

    def _on_link(self, target: str) -> None:
        if target.startswith("term:"):
            self.requested_open_term.emit(target.split(":", 1)[1])
        elif target.startswith("task:"):
            self.requested_open_task.emit(target.split(":", 1)[1])


class TaskWidget(QWidget):
    """Решение одной задачи: описание + редактор + вывод + кнопки."""

    task_solved = Signal(str)
    requested_open_lesson = Signal(str)

    def __init__(self, store: ProgressStore, parent=None) -> None:
        super().__init__(parent)
        self.store = store
        self._palette: Palette = DARK
        self._font_scale = 1.0
        self._task: Task | None = None
        self._hint_index = 0
        self._solution_revealed = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 18, 24, 18)
        outer.setSpacing(10)

        head_row = QHBoxLayout()
        self.label_back = QLabel("⌨ Задача")
        self.label_back.setObjectName("section")
        self.label_back.setStyleSheet("padding: 0;")
        head_row.addWidget(self.label_back)
        head_row.addStretch(1)
        outer.addLayout(head_row)

        self.title_label = QLabel("")
        self.title_label.setObjectName("title")
        outer.addWidget(self.title_label)

        # верх — описание (markdown), низ — редактор + вывод
        v_split = QSplitter(Qt.Orientation.Vertical)
        outer.addWidget(v_split, stretch=1)

        self.desc_view = MarkdownView()
        v_split.addWidget(self.desc_view)

        bottom = QWidget()
        bv = QVBoxLayout(bottom)
        bv.setContentsMargins(0, 0, 0, 0)
        bv.setSpacing(6)

        h_split = QSplitter(Qt.Orientation.Horizontal)
        self.editor = CodeEditor()
        self.editor.textChanged.connect(self._on_editor_changed)
        h_split.addWidget(self.editor)

        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(6)
        rv.addWidget(QLabel("Вывод программы:"))
        self.output = QPlainTextEdit()
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        rv.addWidget(self.output, stretch=1)
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusInfo")
        sl = QHBoxLayout(self.status_frame)
        sl.setContentsMargins(10, 6, 10, 6)
        self.status_label = QLabel("Готов проверить решение.")
        self.status_label.setWordWrap(True)
        sl.addWidget(self.status_label)
        rv.addWidget(self.status_frame)
        h_split.addWidget(right)
        h_split.setStretchFactor(0, 1)
        h_split.setStretchFactor(1, 1)

        bv.addWidget(h_split, stretch=1)

        # buttons row
        buttons = QHBoxLayout()
        self.btn_run = QPushButton("▶ Запустить")
        self.btn_run.setObjectName("primary")
        self.btn_run.clicked.connect(self._on_run)
        buttons.addWidget(self.btn_run)

        self.btn_check = QPushButton("✓ Проверить")
        self.btn_check.setObjectName("success")
        self.btn_check.clicked.connect(self._on_check)
        buttons.addWidget(self.btn_check)

        self.btn_hint = QPushButton("💡 Подсказка")
        self.btn_hint.clicked.connect(self._on_hint)
        buttons.addWidget(self.btn_hint)

        self.btn_solution = QPushButton("📖 Показать решение")
        self.btn_solution.setObjectName("ghost")
        self.btn_solution.clicked.connect(self._on_solution)
        buttons.addWidget(self.btn_solution)

        self.btn_reset = QPushButton("Сбросить")
        self.btn_reset.setObjectName("ghost")
        self.btn_reset.clicked.connect(self._on_reset)
        buttons.addWidget(self.btn_reset)

        buttons.addStretch(1)
        bv.addLayout(buttons)

        v_split.addWidget(bottom)
        v_split.setStretchFactor(0, 0)
        v_split.setStretchFactor(1, 1)
        v_split.setSizes([180, 480])

    def set_theme(self, palette: Palette, font_scale: float) -> None:
        self._palette = palette
        self._font_scale = font_scale
        self.editor.set_theme_dark(palette.name == "dark")
        if self._task:
            self.desc_view.set_markdown(self._task.description_md, palette, font_scale)

    def refresh(self) -> None:
        if self._task is None:
            return
        self._update_status_done_state()

    def show_task(self, task: Task) -> None:
        self._task = task
        self._hint_index = 0
        self._solution_revealed = False
        self.title_label.setText(task.title)
        self.desc_view.set_markdown(task.description_md, self._palette, self._font_scale)
        saved = self.store.get_task_code(task.id)
        self.editor.setPlainText(saved if saved is not None else task.starter_code)
        self.output.clear()
        self._set_status("Готов проверить решение.", "info")
        self.btn_solution.setText("📖 Показать решение")
        self.btn_solution.setObjectName("ghost")
        self.btn_solution.style().unpolish(self.btn_solution)
        self.btn_solution.style().polish(self.btn_solution)
        self.btn_hint.setEnabled(bool(task.hints))
        self._update_status_done_state()

    def _update_status_done_state(self) -> None:
        if self._task and self._task.id in self.store.progress.completed_tasks:
            self._set_status("Эта задача уже решена. Можно перезапустить и сравнить с решением.", "ok")

    def _on_editor_changed(self) -> None:
        if self._task:
            self.store.save_task_code(self._task.id, self.editor.toPlainText())

    def _on_run(self) -> None:
        if self._task is None:
            return
        code = self.editor.toPlainText()
        result = run_user_code(code, timeout=5.0)
        text = result.stdout
        if result.stderr:
            text = (text + ("\n" if text and not text.endswith("\n") else "") + result.stderr)
        if not text.strip():
            text = "(пустой вывод)"
        self.output.setPlainText(text)

    def _on_check(self) -> None:
        if self._task is None:
            return
        code = self.editor.toPlainText()
        all_ok = True
        first_fail = ""
        outputs: list[str] = []
        for test in self._task.tests:
            ok, message = self._run_one_test(code, test)
            outputs.append(f"• {test.name}: {'OK' if ok else 'НЕ ПРОШЛА'}")
            if not ok and not first_fail:
                first_fail = message
            if not ok:
                all_ok = False
        self.output.setPlainText(
            "\n".join(outputs) + ("" if all_ok else "\n\n" + first_fail)
        )
        if all_ok:
            self._set_status("✓ Решение принято! Молодец.", "ok")
            self.task_solved.emit(self._task.id)
        else:
            self._set_status(
                "Не сходится. Посмотри подсказку или жми «Показать решение».", "bad"
            )

    def _run_one_test(self, code: str, test) -> tuple[bool, str]:
        if test.kind == "stdio":
            res = run_user_code(code, stdin=test.stdin, timeout=5.0)
            if res.timed_out:
                return False, "Превышен таймаут — может быть бесконечный цикл."
            if res.return_code != 0 and res.stderr.strip():
                return False, f"Ошибка при запуске:\n{res.stderr.strip()}"
            got = normalize_text(res.stdout)
            expected = normalize_text(test.expected_stdout)
            if got != expected:
                return False, (
                    f"Вывод не совпадает.\nОжидалось:\n{expected}\n\nПолучилось:\n{got}"
                )
            return True, "OK"
        elif test.kind == "functional":
            return run_functional_check(
                code,
                test.function,
                [(test.args, test.kwargs, test.expected)],
                timeout=5.0,
            )
        return False, f"Неизвестный тип теста: {test.kind}"

    def _on_hint(self) -> None:
        if self._task is None or not self._task.hints:
            return
        if self._hint_index >= len(self._task.hints):
            self._set_status(
                "Подсказки закончились — попробуй «Показать решение».", "info"
            )
            return
        hint = self._task.hints[self._hint_index]
        self._hint_index += 1
        self._set_status(f"💡 {hint}", "info")

    def _on_solution(self) -> None:
        if self._task is None:
            return
        if not self._solution_revealed:
            self.editor.setPlainText(self._task.solution_code)
            self._solution_revealed = True
            self.btn_solution.setText("📖 Скрыть разбор")
            text = "## Решение\n\n```python\n" + self._task.solution_code + "\n```\n\n"
            text += "## Почему так\n\n" + self._task.solution_explanation_md
            self.desc_view.set_markdown(text, self._palette, self._font_scale)
        else:
            self.btn_solution.setText("📖 Показать решение")
            self._solution_revealed = False
            self.desc_view.set_markdown(
                self._task.description_md, self._palette, self._font_scale
            )

    def _on_reset(self) -> None:
        if self._task is None:
            return
        self.editor.setPlainText(self._task.starter_code)
        self.output.clear()
        self._set_status("Сбросили на стартовый код.", "info")

    def _set_status(self, text: str, kind: str) -> None:
        if kind == "ok":
            self.status_frame.setObjectName("statusOk")
        elif kind == "bad":
            self.status_frame.setObjectName("statusBad")
        else:
            self.status_frame.setObjectName("statusInfo")
        self.status_frame.style().unpolish(self.status_frame)
        self.status_frame.style().polish(self.status_frame)
        self.status_label.setText(text)


# подгрузим достижения, чтобы при первом импорте ничего не упало
_ = all_achievements
