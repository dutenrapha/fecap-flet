import flet as ft
import time

def main(page: ft.Page):
    t = ft.Text(value="sistema de tempo", color="Blue")
    page.controls.append(t)
    page.update()

    for i in range(10000):
        t.value = f"Contagem {i} segundos"
        page.update()
        time.sleep(1)

    page.update()

ft.app(target=main)