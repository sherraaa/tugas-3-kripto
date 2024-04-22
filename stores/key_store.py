from lib.rsa_oop import RSA
from flet import *
import asyncio

class KeyStore:
    rsa : RSA

    def __init__(self, page: Page):
        self.page = page
        self.rsa = RSA()

        asyncio.create_task(self.load_keys())

    async def load_keys(self):
        public_key = await self.page.client_storage.get_async('user.public_key')
        private_key = await self.page.client_storage.get_async('user.private_key')

        if public_key and private_key:
            self.rsa.set_keys(public_key, private_key)

    def set_keys(self, public_key, private_key):
        self.rsa.set_keys(public_key, private_key)
        self.page.client_storage.set("user.public_key", public_key)
        self.page.client_storage.set("user.private_key", private_key)
        self.page.update()

