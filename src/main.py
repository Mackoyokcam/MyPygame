#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

#Import Modules
import numpy
import os, pygame
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
        self.robot = Robot(0)
        self.jack = Jack(0)
        self.target = None
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
            self.target.hit = 1
            self.target.kunai_hit = 1
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
        if not self.direction:
            hitpoint = self.rect.midright

        else:
            hitpoint = self.rect.midleft

        hitbox = self.enemies.rect.inflate((-50, 0))
        if hitbox.collidepoint(hitpoint) and not self.enemies.hit:
            self.target = self.enemies
            return True

        hitbox = self.robot.rect.inflate(-50, 0)
        if hitbox.collidepoint(hitpoint) and not self.robot.a_hit:
            self.target = self.robot
            return True

        hitbox = self.jack.rect.inflate(-50, 0)
        if hitbox.collidepoint(hitpoint) and not self.jack.hit:
            self.target = self.jack
            return True

        return False


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

                if self.check and self.down:
                    if self.rect.bottom > self.default + 150:
                        self.index = len(self.jumping)
                        self.check = 0
                        self.default += 150
                        self.newpos = self.rect.move((0, self.default - self.rect.bottom))

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
            self.ani_speed = 30
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

    def hit(self, target):
        hit = False
        if not self.direction:
            hitpoint = self.rect.inflate((125, 0)).midright

        else:
            hitpoint = self.rect.inflate((150, 0)).midleft

        hitpoint_c = self.rect.center
        hitbox = target.rect.inflate((20, 0))
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
        self.give_score = 0

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


