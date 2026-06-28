import pygame
from src.core.game import Game
from src.ui.menu import create_main_menu

pygame.init()

game_instance = Game()

clock = pygame.time.Clock()
menu = create_main_menu()
current_screen = 'menu'
start = True
while start:
    events = pygame.event.get()
    for event in events:
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
        game_instance.update_and_draw(events)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()