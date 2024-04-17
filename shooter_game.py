from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
font.init()
style = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.h = h
        self.w = w
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def ohMyGyattItAppearsToHaveCollided(self, obj):
        return Rect.colliderect(self.rect, obj.rect)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

x1, y1 = 100, 300
maxy = 500

score = 0
missed = 0

clock = time.Clock()
FPS = 60

class player(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.cooldown = 10
    def fire(self):
        keysPressed = key.get_pressed()
        if keysPressed[K_e] and self.cooldown <= 0:
            Bullet = bullet('rabbid.png', (self.rect.x + self.w / 2) - ((640/25)/2), self.rect.y, 640//25, 1280//25, 5)
            bullets.append(Bullet)
            self.cooldown = 10
    def move(self):
        keysPressed = key.get_pressed()
        if keysPressed[K_RIGHT]:
            self.rect.x += self.speed
        elif keysPressed[K_LEFT]:
            self.rect.x -= self.speed

class enemy(GameSprite):
    def __init__(self, sprite, x, y, w, h, speed):
        super().__init__(sprite, x, y, w, h, speed)
    def down(self):
        self.rect.y += self.speed
        if self.rect.y > maxy + 100:
            self.rect.y = -50
            self.speed = randint(1, 4)
            self.rect.x = randint(10, 690)
            global missed
            missed += 1
    def pluh(self):
        for i in bullets:
            if self.ohMyGyattItAppearsToHaveCollided(i):
                self.speed = randint(1, 4)
                self.rect.y = -50
                self.rect.x = randint(10, 690)
                bullets.remove(i)
                global score
                score += 1

class bullet(GameSprite):
    def __init__(self, sprite, x, y, w, h, speed):
        super().__init__(sprite, x, y, w, h, speed)
    def whenFired(self):
        self.rect.y -= self.speed

enemies = []

Player = player('rabbid.png', 300, 425, 1302//25, 1920//25, 5)
for i in range(3):
    Enemy = enemy('rabbid.png', randint(10, 690), 0, 1280//15, 649//15, randint(1,4))
    enemies.append(Enemy)

bullets = []


game = True
while game:

    window.blit(background, (0, 0))
    Player.move()
    Player.fire()

    for i in bullets:
        window.blit(i.image, (i.rect.x, i.rect.y))
        i.whenFired()
    for i in enemies:
        window.blit(i.image, (i.rect.x, i.rect.y))
        i.pluh()
        i.down()

    hahaYouMissedText = style.render('Missed:' + str(missed), 1, (0, 0, 0))
    wowYouHitThemGyattsText = style.render('Score:' + str(score), 1, (0, 0, 0))
    heresWhatYouNeedToDoBluddy = style.render('Objective: rabbid', 1, (255, 0, 0))
    window.blit(wowYouHitThemGyattsText, (1, 1))
    window.blit(hahaYouMissedText, (1, 31))
    window.blit(heresWhatYouNeedToDoBluddy, (1, 61))

    window.blit(Player.image, (Player.rect.x, Player.rect.y))

    keysPressed = key.get_pressed()

    Player.cooldown -= 1

    for e in event.get():
        if e.type == QUIT:
            game = False

    clock.tick(FPS)
    display.update()