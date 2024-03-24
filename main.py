
import flet as ft
import requests
api_token = "mytoken"

def main(page: ft.Page):
    lbl_output = ft.Text("", size=100, text_align="center", width=3000)

    def on_send_click(e):
        text = txt_input.value
        response = requests.post(
            "http://gustavogranero.pythonanywhere.com/hello",
            headers={"Authorization": f"Token {api_token}"},
            json={"name": text},
        )
        if response.status_code == 200:
            output = response.json()["message"]
        else:
            output = "Erro ao processar" + str(response)

        lbl_output.value = output
        lbl_output.update()

        txt_input.value = ""
        page.update()

    txt_input = ft.TextField(hint_text="Digite seu nome aqui", width=300, autofocus=True)
    send_button = ft.ElevatedButton(text="Enviar", on_click=on_send_click)

    input_container = ft.Row(
        controls=[txt_input, send_button],
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

