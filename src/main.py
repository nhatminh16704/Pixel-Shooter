import pygame
import sys
from utils import load_sound
from const import SCREEN_HEIGHT, SCREEN_WIDTH
from ui import draw_equiqment
from world import World, load_level, check_comple
from background import draw_bg


load_sound()

SCROLL = 0


# Set the dimensions of the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# bg_img = pygame.image.load("assets/Background.png").convert_alpha()
# bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Shooter")

# Create a group for bullets
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()
			
# Initialize Pygame
pygame.init()



# Load the initial level
current_level = 0
world_data = load_level(current_level)
world = World(world_data)
player1, health_bar = world.process_data(enemy_group)
# Create a HealthBar instance


# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
		 # Get key states (which keys are pressed)
    keys = pygame.key.get_pressed()
    # screen.blit(bg_img, (0, 0))

    # Update player position based on key presses
    SCROLL = player1.move(keys, bullet_group, grenade_group, world.tile_rects, world.items)
    draw_bg(SCROLL)
    world.draw(screen, SCROLL)
    if player1.reached_exit:
        player1, health_bar, current_level = check_comple(current_level, player1, health_bar, enemy_group)
        player1.reached_exit = False

    player1.update_animation()
    player1.check_alive()
    player1.check_hurt()
    bullet_group.update(player1, enemy_group, world.tile_rects)
    grenade_group.update(explosion_group, enemy_group, player1, world.tile_rects)
    explosion_group.update()
    health_bar.update_health(player1.health)
    
    for enemy in enemy_group:
      enemy.check_alive()
      enemy.check_hurt()
      enemy.update_animation()
      enemy.npc_vision_and_shoot(player1, bullet_group, world.tile_rects)
      enemy.draw(screen, SCROLL)
    
    player1.draw(screen, SCROLL)
    health_bar.draw(screen)
    draw_equiqment(screen, player1)
		# Draw the bullets
    bullet_group.draw(screen)
    for grenade in grenade_group:
        grenade.draw(screen, SCROLL)
    for ex in explosion_group:
        ex.draw(screen, SCROLL)
  
    # load_level(current_level)
    
    # Update the display
    pygame.display.flip()