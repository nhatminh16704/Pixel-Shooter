import pygame
from const import SCREEN_HEIGHT, SCREEN_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Load image
bg1_img = pygame.image.load('assets/Background/industry/1.png').convert_alpha()
bg2_img = pygame.image.load('assets/Background/industry/2.png').convert_alpha()
bg3_img = pygame.image.load('assets/Background/industry/3.png').convert_alpha()
bg4_img = pygame.image.load('assets/Background/industry/4.png').convert_alpha()
bg5_img = pygame.image.load('assets/Background/industry/5.png').convert_alpha()

bg1_scaled = pygame.transform.scale(bg1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg2_scaled = pygame.transform.scale(bg2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg3_scaled = pygame.transform.scale(bg3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg4_scaled = pygame.transform.scale(bg4_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg5_scaled = pygame.transform.scale(bg5_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define color
BLACK = (0, 0, 0)

def draw_bg(scroll):
    screen.fill(BLACK)
    num_repeats = int(SCREEN_WIDTH / bg1_img.get_width()) + 1  
    extra_repeats = 3
    
    for x in range(num_repeats * extra_repeats):
        screen.blit(bg1_scaled, ((x * SCREEN_WIDTH) - scroll, 0))
        screen.blit(bg2_scaled, ((x * SCREEN_WIDTH) - scroll * 0.5, 0))
        screen.blit(bg3_scaled, ((x * SCREEN_WIDTH) - scroll * 0.6, 0))
        screen.blit(bg4_scaled, ((x * SCREEN_WIDTH) - scroll * 0.7, 0))
        screen.blit(bg5_scaled, ((x * SCREEN_WIDTH) - scroll * 0.8, 0))
		