class Robot(pygame.sprite.Sprite):
    def __init__(self, health):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.ani_speed = 10
        self.running = []
        self.running.append(load_image('robot/running/Run (1).png', -1))
        self.running.append(load_image('robot/running/Run (2).png', -1))
        self.running.append(load_image('robot/running/Run (3).png', -1))
        self.running.append(load_image('robot/running/Run (4).png', -1))
        self.running.append(load_image('robot/running/Run (5).png', -1))
        self.running.append(load_image('robot/running/Run (6).png', -1))
        self.running.append(load_image('robot/running/Run (7).png', -1))
        self.running.append(load_image('robot/running/Run (8).png', -1))
        self.dying = []
        self.dying.append(load_image('robot/dying/Dead (1).png', -1))
        self.dying.append(load_image('robot/dying/Dead (2).png', -1))
        self.dying.append(load_image('robot/dying/Dead (3).png', -1))
        self.dying.append(load_image('robot/dying/Dead (4).png', -1))
        self.dying.append(load_image('robot/dying/Dead (5).png', -1))
        self.dying.append(load_image('robot/dying/Dead (6).png', -1))
        self.dying.append(load_image('robot/dying/Dead (7).png', -1))
        self.dying.append(load_image('robot/dying/Dead (8).png', -1))
        self.dying.append(load_image('robot/dying/Dead (9).png', -1))
        self.dying.append(load_image('robot/dying/Dead (10).png', -1))
        self.index = 0
        self.move = 1
        # States
        self.x = random.randint(0, 1)
        self.xlist = [-150, self.area.right + 150]
        self.y = random.randint(0, 3)
        self.ylist = [560, 410, 260, 110]
        self.attacked = 0
        self.thrown = 0
        self.dead = 0
        self.reached_end = 0
        self.health = health

        if self.xlist[self.x] == -150:
            self.direction = 0
        else:
            self.direction = 1
            self.move = -self.move
        self.image, self.rect = self.running[self.index]
        self.rect = self.rect.move((self.xlist[self.x], self.ylist[self.y]))
        self.default = self.rect.bottom
        self.newpos = self.rect
        self.hit = 0
        self.a_hit = 0
        self.kunai_hit = 0
        self.timer = 300
        self.sound_hit = 0

    def update(self):
        if not self.timer:
            self.kill()
        elif self.dead:
            self.timer -= 1
        elif not self.a_hit:
            self._run()
        else:
            self.health -= 1
            if self.health > 0:
                self.a_hit = 0
            else:
                self._dead()

    def _dead(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = 10
            self.index += 1
            if self.index >= len(self.dying):
                self.dead = 1
                #self.a_hit = 0
                self.sound_hit = 1
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


class Jack(pygame.sprite.Sprite):
    def __init__(self, lives):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.ani_speed = 10
        self.running = []
        self.running.append(load_image('jack/running/Run (1).png', -1))
        self.running.append(load_image('jack/running/Run (2).png', -1))
        self.running.append(load_image('jack/running/Run (3).png', -1))
        self.running.append(load_image('jack/running/Run (4).png', -1))
        self.running.append(load_image('jack/running/Run (5).png', -1))
        self.running.append(load_image('jack/running/Run (6).png', -1))
        self.running.append(load_image('jack/running/Run (7).png', -1))
        self.running.append(load_image('jack/running/Run (8).png', -1))
        self.dying = []
        self.dying.append(load_image('jack/dying/Dead (1).png', -1))
        self.dying.append(load_image('jack/dying/Dead (2).png', -1))
        self.dying.append(load_image('jack/dying/Dead (3).png', -1))
        self.dying.append(load_image('jack/dying/Dead (4).png', -1))
        self.dying.append(load_image('jack/dying/Dead (5).png', -1))
        self.dying.append(load_image('jack/dying/Dead (6).png', -1))
        self.dying.append(load_image('jack/dying/Dead (7).png', -1))
        self.dying.append(load_image('jack/dying/Dead (8).png', -1))
        self.dying.append(load_image('jack/dying/Dead (9).png', -1))
        self.dying.append(load_image('jack/dying/Dead (10).png', -1))
        self.index = 0
        self.move = 1
        # States
        self.x = random.randint(0, 1)
        self.xlist = [-150, self.area.right + 150]
        self.y = random.randint(0, 3)
        self.ylist = [560, 410, 260, 110]
        self.attacked = 0
        self.thrown = 0
        self.dead = 0
        self.reached_end = 0
        self.lives = lives
        self.laugh_sound = load_sound('laugh.ogg')

        if self.xlist[self.x] == -150:
            self.direction = 0
        else:
            self.direction = 1
            self.move = -self.move
        self.image, self.rect = self.running[self.index]
        self.rect = self.rect.move((self.xlist[self.x], self.ylist[self.y]))
        self.default = self.rect.bottom
        self.newpos = self.rect
        self.hit = 0
        self.a_hit = 0
        self.kunai_hit = 0
        self.timer = 300
        self.death_timer = 500


    def update(self):
        if not self.timer:
            self.kill()
        elif self.dead:
            if self.lives > 0:
                self.death_timer -= 1
                if self.death_timer <= 0:
                    self.laugh_sound.play()
                    self.lives -= 1
                    self.dead = 0
                    self.hit = 0
                    self.kunai_hit = 0
                    self.death_timer = 500
            else:
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


class Menu:
    def __init__(self, screen, items, background_color=(0, 0, 0), font_color=(255, 0, 0)):
        self.background_color = background_color
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.items = []
        self.rect1 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 400 - 15, 200, 50])
        self.rect2 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 400 + 100 - 15, 200, 50])
        self.rect3 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 400 + 200 - 15, 200, 50])
        self.rect4 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 400 + 300 - 15, 200, 50])
        self.tutorial = Tutorial(self.screen)
        self.about = About(self.screen)
        for item in items:
            label = self.font.render(item, 1, font_color)
            self.items.append(label)

    def run(self):
        menu_loop = 1
        while menu_loop:
            self.clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == MOUSEBUTTONDOWN and self.rect1.collidepoint(pygame.mouse.get_pos()):
                    menu_loop = 0

                elif event.type == MOUSEBUTTONDOWN and self.rect2.collidepoint(pygame.mouse.get_pos()):
                    self.tutorial.run()
                    self.tutorial = Tutorial(self.screen)

                elif event.type == MOUSEBUTTONDOWN and self.rect3.collidepoint(pygame.mouse.get_pos()):
                    self.about.run()

                elif event.type == MOUSEBUTTONDOWN and self.rect4.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()


            self.screen.fill(self.background_color)
            y = 400
            count = 0
            self.rect1 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y - 15, 200, 50])
            self.rect2 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y + 100 - 15, 200, 50])
            self.rect3 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y + 200 - 15, 200, 50])
            self.rect4 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y + 300 - 15, 200, 50])
            for label in self.items:
                position = label.get_rect()
                position.centerx = self.rect1.centerx
                position.centery = 410 + count
                self.screen.blit(label, position)
                count += 100
            pygame.display.flip()


