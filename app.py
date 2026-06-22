import asyncio

import flet as ft
from click import clear
from flet import ThemeMode, Text, TextField, Column, Container, Colors, FontWeight, ElevatedButton, Row, Icon, icons, \
    border_radius, padding, Icons, FloatingActionButton, View, Alignment, ListTile, ListView, TextButton
from rich import align

from api import post_movimentacao


def main(page: ft.Page):
    page.title = "Primeiro APP"
    page.theme_mode = ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 800
    page.bgcolor = "#F5F5F5"  # Fundo cinza claro como na imagem

    def navegar(route):
        asyncio.create_task(
            page.push_route(route)
        )

    # --- COMPONENTES ---

    ultimas_encomendas = []
    list_view_ultimas = ListView()


    input_codigo = TextField(
        label="Insira o código de rastreamento",
        border_radius=15,
        bgcolor=Colors.WHITE,
        border_color=Colors.TRANSPARENT,
        filled=True
    )

    btn_acompanhar = ElevatedButton(
        "Acompanhar agora  →",
        bgcolor="#002B5B",  # Azul escuro da imagem
        color=Colors.WHITE,
        width=400,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
        on_click=lambda: navegar("/rastrear_encomenda"),
    )

    def limpar_ultimas():
        list_view_ultimas.controls.clear()
        ultimas_encomendas.clear()
        print(ultimas_encomendas)
        navegar("/")

    btn_limpar = TextButton(
        "Limpar tudo",
        width=200,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
        on_click=limpar_ultimas,
    )

    txt_destino = Text(size=15, weight=FontWeight.BOLD)
    txt_remetente = Text(size=15, weight=FontWeight.BOLD)
    txt_codigo = Text(size=22, color=Colors.BLUE_900, weight=FontWeight.BOLD)
    list_view = ListView(height=500)

    # --- ESTRUTURA DA TELA ---
    def route_change():
        page.views.clear()
        page.views.append(
            View(
                controls=[
                    # Área de Input
                    Container(
                        Column([Text("Rastrear Encomenda", weight=FontWeight.BOLD, size=36,
                                     color=Colors.BLUE_900, ),
                                Text("Gerencie suas entregas globais com precisão arquitetônica",
                                     weight=FontWeight.BOLD, ),
                                input_codigo,
                                btn_acompanhar
                                ], spacing=15),
                        padding=20
                    ),

                    # Seção de Últimas Pesquisas
                    Container(
                        Column([
                            Row([
                                Text("Últimas Pesquisas", weight=FontWeight.BOLD, size=20),
                                btn_limpar,
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                            list_view_ultimas
                        ]),
                        padding=20
                    ),

                ],
                expand=True
            )
        )
        if page.route == "/rastrear_encomenda":
            movimentacao_lista()
            page.views.append(
                View(
                    route="/rastrear_encomenda",
                    controls=[
                        ft.AppBar(
                            title="Sua Encomenda",
                            color=Colors.BLUE_900

                        ),
                        Container(
                            Column([
                                Text("Código de rastreamento", size=12, weight=FontWeight.BOLD),
                                txt_codigo,
                            ]),
                            border_radius=10,
                            bgcolor=Colors.GREY_300,
                            width=350,
                            height=100,
                            padding=15,
                            margin=10,
                            # alignment=ft.Alignment.CENTER,

                        ),

                        Container(
                            Row([
                                Container(
                                        Column([
                                            Row([
                                                ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.PRIMARY, size=20),
                                                Text("Destino", size=14, weight=FontWeight.BOLD),
                                            ]),

                                            txt_destino

                                        ]),

                                    bgcolor=Colors.GREY_300,
                                    width=180,
                                    height=105,
                                    padding=8,
                                    border_radius=15,
                                    margin=10,

                                ),
                                Container(
                                    Column([
                                        Row([
                                            ft.Icon(ft.Icons.SPEED, color=ft.Colors.PRIMARY, size=20),
                                            Text("Remetente", size=14, weight=FontWeight.BOLD),
                                        ]),

                                        txt_remetente,
                                    ]),
                                    bgcolor=Colors.GREY_300,
                                    width=150,
                                    height=105,
                                    padding=8,
                                    border_radius=15,

                                )
                                # bgcolor=Colors.GREY_300,
                            ])
                        ),
                        list_view
                    ]
                )
            )

    def movimentacao_lista():
        list_view.controls.clear()
        list_view_ultimas.controls.clear()
        ultimas_encomendas.append(input_codigo.value)

        for item in ultimas_encomendas:
            list_view_ultimas.controls.append(
                ListTile(
                    leading=Icon(Icons.EMAIL_ROUNDED),
                    title=Text(item),
                )
            )

        dados_movimentacao = post_movimentacao(input_codigo.value)
        print(dados_movimentacao)
        txt_codigo.value = dados_movimentacao["encomenda"]["codigo_rastreio"]
        txt_destino.value = dados_movimentacao["encomenda"]["remetente"]["cidade"]
        txt_remetente.value = dados_movimentacao["encomenda"]["remetente"]["nome"]


        for item in dados_movimentacao["movimentacoes"]:
            list_view.controls.append(
                ListTile(
                    leading=Icon(Icons.LOCAL_SHIPPING),
                    title=Text(item["criado_em"]),
                    subtitle=Text(f'{item["tipo"]} em {item["localizacao"]["cidade"]}'),
                )
            )

    # Voltar
    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    # Eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


ft.run(main)
