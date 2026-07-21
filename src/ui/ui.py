from .button import Button

class UI:
    def __init__(self, context):
        self.buttons = [
            Button(context, position=(500,350), size=(200,80),purpose=self.onClick)
        ]

    def onClick(self):
        print("THIS BUTTON HAS BEEN PRESSED")

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def render(self):
        for button in self.buttons:
            button.render()