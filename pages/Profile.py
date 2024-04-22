from flet import *
from service.supabase import supabase
from gotrue.types import AuthResponse
from lib.rsa_oop import RSA
              
class ProfileView(View):
    def __init__(self, page: Page,):
        super().__init__()
        self.route = "/profile"
        self.page = page
        self.username = self.page.user.user.username or "Dummy"
        self.scroll = ScrollMode.ADAPTIVE

        # Components
        self.pInput = TextField(
            label="P",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            input_filter=NumbersOnlyInputFilter(),
            expand=True,
            read_only=True
        )

        self.qInput = TextField(
            label="Q",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            input_filter=NumbersOnlyInputFilter(),
            expand=True,
            read_only=True
        )

        self.private_key = TextField(
            label="Private Key",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            password=True,
            can_reveal_password=True,
            read_only=True,
        )

        self.public_key = TextField(
            label="Public Key",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            read_only=True,
        )

        # Buttons

        self.randomizeButton = ElevatedButton(
            text="Randomize",
            style=ButtonStyle(
                padding=15,
            ),
            width=2000,
            on_click=self.handleRandomize,
        )

        self.exportButton = ElevatedButton(
            text="Export",
            style=ButtonStyle(
                padding=15,
            ),
            expand=True,
            on_click=self.handleExport,
        )

        self.uploadButton = ElevatedButton(
            text="Upload",
            style=ButtonStyle(
                padding=15,
            ),
            expand=True,
            on_click=self.handleUpload,
        )

        self.saveButton = FilledButton(
            text="Save",
            style=ButtonStyle(
                padding=15,
            ),
            width=2000,
            on_click=self.handleSave,
        )

        self.logoutButton = FilledButton(
            text="Logout",
            style=ButtonStyle(
                color=colors.ON_ERROR,
                bgcolor=colors.ERROR,
                padding=15,
            ),
            width=2000,
            on_click=self.handleLogout,
        )

        self.controls = [
            Container(
                content=Column(
                    [
                        Column(
                            [
                                Container(
                                    content=Text(self.username[0:2].upper(), color=colors.ON_SECONDARY_CONTAINER, weight=FontWeight.BOLD),
                                    alignment=alignment.center,
                                    width=50,
                                    height=50,
                                    border_radius=25,
                                    bgcolor=colors.SECONDARY_CONTAINER,
                                ),
                                Text("@" + self.username, weight=FontWeight.W_600, size=20)
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            width=20000
                        ),
                        Column(
                            [
                                Row(
                                    [
                                        self.pInput,
                                        self.qInput,              
                                    ],
                                    spacing=8,
                                ),
                                self.randomizeButton,
                            ],
                            spacing=10,
                        ),
                        Column(
                            [
                                self.private_key,
                                self.public_key,
                                Row(
                                    [
                                        self.exportButton,
                                        self.uploadButton,
                                    ],
                                    spacing=8,
                                )
                            ],
                            spacing=10,
                        ),
                        Column(
                            [
                                self.saveButton,
                                self.logoutButton,
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=25,
                ),
                margin=margin.only(left=25, top=75, right=25),
                alignment=alignment.top_center
            )
        ]

    # Handlers
    def handleRandomize(self, e):
        rsa_keys = RSA()
        rsa_keys.generate_keys()
        self.pInput.value = str(rsa_keys.p)
        self.qInput.value = str(rsa_keys.q)
        self.private_key.value = f"({rsa_keys.d}, {rsa_keys.n})"
        self.public_key.value = f"({rsa_keys.e}, {rsa_keys.n})"
        self.page.update()

    def handleExport(self, e):
        pass

    def handleUpload(self, e):
        pass

    def handleSave(self, e):
        self.page.user.set_private_key(self.private_key.value)
        self.page.update()
        self.page.go("/")
        pass

    def handleLogout(self, e):
        self.page.user.logout()
        self.page.contacts.clear()
        self.page.go("/auth")
