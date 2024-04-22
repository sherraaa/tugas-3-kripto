from flet import *

class LoadingView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/loading"
        self.page = page
        self.controls = [
            ProgressRing(
                width=50,
                height=50,
                stroke_width=4,
                stroke_cap=StrokeCap.ROUND
            ),
        ]
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.on_load()

    def on_load(self):
        while not self.page.contacts.loaded or not self.page.user.loaded:
            pass
        print(self.page.user.user.id)
        print(self.page.user.user.private_key)
        if self.page.user.user.id == None:
            self.page.go("/auth")
        elif self.page.user.user.private_key == None:
            self.page.go("/profile")
        else:
            self.page.go("/")