class Tutorial:
    def __init__(self, screen, background_color=(0, 0, 0)):
        self.background_color = background_color
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.ninja = Ninja()
        self.kunai = Kunai()
        self.step = 0
        self.texts = ['Press the left or right arrow keys to move left or right.',
                      'Press the up or down arrow keys to switch lanes.',
                      'Press A to attack with the katana.',
                      'Press S to throw a kunai',
                      'Hit ESC to return to the main menu.']
        self.allsprites = pygame.sprite.RenderPlain(self.ninja)
        self.text = self.font.render(self.texts[self.step], 1, (0, 250, 0))
        self.textpos = self.text.get_rect(centerx=screen.get_width() / 2)
        self.attack_sound = load_sound('attack.wav')
        self.throw_sound = load_sound('throw.wav')
        self.jump_sound = load_sound('jump.wav')

    def run(self):
        tutorial_loop = 1
        while tutorial_loop:
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    tutorial_loop = 0

                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    if self.step == 0:
                        self.step = 1
                    if not self.ninja.dead:
                        self.ninja.moving = 1
                        if self.ninja.direction == 1:
                            self.ninja.move = -self.ninja.move
                        self.ninja.direction = 0
                elif event.type == KEYUP and event.key == K_RIGHT:
                    if self.step == 0:
                        self.step = 1
                    if self.ninja.moving and self.ninja.direction == 1:
                        self.ninja.moving = 1
                    else:
                        self.ninja.moving = 0

                elif event.type == KEYDOWN and event.key == K_LEFT:
                    if self.step == 0:
                        self.step = 1
                    if not self.ninja.dead:
                        self.ninja.moving = 1
                        if self.ninja.direction == 0:
                            self.ninja.move = -self.ninja.move
                        self.ninja.direction = 1

                elif event.type == KEYUP and event.key == K_LEFT:
                    if self.step == 0:
                        self.step = 1
                    if self.ninja.moving and self.ninja.direction == 0:
                        self.ninja.moving = 1
                    else:
                        self.ninja.moving = 0

                elif event.type == KEYDOWN and event.key == K_UP:
                    if self.step == 1:
                        self.step = 2
                    if not self.ninja.dead and self.ninja.default > 249:
                        if not self.ninja.attacked and not self.ninja.jumped and not self.ninja.thrown:
                            self.ninja.ani_speed = 5
                            self.ninja.up = 1
                            self.ninja.initial = 1
                            self.ninja.jumped = 1
                            self.ninja.jump()
                            self.ninja.index = 0
                            self.jump_sound.play()

                elif event.type == KEYDOWN and event.key == K_DOWN:
                    if self.step == 1:
                        self.step = 2
                    if not self.ninja.dead and self.ninja.default < 550:
                        if not self.ninja.attacked and not self.ninja.jumped and not self.ninja.thrown:
                            self.ninja.ani_speed = 5
                            self.ninja.down = 1
                            self.ninja.jump_y = -self.ninja.jump_y
                            self.ninja.initial = 1
                            self.ninja.jumped = 1
                            self.ninja.jump()
                            self.ninja.index = 0
                            self.jump_sound.play()

                elif event.type == KEYDOWN and event.key == K_a:
                    if self.step == 2:
                        self.step = 3
                    if not self.ninja.dead:
                        if not self.ninja.attacked and not self.ninja.thrown:
                            self.ninja.attacked = 1
                            self.ninja.attack()
                            self.attack_sound.play()

                elif event.type == KEYDOWN and event.key == K_s:
                    if self.step == 3:
                        self.step = 4
                    if not self.ninja.dead:
                        if not self.ninja.thrown and not self.kunai.active and not self.ninja.attacked:
                            self.kunai.add(self.allsprites)
                            self.kunai.rect = self.kunai.default
                            self.ninja.thrown = 1
                            self.kunai.active = 1
                            self.kunai.newpos = self.kunai.rect.move(self.ninja.rect.center)
                            self.kunai.direction = self.ninja.get_dir()
                            self.throw_sound.play()
                            if self.kunai.direction:
                                self.kunai.speed = -self.kunai.speed
                                self.kunai.initial = 1

            self.text = self.font.render(self.texts[self.step], 1, (0, 250, 0))
            self.screen.fill(self.background_color)
            self.screen.blit(self.text, (400, 100))
            self.allsprites.update()
            self.allsprites.draw(self.screen)

            pygame.display.flip()


