import os
import pygame
from src.core.window import new_form

def load_animation_frames(folder_path, prefix):
    frames = []
    try:
        files = sorted(os.listdir(folder_path))
    except FileNotFoundError:
        print(f"Ошибка: Папка {folder_path} не найдена!")
        return frames

    for file_name in files:
        if file_name.startswith(prefix) and file_name.endswith('.png'):
            full_path = os.path.join(folder_path, file_name)
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * new_form, img.get_height() * new_form))
            
            frames.append(img)
            
    return frames

def load_image(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (img.get_width() * new_form, img.get_height() * new_form))

def load_pure_image(path, use_alpha=False):
    if use_alpha:
        return pygame.image.load(path).convert_alpha()
    return pygame.image.load(path).convert()

def load_block_image(path, use_alpha=False):
    img = pygame.image.load(path)
    img = img.convert_alpha() if use_alpha else img.convert()
    
    return pygame.transform.scale(img, (img.get_width() * new_form, img.get_height() * new_form))