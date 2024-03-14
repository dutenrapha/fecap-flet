import flet as ft

def main(pagina: ft.Page): #cria a funcao que nela voce vai criar o aplicativo
    pagina.title= "contador"   #cria o titulo da pagina
    pagina.vertical_alignment= ft.MainAxisAlignment.CENTER # define qaul sera o alinhamento das cois e os elas ficarao nesse caos no centro


    #cria as funcoes que sra utilizadas quando o botao for clicado

    def diminuir(d):# o d é a variavel que vai recebr a acao no botao que o usuario fizer
        caixa_texto.value= str(int(caixa_texto.value)-1) #tasfroma o valor da caixa de texto em numero depois tira 1 e destrasforma para texto de novo
        pagina.update()#atualiza a pagina

    def somar(d):
        caixa_texto.value = str(int(caixa_texto.value) +1 )
        pagina.update()

    #criar os itens que queremos no site
    botao_menos=ft.IconButton(ft.icons.REMOVE, on_click=diminuir) # cria o botao com o icon remove para ele tirar os valores
    caixa_texto = ft.TextField(value="0", width=100, text_align=ft.TextAlign.RIGHT) #cria um campo de texto para o usuario preencher, ALEM DE PASSAR AS MEDIDAS DELE E COM QUAL VALOR ELE COMECARA
    botao_mais= ft.IconButton(ft.icons.ADD, on_click=somar) # como no diminuir utiliza a fucao  somar ao o usuario clicar no botao
    txt_input = ft.TextField(hint_text="Digite seu texto aqui", width=500, autofocus=True)
    #adicionar os intens na pagina
    pagina.add(
        ft.Row([botao_menos, caixa_texto, botao_mais],alignment=ft.MainAxisAlignment.CENTER)#ele indica as coisas que serao colocadas e a ordem delas, alem de alinha a liha
    )


ft.app(target=main)#pass a funcao que sera utilizada no app nesse caso a main
