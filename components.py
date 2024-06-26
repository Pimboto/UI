import flet as ft
import json
import csv
import datetime

def create_navigation_rail(on_change):
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=False,
        min_width=70,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.PHONE_IPHONE, selected_icon=ft.icons.PHONE_IPHONE
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_INPUT_COMPONENT_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS_INPUT_COMPONENT),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TABLE_CHART_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.TABLE_CHART),
            ),
        ],
        on_change=on_change
    )

def create_cards():
    return ft.Column(
        [
            ft.Card(
                variant=ft.CardVariant.FILLED,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.APPS),
                                title=ft.Text("Total Processes"),
                                subtitle=ft.Text("1,234", size=30, weight=ft.FontWeight.W_800),
                
                            ),
                        ]
                    ),
                    width=250,
                    padding=20,
                )
            ),
            ft.Card(
                variant=ft.CardVariant.FILLED,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.HISTORY),
                                title=ft.Text("Processes Remaining"),
                                subtitle=ft.Text("567", size=30, weight=ft.FontWeight.W_800),
                            ),
                        ]
                    ),
                    width=250,
                    padding=20,
                )
            ),
            ft.Card(
                variant=ft.CardVariant.FILLED,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.CHECK),
                                title=ft.Text("Successful Processes"),
                                subtitle=ft.Text("897", size=30, weight=ft.FontWeight.W_800),
                            ),
                        ]
                    ),
                    width=250,
                    padding=20,
                ),
                color="#14452f"
            ),
            ft.Card(
                variant=ft.CardVariant.FILLED,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.CLOSE),
                                title=ft.Text("Failed Processes"),
                                subtitle=ft.Text("123", size=30, weight=ft.FontWeight.W_800),
                            ),
                        ]
                    ),
                    width=250,
                    padding=20,
                ),
                color="#720714"
            ),
        ],
        height=500,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=10
    )

def create_file_picker(label_text):
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    return ft.Row(
        [
            ft.Text(label_text, style="subtitle1"),
                    ft.ElevatedButton(
                        "Pick files",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=False
                        ),
                    ),
                    selected_files,
            pick_files_dialog
        ]
    )

def create_date_picker(label_text, page):
    def handle_change(e):
        page.show_snack_bar(ft.SnackBar(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}")))

    def handle_dismissal(e):
        page.show_snack_bar(ft.SnackBar(ft.Text(f"DatePicker dismissed")))

    return ft.Row(
        [
            ft.Text(label_text, style="subtitle1"),
            ft.ElevatedButton(
                "Pick date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: page.open(
                    ft.DatePicker(
                        first_date=datetime.datetime(year=2023, month=10, day=1),
                        last_date=datetime.datetime(year=2024, month=10, day=1),
                        on_change=handle_change,
                        on_dismiss=handle_dismissal,
                    )
                ),
            ),
        ],
    )

def create_connection_settings(page):
    text_fields = [
        ft.TextField(adaptive=True, label="DaisySMS API Key", width=400),
        ft.TextField(adaptive=True, label="Proxy String", width=400),
        ft.TextField(adaptive=True, label="Proxy Rotation Token", width=400),
        ft.TextField(adaptive=True, label="Iphone UDID", width=400),
        ft.TextField(adaptive=True, label="Iphone Root", width=400),
        ft.TextField(adaptive=True, label="Iphone Root Pass", width=400),
        ft.TextField(adaptive=True, label="Iphone IP", width=400),
        ft.TextField(adaptive=True, label="Port", width=400)
    ]

    def validate_and_save(e):
        valid = True
        for tf in text_fields:
            if not tf.value:
                tf.border_color = ft.colors.RED
                tf.helper_text = f"{tf.label} cannot be empty"
                tf.helper_style = ft.TextStyle(color=ft.colors.RED)
                valid = False
            else:
                tf.border_color = None
                tf.helper_text = ""
                tf.helper_style = None
            tf.update()
        if valid:
            page.show_snack_bar(ft.SnackBar(ft.Text("All fields are filled. Save logic here.")))
            # Add your save logic here

    return ft.Container(
        content=ft.Column(
            text_fields + [
                ft.Row(
                    [
                        ft.CupertinoFilledButton(
                            content=ft.Text("Save"),
                            opacity_on_click=0.3,
                            on_click=validate_and_save,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            wrap=True,
            height=600,
            spacing=50,
            run_spacing=50,
        ),
        alignment=ft.alignment.center
    )

def create_account_settings(page):
    return ft.Container(
        ft.Column(
            [
                create_file_picker("Name"),                   
                ft.Switch(
                    adaptive=True,
                    label="Upload to matchfix",
                    value=True,
                ),                
                ft.CupertinoFilledButton(
                    content=ft.Text("Save"),
                    opacity_on_click=0.3,
                    on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("CupertinoFilledButton clicked!"))),
                ), 
            ],
            wrap=True,
            height=250,
            spacing=50,
            run_spacing=50,
            alignment=ft.CrossAxisAlignment.CENTER

        ),
        alignment=ft.alignment.center
    )

def create_table(data):
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(item["id"]))),
                ft.DataCell(ft.Text(item["token"])),
            ],
        )
        for item in data
    ]

    return ft.DataTable(
        width=800,
        border=ft.border.all(1.5, "#66545e"),
        border_radius=5,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Token")),
        ],
        rows=rows,
    )

def create_buttons(page, update_table_callback):
    def dialog_dismissed(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("Action done!")))

    def handle_action_click(e):
        if e.control.text == "Yes":
            with open('data.json', 'w') as f:
                json.dump([], f)
            update_table_callback()
            page.show_snack_bar(ft.SnackBar(ft.Text("Table deleted!")))
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Action clicked: {e.control.text}")))
        page.close(e.control.parent)
        page.update()

    def open_dialog(e):
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Delete CSV"),
            content=ft.Text("Do you want to delete this file?"),
            on_dismiss=dialog_dismissed,
            actions=[
                ft.CupertinoDialogAction(
                    text="Yes",
                    is_destructive_action=True,
                    on_click=handle_action_click,
                ),
                ft.CupertinoDialogAction(
                    text="No",
                    is_default_action=True,
                    on_click=handle_action_click,
                ),
            ],
        )
        page.open(cupertino_alert_dialog)
        page.update()

    def download_csv():
        with open('data.json') as f:
            data = json.load(f)
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Token"])
            for item in data:
                writer.writerow([item["id"], item["token"]])
        page.show_snack_bar(ft.SnackBar(ft.Text("CSV downloaded!")))

    delete_button = ft.CupertinoFilledButton(
        text="Delete CSV info",
        width=350,
        on_click=open_dialog,
    )

    download_button = ft.CupertinoFilledButton(
        width=350,
        content=ft.Text("Download as CSV"),
        opacity_on_click=0.3,
        on_click=lambda e: download_csv(),
    )

    return ft.Column(
        [
            delete_button,
            download_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
