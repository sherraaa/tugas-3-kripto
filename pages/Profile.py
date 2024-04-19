from flet import *
from service.supabase import supabase
from gotrue.types import AuthResponse
              
class Profile(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.username = self.page.client_storage.get("user.username") or "Dummy"

    def build(self):
        pInput = TextField(
            label="P",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            input_filter=NumbersOnlyInputFilter(),
            expand=True,
        )
        qInput = TextField(
            label="Q",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            input_filter=NumbersOnlyInputFilter(),
            expand=True,
        )
        private_key = TextField(
            label="Private Key",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            password=True,
            can_reveal_password=True,
            read_only=True,
        ) 
        public_key = TextField(
            label="Public Key",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            read_only=True,
            min_lines=2,
            max_lines=2,
        )

        # Buttons
        randomizeButton = ElevatedButton(
            text="Randomize",
            style=ButtonStyle(
                padding=15,
            ),
            width=1000,
        )
        exportButton = ElevatedButton(
            text="Export",
            style=ButtonStyle(
                padding=15,
            ),
            expand=True,
        )
        if private_key.value == "" or public_key.value == "":
            exportButton.disabled = True
        uploadButton = ElevatedButton(
            text="Upload",
            style=ButtonStyle(
                padding=15,
            ),
            expand=True,
        )
        saveButton = FilledButton(
            text="Save",
            style=ButtonStyle(
                padding=15,
            ),
            width=1000,
            on_click=self.handleSave,
        )
        logoutButton = FilledButton(
            text="Logout",
            style=ButtonStyle(
                color=colors.ON_ERROR,
                bgcolor=colors.ERROR,
                padding=15,
            ),
            width=1000,
            on_click=self.handleLogout,
        )

        return Column(
            controls=[
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
                                width=10000
                            ),
                            Column(
                                [
                                    Row(
                                        [
                                            pInput,
                                            qInput,              
                                        ],
                                        spacing=8,
                                    ),
                                    randomizeButton,
                                ],
                                spacing=10,
                            ),
                            Column(
                                [
                                    private_key,
                                    public_key,
                                    Row(
                                        [
                                            exportButton,
                                            uploadButton,
                                        ],
                                        spacing=8,
                                    )
                                ],
                                spacing=10,
                            ),
                            Column(
                                [
                                    saveButton,
                                    logoutButton,
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=25,
                    ),
                    margin=margin.only(left=25, top=75, right=25),
                    alignment=alignment.top_center
                )
            ],
        )
        

    # Handlers
    def handleRandomize(self, e):
        # p = random_prime(10)
        # q = random_prime(10)
        # private_key.value = str(p * q)
        # public_key.value = f"({p}, {q})"
        # page.update()
        pass

    def handleExport(self, e):
        pass

    def handleUpload(self, e):
        pass

    def handleSave(self, e):
        self.page.client_storage.set("user.private_key", "test")
        self.page.client_storage.set("user.public_key", "test")
        self.page.update()
        self.page.go("/")
        pass

    def handleLogout(self, e):
        self.page.client_storage.clear()
        self.page.update()
        self.page.go("/auth")

    # Input Fields
    