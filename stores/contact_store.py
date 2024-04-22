import base64
from typing import List
from flet import Page
import asyncio

class Message:
    id: str
    type: str
    author: str
    content: str
    created_at: str

    def __init__(self, id: str, type: str, author: str, content: str, created_at: str):
        self.id = id
        self.type = type
        self.author = author
        self.content = content
        self.created_at = created_at

class Contact:
    username: str
    last_message: str
    chat: List[Message] = []

    def __init__(self, username: str, last_message: str = None, chat = []):
        self.username = username
        self.last_message = last_message if last_message else "Start a conversation with " + username + " now!"
        self.load_chat(chat)

    def load_chat(self, chat):
        self.chat = []
        for message in chat:
            self.chat.append(Message(message["id"], message["type"], message["author"], message["content"], message["created_at"]))

    def add_message(self, message: Message, page: Page):
        self.chat.append(message)
        if message.type == "file":
            self.last_message = "Sent an encrypted file"
            return
        self.last_message = message.content 
        if message.author == self.username:
            last_message = message.content
            decoded_string = base64.b64decode(last_message).decode()
            decoded_numbers = [int(number) for number in decoded_string.split(",")]
            decrypted = page.rsa.rsa.decrypt(decoded_numbers)
            decrypted = base64.b64decode(decrypted.encode()).decode()
            self.last_message = decrypted
            
        

class ContactStore: 
    contacts: List[Contact] = []

    def __init__(self, page: Page):
        self.page = page
        self.contacts = []
        self.loaded = False
        asyncio.create_task(self.load_contacts())
        print("Contact store initialized")
        self.print_contacts()

    async def load_contacts(self):
        self.contacts = []
        self.loaded = False
        contacts = await self.page.client_storage.get_async("contacts")
        if contacts:
            for contact in contacts:
                self.contacts.append(Contact(contact["username"], contact["last_message"], contact["chat"]))
        self.loaded = True

    def add_contact(self, contact: Contact):
        # check if contact already exists
        for c in self.contacts:
            if c.username == contact.username:
                return
            
        # adding to the top
        self.contacts.insert(0, contact)
        self.page.client_storage.set("contacts", self.contacts)

    def search_contact(self, username: str):
        for contact in self.contacts:
            if contact.username == username:
                return contact
        return None

    def update_last_message(self, username: str, message: str):
        for contact in self.contacts:
            if contact.username == username:
                contact.last_message = message
                asyncio.create_task(self.page.client_storage.set_async("contacts", self.contacts))
                break

    def print_contacts(self):
        print("All contacts:")
        for contact in self.contacts:
            print(contact.username)

    def clear(self):
        self.contacts = []
        self.loaded = False
        self.page.client_storage.clear()
        self.page.update()

    def get_contact(self, username: str) -> Contact:
        for contact in self.contacts:
            if contact.username == username:
                return contact
        return None
    
    def update_client_storage(self):
        asyncio.create_task(self.page.client_storage.set_async("contacts", self.contacts))
        self.page.update()
    
    def move_contact_to_top(self, contact: Contact):
        self.contacts.remove(contact)
        self.contacts.insert(0, contact)
        self.update_client_storage()
        self.page.update()

    def add_message(self, message : Message):
        contact = self.get_contact(message.author)
        if contact:
            contact.add_message(message, self.page)
            self.move_contact_to_top(contact)
        else:
            contact = Contact(
                username=message.author,
                last_message=message.content,
            )
            contact.add_message(message, self.page)
            self.add_contact(contact)