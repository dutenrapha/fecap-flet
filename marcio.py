import flet as ft
import random

def main(página: ft.Página):
    número_aleatório = random.randint(1, 100)
    tentativas = 0

    def ao_texto_alterado(e):
        nonlocal tentativas
        tentativas += 1
        palpite_do_usuário = int(e.control.valor)

        if palpite_do_usuário < número_aleatório:
            texto_do_resultado.valor = "Muito baixo! Tente novamente."
        elif palpite_do_usuário > número_aleatório:
            texto_do_resultado.valor = "Muito alto! Tente novamente."
        else:
            texto_do_resultado.valor = f"Parabéns! Você encontrou o número em {tentativas} tentativas."
            e.control.desabilitado = True

    página.título = "Jogo de Adivinhação de Números"
    página.alinhamento_vertical = ft.MainAxisAlignment.CENTRO

    página.adicionar(
        ft.Coluna(
            [
                ft.Texto("Adivinhe um número entre 1 e 100.", tamanho=20),
                ft.CaixaDeTexto(
                    texto_dica="Digite seu palpite aqui...",
                    ao_alterar=ao_texto_alterado,
                ),
                ft.Texto(valor="", ref=texto_do_resultado),
            ],
            alinhamento=ft.MainAxisAlignment.CENTRO,
        )
    )

if __name__ == "__main__":
    ft.aplicativo(alvo=main)
