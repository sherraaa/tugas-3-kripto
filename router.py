from flet import *
from pages.Contact import Contact
from pages.Profile import Profile
from pages.Auth import Auth
from pages.AddContact import AddContact
from pages.Chat import ChatPage


def views_handler(page: Page, path: str):
    troute = TemplateRoute(path)
    view = None
    if troute.match('/'):
        view = View(
            "/",
            controls=[
                AppBar(
                    title=Text("Suslicious", weight=FontWeight.BOLD),
                    center_title=True,
                    toolbar_height=64,
                    leading=Container(),
                    actions=[
                        IconButton(
                            icon=icons.MANAGE_ACCOUNTS,
                            on_click=lambda _: page.go("/profile"),
                            style=ButtonStyle(
                                padding=Padding(left=25, top=8, right=25, bottom=8),
                            )
                        )
                    ]
                ),
                Contact(page),
                FloatingActionButton(
                    icon=icons.CHAT,
                    on_click=lambda _: page.go("/addContact"),
                    bgcolor=colors.SECONDARY_CONTAINER
                )
            ]
        )
    elif troute.match('/profile'):
        view = View(
            '/profile',
            controls=[
                Profile(page)
            ]
        )
    elif troute.match('/auth'):
        view = View(
            '/auth',
            controls=[
                Auth(page)
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            padding=25
        )
    elif troute.match('/addContact'):
        view = View(
            '/addContact',
            controls=[
                AppBar(
                    title=Text("Add Contact", weight=FontWeight.BOLD),
                    center_title=True,
                    toolbar_height=64,
                    leading=IconButton(
                        icon=icons.ARROW_BACK,
                        on_click=lambda e: page.go("/"),
                    ),
                ),
                AddContact(page)
            ]
        )
    elif troute.match('/chat/:username'):
        view = View(
            path,
            controls=[
                AppBar(
                    title=Text("@" + troute.username, weight=FontWeight.BOLD),
                    center_title=False,
                    toolbar_height=64,
                    leading=IconButton(
                        icon=icons.ARROW_BACK,
                        on_click=lambda e: page.go("/"),
                    ),
                ),
                ChatPage(page, troute.username)
            ],
        )

    return view