import flet as ft

def main(page):
    def btn(e):
        if not txt_nome.value:
            txt_nome.error_text = "Por favor, digite seu nome"
            page.update()
        else:
            nome = txt_nome.value
            page.clean()
            page.add(ft.Text(f"Olá, {nome}!"))

    txt_nome = ft.TextField(label="Digite seu nome")

    page.add(txt_nome, ft.ElevatedButton("Enviar", on_click=btn))

ft.app(target=main)