import flet as ft
from flet.core.types import WEB_BROWSER, CrossAxisAlignment


def main(page: ft.Page):
    page.title = "Avaliador de risco de DM2"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.padding = ft.padding.all(50)
    # variável que armazena mensagem que será exibida ao usuário no fim
    mensagem = ft.Text("", weight=ft.FontWeight.BOLD)

    # componentes da interface
    # opções para o usuário selecionar idade
    idade = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="menosDe45", label="Menos de 45"),
        ft.Radio(value="45a54", label="Entre 45 e 54"),
        ft.Radio(value="54a64", label="Entre 54 e 64"),
        ft.Radio(value="maisDe64", label="Mais de 64")
    ]))

    # opções para o usuário selecionar imc
    imc = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="menos25", label="Menos que 25kg/m²"),
        ft.Radio(value="25a30", label="Entre 25-30kg/m²"),
        ft.Radio(value="mais30", label="Maior do que 30kg/m²")
    ]))

    selected_sexo = ft.Text() # variavel para armazenar seleção do sexo

    # pergunta ao usuário qual sua circunferência abdominal
    circunferencia = ft.Text(
        "Qual sua circunferência abdominal medida abaixo da costela?",
        weight=ft.FontWeight.BOLD,
        visible= False
    )

    # grupos de radio ocultos
    # opções de circunferência abdominal para mulheres
    abdome_m = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="menos80", label="Menor que 80 cm"),
        ft.Radio(value="80a88", label="Entre 80 e 88 cm"),
        ft.Radio(value="mais88", label="Maior que 88 cm")
    ]),
        visible=False
    )

    # opções de circunferência abdominal para homens
    abdome_h = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="menos94", label="Menor que 94 cm"),
        ft.Radio(value="94a102", label="Entre 94 e 102 cm"),
        ft.Radio(value="mais102", label="Maior que 102 cm")
    ]),
        visible=False
    )

    # função para atualizar as opções dependendo do sexo selecionado
    def on_sexo_change(e):
        escolha = e.control.value

        circunferencia.visible = True

        if escolha == "f":
            abdome_m.visible = True
        elif escolha == "m":
            abdome_h.visible = True

        page.update()

    # opções para usuário selecionar o sexo
    sexo = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="f", label="Feminino"),
        ft.Radio(value="m", label="Masculino")
    ]),
        on_change=on_sexo_change,
    )

    # opções para usuário selecionar se pratica exercicios fisicos
    exerciciof = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="sim", label="Sim"),
        ft.Radio(value="nao", label="Nao")
    ]))

    # opções para usuário selecionar se consome vegetais e frutas
    alimentacao = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="sempre", label="Todos os dias"),
        ft.Radio(value="asvezes", label="Nem todo dia")
    ]))

    # opções para usuário selecionar se faz uso de medicação para pressão alta
    has = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="sim", label="Sim"),
        ft.Radio(value="nao", label="Não")
    ])
    )

    # opções para usuário selecionar se já teve glicemia alta
    hiperglicemia = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="sim", label="Sim"),
        ft.Radio(value="nao", label="Não")
    ]))

    # variável que armazena opção selecionada pelo usuário sobre histórico familiar de diabetes
    historico_selecionado = ft.Text()

    # pergunta exibida ao usuário CASO ele tenha marcado 'sim' para histórico familiar de diabetes
    grau_f = ft.Text(
        "Selecione o grau de parentesco:",
        weight = ft.FontWeight.BOLD,
        visible = False
    )

    # função para exibir opções de grau de parentesco caso o usuário tenha marcado 'sim' para histórico familiar de diabetes
    def on_familia_change(e):
        escolhido = e.control.value

        grau_f.visible = True
        familia.visible = False

        if escolhido == "sim":
            familia.visible = True
            grau_f.visible = True

        page.update()

    # opções para usuário selecionar se possui histórico familiar de diabetes
    historico_f = ft.RadioGroup(ft.Column([
        ft.Radio(value="sim", label="Sim"),
        ft.Radio(value="nao", label="Não")
    ]),
        on_change=on_familia_change
    )

    # opções para o usuário selecionar grau de parentesco no caso de haver histórico familiar
    familia = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="1ograu", label="Pais, irmãos ou filhos"),
        ft.Radio(value="2ograu", label="Avós ou tios")
    ]),
        visible=False
    )

    # funções auxiliares
    def avaliar_idade(value): return {"45a54": 2, "54a64": 3, "maisDe64": 4}.get(value,0)
    def avaliar_imc(value): return {"25a30": 1, "mais30": 3}.get(value, 0)
    def avaliarcircunferencia_m(value): return {"80a88": 3, "mais88": 4}.get(value, 0)
    def avaliarcircunferencia_h(value): return {"94a102": 3, "mais102": 4}.get(value, 0)
    def avaliar_ativfis(value): return 2 if value == "nao" else 0
    def avaliar_alimentacao(value): return 2 if value == "asvezes" else 0
    def avaliar_has(value): return 2 if value == "sim" else 0
    def avaliar_glicemia(value): return 2 if value == "sim" else 0
    def avaliarfamilia(value): return {"1ograu": 5, "2ograu": 3}.get(value, 0)

    # função para realizar o calculado de risco de desenvolver dm2 com base nos dados informados pelo usuário
    def calcular_risco():
        risco = 0

        risco += avaliar_idade(idade.value)
        risco += avaliar_imc(imc.value)
        risco += avaliarcircunferencia_m(abdome_m.value)
        risco += avaliarcircunferencia_h(abdome_h.value)
        risco += avaliar_ativfis(exerciciof.value)
        risco += avaliar_alimentacao(alimentacao.value)
        risco += avaliar_has(has.value)
        risco += avaliar_glicemia(hiperglicemia.value)
        risco += avaliarfamilia(familia.value)
        return risco

    def onclick(e):
        if ( # verificar se não há nenhum campo sem ser selecionado
            idade.value is None
            or imc.value is None
            or sexo.value is None
            or (sexo.value == "f" and abdome_m.value is None)
            or (sexo.value == "m" and abdome_h.value is None)
            or exerciciof.value is None
            or alimentacao.value is None
            or has.value is None
            or hiperglicemia.value is None
            or historico_f.value is None
        ):
            mensagem.value = "Você precisa preencher todos os campos para que o risco seja calculado corretamente."
            page.update()
            return

        risco = calcular_risco()

       # mensagem que é exibida ao usuário informando-o sobre o seu risco de desenvolver a dm2
        if risco < 7:
            mensagem.value = f'Sua pontuação é {risco}. Isso significa que você possui um baixo risco de desenvolver DM2 nos próximos 10 anos.'
        elif 7 <= risco <= 11:
            mensagem.value = f'Sua pontuação é {risco}. Isso significa que você possui um risco um pouco elevado de desenvolver DM2 nos próximos 10 anos.'
        elif 12 <= risco <= 14:
            mensagem.value = f'Sua pontuação é {risco}. Isso significa que você possui um risco moderado de desenvolver DM2 pelos próximos 10 anos.'
        elif 15 <= risco <= 20:
            mensagem.value = f'Sua pontuação é {risco}. Isso significa que você possui um risco alto em desenvolver DM2 pelos próximos 10 anos.'
        else:
            mensagem.value = f'Sua pontuação é {risco}. Isso significa que você possui um risco muito alto em desenvolver a DM2.'

        page.update()


   # layout da interface
    page.add(
        ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            controls=[
                ft.Text("Avaliador de risco de Diabetes Mellitus 2 (DM2)", size=20, color="blue", weight=ft.FontWeight.BOLD),
                ft.Text("A diabetes mellitus tipo 2 é uma doença metabólica que ocorre quando o corpo não aproveita adequadamente a insulina produzida. "
                        "Um diagnóstico precoce é importante para evitar complicações."),
                ft.Text("Este teste calcula o risco do indivíduo desenvolver DM2 dentro de 10 anos baseado em seu estilo de vida e histórico familiar."),
                ft.Text("Qual a sua idade?", weight=ft.FontWeight.BOLD),
                idade,
                ft.Text("Qual o seu IMC?", weight=ft.FontWeight.BOLD),
                ft.Text("*Para calcular o seu IMC basta dividir o seu peso por sua altura elevada ao quadrado."),
                imc,
                ft.Text("Qual seu sexo?", weight=ft.FontWeight.BOLD),
                sexo,
                selected_sexo,
                circunferencia,
                abdome_m,
                abdome_h,
                ft.Text("Você faz ao menos 30 minutos de exercícios físicos no trabalho e/ou em seu tempo livre (incluindo suas atividades normais diárias)?", weight=ft.FontWeight.BOLD),
                exerciciof,
                ft.Text("Com que frequência você come legumes, frutas ou sementes?", weight=ft.FontWeight.BOLD),
                alimentacao,
                ft.Text("Você faz uso de medicamento para a pressão alta?", weight=ft.FontWeight.BOLD),
                has,
                ft.Text("Já teve a glicemia alta?", weight=ft.FontWeight.BOLD),
                hiperglicemia,
                ft.Text("Possui histórico familiar?", weight=ft.FontWeight.BOLD),
                historico_f,
                historico_selecionado,
                grau_f,
                familia,
                ft.ElevatedButton(text="Finalizar", on_click=onclick, width=200),
                mensagem,
            ]
        )
    )

ft.app(main, view=WEB_BROWSER)