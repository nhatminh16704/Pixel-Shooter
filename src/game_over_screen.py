import pygame

from src.button import Button
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, NAVY_BLUE
from src.screen_fade import ScreenFade


def game_over_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Shooter")
    logo = pygame.image.load('assets/logo.png')
    pygame.display.set_icon(logo)
    clock = pygame.time.Clock()
    FPS = 60

    #variables
    restart = False
    exit_game = False
    death_fade = ScreenFade(2, NAVY_BLUE, 8)

    #load images
    restart_img = pygame.image.load('assets/Button/restart_btn.png').convert_alpha()

    #create button
    restart_button = Button(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 50, restart_img, 2.5)

    # define font
    title_font = pygame.font.Font('assets/title_text_font.ttf', 70)
    title_text = title_font.render("GAME OVER", True, BLACK)

    run = True
    while run:
        clock.tick(FPS)

        if death_fade.fade(screen, SCREEN_WIDTH):
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 200))
            if restart_button.draw(screen):
                run = False
                restart = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit_game = True

        pygame.display.update()

    return restart, exit_game


if __name__ == "__main__":
    restart = game_over_screen()
    if restart:
        pygame.quit()