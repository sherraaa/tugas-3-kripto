from flet import *
from pages.Contact import ContactView
from pages.Profile import ProfileView
from pages.Auth import AuthView
from pages.AddContact import AddContactView
from pages.Chat import ChatView
from pages.Loading import LoadingView

def views_handler(page: Page, path: str):
    troute = TemplateRoute(path)
    view = None
    if troute.match('/'):
        view = ContactView(page=page)
    elif troute.match('/profile'):
        view = ProfileView(page=page)
    elif troute.match('/addContact'):
        view = AddContactView(page)
    elif troute.match('/auth'):
        view = AuthView(page=page)
    elif troute.match('/chat/:username'):
        view = ChatView(page=page, contact=troute.username)
    elif troute.match('/loading'):
        view = LoadingView(page=page)

    return view