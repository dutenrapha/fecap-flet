import flet as ft
from main import create_task, read_tasks, update_task, delete_task

def main(page: ft.Page):
    global app
    app = page.app

    page.title = "Lista de Tarefas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Column(
            [
                ft.Text("Tarefas:", size=20),
                ft.ListView(
                    expand=True,
                    spacing=10,
                    on_click=on_click_task,
                    data=read_tasks(),
                    item_extent=50,
                    item_builder=lambda e, i: ft.Container(
                        content=ft.Text(f"{i.title} - {i.completed}")
                    ),
                ),
                ft.TextField(hint_text="Adicione uma tarefa...", on_change=on_text_changed),
                ft.ElevatedButton("Adicionar", on_click=on_click_add_task),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

def on_text_changed(e):
    global task_input
    task_input = e.control

def on_click_task(e):
    global task_input, selected_task
    selected_task = e.control.data[e.index]
    task_input.value = selected_task.title

def on_click_add_task(e):
    global task_input
    create_task(Task(title=task_input.value, completed=False))
    task_input.value = ""

def update_task_status():
    global selected_task
    selected_task.completed = not selected_task.completed
    update_task(selected_task.title, selected_task)

if __name__ == "__main__":
    ft.app(target=main)
