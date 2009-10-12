import pygame
import math
import effects
import util


class Player(effects.SpriteSheet):
    
    def __init__(self, location, constraint, flyers, bombs, boomboxes, turkeyshakes, *groups):
        effects.SpriteSheet.__init__(self, util.load_image( "playerMove_sheet.png" ), (30,45) )
        self.constraint = constraint
        self.movement = { 'up':0, 'down':0, 'left':0, 'right':0 }
        self.facing = 'right'
        self.speed = 5
        self.flyers = flyers
        self.bombs = bombs
        self.boomboxes = boomboxes
        self.turkeyshakes = turkeyshakes
        self.contacting = ''
        self.time = 0
        self.anim_frame = 0
        self.state = 0
        self.flipped = False
        self.booltop = False
        
        self.rect.center = location
        print(self.rect.top)
        self.rect.inflate_ip( 0,-22.5 )
        self.rect.top = location[1]
        print(self.rect.top)
        
    @property
    def booltop(self):
        return self._booltop
        
    @booltop.setter
    def booltop(self, val):
        self._booltop = val
        if val == True:
            self.rect.bottom = self.rect.top
        else:
            self.rect.top = self.rect.bottom
        
    def update(self):
        lr = False
        if self.movement['left'] == 1 and self.movement['right'] == 0:
            self.facing = 'left'
            lr = True
            if self.flipped == False:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = True
        elif self.movement['right'] == 1 and self.movement['left'] == 0:
            self.facing = 'right'
            lr = True
            if self.flipped == True:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = False
        if lr:
            self.state = 2
        if self.movement['up'] == 1 and self.movement['down'] == 0:
            if lr:
                self.facing += 'up'
                self.state = 1
            else:
                self.facing = 'up'
                self.state = 0
        if self.movement['down'] == 1 and self.movement['up'] == 0:
            if lr:
                self.facing += 'down'
                self.state = 3
            else:
                self.facing = 'down'
                self.state = 4
        if self.movement['up']==1 or self.movement['down']==1 or self.movement['left']==1 or self.movement['right']==1:
            if self.flipped == True:
                self.time -= 1
            else:
                self.time += 1
            self.anim_frame = self.time / 2
            if self.anim_frame > 11:
                self.time = 0
                self.anim_frame = 0
            elif self.anim_frame < 0:
                self.time = 2 * 11
                self.anim_frame = 11
                
        self.speed = 5
        if self.movement['up'] ^ self.movement['down'] == 1 and self.movement['left'] ^ self.movement['right'] == 1:
            self.speed = math.sqrt( 12.5 )
        
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        
    
    def draw(self, screen):
        screen.blit( pygame.surface((800,600)), self.rect, self.rect )
        
