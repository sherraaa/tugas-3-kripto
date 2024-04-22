import asyncio
import websockets
from flet import *
import json

from pages.Chat import MessageBubble, MessageList
from router import views_handler

from stores.user_store import UserStore
from stores.contact_store import ContactStore, Contact, Message
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
        parsed_data = json.loads(data)
        if parsed_data["event"] == "INSERT":
            if parsed_data['payload'].get('record', {}).get('recipient') == page.user.user.username:
                print("Message for me")

                
                print("Adding message to contact")
                contacts : ContactStore = page.contacts
                contacts.add_message(
                    Message(
                        id=parsed_data['payload'].get('record', {}).get('id'),
                        type=parsed_data['payload'].get('record', {}).get('type'),
                        author=parsed_data['payload'].get('record', {}).get('author'),
                        content=parsed_data['payload'].get('record', {}).get('content'),
                        created_at=parsed_data['payload'].get('record', {}).get('created_at'),
                    )
                )
                if '/chat/' in page.route:
                    print("Updating chat")
                    message_list : MessageList = page.message_list
                    message_list.add_message(
                        MessageBubble(
                            page=page,
                            message=Message(
                                id=parsed_data['payload'].get('record', {}).get('id'),
                                type=parsed_data['payload'].get('record', {}).get('type'),
                                author=parsed_data['payload'].get('record', {}).get('author'),
                                content=parsed_data['payload'].get('record', {}).get('content'),
                                created_at=parsed_data['payload'].get('record', {}).get('created_at'),
                            )
                        )
                    )
                else:
                    if page.route == '/':
                        page.contact_list.load_contacts()
                    print("Notification")
                    page.snack_bar = SnackBar(
                        content=Text("New message from " + parsed_data['payload'].get('record', {}).get('author')),
                    )
                    page.snack_bar.open = True
                    page.update()


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