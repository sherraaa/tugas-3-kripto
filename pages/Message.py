import base64
from datetime import datetime
import os
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
            file_id = self.message.content
            decoded_file_id = base64.b64decode(file_id).decode()
            decoded_numbers = [int(number) for number in decoded_file_id.split(",")]
            decrypted_content = self.page.rsa.rsa.decrypt(decoded_numbers)
            decrypted_content_base64 = base64.b64decode(decrypted_content).decode()
            file_id = decrypted_content_base64
            data, count = supabase.table("files").select("*").eq("id", file_id).execute()
            
            self.content = data[1][0]["data"]
            self.label = "File"

            if self.encrypt_or_decrypt == "decrypt":
                encrypted_file = self.content
                decoded_file = base64.b64decode(encrypted_file).decode()
                decoded_file_numbers = [int(number) for number in decoded_file.split(",")]
                decrypted_content = self.page.rsa.rsa.decrypt(decoded_file_numbers)
                decrypted_content_base64 = base64.b64decode(decrypted_content).decode()
                self.content = decrypted_content_base64
                
        else:
            if self.encrypt_or_decrypt == "encrypt":
                content = self.message.content
                content_base64 = base64.b64encode(content.encode()).decode()
                encrypted_content = self.page.recipient_rsa.encrypt(content_base64)
                numbers = encrypted_content
                numbers_str = [str(number) for number in numbers]
                numbers_combined = ",".join(numbers_str)
                self.content = base64.b64encode(numbers_combined.encode()).decode()
                self.label = "Ciphertext"
            else:
                self.content = self.message.content
                self.label = "Ciphertext"

        self.save_file = FilePicker(
            on_result=self.handle_save,
        )
        self.page.overlay.append(self.save_file)


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
            value=self.content,
            label=self.label,
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            expand=True,
            min_lines=3,
            max_lines=25,
        )

        self.save_button = FilledButton(
            text="Save",
            width=200,
            on_click=lambda _ : self.save_file.get_directory_path(),
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
    
    def handle_save(self, e):
        save_location = e.path
        if save_location:
            try:
                if '||||||' in self.content:
                    file_name, file_content = self.content.split("||||||")
                else:
                    time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = "susisasisu " + time + ".sus"
                    file_content = self.content
                with open(os.path.join(save_location, file_name), "w") as file:
                    file.write(file_content)
                file.close()
            except Exception as e:
                print(e)
                self.page.snack_bar = SnackBar(
                    content=Text("Failed to save file"),
                )
                self.page.snack_bar.open = True
                self.page.update()
            else:
                self.page.snack_bar = SnackBar(
                    content=Text("File saved successfully"),
                )
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = SnackBar(
                content=Text("No save location selected"),
            )
            self.page.snack_bar.open = True
            self.page.update()

                

        