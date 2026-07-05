import pygame
from src.ui.menu import Menu
from src.ui.settings import Settings
from src.core.game import Game

menu = Menu()
settings = Settings()
game = Game()
current_screen = 'menu'

clock = pygame.time.Clock()
start = True
while start:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            start = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        if current_screen == 'menu':
            action = menu.check_click(event)
            if action == 'play':
                current_screen = 'game'
            if action == 'settings':
                current_screen = 'settings'
            elif action == 'exit':
                start = False
        elif current_screen == 'settings':
            action = settings.check_click(event)
            if action == 'back':
                current_screen = 'menu'

    if current_screen == 'menu':
        menu.draw()
    elif current_screen == 'settings':
        settings.draw()
    elif current_screen == 'game':
        game.update_and_draw(events)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()