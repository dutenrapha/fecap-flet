from pydantic import BaseModel
from passlib.context import CryptContext
import flet as ft
import requests
import uvicorn

# URL base do servidor local onde o FastAPI está sendo executado
base_url = "http://127.0.0.1:8001"

# Endpoint de registro
registro_url = f"{base_url}/register"

# Endpoint de login
login_url = f"{base_url}/login"

# Contexto para encriptar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos Pydantic para entrada e saída
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Funções de solicitação HTTP POST
def send_request(url, data):
    response = requests.post(url, json=data)
    return response

# Função para lidar com a resposta da solicitação HTTP
def handle_response(response, lbl_output):
    if response.ok:
        response_data = response.json()
        lbl_output.value = response_data["mensagem"]
    else:
        lbl_output.value = f"Erro: {response.text}"
    lbl_output.update()  # Atualize o elemento da interface gráfica após a alteração

# Função para registrar um novo usuário
def register_user(name: str, email: str, password: str, lbl_output: ft.Text):
    user_data = {
        "name": name,
        "email": email,
        "password": password
    }
    response = send_request(registro_url, user_data)
    handle_response(response, lbl_output)

# Função para verificar o login do usuário
def verify_user_login(name: str, email: str, password: str):
    params = {
        "name": name,
        "email": email,
        "password": password
    }
    response = send_request(login_url, params)
    if response.ok:
        response_data = response.json()
        return response_data  # Return the entire response data
    else:
        raise Exception(f"Erro: {response.text}")

# Função para limpar a página antes de adicionar elementos
def clean_page(page: ft.Page):
    page.clean()

# Função para organizar a interface gráfica
def organize_controls(controls):
    return ft.Column(controls, alignment="center", expand=True)

# Página principal----------------------------------------------------------------------------------
def main(page: ft.Page):
    lbl_title = ft.Text("$ynaptaInvest", size=50, text_align="center", width=3000)
    lbl_output = ft.Text("", size=100, text_align="center", width=3000)

    btn_goto_register = ft.ElevatedButton(text="Registrar", on_click=lambda e: register_page(page, lbl_output))
    btn_goto_login = ft.ElevatedButton(text="Login", on_click=lambda e: goto_login_page(page, lbl_output))
    
    # Organização da interface gráfica
    main_container = ft.Column(
        controls=[
            lbl_title,
            lbl_output,
            ft.Row(controls=[btn_goto_register, btn_goto_login],
                    alignment="center", 
                    spacing=10 
                    )
        ],
        alignment="center",
        expand=True
    )

    # Adiciona contêiner principal à página
    page.add(main_container)

# Página de registro
def register_page(page: ft.Page, lbl_output: ft.Text):
    # Limpa a página antes de adicionar elementos
    page.clean()

    lbl_title = ft.Text("Registro", size=30, text_align="center", width=3000)

    def on_register_click(e):
        name = txt_name.value
        email = txt_email.value
        password = txt_password.value
        register_user(name, email, password, lbl_register_output)
        goto_confirmation_page(page, lbl_output, name, email, password)

    def on_goto_login_click(e, page, lbl_output, email, password):
        goto_login_page(page, lbl_output, email, password)
    
    # Elementos da interface gráfica
    txt_name = ft.TextField(hint_text="Nome", width=300, autofocus=True)
    txt_email = ft.TextField(hint_text="Email", width=300)
    txt_password = ft.TextField(hint_text="Senha", width=300, password=True)
    lbl_register_output = ft.Text("", size=20, text_align="center", width=3000)
    btn_register = ft.ElevatedButton(text="Registrar", on_click=on_register_click)
    btn_goto_login = ft.ElevatedButton(text="Clique caso já possua um login", on_click=lambda e: on_goto_login_click(e, page, lbl_output, txt_email.value, txt_password.value))

    # Organização da interface gráfica
    register_container = ft.Column(
        controls=[
            ft.Row(controls=[ft.Text("Nome:"), txt_name], alignment="center", expand=True),
            ft.Row(controls=[ft.Text("Email:"), txt_email], alignment="center", expand=True),
            ft.Row(controls=[ft.Text("Senha:"), txt_password], alignment="center", expand=True),
            ft.Row(controls=[btn_register], alignment="center", expand=True),
            ft.Row(controls=[btn_goto_login], alignment="center", expand=True),
            ft.Row(controls=[lbl_register_output], alignment="center", expand=True)
        ],
        alignment="center",
        expand=True
    )

    # Adiciona contêiner principal à página
    page.add(lbl_title)
    page.add(register_container)

