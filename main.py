import flet as ft
import requests

def main(page: ft.Page):
    lbl_output = ft.Text("SEU EMOJI SORTEADO É:", size=100, text_align="center", width=3000, style={"background-color": "lightgreen", "padding": "10px", "border": "1px solid green", "border-radius": "5px"})

    def on_send_click(e):
        response = requests.get("http://localhost:8080/api/emoji")  
        sorteio_response = ""
        if response.status_code == 200:
            sorteio = response.text
            sorteio_response = sorteio
        else:
            sorteio_response = "Erro ao processar o sorteio"

        lbl_output.value = sorteio_response
        lbl_output.update()

    send_button = ft.ElevatedButton(text="Sortear Emoji", on_click=on_send_click)

    input_container = ft.Row(
        controls=[send_button],
        alignment="center",
        expand=True
    )

    main_container = ft.Column(
        controls=[lbl_output, input_container],
        alignment="center",
        expand=True
    )

    page.add(main_container)

ft.app(target=main)
