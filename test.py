from flet import *

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                CircleAvatar(
                    content=Text(self.get_initials(message.user_name)),
                    color=colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                Column(
                    [
                        Text(message.user_name, weight="bold"),
                        Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            colors.AMBER,
            colors.BLUE,
            colors.BROWN,
            colors.CYAN,
            colors.GREEN,
            colors.INDIGO,
            colors.LIME,
            colors.ORANGE,
            colors.PINK,
            colors.PURPLE,
            colors.RED,
            colors.TEAL,
            colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = Text(message.text, italic=True, color=colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text("Welcome!"),
        content=Column([join_user_name], width=300, height=70, tight=True),
        actions=[ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    # Chat messages
    chat = ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.views.append(
        View(
            '/chat',
            [
                AppBar(
                    title=Text("Flet Chat", weight="bold"),
                    center_title=True,
                ),
                Column(
                    [
                        Container(
                            content=chat,
                            border=border.all(1, colors.OUTLINE),
                            border_radius=5,
                            padding=10,
                            expand=True,
                        ),
                        Row(
                            [
                                new_message,
                                IconButton(
                                    icon=icons.SEND_ROUNDED,
                                    tooltip="Send message",
                                    on_click=send_message_click,
                                ),
                            ]
                        ),

                    ],
                    expand=True,
                )
            ]
        )
    )
    page.go('/chat')

app(port=8550, target=main, view=WEB_BROWSER)