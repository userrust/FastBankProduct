import flet as ft


def main(page: ft.Page):
    #a = ft.Container(width=50, height=250, bgcolor="red")
    a = ft.Text()
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.add(
        ft.Row(
            [
                a
            ],
            ft.MainAxisAlignment.CENTER
        )
    )


ft.app(main)
