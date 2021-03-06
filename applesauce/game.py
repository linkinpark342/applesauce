# This file is part of applesauce.
#
# applesauce is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# applesauce is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with applesace.  If not, see <http://www.gnu.org/licenses/>.
import logging
import pkg_resources

import pygame

from applesauce import settings
from applesauce import level
from applesauce import level_config
from applesauce.sprite import util


LOG = logging.getLogger(__name__)


class InvalidStateException(Exception):
    
    def __init__(self, state):
        self.state = state

    def __unicode__(self):
        return unicode(self.state)

    def __str__(self):
        return str(unicode(self))


class Game( object ):

    def __init__( self ):
        self.caption = settings.CAPTION
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        self.level = None
        self.state = 'splash'
        if pygame.mixer.get_init():
            self.music = pygame.mixer.Sound(
                    pkg_resources.resource_stream(
                        "applesauce",
                        "sounds/BackgroundMusic.ogg"))
            self.music.set_volume(1)
            self.music.play(-1)
        else:
            self.music = None
        
        #self.splash = util.load_image( self.splash_image )
        #self.win = util.load_image( self.win_image )
        #self.lose = util.load_image( self.lose_image )
        #self.read_level( self.level_data )

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, val):
        self.__state = val
        if val == "act1":
            self.level_config = "level_data/level0.ini"
        elif val == "act2":
            self.level_config = "level_data/level1.ini"
        elif val == "splash":
            self.level_config = "level_data/splash.ini"
        elif val == "info1":
            self.level_config = "level_data/info1.ini"
        elif val == "info2":
            self.level_config = "level_data/info2.ini"
        elif val == "info3":
            self.level_config = "level_data/info3.ini"
        elif val == "lose":
            self.level_config = "level_data/gameover.ini"
            if self.music is not None:
                self.music.stop()
        elif val == "win":
            self.level_config = "level_data/victory.ini"
            if self.music is not None:
                self.music.stop()
        elif val == "over":
            pass
        else:
            raise InvalidStateException(val)

    @property
    def level_config(self):
        return self.__level_config

    @level_config.setter
    def level_config(self, val):
        self.__level_config = level_config.LevelConfig(val)
        self.level = level.Level(self.level_config.image(), self.level_config.big(), self.level_config.start())
        self.populate_level()

    def populate_level(self):
        for location in self.level_config.player():
            self.level.add_player(
                    location[0],
                    location[1],
                    location[2],
                    location[3],
                    location[4])
        for location in self.level_config.basic_enemies():
            self.level.add_enemy(0, location)
        for location in self.level_config.officers():
            self.level.add_enemy(1, location)
        for location in self.level_config.walls():
            self.level.add_wall(location)
        for location in self.level_config.bombsites():
            self.level.add_bombsite(location)
        for location in self.level_config.doors():
            self.level.add_door(location[0], location[1])
        for location in self.level_config.end():
            self.level.add_end(location)
        if self.level_config.hud_level() is not None:
            self.level.add_hud(self.level_config.hud_level())
     
    @property
    def caption(self):
        return pygame.display.get_caption()
        
    @caption.setter
    def caption(self, val):
        pygame.display.set_caption(val)
        
    def update( self ):
        self.clock.tick( 50 )
        if self.level.lives <= 0:
            self.state = 'lose'
        elif self.state == 'act1' and self.level.player.sprite.flyers == 0:
            self.state = 'act2'
        elif self.state == 'act2' and self.level.player.sprite.bombs == 0 and self.level.player.sprite.end == True:
            self.state = 'win'
        for event in pygame.event.get():
            self.handle_event( event )
        if self.state == 'act1' or self.state == 'act2':
            self.level.update()

    def handle_event( self, event ):
        if event.type == pygame.QUIT:
            self.state = 'over'
        player = self.level.player.sprite
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, pygame.FULLSCREEN )
            elif event.key == pygame.K_ESCAPE and self.state != 'lose':
                self.state = 'lose'
            elif self.state == 'splash':
                self.state = 'info1'
            elif self.state == 'info1':
                self.state = 'info2'
            elif self.state == 'info2':
                self.state = 'info3'
            elif self.state == 'info3':
                self.state = 'act1'
            elif self.state == 'lose':
                self.state = 'over'
            elif self.state == 'win':
                self.state = 'over'
            elif event.key == pygame.K_LEFT:
                self.level.add_boombox()
            elif event.key == pygame.K_UP:
                if self.state == 'act1':
                    self.level.add_flyer()
                elif self.state == 'act2':
                    self.level.add_bomb(True)
            elif event.key == pygame.K_RIGHT:
                self.level.add_turkeyshake()
            elif event.key == pygame.K_DOWN:
                self.level.touch_door()
            elif event.key == pygame.K_o:
                if self.level.draw_walls:
                    self.level.draw_walls = False
                else:
                    self.level.draw_walls = True
            elif event.key == pygame.K_w:
                player.movement['up'] = 1
            elif event.key == pygame.K_s:
                player.movement['down'] = 1
            elif event.key == pygame.K_a:
                player.movement['left'] = 1
            elif event.key == pygame.K_d:
                player.movement['right'] = 1
        elif event.type == pygame.KEYUP and (self.state == 'act1' or self.state == 'act2'):
            if event.key == pygame.K_w:
                player.movement['up'] = 0
            elif event.key == pygame.K_s:
                player.movement['down'] = 0
            elif event.key == pygame.K_a:
                player.movement['left'] = 0
            elif event.key == pygame.K_d:
                player.movement['right'] = 0
            elif event.key == pygame.K_UP:
                self.level.add_bomb(False)

    def draw(self):
        self.screen.fill( (50, 50, 50) )
        if self.level_config.magic_scroll():
            self.level.draw(self.screen)
        else:
            self.screen.blit(self.level.image, (0, 0))
        
        
def main():
    pygame.init()
    g = Game()
    while g.state != 'over':
        g.update()
        g.draw()
        pygame.display.flip()
#pygame.mixer.music.stop()
