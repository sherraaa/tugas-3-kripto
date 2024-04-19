from datetime import datetime
from flet import *

class DateDivider(UserControl):
    def __init__(self, date):
        super().__init__()
        self.date = date

    def build(self):
        # Transforming to Sun, 10 Oct 2021
        return Row(
            controls=[
                Container(
                    content=Text(datetime.fromisoformat(self.date).strftime("%a, %d %b %Y"), size=10),
                    bgcolor=colors.SECONDARY_CONTAINER,
                    padding=8,
                    border_radius=8,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )

class Chat(UserControl):
    def __init__(self, page : Page, username, id, type, from_user, to_user, content, created_at):
        super().__init__()
        self.page = page
        self.username = username
        self.id = id
        self.type = type
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        self.created_at = created_at
        self.container_width = None
        if len(self.content) * 12 > self.page.width:
            self.container_width = self.page.width - 150 + ((len(self.content) * 8 - self.page.width) / (len(self.content) * 8) * 50)


    def build(self):
        if self.type == "text":
            content = Container(
                content=Text(self.content),
                padding=8,
                width=self.container_width,
            )
        else:
            content = Container(
                content=Column(
                    controls=[
                        Container(
                            content=Text("Encrypted File", size=16),
                            width=190,
                            padding=8,
                            alignment=alignment.center,
                            bgcolor=colors.BACKGROUND,
                            border_radius=8,
                            border=border.all(1, colors.OUTLINE_VARIANT)
                        ),
                        Row(
                            controls=[
                                ElevatedButton(
                                    text=("Open"),
                                ),
                                FilledButton(
                                    text=("Decrypt"),
                                )
                            ]
                        )
                    ]
                ),
                padding=8,
            )

        if self.from_user == self.username:
            return Row(
                controls=[
                    Card(
                        content=content,
                        color=colors.BACKGROUND
                    ),           
                    Text(datetime.fromisoformat(self.created_at).strftime("%H:%M"), size=12),
                ],
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.END,
            )
        else:
            return Row(
                controls=[
                    Text(datetime.fromisoformat(self.created_at).strftime("%H:%M"), size=12),
                    Card(
                        content=content,
                    ),
                ],
                alignment=MainAxisAlignment.END,
                vertical_alignment=CrossAxisAlignment.END,
            )
        
    async def details(self, e):
        print("Going to chat details", self.id)

class ChatRoom(UserControl):
    def __init__(self, page, username, chats):
        super().__init__()
        self.page = page
        self.username = username
        self.chats = chats
        self.chat_list = ListView(
            spacing=4,
            expand=True,
            auto_scroll=True,
        )
        self.dates = {}

    def build(self):
        for chat in self.chats:
            date = datetime.fromisoformat(chat["created_at"]).date()
            if date not in self.dates:
                self.dates[date] = DateDivider(chat["created_at"])
                self.chat_list.controls.append(self.dates[date])
            self.chat_list.controls.append(
                Chat(
                    page=self.page,
                    username=self.username,
                    id=chat["id"],
                    type=chat["type"],
                    from_user=chat["from_user"],
                    to_user=chat["to_user"],
                    content=chat["content"],
                    created_at=chat["created_at"],
                )
            )
        return Container(
            content=self.chat_list,
            padding=4,
            expand=True,
            bgcolor=colors.RED_50
        )
    
    async def add_chat(self, chat):
        date = datetime.fromisoformat(chat["created_at"]).date()
        if date not in self.dates:
            self.dates[date] = DateDivider(chat["created_at"])
            self.chat_list.controls.append(self.dates[date])
        self.chat_list.controls.append(
            Chat(
                page=self.page,
                username=self.username,
                id=chat["id"],
                type=chat["type"],
                from_user=chat["from_user"],
                to_user=chat["to_user"],
                content=chat["content"],
                created_at=chat["created_at"],
            )
        )
        
class ChatPage(UserControl):
    def __init__(self, page, username):
        super().__init__()
        self.page = page
        self.chats = [
            {
                "id": "1",
                "type": "text",
                "from_user": "test",
                "to_user": "nat",
                "content": "Hello",
                "created_at": "2021-10-10 19:00:00",
            },
            # {
            #     "id": "2",
            #     "type": "text",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "Hi",
            #     "created_at": "2021-10-10 19:02:30",
            # },
            # {
            #     "id": "3",
            #     "type": "text",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "How are you?",
            #     "created_at": "2021-10-10 19:02:35",
            # },
            # {
            #     "id": "4",
            #     "type": "text",
            #     "from_user": "test",
            #     "to_user": "nat",
            #     "content": "I'm fine. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio",
            #     "created_at": "2021-10-10 19:02:40",
            # },
            # {
            #     "id": "5",
            #     "type": "file",
            #     "from_user": "test",
            #     "to_user": "nat",
            #     "content": "Link",
            #     "created_at": "2021-10-10 19:02:40",
            # },
            # {
            #     "id": "6",
            #     "type": "file",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "Link",
            #     "created_at": "2021-10-10 19:02:40",
            # },
            # {
            #     "id": "1",
            #     "type": "text",
            #     "from_user": "test",
            #     "to_user": "nat",
            #     "content": "Hello",
            #     "created_at": "2021-10-10 19:00:00",
            # },
            # {
            #     "id": "2",
            #     "type": "text",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "Hi",
            #     "created_at": "2021-10-10 19:02:30",
            # },
            # {
            #     "id": "3",
            #     "type": "text",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "How are you?",
            #     "created_at": "2021-10-10 19:02:35",
            # },
            # {
            #     "id": "4",
            #     "type": "text",
            #     "from_user": "test",
            #     "to_user": "nat",
            #     "content": "I'm fine. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio",
            #     "created_at": "2021-10-10 19:02:40",
            # },
            # {
            #     "id": "5",
            #     "type": "file",
            #     "from_user": "test",
            #     "to_user": "nat",
            #     "content": "Link",
            #     "created_at": "2021-10-10 19:02:40",
            # },
            # {
            #     "id": "6",
            #     "type": "file",
            #     "from_user": "nat",
            #     "to_user": "test",
            #     "content": "Link",
            #     "created_at": "2021-10-10 19:02:40",
            # },
        ]
        self.username = username
        

    def build(self):
        return Column(
            [
                ChatRoom(
                    page=self.page,
                    username=self.username,
                    chats=self.chats,
                ),
                Row(
                    [
                        TextField(
                            label="Type a message",
                        )
                    ]
                )
            ],
            expand=True,
        )