import base64
from datetime import datetime
from typing import List
from flet import *
from lib.rsa_oop import RSA
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
        self.message = message
        self.id = message.id
        self.type = message.type
        self.author = message.author
        self.content = message.content
        print(self.content)

        self.created_at = message.created_at
        self.status = Text(datetime.fromisoformat(message.created_at).strftime("%H:%M"), size=12)

        content = self.content

        if self.author != self.page.user.user.username:
            # decrypting
            decoded_string = base64.b64decode(self.content).decode()
            decoded_numbers = [int(number) for number in decoded_string.split(",")]
            decrypted = self.page.rsa.rsa.decrypt(decoded_numbers)
            decrypted = base64.b64decode(decrypted.encode()).decode()
            content = decrypted


        
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
                                            text=("Save"),
                                            on_click=self.handle_save,
                                        ),
                                        FilledButton(
                                            text=("Decrypt"),
                                            on_click=self.handle_decrypt,
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
                        content=Text(content),
                        padding=8,
                        width=self.container_width,
                        on_click=self.on_click_text,
                    ),
                    color=colors.SURFACE if self.rtl else colors.BACKGROUND,
                ),
                self.status,
            ]

    def on_click_text(self, e):
        self.page.message = self.message
        if self.author == self.page.user.user.username:
            self.page.go("/message/text/encrypt")
        else:
            self.page.go("/message/text/decyrpt")

    def handle_save(self, e):
        self.page.message = self.message
        self.page.go("/message/file/encrypt")

    def handle_decrypt(self, e):
        self.page.message = self.message
        self.page.go("/message/file/decrypt")

class MessageList(Container):
    message_list = ListView(
        expand=True,
        spacing=4,
        auto_scroll=True,
    )
    dates = {}

    def __init__(self, page: Page, chat, recipient: Contact):
        super().__init__()
        self.page = page
        self.chat = chat
        self.recipient = recipient
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
        # self.recipient.add_message(message)
        self.page.update()

class ChatInput(Row):
    def __init__(self, page: Page, message_list: MessageList, recipient: Contact):
        super().__init__()
        self.page = page
        self.message_list = message_list
        self.recipient = recipient

        self.type = "text"

        self.file_picker = FilePicker(
            on_result=self.file_picker_result,
        )
        self.page.overlay.append(self.file_picker)

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

        self.attach_file_button = IconButton(
            icon=icons.ATTACH_FILE,
            on_click=lambda _ : self.file_picker.pick_files(allow_multiple=False),
        )

        self.send_button = IconButton(
            icon=icons.ARROW_FORWARD,
            on_click=self.handle_send,
        )

        self.cancel_button = IconButton(
            icon=icons.CANCEL_OUTLINED,
            on_click=self.handle_cancel,
        )

        self.controls = [
            self.text_field,
            self.attach_file_button,
            self.send_button,
        ]

    def file_picker_result(self, e : FilePickerResultEvent):
        self.attach_file_button.disabled = True if e.files is None else False
        if e.files:
            self.file_dir = e.files[0].path
            self.text_field.value = ", ".join(map(lambda f: f.name, e.files))
            self.text_field.read_only = True

            self.type = "file"
            self.controls = [
                self.text_field,
                self.cancel_button,
                self.send_button,
            ]
        self.page.update()

    def on_upload(self) -> str:
        # uploading file returning string
        file = open(self.file_dir, "rb")
        file_data = file.read()
        file.close()

        if '/' in self.file_dir:
            filename = self.file_dir.split("/")[-1]
        else:
            filename = self.file_dir.split("\\")[-1]

        file_data = (filename + "||||||").encode() + file_data
        print(file_data)
        
        # convert to base64
        file_data = base64.b64encode(file_data).decode()

        return supabase.table("files").insert({
            "data" : file_data,
        }).execute()


    def handle_send(self, e):
        print("Send message")
        try:
            if self.type == "file":
                file_data, count = self.on_upload()

            content = self.text_field.value if self.type == "text" else file_data[1][0]['id']
            content_base64 = base64.b64encode(content.encode()).decode()
            encrypted_content = self.page.recipient_rsa.encrypt(content_base64)
            numbers = encrypted_content
            numbers_str = [str(number) for number in numbers]
            numbers_combined = ",".join(numbers_str)
            base64_encoded = base64.b64encode(numbers_combined.encode()).decode()

            data, count = supabase.table("messages").insert({
                "type": "text" if self.type == "text" else "file",
                "author": self.page.user.user.username,
                "recipient": self.recipient.username,
                "content": base64_encoded,
                "created_at": datetime.now().isoformat(),
            }).execute()

            message : Message = Message(
                id=data[1][0]['id'],
                type=data[1][0]['type'],
                author=data[1][0]['author'],
                content=content,
                created_at=data[1][0]['created_at'],
            )

            self.message_list.add_message(message=MessageBubble(self.page, message))
            self.recipient.add_message(message)
            self.page.client_storage.set("contacts", self.page.contacts.contacts)
            
            self.text_field.value = ""
            self.text_field.read_only = False
            self.type = "text"
            self.controls = [
                self.text_field,
                self.attach_file_button,
                self.send_button,
            ]
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

    def handle_cancel(self, e):
        print("Cancel")
        self.text_field.value = ""
        self.text_field.read_only = False
        self.type = "text"
        self.controls = [
            self.text_field,
            self.attach_file_button,
            self.send_button,
        ]
        self.page.update()
        
class ChatView(View):
    def __init__(self, page: Page, contact):
        super().__init__()
        self.route = f"/chat/{contact}"
        self.page : Page = page
        self.contact : Contact = self.page.contacts.get_contact(contact)
        self.chat : List[Message] = self.contact.chat

        data, count = supabase.table("users").select("public_key").eq("username", self.contact.username).execute()
        self.page.recipient_public_key = data[1][0]['public_key']
        self.page.recipient_rsa = RSA(self.page.recipient_public_key)

        # COMPONENTS
        self.message_list = MessageList(page, self.chat, self.contact)
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