# Página de confirmação
def goto_confirmation_page(page: ft.Page, lbl_output: ft.Text, name: str, email: str, password: str):
    clean_page(page)

    lbl_title = ft.Text("Confirmação de Registro", size=20, text_align="center", width=2500)
    lbl_register_output = ft.Text(f"Usuário {name} registrado com sucesso!", size=20, text_align="center", width=3000)
    btn_goto_login = ft.ElevatedButton(text="Ir para o Login",on_click=lambda e: goto_login_page(page, lbl_output, email, password))

    # Organização da interface gráfica na página de confirmação
    confirmation_container = organize_controls([lbl_register_output,btn_goto_login])

    # Adiciona contêiner à página
    page.add(lbl_title)
    page.add(confirmation_container)

#Pagina de login
def goto_login_page(page: ft.Page, lbl_output: ft.Text, email: str = None, password: str = None):
    clean_page(page)

    lbl_title = ft.Text("Login", size=30, text_align="center", width=3000)

    def on_login_click(e):
        email = txt_login_email.value
        password = txt_login_password.value
        response_data = verify_user_login(email, password, user_name)
        if "user_name" in response_data: 
            user_name = response_data["user_name"]
            goto_confirmation_page(page, lbl_output, user_name)
        else:
            lbl_output.value = response_data["detail"]  


    txt_login_email = ft.TextField(hint_text="Email de Login", width=300, value=email)
    txt_login_password = ft.TextField(hint_text="Senha de Login", width=300, password=True, value=password)
    btn_login = ft.ElevatedButton(text="Login", on_click=on_login_click)
    btn_goto_register = ft.ElevatedButton(text="Clique caso não possua um registro", on_click=lambda e: register_page(page, lbl_output))

    # Organização da interface gráfica
    login_container = organize_controls([
        ft.Row(controls=[ft.Text("Email de Login:"), txt_login_email], alignment="center", expand=True),
        ft.Row(controls=[ft.Text("Senha de Login:"), txt_login_password], alignment="center", expand=True),
        ft.Row(controls=[btn_login], alignment="center", expand=True),
        ft.Row(controls=[btn_goto_register], alignment="center", expand=True)
    ])

    # Adiciona contêiner principal à página
    page.add(lbl_title)
    page.add(login_container)

# Segunda página de confirmação
def goto_confirmation1_page(page: ft.Page, lbl_output: ft.Text, user_login: UserLogin):
    clean_page(page)

    lbl_title = ft.Text("Confirmação de Login", size=20, text_align="center", width=2500)
    lbl_register_output = ft.Text("", size=20, text_align="center", width=3000)
    user_name = verify_user_login(user_login, lbl_output)

    if user_name:
        lbl_output.value = f"{user_name}, Seu login foi bem-sucedido! Bem-vindo a $ynaptaInvest!"
        btn_login = ft.ElevatedButton(text="Deseja fazer outro login?", on_click=lambda e: goto_login_page(page, lbl_output))
        btn_register = ft.ElevatedButton(text="Deseja fazer outro registro?", on_click=lambda e: register_page(page, lbl_output))
        success_container = organize_controls([lbl_output, btn_register, btn_login])
        page.add(lbl_title)
        page.add(success_container)
    else:
        lbl_output.value = ("Login falhou. Verifique seu email e senha.")
        btn_login = ft.ElevatedButton(text="Voltar para o login", on_click=lambda e: goto_login_page(page, lbl_output))
        failure_container = organize_controls([lbl_output, btn_login])
        page.add(lbl_title)
        page.add(failure_container)

# Inicia o aplicativo Flet
ft.app(target=main)

# Inicia o aplicativo FastAPI
uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
