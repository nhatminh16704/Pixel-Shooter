import pygame
from utils import scale_img

class HealthBar:
	def __init__(self, max_health, scale=0.2):

		self.max_health = max_health
		self.current_health = max_health

		# Load the health indicator image
		self.health_image = pygame.image.load('assets/icons/health_bar.png').convert_alpha()
		self.health_image = scale_img(self.health_image, scale)

	def draw(self, screen):
		# Calculate the width of the foreground based on current health
		health_ratio = self.current_health / self.max_health
		current_width = int(185 * health_ratio)
		# Draw the background (red rectangle)
		pygame.draw.rect(screen, (255, 0, 0), (30, 20, current_width, 30))
		screen.blit(self.health_image, (10, 10))

	def update_health(self, health):
		# Update current health and clamp it between 0 and max_health
		self.current_health = max(0, min(health, self.max_health))

	# def reset(self):
	# 	# Reset health to maximum
	# 	self.current_health = self.max_health
 
 
def draw_equiqment(screen, player, scale=0.08):
  font = pygame.font.SysFont('Futura', 30)
  bullet_image = pygame.image.load('assets/icons/bulletimg1.png')
  bullet_image = scale_img(bullet_image, scale)
  grenade_image = pygame.image.load('assets/icons/grenadeimage.png')
  grenade_image = scale_img(grenade_image, 0.2)
  screen.blit(bullet_image, (20, 60))
  screen.blit(grenade_image, (13, 100))
 
  # Prepare the text to be drawn
  WHITE = (0, 0, 0)
  ammo_text = f": {player.magazine}/{player.ammo}"  # Create the text string with player ammo
  text_surface = font.render(ammo_text, True, WHITE)
  nade_text = f": x {player.grenades}"  # Create the text string with player ammo
  text_surface = font.render(ammo_text, True, WHITE)
  text_surface2 = font.render(nade_text, True, WHITE)  
  
  # Get the position to draw the text, right after the bullet image
  text_x = 20 + bullet_image.get_width() + 10  # Add 10 pixels of padding to the right of the image
  text_y = 70  # Same y position as the bullet image
  
  # Blit the text surface to the screen
  screen.blit(text_surface, (text_x, text_y))
  screen.blit(text_surface2, (text_x, 110))