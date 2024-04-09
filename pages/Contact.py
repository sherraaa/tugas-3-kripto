from flet import *
import flet_router as fr
from .Base import router

class Contact(UserControl):
    def __init__(self, router, username, last_message, path):
        super().__init__()
        self.router = router
        self.username = username
        self.last_message = last_message
        self.path = path

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
        self.router.go_push(self.path)

@router.route(name="contact")
async def contact(router: fr.FletRouter, page: Page):

    if not await page.client_storage.contains_key_async("user.id"):
        router.go_push("/auth")
    if not await page.client_storage.contains_key_async("user.private_key"):
        router.go_push("/profile")


    # Handler
    async def handleProfile(e):
        router.go_push("/profile")

    async def handleAddContact(e):
        router.go_push("/addContact")

    # Components
    chatRoom = Column(
        controls=[],
        spacing=8,
    )
    contacts = await page.client_storage.get_async("contacts")
    if contacts:
        for contact in contacts:
            print(contact)
            
            chatRoom.controls.append(
                Contact(
                    router=router,
                    username=contact["username"],
                    last_message=contact["last_message"],
                    path=f"/chat/{contact['username']}"
                )
            )

    return View(
        controls=[
            AppBar(
                title=Text("Sus Chat?", weight=FontWeight.BOLD),
                center_title=True,
                toolbar_height=64,
                leading=Container(),
                actions=[
                    IconButton(
                        icon=icons.MANAGE_ACCOUNTS,
                        on_click=handleProfile,
                        style=ButtonStyle(
                            padding=Padding(left=25, top=8, right=25, bottom=8),
                        )
                    )
                ]
            ),
            chatRoom,
            FloatingActionButton(
                icon=icons.CHAT,
                on_click=handleAddContact,
                bgcolor=colors.SECONDARY_CONTAINER
            )
        ]
    )
