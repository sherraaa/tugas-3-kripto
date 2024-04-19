from flet import *

class ContactCard(UserControl):
    def __init__(self, page: Page, username: str, last_message: str):
        super().__init__()
        self.page = page
        self.username = username
        self.last_message = last_message

    def build(self):
        
        return Card(
            content=Container(
                content=ListTile(
                    title=Text("@" + self.username, weight=FontWeight.W_500),
                    subtitle=Text(self.last_message),
                    leading=Container(
                        content=Text(self.username[0:2].upper(), color=colors.ON_SECONDARY_CONTAINER, weight=FontWeight.BOLD),
                        alignment=alignment.center,
                        width=50,
                        height=50,
                        border_radius=25,
                        bgcolor=colors.SECONDARY_CONTAINER
                    )
                ),
                on_click=self.go_chat
            )
        )
    
    def go_chat(self, e):
        print("Going to chat", self.username)
        self.page.go(f"/chat/{self.username}")

class Contact(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.contacts = self.page.client_storage.get("contacts") or []

    def build(self):
        
        # Components
        chatRoom = Column(
            controls=[],
            spacing=8,
            scroll=ScrollMode.AUTO,
        )
        container = Container(
            content=chatRoom,
            height=self.page.height - 120,
            border_radius=16,
        )
        if self.contacts:
            for contact in self.contacts:
                print(contact)
                
                chatRoom.controls.append(
                    ContactCard(
                        page=self.page,
                        username=contact["username"],
                        last_message=contact["last_message"],
                    )
                )

        return container
