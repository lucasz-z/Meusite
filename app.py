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
    pagina.bgcolor = ft.colors.GREY_50
    pagina.expand = True

    barra_visivel = False

    # Carregar a planilha com os dados
    df = carregar_dados()
    
    # Lista de códigos para o autocomplete
    codigos_sugestoes = df["CÓDIGOS NOVO"].tolist()

    #função para alterar a visibilidade da aba
    def alterar_barra(e):
        nonlocal barra_visivel
        barra_visivel = not barra_visivel
        atualizar_layout()


    conteudo = ft.Column(expand=True)

    #Funçao para mudar conteudo
    def mudar_aba(e):
        conteudo.controls.clear()
        if e.control.selected_index == 0:
            conteudo.controls.append(Blindagem())
        elif e.control.selected_index == 1:
            conteudo.controls.append(ft.Text("em breve"))
        pagina.update()

    #função de contrução
    def Blindagem():

        pagina_pequena = pagina.width <= 600
            
        # Campo de entrada para o código
        codigo_input = ft.TextField(label="Insira o Código (múltiplos códigos separados por vírgula)",width=pagina.width * 0.9 if pagina_pequena else 400, border_color= ft.colors.BLUE, hint_text= "digite o codigo aqui", border_radius=10)
        
        # Lista de sugestões que será exibida
        sugestoes_lista = ft.Column()

        # Campo para exibir os resultados
        resultado_texto = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, height=450, expand=True)
        pagina.update


        # Função para sugerir códigos com base no input do usuário
        def sugerir_codigos(e):
            input_valor = codigo_input.value.upper() # Texto digitado
            
            # Limpa a lista de sugestões
            sugestoes_lista.controls.clear()

            # Adiciona códigos compatíveis com o texto digitado
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
            codigo = [c.strip().upper() for c in codigo_input.value.split(",")]
            resultado_texto.controls.clear()

            if len(codigo) == 0 or codigo ==[""]:  # Validação para verificar se o campo não está vazio
                resultado_texto.controls.append(ft.Text("Por favor, insira um código.", color="red"))
            else:
                for codigo in codigo:
                    if codigo == "":
                        continue #pula se estiver vazio
                    
                    #consulta indivual
                    informacao = buscar_informacoes(df, codigo.upper())
                    if informacao is not None:
                        resultado_texto.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, color = ft.colors.GREEN), ft.Text(f"Código: {informacao['CÓDIGOS NOVO']}", color=ft.colors.BLACK)]),
                                    ft.Text(f"Descrição do Código: {informacao['Descrição']}", color=ft.colors.BLACK54),
                                    ft.Text(f"Blindagem: {informacao['Blindagem']}", color=ft.colors.BLACK54),
                                    ft.Text(f"Causas BT: {informacao['Causas BT']}", color=ft.colors.BLACK54),
                                    ft.Text(f"Causas BT e MT: {informacao['Causas BT e MT']}", color=ft.colors.BLACK54),
                                    ft.Text(f"Codigo Antigo: {informacao['COD Antigo']}", color=ft.colors.BLACK54)
                                ]),
                                bgcolor = ft.colors.WHITE, border = ft.border.all(1, ft.colors.GREEN_ACCENT), padding=15, margin = 10, border_radius = 8, shadow = ft.BoxShadow(blur_radius=5, spread_radius=2, color=ft.colors.BLACK12) 
                                        
                            )
                        )
                    else:
                        resultado_texto.controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.ERROR, color=ft.colors.RED_ACCENT),
                                    ft.Text(f"Código {codigo} não encontrado.", color="red")
                                ]), border= ft.border.all(1, ft.colors.RED_ACCENT), padding=10, margin=5, border_radius=8, shadow= ft.BoxShadow(blur_radius=5, spread_radius=1)
                            )
                        )
                pagina.update()
        # função botão limpar
        
        def limpar_input(e):
            codigo_input.value = ""
            sugestoes_lista.controls.clear()
            resultado_texto.controls.clear()
            pagina.update()
        
        botao_limpar = ft.ElevatedButton("Limpar", on_click=limpar_input, icon= ft.icons.CLEAR_ALL, bgcolor=ft.colors.RED_ACCENT_100)

        botao_consulta = ft.ElevatedButton("Consultar", on_click=consultar_codigo, icon= ft.icons.SEARCH, bgcolor=ft.colors.GREEN_ACCENT)
        
        #atribui a função de susgest
        codigo_input.on_change = sugerir_codigos

        #retorna o componente conforme o tamanho da tela
        return ft.Column([
            codigo_input, botao_limpar, botao_consulta,sugestoes_lista,
            resultado_texto], spacing=25, alignment= ft.MainAxisAlignment.CENTER)

    def atualizar_layout():
        pagina.controls.clear()
        botao_menu = ft.IconButton(icon=ft.icons.MENU, on_click=alterar_barra)

        #barra lateral
        rail = ft.NavigationRail(
            selected_index=0,
            label_type= ft.NavigationRailLabelType.ALL,
            group_alignment= -1.0, indicator_color= "blue",
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.SEARCH_ROUNDED, selected_icon=ft.icons.SEARCH, label="Consulta de Códigos"),
                ft.NavigationRailDestination(icon=ft.icons.PERCENT_ROUNDED, selected_icon= ft.icons.PERCENT,label = "Em breve"),
            ],
            on_change= lambda e: mudar_aba(e),
            visible= barra_visivel
        )
        #aba que sera mudada
        conteudo = ft.Column(expand=True)
        conteudo.controls.append(Blindagem())

        # Adiciona os componentes na página
        pagina.add(
            ft.Row(
                [rail,
                ft.VerticalDivider(width=1),
                conteudo] if barra_visivel else [botao_menu, conteudo],expand=True
            )
        )
        pagina.update()
    atualizar_layout()


# Executa a aplicação
ft.app(target=main)
