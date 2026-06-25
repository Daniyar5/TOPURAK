from src.core.window import window, width
from src.utils.assets import load_image
from src.ui.button import Button

class Menu:
    def __init__(self, background_path, buttons):
        self.background = load_image(background_path)
        self.buttons = buttons

    def draw(self):
        window.blit(self.background, (0, 0))
        for button in self.buttons.values():
            button.draw()

    def check_clicks(self, event):
        for name ,button in self.buttons.items():
            if button.click(event):
                print(f'Нажата кнопка: {name}')
                return name
        return None
    
def create_main_menu():
    return Menu('assets/sprites/backgrounds/bg_menu.png', {
        "TOPURAK": Button(width / 2, 100, 'assets/sprites/title/TOPURAK.png'),
        "play": Button(width / 2, 300, 'assets/sprites/buttons/play.png'),
        "settings": Button(width / 2, 400, 'assets/sprites/buttons/settings.png'),
        "exit": Button(width / 2, 500, 'assets/sprites/buttons/exit.png')
    })