from flet import *
from service.supabase import supabase
from postgrest.base_request_builder import APIResponse

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
                        title=Text("No results found"),
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
            contact_list = [{
                    "username": self.data["username"],
                    "last_message": "",
            }]
            load_contact =  self.page.client_storage.get("contacts")
            if load_contact:
                # check if contact already exists
                for contact in load_contact:
                    if contact["username"] == self.data["username"]:
                        self.page.go("/")
                        return
                contact_list = contact_list + load_contact
            self.page.client_storage.set("contacts", contact_list)
            print(contact_list)
            self.page.go("/")
            

class AddContact(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        # Input Fields
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

    def build(self):
        self.column = Column()
        self.column.controls.append(self.searchInput)
        return self.column
    
    async def handleSearch(self, e):
        if not self.searchInput.value:
            self.searchInput.focus()
            return
        print("Searching for user", self.searchInput.value)
        self.column.controls.clear()
        self.column.controls.append(self.searchInput)
        
        data : APIResponse = supabase.table("users").select("*").eq("username", self.searchInput.value).execute()
        print(data)

        if data.data == []:
            self.column.controls.append(ResultCard(self.page, {}))
            self.update_async()
            return
        
        data = data.data[0]    
        self.column.controls.append(ResultCard(self.page, data))
        self.update()




        