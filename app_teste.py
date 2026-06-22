import asyncio

import flet as ft
from flet import ThemeMode, Text, TextField, Column, Container, Colors, FontWeight, ElevatedButton, Row, Icon, icons, \
    border_radius, padding, Icons, FloatingActionButton, View


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
    text = Text()

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
                                     weight=FontWeight.BOLD, ), input_codigo, btn_acompanhar], spacing=15),
                        padding=20
                    ),

                    # Seção de Últimas Pesquisas
                    Container(
                        Column([
                            Row([
                                Text("Últimas Pesquisas", weight=FontWeight.BOLD, size=20),
                                Text("Limpar tudo", color=Colors.ORANGE_700, size=12, weight=FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        ]),
                        padding=20
                    ),
                ],
                expand=True

            )
        )
        if page.route == "/rastrear_encomenda":
            page.views.append(
                View(
                    route="/rastrear_encomenda",
                    controls=[
                        ft.AppBar(
                            title="Rastrear Encomenda",

                        ),
                    ],
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
