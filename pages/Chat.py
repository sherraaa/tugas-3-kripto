from datetime import datetime
from typing import List
from flet import *
from service.supabase import supabase
from stores.contact_store import Contact, Message

class DateDivider(Row):
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.height = 48

        self.alignment = MainAxisAlignment.CENTER
        self.vertical_alignment = CrossAxisAlignment.CENTER
        self.controls = [
            Container(
                content=Text(datetime.fromisoformat(self.date).strftime("%a, %d %b %Y"), size=10),
                bgcolor=colors.SECONDARY_CONTAINER,
                padding=8,
                border_radius=8,
            ),
        ]

class MessageBubble(Row):
    def __init__(self, page : Page, message: Message):
        super().__init__()
        self.page = page
        self.id = message.id
        self.type = message.type
        self.author = message.author
        self.content = message.content
        self.created_at = message.created_at
        self.status = Text(datetime.fromisoformat(message.created_at).strftime("%H:%M"), size=12)
        
        self.container_width = None
        if len(self.content) * 12 > self.page.width:
            self.container_width = self.page.width - 150 + ((len(self.content) * 8 - self.page.width) / (len(self.content) * 8) * 50)

        self.rtl = self.author == self.page.user.user.username
        self.vertical_alignment = CrossAxisAlignment.END
        if self.type == "file":
            self.controls = [
                Card(
                    content=Container(
                        content=Column(
                            controls=[
                                Container(
                                    content=Text("Encrypted File", size=16),
                                    width=190,
                                    padding=8,
                                    alignment=alignment.center,
                                    bgcolor=colors.BACKGROUND,
                                    border_radius=8,
                                    border=border.all(1, colors.OUTLINE_VARIANT)
                                ),
                                Row(
                                    controls=[
                                        ElevatedButton(
                                            text=("Open"),
                                        ),
                                        FilledButton(
                                            text=("Decrypt"),
                                        )
                                    ]
                                )
                            ]
                        ),
                        padding=8,
                    ),
                    color=colors.SURFACE if self.rtl else colors.BACKGROUND,
                ),
                self.status,
            ]
        else:
            self.controls = [
                Card(
                    content=Container(
                        content=Text(self.content),
                        padding=8,
                        width=self.container_width,
                    ),
                    color=colors.SURFACE if self.rtl else colors.BACKGROUND,
                ),
                self.status,
            ]

class MessageList(Container):
    message_list = ListView(
        expand=True,
        spacing=4,
        auto_scroll=True,
    )
    dates = {}

    def __init__(self, page: Page, chat):
        super().__init__()
        self.page = page
        self.chat = chat
        if self.message_list.controls:
            self.message_list.controls.clear()
            self.dates.clear()
        self.load_message()

        self.content = self.message_list
        self.padding = 4
        self.expand = True

    def load_message(self):
        for message in self.chat:
            m = MessageBubble(
                page=self.page,
                message=message,
            )
            self.add_message(m)
        self.page.update()
            
    def add_message(self, message: MessageBubble):
        date = datetime.fromisoformat(message.created_at).date()
        if date not in self.dates:
            self.dates[date] = DateDivider(message.created_at)
            self.message_list.controls.append(self.dates[date])
        self.message_list.controls.append(
            message
        )
        self.page.update()

class ChatInput(Row):
    def __init__(self, page: Page, message_list: MessageList, recipient: Contact):
        super().__init__()
        self.page = page
        self.message_list = message_list
        self.recipient = recipient

        self.text_field = TextField(
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=3,
            expand=True,
            on_submit=self.handle_send,
        )

        self.controls = [
            self.text_field,
            IconButton(
                icon=icons.ATTACH_FILE,
                on_click=self.handle_attach_file,
            ),
            IconButton(
                icon=icons.ARROW_FORWARD,
                on_click=self.handle_send,
            ),
        ]

    def handle_attach_file(self, e):
        print("Attach file")

    def handle_send(self, e):
        print("Send message")
        try:

            data, count = supabase.table("messages").insert({
                "type": "text",
                "author": self.page.user.user.username,
                "recipient": self.recipient.username,
                "content": self.text_field.value,
                "created_at": datetime.now().isoformat(),
            }).execute()

            message : Message = Message(
                id=data[1][0]['id'],
                type=data[1][0]['type'],
                author=data[1][0]['author'],
                content=data[1][0]['content'],
                created_at=data[1][0]['created_at'],
            )

            self.recipient.add_message(message)
            self.message_list.add_message(message=MessageBubble(self.page, message))

            self.text_field.value = ""
            self.page.update()
        except Exception as e:
            # print stacktrace
            print(e)
            # show error message
            self.page.snack_bar = SnackBar(
                content=Text("Failed to send message."),
            )
            self.page.snack_bar.open = True
            self.page.update()
        
class ChatView(View):
    def __init__(self, page: Page, contact):
        super().__init__()
        self.route = f"/chat/{contact}"
        self.page : Page = page
        self.contact : Contact = self.page.contacts.get_contact(contact)
        self.chat : List[Message] = self.contact.chat

        # COMPONENTS
        self.message_list = MessageList(page, self.chat)
        self.page.message_list = self.message_list
        self.chat_input = ChatInput(page, self.message_list, self.contact)

        # UI
        self.appbar = AppBar(
            title=Text("@" + self.contact.username, weight=FontWeight.BOLD),
            center_title=False,
            toolbar_height=64,
            leading=IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
            ),
        )
        self.controls = [
            self.message_list,
            self.chat_input,
        ]




