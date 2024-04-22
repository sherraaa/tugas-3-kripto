from flet import *
from service.supabase import supabase
from pages.Chat import MessageBubble
from stores.contact_store import Message

class MessageView(View):
    def __init__(self, page: Page, type: str, encrypt_or_decrypt: str):
        super().__init__()
        self.route = f"/message/{type}/{encrypt_or_decrypt}"
        self.page = page
        self.type = type
        self.encrypt_or_decrypt = encrypt_or_decrypt
        
        self.message : Message = self.page.message
        self.message_bubble = MessageBubble(
            page=self.page,
            message=self.message
        )

        if self.type == "file":
            data, count = supabase.table("files").select("*").eq("id", self.message.content).execute()
            print(data)

        self.appbar = AppBar(
            title=Text("Message", weight=FontWeight.BOLD),
            center_title=False,
            toolbar_height=64,
            leading=IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
            ),
        )

        self.text_field = TextField(
            value=self.message.content,
            label="Plaintext",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            expand=True,
        )


        self.save_button = FilledButton(
            text="Save",
            width=200,
        )

        self.controls = [
            Stack(
                controls=[
                    ListView(
                        controls=[
                            self.message_bubble,
                            Divider(),
                            self.text_field
                        ],
                        spacing=8,
                    ),
                    Container(
                        content=self.save_button,
                        alignment=alignment.bottom_center,
                        expand=True
                    ) if self.type == "file" else Container(),
                ],
                expand=True
            )
        ]

        