import flet as ft
import requests

def main(page: ft.Page):
    # a = ft.Container(width=50, height=250, bgcolor="red")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    req = requests.get("https://hellohost-8hql.onrender.com/info_user")
    print(req.text)
    a = ft.Text(f"{req.text}", size=50)
    page.add(
        ft.Row(
            [
                a
            ],
            ft.MainAxisAlignment.CENTER
        )
    )


ft.app(main)
