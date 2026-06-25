import pygame
from src.core.game import Game
from src.ui.menu import create_main_menu

pygame.init()

clock = pygame.time.Clock()
menu = create_main_menu()
current_screen = 'menu'
start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if current_screen == 'menu':
            action = menu.check_clicks(event)
            if action == 'play':
                current_screen = 'game'
            elif action == 'exit':
                start = False

    if current_screen == 'menu':
        menu.draw()
    elif current_screen == 'game':
        Game.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()