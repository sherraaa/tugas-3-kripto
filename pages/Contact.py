from flet import *

class ContactCard(Card):
    def __init__(self, page: Page, username: str, last_message: str):
        super().__init__()
        self.page = page
        self.username = username
        self.last_message = last_message

        self.content = Container(
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
    
    def go_chat(self, e):
        print("Going to chat", self.username)
        self.page.go(f"/chat/{self.username}")

class ContactList(Container):
    contact_list = ListView(
        expand=True,
        spacing=4,
    )

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.contacts = self.page.contacts.contacts
        self.contact_list.controls = []
        if self.contact_list.controls:
            self.contact_list.controls.clear()
        self.load_contacts()

        self.content = self.contact_list
        self.padding = 4
        self.expand = True

    def load_contacts(self):
        for contact in self.contacts:
            self.contact_list.controls.append(
                ContactCard(
                    page=self.page,
                    username=contact.username,
                    last_message=contact.last_message,
                )
            )
        self.page.update()

class ContactView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/"
        self.page = page

        self.appbar = AppBar(
            title=Text("Suslicious", weight=FontWeight.BOLD),
            center_title=True,
            toolbar_height=64,
            leading=Container(),
            actions=[
                IconButton(
                    icon=icons.MANAGE_ACCOUNTS,
                    on_click=lambda _: page.go("/profile"),
                    style=ButtonStyle(
                        padding=Padding(left=25, top=8, right=25, bottom=8),
                    )
                )
            ]
        )
    
        self.floating_action_button = FloatingActionButton(
            icon=icons.CHAT,
            on_click=lambda _: page.go("/addContact"),
            bgcolor=colors.SECONDARY_CONTAINER
        )

        self.controls = [
            ContactList(page),
        ]