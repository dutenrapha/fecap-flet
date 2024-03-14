import flet as ft

async def main(page: ft.Page):
    page.title = "Jogo da Velha"

    game_state = await ft.http.post("/move/", json={"player": "X", "position": -1})

    async def make_move(position):
        response = await ft.http.post("/move/", json={"player": game_state["player"], "position": position})
        if response.status_code == 200:
            nonlocal game_state
            game_state = response.json()

    async def render_board():
        board = game_state["board"]
        buttons = []
        for i, cell in enumerate(board):
            buttons.append(ft.Button(
                text=cell if cell else " ",
                on_click=lambda e, i=i: make_move(i) if not game_state["winner"] and not cell else None
            ))
            if (i + 1) % 3 == 0:
                buttons.append(ft.LineBreak())
        return ft.Column(controls=buttons)

    await page.add_async(
        ft.Column(
            controls=[
                await render_board(),
                ft.Text("Vencedor: " + (game_state["winner"] if game_state["winner"] != "tie" else "Empate") if game_state["winner"] else "")
            ]
        )
    )

ft.app(main)
