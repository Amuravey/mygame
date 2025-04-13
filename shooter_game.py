from pygame import *
from random import randint

win_up = 500
win_line = 700

font.init()
font1 = font.SysFont('Arial', 40)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

rocket_x = 100
rocket_y = 420

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):   #Класс врага
    def update(self):    #Метод для движения
        global lost
        if self.rect.y >= 500:   #Если координата у > 500 (спрайт очень низко)
            self.rect.y = 0  #Перемещаем спрайт наверх
            self.rect.x = randint(0, win_line - 65) # чтобы не вылетали за край
            lost = lost + 1
        else:  #Если координата у < 500 (не достигли низа)
            self.rect.y += self.speed #Увеличиваем координату (спрайт плывет вниз)


bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):    #Метод для движения
        self.rect.y -= self.speed
        if self.rect.y <= 0: 
            self.kill()

class Player(GameSprite):
        def update(self):
            keys = key.get_pressed()
            if keys[K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_line - 65:
                self.rect.x += self.speed
        def fire(self):
            bullet = Bullet('bullet.png', self.rect.x + 25, self.rect.y, 5) #стреляем из центра
            bullets.add(bullet)

rocket = Player('rocket.png', rocket_x , rocket_y, 6)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, win_line - 65), -40, randint(1, 2)) #чтобы не вылетали за край
    monsters.add(monster)


lost = 0 
max_lost = 5 #увеличил кол-во проигрышей

window = display.set_mode((win_line, win_up))
display.set_caption('Шутер')
backgrond = transform.scale(
    image.load('galaxy.jpg'), (win_line, win_up)
    )

finish = False
score = 0
max_score = 200 #увеличил кол-во побед

clock = time.Clock()
FPS = 90

game = True
while game:    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:  #стрельба по нажатию
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        window.blit(backgrond,(0,0))
        bullets.update()
        rocket.update()
        monsters.update()
        rocket.reset()
        bullets.draw(window)
        monsters.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides :
            score = score + 1
            monster = Enemy('ufo.png', randint(0, win_line - 65), -40, randint(1, 2)) #чтобы не вылетали за край
            monsters.add(monster)

        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:  #проигрыш
            finish = True
            window.blit(lose,(200, 200)) #чтобы текст был по центру
        if score >= max_score:  #выигрыш
            finish = True
            window.blit(win,(200,200))  #чтобы текст был по центру

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters: #обновление врагов
            m.kill()
        for i in range(5):
            monster = Enemy('ufo.png', randint(0, win_line - 65), -40, randint(1, 2)) #чтобы не вылетали за край
            monsters.add(monster)
        time.delay(3000) # чтобы не было моментального рестарта

    display.update()
    clock.tick(FPS)
