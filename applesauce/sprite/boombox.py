import weakref

import pygame

from applesauce import settings
from applesauce.sprite import util


class Boombox(pygame.sprite.Sprite):
    
    def __init__(self, big, center, enemies, *groups):
        self.type = 'boombox'
        pygame.sprite.Sprite.__init__( self, *groups )
        if big == True:
            self.boombox = util.load_image( "boomboxBig.png" )
            self.rect = pygame.Rect( 0, 0, 75, 56 )
        else:
            self.boombox = util.load_image( "boombox.png" )
            self.rect = pygame.Rect( 0, 0, 38, 28 )
        self.bar = pygame.Surface( ( self.rect.width, 2 ) )
        self.bar.fill( ( 255, 0, 0 ) )
        self.bar_rect = self.bar.get_rect()
        self.time = 300
        self.sound = None
        self.enemies = enemies
        
        self.rect.centerx = center[0]
        self.rect.centery = center[1] - 2
        
    @property
    def image(self):
        image = pygame.Surface( ( self.rect.width, self.rect.height ), pygame.SRCALPHA, 32 ).convert_alpha()
        image.blit( self.boombox, self.boombox.get_rect() )
        image.blit( self.bar, self.bar.get_rect(), pygame.Rect( 0, 0, self.rect.width*(self.time/300.0), 2 ) )
        return image

    def _attract_nearby_enemies(self):
        print self.enemies
        if self.enemies is None:
            return
        bounding_rect = pygame.Rect((0, 0),
                [settings.BOOMBOX_RADIUS * 2] * 2)
        bounding_rect.center = self.rect.center
        class BoundingRectSprite:
            rect = bounding_rect
            radius = settings.BOOMBOX_RADIUS
        x = BoundingRectSprite
        sprites = pygame.sprite.spritecollide(
                x,
                self.enemies,
                False,
                pygame.sprite.collide_circle
                )
        for sprite in sprites:
            if hasattr(sprite, 'attractor_weakref'):
                sprite.attractor_weakref = weakref.ref(self)
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        self._attract_nearby_enemies()
