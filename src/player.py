import random
import pygame
from bullet import Bullet
from grenade import Grenade
from utils import load_animation, get_sound
from const import PLAYER_SPEED, TILE_SIZE, SCROLL_THRESHOLD, SCREEN_WIDTH



class Player(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, ammo, grenades):
		super().__init__()  # Call the parent class (Sprite) constructor
		self.update_time = pygame.time.get_ticks()
		self.scroll = 0
		self.action = 'idle'
		self.frame_index = 0
		self.vel_y = 0
		self.on_ground = True
		self.gravity = 0
		self.shoot_cooldown = 500  # Cooldown timer for shooting
		self.last_shot = pygame.time.get_ticks()
		self.ammo = ammo
		self.start_ammo = ammo
		self.alive = True
		self.health = 1000 if char_type == 'Main_char' else 100
		self.max_health = self.health
		self.throw_cooldown = 1000
		self.last_throw = pygame.time.get_ticks()
		self.grenades = grenades
		self.animation_cooldown = 100
		self.magazine = 5 if char_type == 'Main_char' else 20
		self.speed = 2
		self.is_npc = True if char_type == 'Enemy' else False
		self.is_reloading = False  # Flag to track if the player is reloading
  
		#npc var
		self.patrol_direction = 1
		self.count_move = 0
		self.idle_start_time = 0
		self.idle_duration = 0

		self.animation_list = load_animation(char_type, scale)
	
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect.center = (x, y)
		self.direction = 0  # Initial direction
	
	def move(self, keys, bullet_group, grenade_group, tile_rects, items):
		# Store the current position for collision checking
		dx = 0
		dy = 0
		# Move player based on arrow key input
		if keys[pygame.K_a]:
			dx -= PLAYER_SPEED
			self.direction = 1
		if keys[pygame.K_d]:
			dx = PLAYER_SPEED
			self.direction = 0
		if keys[pygame.K_w] and self.on_ground and not self.is_reloading:
			self.vel_y = -10
			self.rect.y += self.vel_y
			self.gravity = 0.5
			self.on_ground = False
			jump_sound = get_sound("jump")  # Play jump sound effect
			jump_sound.play()  # Play jump sound effect
		if keys[pygame.K_SPACE] and not self.is_reloading:
			self.shoot(bullet_group)  # Call shoot function
		if keys[pygame.K_q] and not self.is_reloading:
			self.throw(grenade_group)  # Call shoot function
		if keys[pygame.K_r] and self.on_ground:
			self.reload()

		# Apply gravity
		self.vel_y += self.gravity
		dy += self.vel_y
  


		# Horizontal movement (x-direction)
		self.rect.x += dx
		for tile in tile_rects:
				# Check for collisions in the x-direction
				if tile[1].colliderect(self.rect):
						if dx > 0:  # Moving right
								self.rect.right = tile[1].left
						if dx < 0:  # Moving left
								self.rect.left = tile[1].right

		# Vertical movement (y-direction)
		self.rect.y += dy
		for tile in tile_rects:
				# Check for collisions in the y-direction
				if tile[1].colliderect(self.rect):
						if dy > 0:  # Falling
								self.rect.bottom = tile[1].top
								self.vel_y = 0  # Stop falling
								self.on_ground = True  # Player is now on the ground
						elif dy < 0:  # Jumping
								self.rect.top = tile[1].bottom
								self.vel_y = 0  # Stop upward movement



		# **Item Collection and Exit Collision Logic**
		for item in items[:]:  # Iterate over a copy of the list
				item_type, item_img, item_rect = item
				if self.rect.colliderect(item_rect):  # Check collision with each item
						if item_type == 'health':
								self.health = min(self.health + 50, self.max_health)
								items.remove(item)  # Remove health box after collection
						elif item_type == 'ammo':
								self.ammo += 10
								items.remove(item)  # Remove ammo box after collection
						elif item_type == 'grenade':
								self.grenades += 1
								items.remove(item)  # Remove grenade box after collection
						elif item_type == 'exit':  # Exit tile collision
								self.health = 0  # Set health to zero to kill the player
								self.alive = False  # Set alive status to False
								# Do not remove the exit tile
      
		# Animation logic
		if self.alive:
			if not self.on_ground:
					self.update_action('jump')  # Stay in jump animation while in the air
			elif self.action == 'shoot':
				if self.frame_index == len(self.animation_list['shoot']) - 1:
					self.update_action('idle')  # Return to idle after shooting
			elif self.action == 'hurt':
				if self.frame_index == len(self.animation_list['hurt']) - 1:
					self.update_action('idle')  # Return to idle after shooting
				self.is_reloading = False
			elif self.action == 'throw':
				if self.frame_index == len(self.animation_list['throw']) - 1:
					self.update_action('idle')  # Return to idle after shooting
			elif self.action == 'reload':
				if self.frame_index == len(self.animation_list['reload']) - 1:
					self.finish_reload()
					self.update_action('idle')  # Return to idle after shooting
			elif keys[pygame.K_d] or keys[pygame.K_a]:
					self.update_action('walk')  # Switch to walk only if on the ground
			else:
					self.update_action('idle')  # Switch to idle if on ground and not moving

  		# Update scroll based on the player's position relative to screen edges
		#update scroll based on player position
		scroll = 0
		if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESHOLD or (self.rect.left < SCROLL_THRESHOLD)):
			self.rect.x -= dx
			scroll = -dx

		return scroll
	def shoot(self, bullet_group):
  
		cur_time = pygame.time.get_ticks()
		if cur_time - self.last_shot > self.shoot_cooldown and self.magazine > 0:
			self.last_shot = cur_time
			# Create a new bullet at the player's current position and direction
			self.magazine -= 1
			dir = 1 if self.direction == 0 else -1
			bullet = None
			if self.is_npc:
				bullet = Bullet(self.rect.centerx + self.rect.width // 2 * dir + 10 * dir, self.rect.centery, self.direction, "bullet3", scale=0.03)
			else:
				bullet = Bullet(self.rect.centerx + self.rect.width // 2 * dir + 10 * dir, self.rect.centery, self.direction, "bullet2")
			bullet_group.add(bullet)
			self.update_action('shoot')  # Switch to shooting animation
			shoot_sound = get_sound("shoot")
			shoot_sound.play()  # Play the shooting sound effect

   
	def throw(self, grenade_group):
		cur_time = pygame.time.get_ticks()
		if cur_time - self.last_throw > self.throw_cooldown and self.grenades > 0:
			self.last_throw = cur_time
			self.grenades -= 1
			dir = 1 if self.direction == 0 else -1
			nade = Grenade(self.rect.centerx + self.rect.size[0] * 0.1 * dir, self.rect.centery, self.direction)
			grenade_group.add(nade)
			self.update_action('throw')  # Switch to shooting animation

	def reload(self):
		if not self.is_reloading:  # Start reload only if not already reloading
			self.is_reloading = True
			self.update_action('reload')  # Switch to the reload animation
			
	def finish_reload(self):
		# Define the maximum magazine capacity
		MAX_MAGAZINE_CAPACITY = 5
		
		# Check how much ammo is available and how much can be reloaded into the magazine
		ammo_needed = MAX_MAGAZINE_CAPACITY - self.magazine  # Calculate how much more ammo can be added to the magazine

		# Update the magazine after the animation has completed
		if self.ammo < ammo_needed:
				self.magazine += self.ammo  # Add all remaining ammo to the magazine
				self.ammo = 0  # Set remaining ammo to zero
		else:
				self.magazine = MAX_MAGAZINE_CAPACITY  # Fill the magazine to capacity
				self.ammo -= ammo_needed  # Reduce the ammo by the amount used to fill the magazine

		self.is_reloading = False  # Reset the reloading state


	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.alive = False
			self.update_action('death')
  
	def check_hurt(self):
		if self.action == 'hurt':
			if self.frame_index >= len(self.animation_list['hurt']) - 1:
				self.update_action('idle')  # Return to idle after hurt
     
     
	def npc_patrol(self, tiles_rect):
			# Move the NPC in the current direction
			if self.action == 'idle':
					# Check if the idle duration has passed
					if pygame.time.get_ticks() - self.idle_start_time >= self.idle_duration:
							self.update_action('walk')  # Resume walking animation
					else:
							return  # Skip movement and stay idle

			self.speed = 2
			dx = self.speed * self.patrol_direction
			self.rect.x += dx

			# Check for collisions with tiles in the x-direction
			for tile in tiles_rect:
					if tile[1].colliderect(self.rect):
							# If a collision is detected, adjust the position to the edge of the tile
							if self.patrol_direction == 1:  # Moving right
									self.rect.right = tile[1].left
							elif self.patrol_direction == -1:  # Moving left
									self.rect.left = tile[1].right

							# Reverse the direction
							self.patrol_direction *= -1
							self.count_move = 0  # Reset the patrol distance counter
							break

			foot_rect = pygame.Rect(
					self.rect.x + (self.rect.width if self.patrol_direction == 1 else 0),  # Add width only when moving right
					self.rect.bottom,  # Position at the bottom of the NPC
					TILE_SIZE // 2,    # Width of the ground-check rectangle
					5                  # Height of the ground-check rectangle
			)

			# If no tile is found below in the patrol direction, reverse direction
			grounded = any(tile[1].colliderect(foot_rect) for tile in tiles_rect)
			if not grounded:
					self.patrol_direction *= -1  # Reverse direction
					self.count_move = 0  # Reset the patrol distance counter
					return  # Exit to avoid further updates this frame
			# Increment the patrol distance counter
			self.count_move += self.speed

			# Check if the NPC has moved beyond the patrol distance (in tiles)
			if self.count_move >= 3 * TILE_SIZE:
					self.patrol_direction *= -1  # Reverse direction
					self.count_move = 0  # Reset the count when the direction changes

					# Randomly decide to make the NPC idle for a random duration
					if random.random() < 0.2:  # 20% chance to idle
							self.idle_start_time = pygame.time.get_ticks()
							self.idle_duration = random.randint(1000, 3000)  # Idle between 1 to 3 seconds
							self.update_action('idle')  # Switch to idle animation
							return  # Exit the function to avoid updating 'walk' again

			# Set direction for the NPC animation (1 = left, 0 = right)
			if self.patrol_direction == 1:
					self.direction = 0  # Move right
			else:
					self.direction = 1  # Move left

			# Set the NPC animation to 'walk' while patrolling
			self.update_action('walk')


	def npc_vision_and_shoot(self, player, bullet_group, tiles_rect):
   
		if self.alive and player.alive:
			if self.action == 'hurt':
				if self.frame_index >= len(self.animation_list['hurt']) - 1:
					self.update_action('walk')  # Return to idle after hurta
				else: return
			# Define vision range in tiles (NPC can detect player up to 5 tiles away)
			VISION_RANGE = 5 * TILE_SIZE  
			VERTICAL_TOLERANCE = TILE_SIZE  # Allow for some vertical difference

			# Calculate the horizontal distance between the NPC and the player
			dx = player.rect.centerx - self.rect.centerx
			dy = player.rect.centery - self.rect.centery

			# Check if the player is within the vision range horizontally and within vertical tolerance
			if abs(dx) <= VISION_RANGE and abs(dy) <= VERTICAL_TOLERANCE:  # Check vertical tolerance
					# Check if the player is in front of the NPC (based on NPC direction)
					if (self.direction == 0 and dx > 0) or (self.direction == 1 and dx < 0):
							# Player is in front of the NPC, stop patrolling and shoot
							self.shoot(bullet_group)  # NPC shoots in a straight line
							
							# Set NPC speed to zero to stop movement
							return  # Exit the function after shooting

			# If the player is not detected, continue patrolling
			self.npc_patrol(tiles_rect)

	def update_animation(self):
		ANIMATION_COOLDOWN = self.animation_cooldown
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
   
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 'death':
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0


		self.image = self.animation_list[self.action][self.frame_index]

	def update_action(self, new_action):
		if new_action != self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def draw(self, screen, scroll):
		if self.is_npc: self.rect.x += scroll
		screen.blit(pygame.transform.flip(self.image, self.direction, False), self.rect)