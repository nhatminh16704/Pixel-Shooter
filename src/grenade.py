import math
import pygame
from const import SCREEN_WIDTH, TILE_SIZE
from utils import scale_img, get_sound
from explosion import Explosion


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale=1):
        super().__init__()
        # Load the grenade image
        grenade_image = pygame.image.load("assets/Icons/grenade.png").convert_alpha()
        self.image = scale_img(grenade_image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = 50

        # Initial speed and physics settings
        self.speed_x = 5 * (
            1 if direction == 0 else -1
        )  # Horizontal speed based on direction
        self.speed_y = -12  # Initial upward speed for a parabolic arc
        self.gravity = 1  # Gravity affecting the grenade
        self.friction = (
            0.8  # Friction applied to slow down horizontal movement on ground
        )
        self.bounce = 0.6  # How much the grenade should bounce
        self.timer = (
            3000  # Time in milliseconds before the grenade explodes (e.g., 3 seconds)
        )
        self.creation_time = (
            pygame.time.get_ticks()
        )  # Save the time when the grenade is created

    def update(self, explosion_group, enemy_group, player, tiles_rect):
        # Apply gravity to the grenade's Y movement
        self.speed_y += self.gravity

        # Store the potential changes in position
        dx = self.speed_x
        dy = self.speed_y

        # Move the grenade horizontally and check for collisions
        self.rect.x += dx
        for tile in tiles_rect:
            if tile[1].colliderect(self.rect):
                # Reverse horizontal direction when hitting a wall
                self.speed_x *= -self.bounce
                # Adjust the position to prevent getting stuck in the wall
                if dx > 0:  # Moving right
                    self.rect.right = tile[1].left
                elif dx < 0:  # Moving left
                    self.rect.left = tile[1].right

        # Move the grenade vertically and check for collisions
        self.rect.y += dy
        for tile in tiles_rect:
            if tile[1].colliderect(self.rect):
                # Simulate bouncing when the grenade hits the ground or a ceiling
                if dy > 0:  # Falling down, so adjust to the top of the tile
                    self.rect.bottom = tile[1].top
                    self.speed_y *= (
                        -self.bounce
                    )  # Reverse Y direction for a bounce and reduce speed
                    self.speed_x *= (
                        self.friction
                    )  # Apply friction to slow down horizontal movement
                elif dy < 0:  # Moving up, so adjust to the bottom of the tile
                    self.rect.top = tile[1].bottom
                    self.speed_y *= -self.bounce  # Reverse Y direction

        # Stop the bounce if the speed is too low to avoid endless bouncing
        if abs(self.speed_y) < 1:
            self.speed_y = 0

        # Trigger explosion when the timer ends
        if pygame.time.get_ticks() - self.creation_time >= self.timer:
            self.explode(explosion_group, enemy_group, player)

        # Check for grenade out of bounds and remove it if necessary
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

    def draw(self, screen, screen_scroll):
        # Adjust the grenade's position based on screen scroll for drawing
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

    def explode(self, explosion_group, enemy_group, player):
        # Explosion logic (you can add explosion animation, sound, etc.)
        explosion = Explosion(
            self.rect.centerx, self.rect.centery, scale=1
        )  # Adjust the scale as needed
        explosion_group.add(explosion)  # Add the explosion to the group
        explode_sound = get_sound("explode")
        explode_sound.play()

        self.kill()  # Remove the grenade after it explodes

        # Check for collision with enemies
        for enemy in enemy_group:  # Assuming you have an enemy_group sprite group
            # Calculate distance from grenade to enemy
            distance = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery,
            )
            if distance <= 2 * TILE_SIZE:  # Check if within explosion radius
                enemy.health -= self.damage  # Deal damage
                enemy.update_action("hurt")  # Update enemy action

        # Check collision with player
        distance_to_player = math.hypot(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery,
        )
        if (
            distance_to_player <= 2 * TILE_SIZE
        ):  # Check if player is within explosion radius
            player.health -= self.damage  # Deal damage to the player
            player.update_action("hurt")  # Update player action
