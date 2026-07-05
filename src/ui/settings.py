from src.ui.background import Background
from src.ui.button import Button
from src.core.window import width, height

class Settings:
    def __init__(self):
        self.background = Background('assets/sprites/backgrounds/bg_menu.png')
        self.buttons = {
            'back': Button('assets/sprites/buttons/back.png', width * 0.12, height * 0.9)
        }

    def draw(self):
        self.background.draw()
        for button in self.buttons.values():
            button.draw()

    def check_click(self, event):
        for name ,button in self.buttons.items():
            if button.click(event):
                print(f'Нажата кнопка: {name}')
                return name
        return None