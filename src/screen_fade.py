import pygame.draw


class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen, SCREEN_WIDTH):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(
                screen,
                self.color,
                (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_WIDTH * 0.8),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (
                    SCREEN_WIDTH // 2 + self.fade_counter,
                    0,
                    SCREEN_WIDTH // 2,
                    SCREEN_WIDTH * 0.8,
                ),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_WIDTH * 0.8 // 2),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (
                    0,
                    SCREEN_WIDTH * 0.8 // 2 + self.fade_counter,
                    SCREEN_WIDTH,
                    SCREEN_WIDTH * 0.8,
                ),
            )
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(
                screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter)
            )
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete
