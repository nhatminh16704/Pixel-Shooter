import pygame
import sys
from utils import load_sound
from const import SCREEN_HEIGHT, SCREEN_WIDTH
from ui import draw_equiqment
from world import World, load_level

# Initialize Pygame
pygame.init()

load_sound()

SCROLL = 0

# Set the dimensions of the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_img = pygame.image.load("assets/Background.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Pixels Shooter")

# Create sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load the initial level
current_level = 0
world_data = load_level(current_level)
world = World(world_data)
player1, health_bar = world.process_data(enemy_group)

# Main loop
running = True
while running:
  # Event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Get key states (which keys are pressed)
  keys = pygame.key.get_pressed()
  screen.blit(bg_img, (0, 0))
  world.draw(screen, SCROLL)
  
  # Update player position based on key presses
  SCROLL = player1.move(keys, bullet_group, grenade_group, world.tile_rects, world.items)
  player1.update_animation()
  player1.check_alive()
  player1.check_hurt()
  
  # Update groups
  bullet_group.update(player1, enemy_group, world.tile_rects)
  grenade_group.update(explosion_group, enemy_group, player1, world.tile_rects)
  explosion_group.update()
  health_bar.update_health(player1.health)
  
  # Update and draw enemies
  for enemy in enemy_group:
    enemy.check_alive()
    enemy.check_hurt()
    enemy.update_animation()
    enemy.npc_vision_and_shoot(player1, bullet_group, world.tile_rects)
    enemy.draw(screen, SCROLL)
  
  # Draw player, health bar, and equipment
  player1.draw(screen, SCROLL)
  health_bar.draw(screen)
  draw_equiqment(screen, player1)
  
  # Draw bullets, grenades, and explosions
  bullet_group.draw(screen)
  for grenade in grenade_group:
    grenade.draw(screen, SCROLL)
  for ex in explosion_group:
    ex.draw(screen, SCROLL)
  
  # Update the display
  pygame.display.flip()
  
  # Set frame rate (e.g., 60 frames per second)
  clock.tick(60)  # This will make the game run at 60 FPS

# Cleanly exit Pygame
pygame.quit()
sys.exit()
