import flet as ft
import json
import subprocess
import re
import asyncio
from components import create_navigation_rail, create_cards, create_connection_settings, create_table, create_buttons, create_account_settings

# Diccionario de mapeo de identificadores de producto a nombres de modelos específicos
MODEL_MAP = {
    "iPhone10,1": "iPhone 8",
    "iPhone10,2": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X (GSM)",
    "iPhone10,4": "iPhone 8",
    "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,6": "iPhone X (Global)",
    "iPhone11,2": "iPhone XS",
    "iPhone11,4": "iPhone XS Max",
    "iPhone11,6": "iPhone XS Max",
    "iPhone11,8": "iPhone XR",
    "iPhone12,1": "iPhone 11",
    "iPhone12,3": "iPhone 11 Pro",
    "iPhone12,5": "iPhone 11 Pro Max",
    "iPhone12,8": "iPhone SE (2nd generation)",
    "iPhone13,1": "iPhone 12 mini",
    "iPhone13,2": "iPhone 12",
    "iPhone13,3": "iPhone 12 Pro",
    "iPhone13,4": "iPhone 12 Pro Max",
    "iPhone14,4": "iPhone 13 mini",
    "iPhone14,5": "iPhone 13",
    "iPhone14,2": "iPhone 13 Pro",
    "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,6": "iPhone SE (3rd generation)",
    "iPhone15,2": "iPhone 14",
    "iPhone15,3": "iPhone 14 Plus",
    "iPhone15,4": "iPhone 14 Pro",
    "iPhone15,5": "iPhone 14 Pro Max",
    # Agrega más modelos según sea necesario
}

current_udid = None

async def get_udid():
    result = subprocess.run(["idevice_id", "-l"], stdout=subprocess.PIPE)
    udid = result.stdout.decode("utf-8").strip()
    return udid

async def get_device_info(udid):
    try:
        result = subprocess.run(["ideviceinfo", "-u", udid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_message = result.stderr.decode("utf-8").strip()
            return None, None, error_message
        
        info = result.stdout.decode("utf-8")
        model_identifier_match = re.search(r'ProductType: (.+)', info)
        if model_identifier_match:
            model_identifier = model_identifier_match.group(1).strip()
            model = MODEL_MAP.get(model_identifier, "Modelo desconocido")
        else:
            model = "Modelo no encontrado"
        return model_identifier, model, None
    except Exception as e:
        return None, None, str(e)

async def update_device_info(page, info_label):
    global current_udid
    udid = await get_udid()
    if udid and udid != current_udid:
        current_udid = udid
        model_identifier, model, error = await get_device_info(udid)
        if error:
            info_label.value = f"Error: {error}"
        elif model_identifier and model:
            info_label.value = f"UDID: {udid}\nModelo: {model}"
    elif not udid:
        current_udid = None
        info_label.value = "Connect device..."
    page.update()

async def monitor_device(page, info_label):
    while True:
        await update_device_info(page, info_label)
        await asyncio.sleep(1)  # Verificar cada 1 segundo

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.appbar = ft.CupertinoAppBar(
        border=ft.border.only(bottom=ft.border.BorderSide(1.5, "#66545e")),
        middle=ft.Text("iOS Tinder Bot"),
    )

    def load_data():
        with open('data.json') as f:
            return json.load(f)

    data = load_data()

    info_label = ft.Text("Connect device...", font_family="Helvetica", size=16)

    def update_content(selected_index):
        if selected_index == 0:
            content = ft.Row(
                [
                    ft.Column(
                        [
                            info_label,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    ),
                    ft.VerticalDivider(width=1.5),
                    create_cards()
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
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

    asyncio.create_task(monitor_device(page, info_label))

ft.app(target=main, assets_dir="assets")
