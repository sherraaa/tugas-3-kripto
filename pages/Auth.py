from flet import *
import flet_router as fr
from .Base import router
from service.supabase import supabase
from gotrue.types import AuthResponse

authType = "login"

@router.route(name="auth",
              path="/auth"
              )
async def auth(router: fr.FletRouter, page: Page):

    page.snack_bar = SnackBar(
        content=Text("Loading..."),
    )

    async def handleChange(e):
        global authType
        authType = e.data[2:-2]
        repeatPasswordInput.visible = authType == "register"
        submitButton.text = authType.capitalize()
        page.update()

    async def handleAuth(e):
        global authType
        if authType == "login":
            await handleLogin(e)
        elif authType == "register":
            await handleRegister(e)

    async def handleLogin(e):
        if not usernameInput.value or not passwordInput.value:
            page.snack_bar = SnackBar(
                content=Text("Please fill in all fields."),
            )
            page.snack_bar.open = True
            page.update()
            if not usernameInput.value:
                usernameInput.focus()
            else:
                passwordInput.focus()
            return
        page.snack_bar = SnackBar(
            content=Text("Logging in..."),
        )
        page.snack_bar.open = True
        page.update()

        try:
            user : AuthResponse = supabase.auth.sign_in_with_password({
                "email": usernameInput.value + "@mail.com",
                "password": passwordInput.value,
            })

            userid = user.user.id
            username = user.user.user_metadata['username']

            await page.client_storage.set_async("user.id", userid)
            await page.client_storage.set_async("user.username", username)

            router.go_push(
                fr.Location("contact")
            )
        except Exception as e:
            page.snack_bar = SnackBar(
                content=Text(e),
            )
            page.snack_bar.open = True
            page.update()

    async def handleRegister(e):
        if not usernameInput.value or not passwordInput.value or not repeatPasswordInput.value:
            page.snack_bar = SnackBar(
                content=Text("Please fill in all fields."),
            )
            page.snack_bar.open = True
            page.update()
            if not usernameInput.value:
                usernameInput.focus()
            elif not passwordInput.value:
                passwordInput.focus()
            else:
                repeatPasswordInput.focus()
            return
        if len(usernameInput.value) < 3:
            page.snack_bar = SnackBar(
                content=Text("Username must be at least 3 characters long."),
            )
            page.snack_bar.open = True
            page.update()
            usernameInput.focus()
            return
        if passwordInput.value != repeatPasswordInput.value:
            page.snack_bar = SnackBar(
                content=Text("Passwords do not match."),
            )
            page.snack_bar.open = True
            page.update()
            repeatPasswordInput.focus()
            return
        if len(passwordInput.value) < 6:
            page.snack_bar = SnackBar(
                content=Text("Password must be at least 6 characters long."),
            )
            page.snack_bar.open = True
            page.update()
            passwordInput.focus()
            return

        page.snack_bar = SnackBar(
            content=Text("Registering..."),
        )
        page.snack_bar.open = True
        page.update()
        
        try:
            user: AuthResponse = supabase.auth.sign_up({
                "email": usernameInput.value + "@mail.com",
                "password": passwordInput.value,
                "options": {
                    "data" : {
                        "username": usernameInput.value,
                        "public_key" : "",
                    }
                }
            })

            userid = user.user.id
            username = user.user.user_metadata['username']

            page.client_storage.set_async("user.id", userid)
            page.client_storage.set_async("user.username", username)

            router.go_push(
                fr.Location("contact")
            )

        except Exception as e:
            page.snack_bar = SnackBar(
                content=Text(e),
            )
            page.snack_bar.open = True
            page.update()

    usernameInput = TextField(
        label="Username",
        border_radius=15,
        border_color=colors.ON_SURFACE_VARIANT,
        input_filter=InputFilter(
            regex_string=r"[a-zA-Z0-9_]",
        ),
    )
    passwordInput = TextField(
        label="Password",
        border_radius=15,
        border_color=colors.ON_SURFACE_VARIANT,
        password=True,
        can_reveal_password=True,
    )
    repeatPasswordInput = TextField(
        label="Repeat Password",
        border_radius=15,
        border_color=colors.ON_SURFACE_VARIANT,
        password=True,
        on_submit=handleAuth,
    )
    repeatPasswordInput.visible = False
    submitButton = FilledButton(
        text="Login",
        style=ButtonStyle(
            padding=15,
        ),
        width=1000,
        on_click=handleAuth,
    )

    return View(
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
                on_change=handleChange,
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
                    Column(
                        [
                            usernameInput,
                            passwordInput,
                            repeatPasswordInput,
                        ],
                        spacing=10,
                    ),
                    submitButton,
                ],
                spacing=20,
            )
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=25,
        padding=25
   )