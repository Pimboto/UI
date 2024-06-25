import flet as ft
import json
from components import create_navigation_rail, create_cards, create_connection_settings, create_table, create_buttons, create_account_settings
    
def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.LIGHT



    page.appbar = ft.CupertinoAppBar(
        border=ft.border.only(bottom=ft.border.BorderSide(1.5, "#dce4e4")),
        middle=ft.Text("iOS Tinder Bot"),
    )

    def load_data():
        with open('data.json') as f:
            return json.load(f)

    data = load_data()

    def update_content(selected_index):
        if selected_index == 0:
            content = ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Phone Content"),
                            ft.Text("Phone Content1"),
                            ft.Text("Phone Content2")
                        ],
                        alignment=ft.MainAxisAlignment.START, 
                        expand=True
                    ),
                    ft.Column(
                        [
                            ft.Text("Phone Content"),
                            ft.Text("Phone Content1"),
                            ft.Text("Phone Content2")
                        ],
                        expand=True
                    ),
                    ft.VerticalDivider(width=1.5),
                    create_cards()
                ],
                expand=True,
            )
        elif selected_index == 2:
            content = create_connection_settings(page)
        elif selected_index == 3:
            def update_table():
                nonlocal data
                data = load_data()
                content_area.content = ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    create_table(data),
                                ],
                                alignment=ft.CrossAxisAlignment.CENTER, 
                                expand=True,
                                scroll=ft.ScrollMode.HIDDEN
                            ),
                            alignment=ft.alignment.center,
                            expand=True
                        ),
                        ft.VerticalDivider(width=1.5),
                        create_buttons(page, update_table),  
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER
                )
                page.update()

            content = ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                create_table(data),
                            ],
                            alignment=ft.CrossAxisAlignment.CENTER, 
                            expand=True,
                            scroll=ft.ScrollMode.HIDDEN
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.VerticalDivider(width=1.5),
                    create_buttons(page, update_table),  
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            )
        elif selected_index == 1:
            content = create_account_settings(page)
        return content

    content_area = ft.Container(content=update_content(0), expand=True)

    def update_body(selected_index):
        new_content = update_content(selected_index)
        content_area.content = new_content
        page.update()

    rail = create_navigation_rail(on_change=lambda e: update_body(e.control.selected_index))

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1.5),
                content_area
            ],
            expand=True,
        )
    )

ft.app(target=main)