class About:
    def __init__(self, screen, background_color=(0, 0, 0), font_color=(255, 0, 0)):
        self.screen = screen
        self.background_color = background_color
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.items = []

    def run(self):
        about_loop = 1
        while about_loop:
            self.clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    about_loop = 0

            self.screen.fill(self.background_color)
            y = 400
            count = 0
            pygame.display.flip()


class GameOver:
    def __init__(self, screen, background_color=(0, 0, 0), font_color=(255, 0, 0)):
        self.background_color = background_color
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.font_color = font_color
        self.clock = pygame.time.Clock()
        self.options = []
        self.items = []
        self.rect1 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 300 - 15, 200, 50])
        self.rect2 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 300 + 100 - 15, 200, 50])
        self.rect3 = pygame.draw.rect(self.screen, (0, 200, 0), [680, 300 + 200 - 15, 200, 50])

    def run(self, score, prev_score, options):
        self.items = []
        self.options = options
        for item in self.options:
            label = self.font.render(item, 1, self.font_color)
            self.items.append(label)
        menu_loop = 1
        new_score = self.font.render("Your score: %d" % score, 1, (0, 0, 255))
        old_score = self.font.render("Your previous score: %d" % prev_score, 1, (0, 0, 255))
        while menu_loop:
            self.clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == MOUSEBUTTONDOWN and self.rect1.collidepoint(pygame.mouse.get_pos()):
                    return 1

                elif event.type == MOUSEBUTTONDOWN and self.rect2.collidepoint(pygame.mouse.get_pos()):
                    return 2

                elif event.type == MOUSEBUTTONDOWN and self.rect3.collidepoint(pygame.mouse.get_pos()):
                    return 3

            self.screen.fill(self.background_color)
            y = 400
            count = 0
            self.rect1 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y - 15, 200, 50])
            self.rect2 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y + 100 - 15, 200, 50])
            self.rect3 = pygame.draw.rect(self.screen, (0, 200, 0), [680, y + 200 - 15, 200, 50])
            for label in self.items:
                position = label.get_rect()
                position.centerx = self.rect1.centerx
                position.centery = 410 + count
                self.screen.blit(label, position)
                count += 100
            if score != -1:
                position = new_score.get_rect()
                position.centerx = self.rect1.centerx
                position.centery = 200
                self.screen.blit(new_score, position)
            if prev_score != 0:
                position = old_score.get_rect()
                position.centerx = self.rect1.centerx
                position.centery = 300
                self.screen.blit(old_score, position)
            pygame.display.flip()

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption('Game Menu')
    menu_items = ('Start', 'Tutorial', 'About', 'Quit')
    gm = Menu(screen, menu_items)
    gm.run()
    pygame.display.set_caption('Ninja vs Cowboy, Robot and Jack-O-Lantern')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((200, 200, 200))


#Put Text On The Background, Centered
    score = 0
    prev_score = 0
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Score: %d" % (score), 1, (0, 0, 255))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Difficulty
    speed = 1
    health = 1
    lives = 0

#Prepare Game Objects
    timer = 0
    game_over = False
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    attack_sound = load_sound('attack.wav')
    throw_sound = load_sound('throw.wav')
    jump_sound = load_sound('jump.wav')
    music = load_music("ninja.mp3")
    dink_sound = load_sound('dink.wav')
    robot_sound = load_sound('robot_dead.wav')
    grunt_sound = load_sound('grunt.wav')
    gameover_sound = load_sound('game_over.wav')
    ugh_sound = load_sound('ugh.wav')
    health1 = Heart(10, 10)
    health2 = Heart(70, 10)
    health3 = Heart(130, 10)
    ninja = Ninja()
    kunai = Kunai()
    robot = Robot(1)
    jack = Jack(0)
    cowboy = Cowboy(1)
    go = GameOver(screen, (0, 0, 0))
    allsprites = pygame.sprite.RenderPlain((ninja, health1, health2, health3, cowboy, robot, jack))

    pygame.mixer.music.play(-1)

