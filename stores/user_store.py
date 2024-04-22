import asyncio
from flet import *

class User:
    id : str = None
    username : str = None
    private_key : str = None
    public_key : str = None

    def __init__(self, id, username, private_key, public_key = None):
        self.id = id
        self.username = username
        self.private_key = private_key
        self.public_key = public_key

class UserStore:
    user : User = None

    def __init__(self, page: Page):
        self.page = page
        self.loaded = False
        asyncio.create_task(self.load_user())

    async def load_user(self):
        user_id = await self.page.client_storage.get_async('user.id')
        user_username =  await self.page.client_storage.get_async('user.username')
        user_private_key = await self.page.client_storage.get_async('user.private_key')
        user_public_key = await self.page.client_storage.get_async('user.public_key')

        self.user = User(
            id=user_id,
            username=user_username,
            private_key=user_private_key,
            public_key=user_public_key
        )
        self.loaded = True
        return self.user
    
    def set_user(self, id, username, private_key):
        asyncio.create_task(self._set_user(id, username, private_key))
    
    async def _set_user(self, id, username, private_key, public_key = None):
        self.user = User(
            id=id,
            username=username,
            private_key=private_key,
            public_key=public_key
        )
        await self.page.client_storage.set_async("user.id", id)
        await self.page.client_storage.set_async("user.username", username)
        if private_key:
            await self.page.client_storage.set_async("user.private_key", private_key)
        self.loaded = True
        return self.user
    
    def set_public_key(self, public_key):
        self.user.public_key = public_key
        self.page.client_storage.set("user.public_key", public_key)
        self.page.update()

    def set_private_key(self, private_key):
        self.user.private_key = private_key
        self.page.client_storage.set("user.private_key", private_key)
        self.page.update()

    def logout(self):
        self.user = None
        self.loaded = False
        self.page.client_storage.clear()
        self.page.update()