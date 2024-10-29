import pygame

from src.Button import Button
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK


def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Shooter")
    logo = pygame.image.load('assets/logo.png')
    pygame.display.set_icon(logo)

    # menu variables
    start_game = False
    exit_game = False

    #load images
    bg_image = pygame.image.load('assets/Background.png').convert_alpha()
    bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    start_img = pygame.image.load('assets/Button/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('assets/Button/exit_btn.png').convert_alpha()

    # create button
    start_button = Button(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50, start_img, 1.1)
    exit_button = Button(SCREEN_WIDTH // 2 - 107, SCREEN_HEIGHT // 2 + 100, exit_img, 1)

    #define font
    title_font = pygame.font.Font('assets/title_text_font.ttf', 70)
    title_text = title_font.render("PIXEL SHOOTER", True, BLACK)

    run = True
    while run:
        screen.blit(bg, (0,0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))
        if start_button.draw(screen):
            run = False
            start_game = True
        if exit_button.draw(screen):
            run = False
            exit_game = True

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit_game = True

    return start_game, exit_game


if __name__ == "__main__":
    start_game, exit_game = start_menu()
    if exit_game:
        pygame.quit()