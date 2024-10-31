import pygame

from const import SCREEN_WIDTH, SCREEN_HEIGHT
from button import Button
from const import BLACK


def end_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Shooter")
    logo = pygame.image.load('assets/logo.png')
    pygame.display.set_icon(logo)
    clock = pygame.time.Clock()
    FPS = 60

    #variables
    global exit_game
    exit_game = False

    # load images
    bg_image = pygame.image.load('assets/Background.png').convert_alpha()
    bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    exit_img = pygame.image.load('assets/Button/exit_btn.png').convert_alpha()

    # create button
    exit_button = Button(SCREEN_WIDTH // 2 - 107, SCREEN_HEIGHT // 2 + 100, exit_img, 1)

    # define font
    title_font = pygame.font.Font('assets/title_text_font.ttf', 40)
    end_text1 = title_font.render("PIXEL SHOOTER IS END.", True, BLACK)
    end_text2 = title_font.render("THANKS FOR PLAYING!", True, BLACK)

    # Based between the screen
    end_text1_rect = end_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125))
    end_text2_rect = end_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 45))

    # waiting for close the game screen
    run = True
    while run:
        clock.tick(FPS)

        screen.blit(bg, (0, 0))
        screen.blit(end_text1, end_text1_rect)
        screen.blit(end_text2, end_text2_rect)

        if exit_button.draw(screen):
            run = False
            exit_game = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit_game = True

        pygame.display.flip()

    return exit_game


if __name__ == "__main__":
    exit_game = end_screen()
    if exit_game:
        pygame.quit()