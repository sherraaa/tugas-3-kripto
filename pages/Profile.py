import json
from flet import *
from service.supabase import supabase
from gotrue.types import UserResponse
from lib.rsa_oop import RSA
from stores.key_store import KeyStore
import os
              
class ProfileView(View):
    def __init__(self, page: Page,):
        super().__init__()
        self.route = "/profile"
        self.page = page
        self.username = self.page.user.user.username or "Dummy"
        self.scroll = ScrollMode.ADAPTIVE
        self.rsa : KeyStore = self.page.rsa

        # Components
        self.pick_file = FilePicker(
            on_result=self.handleUpload,
        )
        self.save_file = FilePicker(
            on_result=self.handleExport,
        )
        self.page.overlay.append(self.pick_file)
        self.page.overlay.append(self.save_file)


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
            value=self.rsa.rsa.private_key or "",
            label="Private Key",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            password=True,
            can_reveal_password=True,
            read_only=True,
        )

        self.public_key = TextField(
            value=self.rsa.rsa.public_key or "",
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
            on_click=lambda _: self.save_file.get_directory_path(),
        )

        self.uploadButton = ElevatedButton(
            text="Upload",
            style=ButtonStyle(
                padding=15,
            ),
            expand=True,
            on_click=lambda _ : self.pick_file.pick_files(
                allow_multiple=False,
                allowed_extensions=["sus"]
            )
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
        rsa_keys = self.rsa.rsa
        rsa_keys.generate_keys()
        self.pInput.value = str(rsa_keys.p)
        self.qInput.value = str(rsa_keys.q)
        self.private_key.value = f"({rsa_keys.d}, {rsa_keys.n})"
        self.public_key.value = f"({rsa_keys.e}, {rsa_keys.n})"
        self.page.update()

    def handleExport(self, e):
        private_key = self.private_key.value
        public_key = self.public_key.value

        if not private_key or not public_key:
            self.page.snack_bar = SnackBar(
                content=Text("Please generate keys first."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        save_location = e.path
        if save_location:
            try:
                data = {
                    "private_key" : private_key,
                    "public_key" : public_key
                }
                with open(os.path.join(save_location, "keyeyeyes.sus"), "w") as f:
                    json.dump(data, f)
                self.page.snack_bar = SnackBar(
                    content=Text("Saved!"),
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as e:
                self.page.snack_bar = SnackBar(
                    content=Text(e),
                )
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = SnackBar(
                content=Text("Please select a location."),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def handleUpload(self, e):
        file_dir = e.files[0].path
        if file_dir:
            try:
                with open(file_dir, "r") as f:
                    data = json.load(f)
                    print(data)
                    self.private_key.value = data["private_key"]
                    self.public_key.value = data["public_key"]
                    self.page.update()
            except Exception as e:
                self.page.snack_bar = SnackBar(
                    content=Text(e),
                )
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = SnackBar(
                content=Text("Please select a file."),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def handleSave(self, e):
        try:
            res : UserResponse = supabase.auth.update_user({
                "data" : {
                    "public_key" : self.public_key.value,
                }
            })
            self.rsa.set_keys(self.public_key.value, self.private_key.value)
            self.page.snack_bar = SnackBar(
                content=Text("Saved!"),
            )

            self.page.user.set_public_key(self.public_key.value)
            self.page.user.set_private_key(self.private_key.value)

            self.page.snack_bar.open = True
            self.page.update()
            self.page.go("/")

        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text(e),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def handleLogout(self, e):
        self.page.user.logout()
        self.page.contacts.clear()
        self.page.go("/auth")
