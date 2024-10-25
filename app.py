import flet as ft
import pandas as pd

# Função para carregar a planilha Excel
def carregar_dados():
    # Carrega a planilha do excel
    df = pd.read_excel("codigos.xlsx")
    return df

# Função para buscar informações do código
def buscar_informacoes(df, codigo):
    # Filtra para encontrar o código
    resultado = df[df["CÓDIGOS NOVO"] == codigo]

    if not resultado.empty:
        return resultado.iloc[0]  # Retorna a primeira linha encontrada
    else:
        return None

# Função principal
def main(pagina: ft.Page):
    pagina.title = "Consulta de Códigos - Blindagem"
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Carregar a planilha com os dados
    df = carregar_dados()
    
    # Lista de códigos para o autocomplete
    codigos_sugestoes = df["CÓDIGOS NOVO"].tolist()

    #Funçao para mudar conteudo

    def mudar_aba(e):
        conteudo.controls.clear()
        if e.control.selected_index == 0:
            conteudo.controls.append(Blindagem())
        elif e.control.selected_index == 1:
            conteudo.controls.append(ft.Text("% avalidar"))
        pagina.update()

    #função de contrução
    def Blindagem():
            
        # Campo de entrada para o código
        codigo_input = ft.TextField(label="Insira o Código (múltiplos códigos separados por vírgula)",width=400, border_color= ft.colors.BLUE, hint_text= "digite o codigo aqui")
        
        # Lista de sugestões que será exibida
        sugestoes_lista = ft.Column()

        # Campo para exibir os resultados
        resultado_texto = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Função para sugerir códigos com base no input do usuário
        def sugerir_codigos(e):
            input_valor = e.control.value.upper() # Texto digitado
            pagina.update()
            
            # Limpa a lista de sugestões
            sugestoes_lista.controls.clear()

            # Adiciona códigos compatíveis com o texto digitado
            input_valor = codigo_input.value.upper()
            for codigo in codigos_sugestoes:
                if codigo.upper().startswith(input_valor):
                    sugestoes_lista.controls.append(
                        ft.TextButton(
                            codigo,
                            on_click=lambda e, codigo=codigo: selecionar_codigo(codigo)
                        )
                    )
            pagina.update()  # Atualiza a página para mostrar as sugestões

        # Função para ser chamada ao clicar em uma sugestão
        def selecionar_codigo(codigo):
            # Preenche o campo de texto com o código selecionado
            codigo_input.value = codigo
            sugestoes_lista.controls.clear()  # Limpa as sugestões
            pagina.update()  # Atualiza a página

        # exibir notificação
        def mostrar_alerta(mensagem, tipo = "info"):
            cor = ft.colors.BLUE if tipo == "info" else ft.colors.RED_ACCENT
            pagina.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=cor)
            pagina.snack_bar.open = True
            pagina.update()
        
        # Função para ser chamada ao clicar no botão "Consultar"
        def consultar_codigo(e):
            codigo = codigo_input.value.split(",")
            resultado_texto.controls.clear()

            if len(codigo) == 0 or codigo ==[""]:  # Validação para verificar se o campo não está vazio
                resultado_texto.controls.append(ft.Text("Por favor, insira um código.", color="red"))
            else:
                for codigo in codigo:
                    codigo = codigo.strip() #remove espaços
                    if codigo == "":
                        continue #pula se estiver vazio
                    
                    #consulta indivual
                    informacao = buscar_informacoes(df, codigo)
                    if informacao is not None:
                        # Adiciona as informações do código na interface
                        resultado_texto.controls.append(ft.Text(f"Código: {informacao['CÓDIGOS NOVO']}", color= "black"))
                        resultado_texto.controls.append(ft.Text(f"Descrição do Código: {informacao['Descrição']}"))
                        resultado_texto.controls.append(ft.Text(f"Blindagem: {informacao['Blindagem']}"))
                        resultado_texto.controls.append(ft.Text(f"Causas BT: {informacao['Causas BT']}"))
                        resultado_texto.controls.append(ft.Text(f"Causas BT e MT: {informacao['Causas BT e MT']}"))
                        resultado_texto.controls.append(ft.Divider())
                    else:
                        resultado_texto.controls.append(ft.Text("Codigo não encontrado, por favor verifique o *S* Maiusculo inicial ou *-* entre o codigo", color="red"))

                #Atualiza a página com os resultados
                pagina.update()

        # função botão limpar
        
        def limpar_input(e):
            codigo_input.value = ""
            sugestoes_lista.controls.clear()
            resultado_texto.controls.clear()
            pagina.update()
        
        
        
        #atribui a função de susgest
        codigo_input.on_change = sugerir_codigos

        return ft.Column([
            ft.Row(
                controls=[codigo_input,
                ft.ElevatedButton( "limpar", on_click = limpar_input, icon= ft.icons.CLEAR, bgcolor= ft.colors.RED_ACCENT_100),
                ], alignment= ft.MainAxisAlignment.CENTER,
            
            ),
            ft.ElevatedButton("consultar",on_click= consultar_codigo, icon= ft.icons.SEARCH, bgcolor= ft.colors.WHITE10),
            sugestoes_lista,
            resultado_texto], spacing=20, alignment= ft.MainAxisAlignment.CENTER)

    #barra lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type= ft.NavigationRailLabelType.ALL,
        group_alignment= -0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.SEARCH_ROUNDED, selected_icon=ft.icons.SEARCH, label="Consulta de Códigos"),
            ft.NavigationRailDestination(icon=ft.icons.PERCENT_ROUNDED, selected_icon= ft.icons.PERCENT,label = "% avalidar"),
        ],
        on_change= mudar_aba
    )
    #aba que sera mudada
    conteudo = ft.Column(expand=True)
    conteudo.controls.append(Blindagem())

    # Adiciona os componentes na página
    pagina.add(
        ft.Row(
            [rail,
            ft.VerticalDivider(width=1),
            conteudo],
            expand=True
        )
    )

# Executa a aplicação
ft.app(target=main)
