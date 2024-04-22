from flet import *
from service.supabase import supabase
from postgrest.base_request_builder import APIResponse

from stores.contact_store import ContactStore, Contact

class ResultCard(UserControl):
    def __init__(self, page: Page, data: dict):
        super().__init__()
        self.page = page
        self.data = data

    def build(self):
        if self.data == {}:
            return Card(
                content=Container(
                    content=ListTile(
                        title=Text("No user found"),
                    )
                )
            )
        return Card(
            content=Container(
                content=ListTile(
                    title=Text(self.data["username"], weight=FontWeight.W_500),
                    subtitle=Text(self.data["public_key"]),
                    leading=Container(
                        content=Text(self.data["username"][0:2].upper(), color=colors.ON_SECONDARY_CONTAINER, weight=FontWeight.BOLD),
                        alignment=alignment.center,
                        width=50,
                        height=50,
                        border_radius=25,
                        bgcolor=colors.SECONDARY_CONTAINER
                    )
                ),
                on_click=self.handleAddContact
            )
        )

    def handleAddContact(self, e):
        # on click add to client storage and route to contact page
        contacts : ContactStore = self.page.contacts
        contacts.add_contact(
            Contact(
                username=self.data["username"],
                last_message="Start a conversation with " + self.data["username"] + " now!",
                chat=[]
            )
        )
        self.page.go("/")
            

class AddContactView(View):


    def __init__(self, page: Page):
        super().__init__()
        self.route = "/addContact"
        self.page = page

        # Components
        self.searchInput = TextField(
            label="Search for a user",
            border_radius=15,
            border_color=colors.ON_SURFACE_VARIANT,
            autofocus=True,
            prefix_text="@ ",
            suffix_icon=icons.SEARCH,
            on_submit=self.handleSearch,
            input_filter=InputFilter(
                regex_string=r"[a-zA-Z0-9_]",
            ),
        )

        self.appbar = AppBar(
            title=Text("Add Contact", weight=FontWeight.BOLD),
            center_title=True,
            toolbar_height=64,
            leading=IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: self.page.go("/"),
            ),
        )

        self.controls = [
            self.searchInput
        ]
    
    async def handleSearch(self, e):
        if not self.searchInput.value or self.searchInput.value == self.page.user.user.username:
            self.searchInput.focus()
            return
        print("Searching for user", self.searchInput.value)
        if self.controls:
            self.controls.clear()
            self.controls.append(self.searchInput)
        
        data : APIResponse = supabase.table("users").select("*").eq("username", self.searchInput.value).execute()
        print(data)

        if data.data == []:
            self.controls.append(ResultCard(self.page, {}))
            self.page.update()
            return
        
        data = data.data[0]    
        self.controls.append(ResultCard(self.page, data))
        self.page.update()




        