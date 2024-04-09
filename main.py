from flet import *
import flet_router as fr
from pages.Base import router

# Pages 
from pages.Contact import contact
from pages.Auth import auth
from pages.Profile import profile
from pages.AddContact import addContact
from pages.Chat import chat
  
async def main(page: Page): 
    page.title = "Sus Chat?"
    page.theme = Theme(
        color_scheme_seed=colors.CYAN,
    )
    page.theme_mode = ThemeMode.LIGHT

    app_router = fr.FletRouter.mount(
        page,
        routes=router.routes
    )
   
    # Check if user is logged in
    print("Checking if user is logged in")
    print("Userid:", await page.client_storage.contains_key_async("user.id"))
    print("Private key:", await page.client_storage.contains_key_async("user.private_key"))
    print("Contacts:", await page.client_storage.get_async("contacts"))

    if not await page.client_storage.contains_key_async("user.id"):
        app_router.go_push("/auth")
    elif not await page.client_storage.contains_key_async("user.private_key"):
        app_router.go_push("/profile")
    else:
        app_router.go_root("/")

if __name__ == "__main__":
    app(target=main,
        assets_dir="assets",
    )