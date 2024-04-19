from flet import *
from service.supabase import supabase
from gotrue.types import AuthResponse

class Auth(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        
    def build(self):
        self.usernameInput = TextField(
            label="Username",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            input_filter=InputFilter(
                regex_string=r"[a-zA-Z0-9_]",
            ),
        )
        self.passwordInput = TextField(
            label="Password",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            password=True,
            can_reveal_password=True,
        )
        self.repeatPasswordInput = TextField(
            label="Repeat Password",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            password=True,
        )
        self.submitButton = FilledButton(
            text="Login",
            style=ButtonStyle(
                padding=15,
            ),
            width=1000,
            on_click=self.handleAuth,
        )

        self.column = Column()
        self.column.controls.append(self.usernameInput)
        self.column.controls.append(self.passwordInput)

        return Column(
            controls=[
                Container(
                    content=Image(
                        src="splash.png",
                        width=100,
                        height=100,
                    ),
                    width=500,
                    height=400,
                    bgcolor=colors.SECONDARY_CONTAINER,
                    border_radius=100,
                    padding=50,
                ),
                SegmentedButton(
                    on_change=self.handleChange,
                    show_selected_icon=False,
                    selected={"login"},
                    segments=[
                        Segment(
                            value="login",
                            label=Text("Login"),
                        ),
                        Segment(
                            value="register",
                            label=Text("Register"),
                        ),
                    ]
                ),
                Column(
                    [
                        self.column,
                        self.submitButton,
                    ],
                    spacing=20,
                )
            ],
            spacing=25,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
    
    async def handleChange(self, e):
        authType = self.submitButton.text
        print(authType)
        if authType == "Login":
            print("Adding repeat password input")
            self.column.controls.append(self.repeatPasswordInput)
            self.submitButton.text = "Register"
        else:
            print("Removing repeat password input")
            self.column.controls.remove(self.repeatPasswordInput)
            self.submitButton.text = "Login"
        self.update()

    async def handleAuth(self, e):
        authType = self.submitButton.text
        if authType == "Login":
            await self.handleLogin(e)
        elif authType == "register":
            await self.handleRegister(e)

    async def handleLogin(self, e):
        if not self.usernameInput.value or not self.passwordInput.value:
            self.page.snack_bar = SnackBar(
                content=Text("Please fill in all fields."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            if not self.usernameInput.value:
                self.usernameInput.focus()
            else:
                self.passwordInput.focus()
            return
        self.page.snack_bar = SnackBar(
            content=Text("Logging in..."),
        )
        self.page.snack_bar.open = True
        self.page.update()

        try:
            user : AuthResponse = supabase.auth.sign_in_with_password({
                "email": self.usernameInput.value + "@mail.com",
                "password": self.passwordInput.value,
            })

            userid = user.user.id
            username = user.user.user_metadata['username']

            await self.page.client_storage.set_async("user.id", userid)
            await self.page.client_storage.set_async("user.username", username)

            self.page.go("/")
            print("Logged in")
        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text(e),
            )
            self.page.snack_bar.open = True
            self.page.update()

    async def handleRegister(self, e):
        if not self.usernameInput.value or not self.passwordInput.value or not self.repeatPasswordInput.value:
            self.page.snack_bar = SnackBar(
                content=Text("Please fill in all fields."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            if not self.usernameInput.value:
                self.usernameInput.focus()
            elif not self.passwordInput.value:
                self.passwordInput.focus()
            else:
                self.repeatPasswordInput.focus()
            return
        if len(self.usernameInput.value) < 3:
            self.page.snack_bar = SnackBar(
                content=Text("Username must be at least 3 characters long."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.usernameInput.focus()
            return
        if self.passwordInput.value != self.repeatPasswordInput.value:
            self.page.snack_bar = SnackBar(
                content=Text("Passwords do not match."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.repeatPasswordInput.focus()
            return
        if len(self.passwordInput.value) < 6:
            self.page.snack_bar = SnackBar(
                content=Text("Password must be at least 6 characters long."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.passwordInput.focus()
            return

        self.page.snack_bar = SnackBar(
            content=Text("Registering..."),
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        try:
            user: AuthResponse = supabase.auth.sign_up({
                "email": self.usernameInput.value + "@mail.com",
                "password": self.passwordInput.value,
                "options": {
                    "data" : {
                        "username": self.usernameInput.value,
                        "public_key" : "",
                    }
                }
            })

            userid = user.user.id
            username = user.user.user_metadata['username']

            self.page.client_storage.set_async("user.id", userid)
            self.page.client_storage.set_async("user.username", username)

            self.page.go("/")

        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text(e),
            )
            self.page.snack_bar.open = True
            self.page.update()
