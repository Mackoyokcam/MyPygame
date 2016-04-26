#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

#Import Modules
import numpy
import os, pygame, glob
import random
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):

    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def load_music(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        music = pygame.mixer.music.load(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return music

#classes for our game objects
class Kunai(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Kunai.png')
        self.default = self.rect
        self.rect = self.rect.move((-80, 0))
        self.newpos = 0
        self.direction = 0
        self.speed = 15
        self.initial = 0
        self.active = 0
        self.enemies = Cowboy(0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):
        if self.active:
            self._throw()

    def _throw(self):
        self.image, self.rect = load_image('Kunai.png')
        self.rect = self.newpos
        self.newpos = self.rect.move((self.speed, 0))

        if self._hit():
            self.active = 0
            self.kill()
            self.enemies.hit = 1
            self.enemies.kunai_hit = 1
            if self.direction:
                self.speed = -self.speed
                self.direction = 0

        if self.rect.left < -70 or self.rect.right > self.area.right + 70:
            self.active = 0
            self.kill()
            if self.direction:
                self.speed = -self.speed
                self.direction = 0

        if self.direction:
            self.image = pygame.transform.flip(self.image, 1, 0)
            if self.initial:
                self.newpos = self.rect.move((-80, 0))
                self.initial = 0

        self.rect = self.newpos

    def _hit(self):
        hit = True
        if not self.direction:
            hitpoint = self.rect.midright

        else:
            hitpoint = self.rect.midleft

        hitbox = self.enemies.rect.inflate((-50, 0))
        return hitbox.collidepoint(hitpoint)



class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ani_speed = 5
        self.idle = []
        self.idle.append(load_image('ninja/right/idle/Idle__000.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__001.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__002.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__003.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__004.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__005.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__006.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__007.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__008.png', -1))
        self.idle.append(load_image('ninja/right/idle/Idle__009.png', -1))

        self.running = []
        self.running.append(load_image('ninja/right/running/Run__000.png', -1))
        self.running.append(load_image('ninja/right/running/Run__001.png', -1))
        self.running.append(load_image('ninja/right/running/Run__002.png', -1))
        self.running.append(load_image('ninja/right/running/Run__003.png', -1))
        self.running.append(load_image('ninja/right/running/Run__004.png', -1))
        self.running.append(load_image('ninja/right/running/Run__005.png', -1))
        self.running.append(load_image('ninja/right/running/Run__006.png', -1))
        self.running.append(load_image('ninja/right/running/Run__007.png', -1))
        self.running.append(load_image('ninja/right/running/Run__008.png', -1))
        self.running.append(load_image('ninja/right/running/Run__009.png', -1))

        self.dying = []
        self.dying.append(load_image('ninja/right/dead/Dead__000.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__001.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__002.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__003.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__004.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__005.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__006.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__007.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__008.png', -1))
        self.dying.append(load_image('ninja/right/dead/Dead__009.png', -1))

        self.attacking = []
        self.attacking.append(load_image('ninja/right/attack/Attack__000.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__001.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__002.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__003.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__004.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__005.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__006.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__007.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__008.png', -1))
        self.attacking.append(load_image('ninja/right/attack/Attack__009.png', -1))

        self.l_attacking = []
        self.l_attacking.append(load_image('ninja/left/attack/Attack__000.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__001.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__002.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__003.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__004.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__005.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__006.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__007.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__008.png', -1))
        self.l_attacking.append(load_image('ninja/left/attack/Attack__009.png', -1))

        self.jumping = []
        self.jumping.append(load_image('ninja/right/jumping/Jump__000.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__001.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__002.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__003.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__004.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__005.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__006.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__007.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__008.png', -1))
        self.jumping.append(load_image('ninja/right/jumping/Jump__009.png', -1))

        self.throwing = []
        self.throwing.append(load_image('ninja/right/throwing/Throw__000.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__001.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__002.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__003.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__004.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__005.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__006.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__007.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__008.png', -1))
        self.throwing.append(load_image('ninja/right/throwing/Throw__009.png', -1))

        self.jump_attack = []
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__000.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__001.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__002.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__003.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__004.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__005.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__006.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__007.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__008.png', -1))
        self.jump_attack.append(load_image('ninja/right/jump_attack/Jump_Attack__009.png', -1))

        self.jump_throw = []
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__000.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__001.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__002.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__003.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__004.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__005.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__006.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__007.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__008.png', -1))
        self.jump_throw.append(load_image('ninja/right/jump_throw/Jump_Throw__009.png', -1))


        self.index = 0
        self.move = 5
        self.jump_y = 8
        self.jump_height = 10
        #States
        self.moving = 0
        self.attacked = 0
        self.thrown = 0
        self.punched = 0
        self.dead = 0
        self.jumped = 0
        self.direction = 0
        self.initial = 0
        self.check = 0
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.image, self.rect = self.idle[self.index]
        self.rect = self.rect.move((500, 560))
        self.default = self.rect.bottom
        self.JA_index = 0
        self.JA_speed = 2
        self.JA_counter = 0
        self.newpos = self.rect
        self.up = 0
        self.down = 0
        print self.default
        print self.rect.bottom
        print self.rect.top

    def update(self):
        if self.dead:
            self.image, self.rect = self.dying[self.index]
            self.rect = self.newpos
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)
        elif self.punched:
            self._dead()
        elif self.jumped:
            self.jump()
        elif self.attacked:
            self.attack()
        elif self.thrown:
            self.throw()
        elif self.moving:
            self._run()
        else:
            self._idle()

    def _idle(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 5
            self.index += 1
            if self.index >= len(self.idle):
                self.index = 0
            self.image, self.rect = self.idle[self.index]
            self.rect = self.newpos
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)

    def throw(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 2
            if self.index < len(self.throwing):
                self.image, self.rect = self.throwing[self.index]
                self.rect = self.newpos
                self.index += 1
                if self.direction:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.rect = self.rect.move((-40, 0))
            else:
                self.thrown = 0
                self.JA_counter = 0

    def _run(self):
        if self.rect.left < 0 or self.rect.right > self.area.right:
            self.moving = 0
            if self.rect.left < 0:
                self.rect.left = 10
            else:
                self.rect.right = self.area.right - 10

        else:
            self.ani_speed -= 1
            self.newpos = self.rect.move((self.move, 0))
            if self.ani_speed == 0:
                self.ani_speed = 5
                self.index += 1
                if self.index >= len(self.running):
                    self.index = 0
                self.image, self.rect = self.running[self.index]
                if self.direction:
                    self.image = pygame.transform.flip(self.image, 1, 0)

            self.rect = self.newpos

    def jump(self):
        if not self.attacked and not self.thrown:
            self.ani_speed -= 1
        else:
            self.JA_speed -= 1

        if self.rect.left < 0 or self.rect.right > self.area.right:
            self.moving = 0
            if self.rect.left < 0:
                self.rect.left = 10
            else:
                self.rect.right = self.area.right - 10

        if not self.attacked and not self.thrown:
            self.newpos = self.rect.move((0, -self.jump_y))

            if self.moving:
                self.newpos = self.rect.move((self.move, -self.jump_y))

        if self.ani_speed == 0 or self.JA_speed == 0:
            #not attacking
            if not self.attacked and not self.thrown:
                self.ani_speed = 5
                #falling, start moving down
                if self.index > 3 and self.initial:
                    self.jump_y = -self.jump_y
                    self.initial = 0
                    self.check = 1

                if self.check and self.up:
                    if self.rect.bottom > self.default - 150:
                        self.index = len(self.jumping)
                        self.check = 0
                        self.default -= 150
                        self.newpos = self.rect.move((0, self.default - self.rect.bottom))
                        print self.default
                        print self.rect.bottom
                        print self.rect.top

                if self.check and self.down:
                    if self.rect.bottom > self.default + 150:
                        self.index = len(self.jumping)
                        self.check = 0
                        self.default += 150
                        self.newpos = self.rect.move((0, self.default - self.rect.bottom))
                        print self.default
                        print self.rect.bottom
                        print self.rect.top

                if self.index < len(self.jumping) - 1:
                    if not self.attacked:
                        self.image, self.rect = self.jumping[self.index]
                        self.index += 1
                    if self.direction:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                #done jumping
                else:
                    self.JA_index = 0
                    self.index = 0
                    self.image, self.rect = self.jumping[self.index]
                    if self.direction:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                    self.jump_y = -self.jump_y
                    self.jumped = 0
                    self.JA_counter = 0
                    self.down = 0
                    self.up = 0
                    self.jump_y = abs(self.jump_y)

            #attacking
            elif self.attacked:
                self.JA_speed = 3
                if self.JA_index < len(self.jump_attack):
                    self.image, self.rect = self.jump_attack[self.JA_index]
                    if self.direction:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                    self.JA_index += 1
                else:
                    self.attacked = 0


            #throwing
            else:
                self.JA_speed = 2
                if self.JA_index < len(self.jump_throw):
                    self.image, self.rect = self.jump_throw[self.JA_index]
                    if self.direction:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                    self.JA_index += 1
                else:
                    self.thrown = 0

        self.rect = self.newpos

    def punch(self):
        self.punched = 1
        self.ani_speed = 5
        self.index = 0

    def _dead(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 5
            self.index += 1
            if self.index >= len(self.dying):
                self.dead = 1
                self.index = len(self.dying) - 1
            self.image, self.rect = self.dying[self.index]
            self.rect = self.newpos
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)

    def attack(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 4
            if self.index < len(self.attacking):
                self.image, self.rect = self.attacking[self.index]
                self.rect = self.newpos
                self.index += 1
                if self.direction:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.rect = self.rect.move((-60, 0))
            else:
                self.attacked = 0
                self.JA_counter = 0

    def hit(self, cowboy):
        hit = False
        if not self.direction:
            hitpoint = self.rect.inflate((125, 0)).midright

        else:
            hitpoint = self.rect.inflate((150, 0)).midleft

        hitpoint_c = self.rect.center
        hitbox = cowboy.rect.inflate((20, 0))
        if hitbox.collidepoint(hitpoint) or hitbox.collidepoint(hitpoint_c):
            hit = True

        return hit

    def get_pos(self):
        return self.newpos

    def get_dir(self):
        return self.direction

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('heart.png')
        self.rect = self.rect.move((x, y))
        self.hitpoints = 3

    def update(self):
        if self.hitpoints == 2:
            self.rect = self.rect.move((10, 20))

class Cowboy(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.ani_speed = 10
        self.running = []
        self.running.append(load_image('cowboy/running/Run__000.png', -1))
        self.running.append(load_image('cowboy/running/Run__001.png', -1))
        self.running.append(load_image('cowboy/running/Run__002.png', -1))
        self.running.append(load_image('cowboy/running/Run__003.png', -1))
        self.running.append(load_image('cowboy/running/Run__004.png', -1))
        self.running.append(load_image('cowboy/running/Run__005.png', -1))
        self.running.append(load_image('cowboy/running/Run__006.png', -1))
        self.running.append(load_image('cowboy/running/Run__007.png', -1))
        self.running.append(load_image('cowboy/running/Run__008.png', -1))
        self.running.append(load_image('cowboy/running/Run__009.png', -1))
        self.dying = []
        self.dying.append(load_image('cowboy/dying/Dead__000.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__001.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__002.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__003.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__004.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__005.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__006.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__007.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__008.png', -1))
        self.dying.append(load_image('cowboy/dying/Dead__009.png', -1))
        self.index = 0
        self.move = speed
        # States
        self.x = random.randint(0, 1)
        self.xlist = [-150, self.area.right + 150]
        self.y = random.randint(0, 3)
        self.ylist = [560, 410, 260, 110]
        self.attacked = 0
        self.thrown = 0
        self.hit = 0
        self.dead = 0
        self.reached_end = 0

        if self.xlist[self.x] == -150:
            self.direction = 0
        else:
            self.direction = 1
            self.move = -self.move
        self.image, self.rect = self.running[self.index]
        self.rect = self.rect.move((self.xlist[self.x], self.ylist[self.y]))
        self.default = self.rect.bottom
        self.newpos = self.rect
        self.kunai_hit = 0
        self.timer = 300

    def update(self):
        if not self.timer:
            self.kill()
        elif self.dead:
            self.timer -= 1
        elif not self.hit:
            self._run()
        else:
            self._dead()

    def _dead(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 10
            self.index += 1
            if self.index >= len(self.dying):
                self.dead = 1
                self.index = len(self.dying) - 1
            self.image, self.rect = self.dying[self.index]
            self.rect = self.newpos
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)

    def _run(self):
        self.ani_speed -= 1
        self.newpos = self.rect.move((self.move, 0))
        if not self.direction:
            if self.rect.right >= self.area.right + 150:
                self.reached_end = 1
        if self.direction:
            if self.rect.right <= -150:
                self.reached_end = 1
        if self.ani_speed == 0:
            self.ani_speed = 10
            self.index += 1
            if self.index >= len(self.running):
                self.index = 0
            self.image, self.rect = self.running[self.index]
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)

        self.rect = self.newpos

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.x = 200
        self.y = 300
        self.images = []
        self.ani_speed = 5
        self.images.append(load_image('asteroids/medium/red/a30001.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30002.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30003.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30004.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30005.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30006.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30007.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30008.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30009.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30010.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30011.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30012.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30013.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30014.png', -1))
        self.images.append(load_image('asteroids/medium/red/a30015.png', -1))
        self.index = len(self.images) - 1
        self.move_x = 9
        self.move_y = 5
        self.area = screen.get_rect()
        self.image, self.rect = self.images[self.index]
        self.rect.topleft = 10, 10
        self.rect = self.rect.move((200, 300))
        self.moving = 0

    def _travel(self):
        newpos = self.rect.move((self.move_x, self.move_y))
        if self.rect.left < self.area.left or \
                        self.rect.right > self.area.right:
            self.move_x = -self.move_x
            newpos = self.rect.move((self.move_x, self.move_y))
            self.image = pygame.transform.flip(self.image, 1, 0)

        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 5
            self.index -= 1
            if self.index < 0:
                self.index = len(self.images) - 1
            self.image, self.rect = self.images[self.index]

        self.rect = newpos

class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn act the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < 0 or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption('Ballista Defense')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((200, 200, 200))


#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Cowboy Kills", 1, (0, 0, 255))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Difficulty
    speed = 1

#Prepare Game Objects
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    attack_sound = load_sound('attack.wav')
    throw_sound = load_sound('throw.wav')
    jump_sound = load_sound('jump.wav')
    hit_sound = load_sound('hit.wav')
    music = load_music("ninja.mp3")
    health1 = Heart(10, 10)
    health2 = Heart(70, 10)
    health3 = Heart(130, 10)
    chimp = Chimp()
    asteroid = Asteroid()
    ninja = Ninja()
    fist = Fist()
    kunai = Kunai()
    cowboy = Cowboy(speed)
    allsprites = pygame.sprite.RenderPlain((ninja, fist, health1, health2, health3, cowboy))

    pygame.mixer.music.play(-1)

#Main Loop
    going = True
    while going:
        clock.tick(100)

        if cowboy.kunai_hit:
            punch_sound.play()
            cowboy.kunai_hit = 0

        if cowboy.reached_end:
            cowboy.kill()
            if health3.alive():
                health3.kill()
            elif health2.alive():
                health2.kill()
            elif health1.alive():
                health1.kill()
            else:
                print("Game Over!")
                ninja.dead = 1

        if not cowboy.alive():
            speed += .2
            cowboy = Cowboy(speed)
            cowboy.add(allsprites)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if not ninja.dead:
                    ninja.moving = 1
                    if ninja.direction == 1:
                        ninja.move = -ninja.move
                    ninja.direction = 0
            elif event.type == KEYUP and event.key == K_RIGHT:
                if ninja.moving and ninja.direction == 1:
                    ninja.moving = 1
                else:
                    ninja.moving = 0

            elif event.type == KEYDOWN and event.key == K_LEFT:
                if not ninja.dead:
                    ninja.moving = 1
                    if ninja.direction == 0:
                        ninja.move = -ninja.move
                    ninja.direction = 1

            elif event.type == KEYUP and event.key == K_LEFT:
                if ninja.moving and ninja.direction == 0:
                    ninja.moving = 1
                else:
                    ninja.moving = 0

            elif event.type == KEYDOWN and event.key == K_UP:
                if not ninja.dead and ninja.default > 249:
                    if not ninja.attacked and not ninja.jumped and not ninja.thrown:
                        ninja.ani_speed = 5
                        ninja.up = 1
                        ninja.initial = 1
                        ninja.jumped = 1
                        ninja.jump()
                        ninja.index = 0
                        jump_sound.play()

            elif event.type == KEYDOWN and event.key == K_DOWN:
                if not ninja.dead and ninja.default < 550:
                    if not ninja.attacked and not ninja.jumped and not ninja.thrown:
                        ninja.ani_speed = 5
                        ninja.down = 1
                        ninja.jump_y = -ninja.jump_y
                        ninja.initial = 1
                        ninja.jumped = 1
                        ninja.jump()
                        ninja.index = 0
                        jump_sound.play()

            elif event.type == KEYDOWN and event.key == K_a:
                if not ninja.dead:
                    if not ninja.attacked and not ninja.thrown:
                        ninja.attacked = 1
                        ninja.attack()
                        if ninja.JA_counter == 0:
                            if ninja.hit(cowboy):
                                punch_sound.play()
                                #hit_sound.play()
                                cowboy.hit = 1
                            else:
                                attack_sound.play()
                                ninja.JA_counter = 1

            elif event.type == KEYDOWN and event.key == K_s:
                if not ninja.dead:
                    if not ninja.thrown and not kunai.active and not ninja.attacked:
                        kunai.add(allsprites)
                        kunai.rect = kunai.default
                        ninja.thrown = 1
                        throw_sound.play()
                        kunai.active = 1
                        kunai.newpos = kunai.rect.move(ninja.rect.center)
                        kunai.direction = ninja.get_dir()
                        kunai.enemies = cowboy
                        if kunai.direction:
                            kunai.speed = -kunai.speed
                            kunai.initial = 1

            elif event.type == MOUSEBUTTONDOWN:
                #if fist.punch(chimp):
                #    punch_sound.play() #punch
                 #   chimp.punched()
                if fist.punch(ninja):
                    if not ninja.dead:
                        punch_sound.play()
                        ninja.punch()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        #Draw Everything
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, red, [0, 700, 1500, 100])
        pygame.draw.rect(screen, red, [0, 550, 1500, 10])
        pygame.draw.rect(screen, red, [0, 400, 1500, 10])
        pygame.draw.rect(screen, red, [0, 250, 1500, 10])
        #pygame.draw.rect(screen, green, ninja.rect.inflate(100, 0))
        #pygame.draw.rect(screen, blue, cowboy.rect.inflate(150, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