#Main Loop
    going = True
    while going:
        if game_over:
            if timer > 0:
                timer -= 1
            else:
                options = ['Retry', 'Main Menu', 'Quit']
                result = go.run(score, prev_score, options)
                if result == 1 or result == 2:
                    if result == 2:
                        gm.run()

                    speed = 1
                    health = 1
                    lives = 0
                    health1 = Heart(10, 10)
                    health2 = Heart(70, 10)
                    health3 = Heart(130, 10)
                    ninja = Ninja()
                    kunai = Kunai()
                    robot = Robot(1)
                    jack = Jack(0)
                    cowboy = Cowboy(1)
                    allsprites = pygame.sprite.RenderPlain((ninja, health1, health2, health3, cowboy, robot, jack))
                    prev_score = score
                    score = 0
                    game_over = False
                    pygame.mouse.set_visible(0)
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play(-1)

                else:
                    going = False

        clock.tick(100)
        if timer > 0:
            timer -= 1

        if cowboy.kunai_hit:
            punch_sound.play()
            grunt_sound.play()
            cowboy.kunai_hit = 0

        if robot.kunai_hit:
            dink_sound.play()
            robot.kunai_hit = 0

        if robot.sound_hit:
            robot_sound.play()
            robot.sound_hit = 0

        if jack.kunai_hit:
            punch_sound.play()
            jack.kunai_hit = 0

        if cowboy.reached_end or jack.reached_end or robot.reached_end:
            if not game_over:
                cowboy.kill()
                robot.kill()
                jack.kill()
                if lives > 2:
                    lives /= 2
                if health > 2:
                    health /= 2
                if speed > 2:
                    speed /= 2

                cowboy = Cowboy(speed)
                robot = Robot(health)
                jack = Jack(lives)
                cowboy.add(allsprites)
                robot.add(allsprites)
                jack.add(allsprites)

                if health3.alive():
                    health3.kill()
                    ugh_sound.play()
                elif health2.alive():
                    health2.kill()
                    ugh_sound.play()
                elif health1.alive():
                    health1.kill()
                    ugh_sound.play()
                else:
                    cowboy.move = 0
                    robot.move = 0
                    jack.move = 0
                    gameover_sound.play()
                    pygame.mixer.music.stop()
                    game_over = True
                    timer = 500
                    ninja.dead = 1
                    pygame.mouse.set_visible(1)

        if not cowboy.alive() and not game_over and timer <= 0:
            score += 50
            if speed < 10.1:
                speed += 0.2
            cowboy = Cowboy(speed)
            cowboy.add(allsprites)
        if not robot.alive() and not game_over and timer <= 0:
            score += 50
            if health < 10.1:
                health += 0.2
            robot = Robot(health)
            robot.add(allsprites)
        if not jack.alive() and not game_over and timer <= 0:
            score += 50
            if lives < 10:
                lives += 0.2
            jack = Jack(lives)
            jack.add(allsprites)

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
                            if ninja.hit(cowboy) and not cowboy.hit:
                                punch_sound.play()
                                grunt_sound.play()
                                cowboy.hit = 1
                            elif ninja.hit(robot) and not robot.a_hit:
                                punch_sound.play()
                                robot.a_hit = 1
                            elif ninja.hit(jack) and not jack.hit:
                                punch_sound.play()
                                jack.hit = 1
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
                        kunai.robot = robot
                        kunai.jack = jack
                        if kunai.direction:
                            kunai.speed = -kunai.speed
                            kunai.initial = 1
            elif event.type == KEYDOWN and event.key == K_F1:
                options = ['Continue', 'Main Menu', 'Quit']
                pygame.mouse.set_visible(1)
                pygame.mixer.music.pause()
                result = go.run(-1, 0, options)
                if result == 2:
                    gm.run()
                    speed = 1
                    health = 1
                    lives = 0
                    health1 = Heart(10, 10)
                    health2 = Heart(70, 10)
                    health3 = Heart(130, 10)
                    ninja = Ninja()
                    kunai = Kunai()
                    robot = Robot(1)
                    jack = Jack(0)
                    cowboy = Cowboy(1)
                    allsprites = pygame.sprite.RenderPlain((ninja, health1, health2, health3, cowboy, robot, jack))
                    prev_score = score
                    score = 0
                    game_over = False
                    pygame.mouse.set_visible(0)
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play(-1)
                elif result == 3:
                    going = False

                pygame.mixer.music.play(-1)

            #if game_over and timer < 0:


        allsprites.update()

        text = font.render("Score: %d" % (score), 1, (0, 0, 255))
        menu = font.render("F1: Pause/Menu", 1, (0, 0, 255))

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
        screen.blit(text, textpos)
        screen.blit(menu, (textpos.centerx + 400, textpos.top))
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
