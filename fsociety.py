from lib.ip_osint import checking, get_ip, get_country, get_city, get_isp, get_org, get_cords, get_ip_type
from lib.host_osint import site_exists, safe_get_ip, detect_protection, get_ip_host_data
from lib.phone_osint import is_valid, parse_check, get_data
from lib.ddos import start_ddos, stop_ddos, is_ddos_running
from lib.connectivity import check_connectivity
from ui.inputs import fsociety_input
import phonenumbers
import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Fsociety - HACK"
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.fonts = {
        "JetLight": "fonts/JetLight.ttf",
        "JetMedium": "fonts/JetMedium.ttf",
        "JetBold": "fonts/JetBold.ttf",
        "MrRobot": "fonts/MrRobot.ttf"
    }

    ICON_PATH = "logos/mr-robot-logo.jpg"
    icon_element = ft.Container(content=ft.Image(src=ICON_PATH, width=200, height=200, fit="contain"))

    
    url_entry = fsociety_input("Target URL", "https://")
    size_entry = fsociety_input("Size (KB)", "100")
    ip_entry = fsociety_input("Target IP")
    number_entry = fsociety_input("Target Number")
    host_entry = fsociety_input("Target Host")


    def show_dos_ui():
        page.clean()
        if is_ddos_running():
            asyncio.create_task(stop_ddos())


        error_label = ft.Text("", color="#FF0000", font_family="JetLight")
        status_label = ft.Text("Ready", color="#00FF00", font_family="JetMedium", size=14)
        terminal_view = ft.ListView(expand=True, spacing=2, auto_scroll=True)
        terminal_container = ft.Container(
        content=terminal_view, border=ft.Border(
            top=ft.border.BorderSide(1, "#FF0000"),
            right=ft.border.BorderSide(1, "#FF0000"),
            bottom=ft.border.BorderSide(1, "#FF0000"),
            left=ft.border.BorderSide(1, "#FF0000")
        ),
            border_radius=5, padding=10, bgcolor="#151515", height=150, width=300
        )

        def on_update(total, fake_ip, status):
            if status is None:
                terminal_view.controls.append(
                    ft.Text(f"[{total}] {fake_ip} -> FAIL",
                            color="#FF0000", size=9, font_family="monospace")
                )
            else:
                terminal_view.controls.append(
                    ft.Text(f"[{total}] {fake_ip} -> {status}",
                            color="#00FF00", size=10, font_family="monospace")
                )
            if len(terminal_view.controls) > 200:
                terminal_view.controls.pop(0)
            page.update()

        def on_stats(elapsed, rps, total):
            terminal_view.controls.append(
                ft.Text(f"[STATS] {elapsed}s | {rps} RPS | Total: {total}",
                        color="#FFFF00", size=9, font_family="monospace")
            )
            if len(terminal_view.controls) > 200:
                terminal_view.controls.pop(0)
            page.update()

        async def start_attack(e):
            target = url_entry.value.strip()
            if not target or target == "https://":
                error_label.value = "URL_REQUIRED"
                page.update()
                return
            if not target.startswith("http"):
                target = "http://" + target
                url_entry.value = target
            try:
                kb_val = int(size_entry.value)
                if kb_val > 99: kb_val = 99
                if kb_val <= 0: kb_val = 1
            except:
                error_label.value = "INVALID_SIZE"
                page.update()
                return

            btn_start.disabled = True
            status_label.value = f"ATTACKING: {kb_val}KB | 500 workers"
            status_label.color = "#FF0000"
            error_label.value = ""
            page.update()

            await start_ddos(target, kb_val, 500, on_update, on_stats)

        def stop_process(e):
            stop_ddos()
            show_main_ui()

        btn_start = ft.FilledButton(
            content=ft.Text("INITIALIZE", color="white", font_family="JetMedium"),
            width=222, height=44, bgcolor="#FF0000",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            on_click=lambda e: page.run_task(start_attack, e)
        )

        page.add(
            ft.Column(
                [
                    ft.Container(height=20),
                    ft.Text("Website DDoS", font_family="MrRobot", size=25, color="#FF0000"),
                    ft.Container(height=10),
                    ft.Text("CUSTOM_FLOODER", font_family="JetMedium", size=14, color="white"),
                    ft.Container(height=10),
                    url_entry,
                    ft.Container(height=10),
                    size_entry,
                    error_label,
                    status_label,
                    btn_start,
                    ft.Container(height=5),
                    terminal_container,
                    ft.Container(height=5),
                    ft.TextButton(
                        content=ft.Text("TERMINATE & EXIT", color="white", font_family="JetMedium"),
                        on_click=stop_process, 
                        style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                        width=200, height=40
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )

    def show_choice_ui():
        page.clean()
        def osint_by_ip():
            page.clean()
            error_label = ft.Text("", color="#FF0000", font_family="JetMedium", size=13)

            def final_osint_by_ip(_):
                if not ip_entry.value:
                    error_label.value = "NULL_TARGET"
                    page.update()
                    return
                target_ip = ip_entry.value
                if checking(target_ip):
                    page.clean()
                    page.add(
                        ft.Column(
                            [
                                ft.Container(height=100),
                                ft.Text("IP Info", color="#FF0000", font_family="MrRobot", size=26),
                                ft.Container(height=20),
                                ft.Text("Results:", color="#FF0000", font_family="JetMedium", size=16),
                                ft.Container(height=25),
                                ft.Text(get_ip(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_country(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_city(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_isp(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_org(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_cords(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Text(get_ip_type(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                ft.Container(height=15),
                                ft.TextButton(
                                    content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                                    on_click=lambda _: show_choice_ui(),
                                    style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                                    width=200, height=40
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO
                        )
                    )
                else:
                    error_label.value = "INVALID_IP"
                    page.update()

            page.add(
                ft.Column(
                    [
                        ft.Container(height=100),
                        ft.Text("Osint By IP", font_family="MrRobot", size=25, color="#FF0000"),
                        ft.Container(height=20),
                        ft.Text("Info About IP", font_family="JetMedium", size=15, color="white"),
                        ft.Container(height=25),
                        ip_entry,
                        error_label,
                        ft.Container(height=5),
                        ft.FilledButton(
                            content=ft.Text("INFO", color="white", font_family="JetMedium"),
                            width=222, height=44, bgcolor="#FF0000",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                            on_click=final_osint_by_ip
                        ),
                        ft.Container(height=10),
                        ft.TextButton(
                            content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                            on_click=lambda _: show_choice_ui(),
                            style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                            width=200, height=40
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )

        def osint_by_number():
            page.clean()
            error_label = ft.Text("", color="#FF0000", font_family="JetMedium", size=13)

            def final_osint_by_number(_):
                if not number_entry.value:
                    error_label.value = "NULL_TARGET"
                    page.update()
                    return
                
                phone_numb = number_entry.value

                raw = number_entry.value
                raw = raw.replace("＋", "+")
                raw = raw.replace("\u200e", "").replace("\u200f", "").replace("\u00a0", "")
                clean = "".join(c for c in raw if c.isdigit() or c == "+")

                while clean.startswith("++"): 
                    clean = clean[1:]

                if clean.startswith("+8"): 
                    clean = "+7" + clean[2:]

                if clean.startswith("8") and len(clean) == 11: 
                    clean = "+7" + clean[1:]

                if not clean.startswith("+"): 
                    clean = "+7" + clean

                if not is_valid(phone_numb):
                    error_label.value = "INVALID_NUMBER"
                    page.update()
                    return
                
                if not parse_check(phone_numb):
                    error_label.value = "PARSE_FAILED"
                    page.update()
                    return
                
                parsed = phonenumbers.parse(clean)

                page.clean()
                page.add(
                    ft.Column(
                        [
                            ft.Container(height=50),
                            ft.Text("Number Info", font_family="MrRobot", color="#FF0000", size=25),
                            ft.Container(height=20),
                            ft.Text("Results:", font_family="JetMedium", size=16, color="white"),
                            ft.Container(height=20),
                            ft.Text(f"COUNTRY: {get_data(parsed)['country']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"REGION: {get_data(parsed)['region']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"OPERATOR: {get_data(parsed)['operator']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"TIMEZONE: {get_data(parsed)['tz']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"LINE_TYPE: {get_data(parsed)['line_type']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"COUNTRY CODE: {get_data(parsed)['country_code']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"INTERNATIONAL: {get_data(parsed)['intl']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"E164: {get_data(parsed)['e164']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"LOCAL: {get_data(parsed)['e164']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"VALID: {get_data(parsed)['is_valid']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Text(f"POSSIBLE: {get_data(parsed)['is_possible']}", color="#FF0000", font_family="JetLight", size=12),
                            ft.Container(height=15),
                            ft.TextButton(
                                content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                                on_click=lambda _: show_choice_ui(),
                                style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                                width=200, height=40
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO
                    )
                )

            page.add(
                ft.Column(
                    [
                        ft.Container(height=100),
                        ft.Text("Osint By Number", font_family="MrRobot", size=25, color="#FF0000"),
                        ft.Container(height=20),
                        ft.Text("Info About Number", font_family="JetMedium", size=15, color="white"),
                        ft.Container(height=25),
                        number_entry,
                        error_label,
                        ft.Container(height=5),
                        ft.FilledButton(
                            content=ft.Text("INFO", color="white", font_family="JetMedium"),
                            width=222, height=44, bgcolor="#FF0000",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                            on_click=final_osint_by_number
                        ),
                        ft.Container(height=10),
                        ft.TextButton(
                            content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                            on_click=lambda _: show_choice_ui(),
                            style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                            width=200, height=40
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )

        def osint_by_host():
            page.clean()
            error_label = ft.Text("", color="#FF0000", font_family="JetMedium", size=13)


            def final_osint_by_host(_):
                if not host_entry.value:
                    error_label.value = "NULL_TARGET"
                    page.update()
                    return
                
                if site_exists(host_entry.value):
                    page.clean()

                    host = host_entry.value

                    ip = safe_get_ip(host)
                    protection = detect_protection(host)
                    target_ip = ip
                    page.add(
                        ft.Column(
                            [
                                ft.Container(height=100),
                                ft.Text("Host Info", font_family="MrRobot", size=25, color="#FF0000"),
                                ft.Container(height=20),
                                ft.Text("Results:", font_family="JetMedium", color="white", size=15),
                                ft.Container(height=30),
                                ft.Text(f"Ip: {ip}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(f"Protection: {protection}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(f"Country: {get_ip_host_data(target_ip)['country']}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(f"City: {get_ip_host_data(target_ip)['city']}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(f"ORG: {get_ip_host_data(target_ip)['org']}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(f"ISP: {get_ip_host_data(target_ip)['isp']}", size=13, font_family="JetMedium", color="#FF0000"),
                                ft.Text(get_cords(target_ip), font_family="JetLight", size=13, color="#FF0000"),
                                
                                ft.Container(height=15),
                                ft.TextButton(
                                    content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                                    on_click=lambda _: show_choice_ui(),
                                    style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                                    width=200, height=40
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO
                        )
                    )
                else:
                    error_label.value = "NOT_FOUND"
                    page.update()

            page.add(
                ft.Column(
                    [
                        ft.Container(height=100),
                        ft.Text("Osint By Host", font_family="MrRobot", color="#FF0000", size=25),
                        ft.Container(height=20),
                        ft.Text("Info About Host", font_family="JetMedium", color="white", size=15),
                        ft.Container(height=25),
                        host_entry,
                        error_label,
                        ft.Container(height=5),
                        ft.FilledButton(
                            content=ft.Text("INFO", color="white", font_family="JetMedium"),
                            width=222, height=44, bgcolor="#FF0000",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                            on_click=final_osint_by_host
                        ),
                        ft.Container(height=10),
                        ft.TextButton(
                            content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                            on_click=lambda _: show_choice_ui(),
                            style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                            width=200, height=40
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )


        

        page.add(    
                ft.Column(
                [
                    ft.Container(height=100),
                    ft.Text("Choice", font_family="MrRobot", color="#FF0000", size=27),
                    ft.Container(height=20),
                    ft.Text("Osint By?", font_family="JetMedium", size=15, color="white"),
                    ft.Container(height=20),
                    ft.FilledButton(
                        content=ft.Text("By IP", color="white", font_family="JetMedium"),
                        width=222, height=44, bgcolor="#FF0000",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                        on_click=lambda _: osint_by_ip()
                    ),
                    ft.Container(height=5),
                    ft.FilledButton(
                        content=ft.Text("By Number", color="white", font_family="JetMedium"),
                        width=222, height=44, bgcolor="#FF0000",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                        on_click=lambda _: osint_by_number()
                    ),
                    ft.Container(height=5),
                    ft.FilledButton(
                        content=ft.Text("By Host", color="white", font_family="JetMedium"),
                        width=222, height=44, bgcolor="#FF0000",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                        on_click=lambda _: osint_by_host()
                    ),
                    ft.Container(height=5),
                    ft.Container(height=20),
                    ft.TextButton(
                        content=ft.Text("EXIT", color="white", font_family="JetMedium"),
                        on_click=lambda _: show_main_ui(),
                        style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                        width=200, height=40
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )

    def show_main_ui():
        if is_ddos_running():
            asyncio.create_task(stop_ddos())
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(height=150),
                    ft.Text("FSOCIETY", font_family="MrRobot", size=30, color="#FF0000"),
                    ft.Text("CONNECTION ESTABLISHED", font_family="JetMedium", size=12, color="#00FF00"),
                    ft.Container(height=20),
                    ft.Text("For educational purposes only.", font_family="JetMedium", size=14, color="white"),
                    ft.Container(height=30),
                    ft.FilledButton(
                        content=ft.Text("Website DDoS", font_family="JetMedium", size=15, color="white"),
                        width=222, height=44, style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                        on_click=lambda _: show_dos_ui()
                    ),
                    ft.Container(height=5),
                    ft.FilledButton(
                        content=ft.Text("Powerful Osint", font_family="JetMedium", size=15, color="white"),
                        width=222, height=44, style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                        on_click=lambda _: show_choice_ui()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )

    def show_no_internet_ui():
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(height=100),
                    ft.Text("CONNECTION_TERMINATED", font_family="MrRobot", size=20, color="#FF0000"),
                    ft.Container(height=20),
                    ft.Text("ERROR: REMOTE_HOST_UNREACHABLE", font_family="JetMedium", size=13, color="#FF0000"),
                    ft.Text("System is offline. Encryption failed.", font_family="JetLight", size=12, color="#FF0000"),
                    ft.Container(height=30),
                    ft.FilledButton(
                        content=ft.Text("RE-ESTABLISH UPLINK", font_family="JetMedium", color="white", size=15),
                        on_click=lambda _: check_and_update(),
                        style=ft.ButtonStyle(bgcolor="#FF0000", shape=ft.RoundedRectangleBorder(radius=5)),
                        width=222, height=44
                    ),
                    ft.Container(height=20),
                    icon_element
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )

    def check_and_update():
        if check_connectivity():
            show_main_ui()
        else:
            show_no_internet_ui()
        page.update()

    check_and_update()

ft.run(main, assets_dir="assets")
