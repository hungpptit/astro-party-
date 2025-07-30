import math
from config import *

sword_music = pygame.mixer.Sound(join('..', 'AstroParty','lesson1','sound', 'sword.mp3'))
sword_music.set_volume(1)
sword_channel = pygame.mixer.Channel(4) 

class Sword(pygame.sprite.Sprite):
    def __init__(self, player, offset_angle):
        super().__init__()
        self.image = pygame.image.load('./image/skill_sword/ball_green.png').convert_alpha()
        self.rect = self.image.get_rect(center=(player.x, player.y))
        self.angle = offset_angle
        self.rotation_speed = 0.4
        self.player = player
        self.radius = 50
        

    def rotate_image(self, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image, new_rect

    def update(self, dt, players_group, rocks_group, dragonflies_group, explosions_group):
        if self.angle % 360 < self.rotation_speed * dt:
            sword_channel.play(sword_music, loops=-1)
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
        # Rotate the sword image and get the new rect
        rotated_image, new_rect = self.rotate_image(self.angle)
        if not self.player.groups():
            self.kill()
            sword_channel.stop()
        self.check_collision_with_player(players_group, explosions_group)
        self.check_collision_with_dragonfly(dragonflies_group, explosions_group)
        self.check_collision_with_rock(rocks_group, explosions_group)

    def check_collision_with_player(self, players_group, explosions_group):
        collided_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collided_player:
            player = collided_player[0]
            player.can_sword = False
            player.kill_player(explosions_group)
            self.kill()
            if self in self.player.swords:
                self.player.swords.remove(self)
            sword_channel.stop()
    
    def check_collision_with_dragonfly(self, dragonflies_group, explorsions_group):
        collided_dragonfly = pygame.sprite.spritecollide(self, dragonflies_group, False, pygame.sprite.collide_mask)
        if collided_dragonfly:
            dragonfly = collided_dragonfly[0]
            dragonfly.kill_dragonfly(explorsions_group)
            self.kill()
            if self in self.player.swords:
                self.player.swords.remove(self)
            sword_channel.stop()

    def check_collision_with_rock(self, rocks_group, explorsions_group):
        collided_rock = pygame.sprite.spritecollide(self, rocks_group, False, pygame.sprite.collide_mask)
        if collided_rock:
            rock = collided_rock[0]
            rock.kill_rock(explorsions_group)
            self.kill()
            if self in self.player.swords:
                self.player.swords.remove(self)
            sword_channel.stop()
