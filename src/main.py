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


#classes for our game objects

class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ani_speed = 5
        self.idle = []
        self.idle.append(load_image('ninja/idle/Idle__000.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__001.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__002.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__003.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__004.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__005.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__006.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__007.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__008.png', -1))
        self.idle.append(load_image('ninja/idle/Idle__009.png', -1))

        self.running = []
        self.running.append(load_image('ninja/running/Run__000.png', -1))
        self.running.append(load_image('ninja/running/Run__001.png', -1))
        self.running.append(load_image('ninja/running/Run__002.png', -1))
        self.running.append(load_image('ninja/running/Run__003.png', -1))
        self.running.append(load_image('ninja/running/Run__004.png', -1))
        self.running.append(load_image('ninja/running/Run__005.png', -1))
        self.running.append(load_image('ninja/running/Run__006.png', -1))
        self.running.append(load_image('ninja/running/Run__007.png', -1))
        self.running.append(load_image('ninja/running/Run__008.png', -1))
        self.running.append(load_image('ninja/running/Run__009.png', -1))

        self.dying = []
        self.dying.append(load_image('ninja/dead/Dead__000.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__001.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__002.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__003.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__004.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__005.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__006.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__007.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__008.png', -1))
        self.dying.append(load_image('ninja/dead/Dead__009.png', -1))

        self.index = 0
        self.move = 9
        self.image, self.rect = self.idle[self.index]
        self.rect = self.rect.move((500, 300))
        self.newpos = self.rect
        self.moving = 0
        self.punched = 0
        self.dead = 0
        self.direction = 0

    def update(self):
        if self.dead:
            self.image, self.rect = self.dying[self.index]
            self.rect = self.newpos
            if self.direction:
                self.image = pygame.transform.flip(self.image, 1, 0)
        elif self.punched:
            self._dead()
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

    def _run(self):
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
        #self.images.sort()
        self.index = len(self.images) - 1
        self.move_x = 9
        self.move_y = 5
        self.area = screen.get_rect()
        self.image, self.rect = self.images[self.index]
        self.rect.topleft = 10, 10
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
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Shoot The Asteroid!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp()
    asteroid = Asteroid()
    ninja = Ninja()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((chimp, asteroid, ninja, fist))


#Main Loop
    going = True
    while going:
        clock.tick(60)

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
                ninja.moving = 0

            elif event.type == KEYDOWN and event.key == K_LEFT:
                if not ninja.dead:
                    ninja.moving = 1
                    if ninja.direction == 0:
                        ninja.move = -ninja.move
                    ninja.direction = 1

            elif event.type == KEYUP and event.key == K_LEFT:
                ninja.moving = 0

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
        background.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
