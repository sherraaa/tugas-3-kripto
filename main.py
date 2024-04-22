import asyncio
import websockets
from flet import *
import json

from router import views_handler

from stores.user_store import UserStore
from stores.contact_store import ContactStore, Contact
from service.supabase import supabase

async def listen_for_messages(page: Page, message_queue: asyncio.Queue):
    print("Listening for messages")
    URL = supabase.realtime_url + f'/websocket?apikey={supabase.supabase_key}&vsn=1.0.0'
    ws_connection = await websockets.connect(URL)
    if ws_connection.open:
        await ws_connection.send('{"topic":"realtime:*","event":"phx_join","payload":{},"ref":"1"}')
        while True:
            data = await ws_connection.recv()
            await message_queue.put(data)  # Put received data into the message_queue
    print("Connection closed")

async def process_messages(page: Page, message_queue: asyncio.Queue):
    while True:
        data = await message_queue.get()  # Get data from the message_queue
        if data:
            parsed_data = json.loads(data)
            print("Received message:", data)
            if parsed_data['payload'].get('record', {}).get('recipient') == page.user.user.username:
                print("Message for me")
        # Process the received data here

async def main(page: Page):
    page.title = "Suslicious"
    page.theme = Theme(
        color_scheme_seed=colors.CYAN,
    ) 
    page.theme_mode = ThemeMode.LIGHT
    page.theme.page_transitions.windows = PageTransitionTheme.NONE
    page.theme.page_transitions.android = PageTransitionTheme.NONE

    # Create a message queue
    message_queue = asyncio.Queue()

    # Run listen_for_messages concurrently with app()
    listen_task = asyncio.create_task(listen_for_messages(page, message_queue))
    process_task = asyncio.create_task(process_messages(page, message_queue))

    page.user = UserStore(page)
    page.contacts = ContactStore(page)

    def route_change(route):
        page.views.clear()
        print(page.route)
        page.views.append(
            views_handler(page, page.route)
        )
        page.update()
 
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go("/loading")


if __name__ == "__main__":
    app(target=main, assets_dir="assets")