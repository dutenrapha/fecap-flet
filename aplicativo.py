import flet as ft
import random

def main(page: ft.Page):
    page.title = "Jokenpô"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    lbl_output = ft.Text("", size=50, text_align="center", width=3000)

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def play_jokenpo(escolha_jogador):
        escolhas = ["Pedra", "Papel", "Tesoura"]
        computador = random.choice(escolhas)

        if escolha_jogador == computador:
            return "Empate! Ambos escolheram " + escolha_jogador
        elif (escolha_jogador == "Pedra" and computador == "Tesoura") or \
             (escolha_jogador == "Papel" and computador == "Pedra") or \
             (escolha_jogador == "Tesoura" and computador == "Papel"):
            return "Você venceu! " + escolha_jogador + " ganha de " + escolha_jogador
        else:
            return "Você perdeu! " + computador + " ganha de " + escolha_jogador

    def on_send_click(e):
        escolha_jogador = txt_input.value.strip().capitalize()
        if escolha_jogador not in ["Pedra", "Papel", "Tesoura"]:
            lbl_output.value = "Escolha inválida! Por favor, escolha Pedra, Papel ou Tesoura."
        else:
            result = play_jokenpo(escolha_jogador)
            lbl_output.value = result

        lbl_output.value = result
        lbl_output.update()

        txt_input.value = ""
        page.update()

    txt_input = ft.TextField(hint_text="Digite sua jogada aqui", width=300, autofocus=True)
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