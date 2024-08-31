from typing import Any
import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Important to convert for performance
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Move right
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # # Normalized, with zero vector check
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        # Multiply by delta time to even out
        self.rect.center += self.player_direction * self.player_speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, all_sprites)

            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)

        self.image = surface
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)

        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.laser_speed = 400

    def update(self, dt) -> None:
        self.rect.centery -= self.laser_speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, *groups) -> None:
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(bottom = (randint(0, WINDOW_WIDTH), 0))
        self.speed = 50

    def update(self, dt):
        self.rect.centery += self.speed
        if self.rect.top > WINDOW_HEIGHT: 
            self.kill()
    

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')

running = True
clock = pygame.time.Clock() 

all_sprites = pygame.sprite.Group()

star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()

for _ in range(50):
    Star(star_surface, all_sprites)
    
player = Player(all_sprites)


# Custom Events
## Meteor Event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

## Laser Event

while running:
    # Divide to get seconds
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, all_sprites)

    all_sprites.update(dt)

    # Draw star bg
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()