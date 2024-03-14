import flet
import requests

app = flet.App()

def jogar_cara_coroa(escolha):
    response = requests.get(f"http://localhost:8000/jogar/{escolha}")
    data = response.json()
    return data

@app.route("/")
def index(req, res):
    escolha_cara = flet.Button("Cara", on_click=lambda e: jogar(e, "cara"))
    escolha_coroa = flet.Button("Coroa", on_click=lambda e: jogar(e, "coroa"))
    resultado = flet.Text("", size=100, text_align="center")

    def jogar(event, escolha):
        resultado_jogo = jogar_cara_coroa(escolha)
        resultado.value = f"Resultado: {resultado_jogo['resultado']}. {resultado_jogo['mensagem']}"
        resultado.update()

    res.add(escolha_cara)
    res.add(escolha_coroa)
    res.add(resultado)

if __name__ == "__main__":
    app.run()
