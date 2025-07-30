import math

from config import *

class Sword(pygame.sprite.Sprite):
    def __init__(self, player, offset_angle, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./image/skill_sword/ball_green.png').convert_alpha()
        self.rect = self.image.get_rect(center=(player.x, player.y))
        print(self.rect)
        self.angle = offset_angle
        self.rotation_speed = 0.4
        self.player = player
        self.radius = 50

    def rotate_image(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image, new_rect

    def update(self, display_surface, dt):
        # Update the angle of rotation
        self.angle += self.rotation_speed * dt
        self.angle %= 360

        # Calculate the new position based on the player's position and angle
        radian_angle = math.radians(self.angle)
        offset_angle = math.radians(self.player.angle)
        x_distance = math.cos(radian_angle) * self.radius *1.2
        y_distance = math.sin(radian_angle) * self.radius *1.2
        x_offset = math.cos(offset_angle) * -15
        y_offset = math.sin(offset_angle) * -15
        self.rect.center = ((self.player.x + x_offset) + x_distance, (self.player.y + y_offset) + y_distance)
        print(self.rect.center)
        # Rotate the sword image and get the new rect
        rotated_image, new_rect = self.rotate_image(self.angle)

        # Blit the rotated sword to the display surface
        display_surface.blit(rotated_image, new_rect)

        # Check for collision with dragonflies
        # collision_sprites = pygame.sprite.spritecollide(self, dragonflies, True, pygame.sprite.collide_mask)
        # if collision_sprites:
        #     self.kill()
        #     if self in self.player.swords:
        #         self.player.swords.remove(self)