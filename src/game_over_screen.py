import pygame

from src.button import Button
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK


def game_over_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Shooter")
    logo = pygame.image.load('assets/logo.png')
    pygame.display.set_icon(logo)

    #load images
    restart_img = pygame.image.load('assets/Button/restart_btn.png').convert_alpha()

    #create button
    restart_img = Button(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50, restart_img, 1.1)

    # define font
    title_font = pygame.font.Font('assets/title_text_font.ttf', 70)
    title_text = title_font.render("PIXEL SHOOTER", True, BLACK)

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    game_over_screen()