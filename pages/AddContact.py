from flet import *
import flet_router as fr
from .Base import router
from service.supabase import supabase
from gotrue.types import AuthResponse


@router.route(name="addContact",
              path="/addContact"
              )
async def addContact(router: fr.FletRouter, page: Page):

    # Handler

    async def handleSearch(e):
        if not searchInput.value:
            searchInput.focus()
            return
        
        data = supabase.table("users").select("*").eq("username", searchInput.value).execute()
        print(data)
        
        if data.data == []:
            userData.content = Container(
                content=ListTile(
                    title=Text("User not found"),
                ),
                width=10000,   
            )
            page.update()
            return
        
        data = data.data[0]

        async def handleAddContact(e):
        # on click add to client storage and route to contact page
            contact_list = [{
                    "username": data["username"],
                    "last_message": "",
            }]
            load_contact = await page.client_storage.get_async("contacts")
            if load_contact:
                # check if contact already exists
                for contact in load_contact:
                    if contact["username"] == data["username"]:
                        router.go_push("/")
                        return
                contact_list = contact_list + load_contact
            await page.client_storage.set_async("contacts", contact_list)
            print(contact_list)
            router.go_push("/")

        userData.content = Container(
            content=ListTile(
                leading=Container(
                    content=Text(data["username"][0:2].upper(), color=colors.ON_SECONDARY_CONTAINER, weight=FontWeight.BOLD),
                    alignment=alignment.center,
                    width=50,
                    height=50,
                    border_radius=25,
                    bgcolor=colors.SECONDARY_CONTAINER,
                ),
                title=Text(data["username"]),
                subtitle=Text(
                    "Public Key: " + data["public_key"]
                ),
                on_click=handleAddContact,
            ),
            width=10000,   
            
        )
        page.update()

    # Input Fields
    searchInput = TextField(
        label="Search for a user",
        border_radius=15,
        border_color=colors.ON_SURFACE_VARIANT,
        autofocus=True,
        prefix_text="@ ",
        suffix_icon=icons.SEARCH,
        on_submit=handleSearch,
    )

    # Components
    userData = Card(
    )

    return View(
        controls=[
            AppBar(
                title=Text("Add Contact", weight=FontWeight.BOLD),
                center_title=True,
                toolbar_height=64,
                leading=IconButton(
                    icon=icons.ARROW_BACK,
                    on_click=lambda e: router.go_push("/"),
                ),
            ),
            searchInput,
            userData
        ]
    )
        