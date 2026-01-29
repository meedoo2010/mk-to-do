import json
from flet import *
from plyer import notification

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

def main(page: Page):
    page.scroll = "auto"

    # تحميل المهام عند فتح التطبيق
    tasks = load_tasks()

    task_input = TextField(label="Enter a task", expand=True)
    task_list = Column()

    def refresh_task_list():
        task_list.controls.clear()
        for task in tasks:
            task_list.controls.append(
                Row(
                    [
                        Text(task),
                        IconButton(
                            icon=Icons.DELETE_ROUNDED,
                            on_click=lambda e, t=task: delete_task(t)
                        )
                    ]
                )
            )
        page.update()

    def add_task(e):
        task_name = task_input.value.strip()
        if task_name != "":
            tasks.append(task_name)
            save_tasks(tasks)
            task_input.value = ""
            refresh_task_list()

            # إشعار يظهر اسم المهمة
            notification.notify(
                title="تمت إضافة مهمة",
                message=f"✅ انت ضفت المهمة: {task_name}",
            )
    
    def delete_task(task_name):
        if task_name in tasks:
            tasks.remove(task_name)
            save_tasks(tasks)
            refresh_task_list()

    add_button = Button("Add Task", on_click=add_task)

    page.add(
        Column(
            [
                Row([task_input, add_button], alignment="spaceBetween"),
                task_list
            ]
        )
    )

    # عرض المهام الموجودة عند بدء التطبيق
    refresh_task_list()

app(main)
