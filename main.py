import json
from flet import *


TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    tasks = load_tasks()
    task_input = TextField(label="Enter a task", expand=True)
    task_list = Column()

    def refresh_task_list():
        task_list.controls.clear()
        for task in tasks:
            task_list.controls.append(
                Row(
                    [
                        Text(task, expand=True),
                        IconButton(
                            icon=icons.DELETE_ROUNDED,
                            icon_color=colors.RED,
                            on_click=lambda e, t=task: delete_task(t)
                        )
                    ]
                )
            )
        page.update()

    def add_task(e):
        task_name = task_input.value.strip()
        if task_name:
            tasks.append(task_name)
            save_tasks(tasks)
            task_input.value = ""
            refresh_task_list()

    
    def delete_task(task_name):
        if task_name in tasks:
            tasks.remove(task_name)
            save_tasks(tasks)
            refresh_task_list()

    add_button = ElevatedButton(text="Add Task", on_click=add_task)

    page.add(
        Column(
            [
                Row([task_input, add_button], alignment=MainAxisAlignment.SPACE_BETWEEN),
                task_list
            ]
        )
    )

    refresh_task_list()

app(main)
