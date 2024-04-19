from flet import *
from router import views_handler

   
async def main(page: Page):
    page.title = "Suslicious"
    page.theme = Theme(
        color_scheme_seed=colors.CYAN,
    ) 
    page.theme_mode = ThemeMode.LIGHT
    page.theme.page_transitions.windows = PageTransitionTheme.NONE
    page.theme.page_transitions.android = PageTransitionTheme.NONE

    user = {
        'user.id': await page.client_storage.get_async('user.id'),
        'user.username': await page.client_storage.get_async('user.username'),
        'user.private_key': await page.client_storage.get_async('user.private_key'),
    }

    print(user)
    
    def route_change(route):
        page.views.clear()
        print(page.route)
        page.views.append(
            views_handler(page, '/')
        )
        if page.route != '/':
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
    
    if not user['user.id']:
        page.go('/auth')
    elif not user['user.private_key']:
        page.go('/profile')
    else:
        page.go('/')

if __name__ == "__main__":
    app(target=main,
        assets_dir="assets",
    )