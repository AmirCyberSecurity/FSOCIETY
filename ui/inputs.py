import flet as ft

def fsociety_input(
    hint: str,
    default: str = "",
    width: int = 222,
    font_family: str = "JetMedium",
    color: str = "#00FF00"
):

    field = ft.TextField(
        hint_text=hint,
        value=default,
        width=width,

        text_style=ft.TextStyle(
            font_family=font_family,
            size=15,
            color=color
        ),

        hint_style=ft.TextStyle(
            color="#330000",
            font_family=font_family
        ),

        border=ft.InputBorder.OUTLINE,
        border_width=1,
        border_color="#220000",
        focused_border_color="#FF0000",

        border_radius=8,
        bgcolor="#0A0A0A",
        focused_bgcolor="#0A0A0A",

        cursor_color="#FF0000",
        selection_color="#FF000033",

        content_padding=ft.padding.symmetric(
            horizontal=14,
            vertical=10
        ),

        text_align=ft.TextAlign.CENTER,
    )
    
    return field
