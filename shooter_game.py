#Создай собственный Шутер!

from pygame import *

from random import randint

font.init()
font2 = font.SysFont("impact", 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        self.direction = "right"
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
             self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
             self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,20, 40, -15)
        bullets.add(bullet)

score= 0
lost= 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost +1
        

    


class Bullet(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

bullets = sprite.Group()

window = display.set_mode((700, 500))

display.set_caption("шутер")
background = transform.scale(image.load("galaxy.jpg"), (700,500))

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80,620), -40,80,50,randint(1,5))
    monsters.add(monster)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


# player1 = Enemy("ufo.p/ng",110,120,5,60,60)
player2 = Player("rocket.png",5,400,50,70,5)

finish = False

FPS = 60

clock = time.Clock()
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player2.fire()
    if finish != True:

        window.blit(background,(0,0))

        text = font2.render("счет:" + str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("пропущено:" + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        player2.reset()
        player2.update()
        # player1.reset()
        # player1.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, 620),-40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player2, monsters, False) or lost >=10:
            finish = True

        if score >= 10:
            finish = True

        display.update()
    clock.tick(FPS)
   
