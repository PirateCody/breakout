import random

import pygame

import GameValues as gv

pygame.init()

paddleStartingPositionX = int((gv.windowWidth - gv.paddleWidth) / 2)
paddleStartingPositionY = 550

screen = pygame.display.set_mode((gv.windowWidth, gv.windowHeight))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super(Brick, self).__init__()
        self.image = pygame.Surface((gv.brickWidth, gv.brickHeight))
        self.image.fill(gv.brickColor)
        pygame.draw.rect(self.image, gv.brickColor, (gv.brickWidth, gv.brickHeight, 0, 0))

        self.rect = self.image.get_rect()

    def spawnBricks(self):
        # Attempt to have all of the bricks in a list, rather than each one as an individual object
        brickObjects = []

        for x in range(24):
            brickObjects.append(Brick())

        brickCounter = 0

        # Determines the row
        heightMultiplier = 1

        # Space between the left window edge and the bricks
        brickWidthPadding = 75

        for brick in brickObjects:
            brick.rect.x = brickWidthPadding + (brickCounter * (gv.brickWidth + 10))

            if brick.rect.x >= gv.windowWidth - gv.brickWidth:
                heightMultiplier += 1
                brickCounter = 0
                brick.rect.x = brickWidthPadding

            brick.rect.y = 100 * heightMultiplier
            bricks.add(brick)
            brickCounter += 1
            print("Brick: " + str(brickCounter))


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle, self).__init__()
        self.image = pygame.Surface((gv.paddleWidth, gv.paddleHeight))
        self.image.fill(gv.white)
        self.image.set_colorkey(gv.black)
        pygame.draw.rect(self.image, gv.white, (0, 0, gv.paddleWidth, gv.paddleHeight))

        self.rect = self.image.get_rect()

    def moveRight(self):
        self.rect.x += gv.paddleVelocity

    def moveLeft(self):
        self.rect.x -= gv.paddleVelocity


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.image = pygame.Surface((gv.ballWidth, gv.ballHeight))
        self.image.fill(gv.green)
        self.image.set_colorkey(gv.white)
        pygame.draw.rect(self.image, gv.green, (0, 0, gv.ballWidth, gv.ballHeight))

        self.rect = self.image.get_rect()
        self.velocity = [0.0, 0.0]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

    def respawn(self):
        self.rect.x = gv.ballStartPosX
        self.rect.y = gv.ballStartPosY
        self.setVelocity(-2, 2)

    def setVelocity(self, lowerBound, upperBound):
        self.velocity = [random.randint(lowerBound, upperBound), random.randint(lowerBound, upperBound)]

        # This is to keep the velocities from being -1, 0, or 1;
        # so that they don't bounce completely vertically or horizontally
        if -2 < self.velocity[1] < 2:
            if self.velocity[1] < 0:
                self.velocity[1] = -2
            else:
                self.velocity[1] = 2

        if -2 < self.velocity[0] < 2:
            if self.velocity[0] < 0:
                self.velocity[0] = -2
            else:
                self.velocity[0] = 2


paddle = Paddle()
brick1 = Brick()
brick2 = Brick()
brick3 = Brick()
ball = Ball()

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

bricks = pygame.sprite.Group()

paddle.rect.x = paddleStartingPositionX
paddle.rect.y = paddleStartingPositionY

ball.rect.x = gv.ballStartPosX
ball.rect.y = gv.ballStartPosY

Brick.spawnBricks(Brick)

font = pygame.font.SysFont("Arial", 32)

# GAME LOOP
active = True
while (active):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    screen.fill(gv.black)

    # KEY ACTIONS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and paddle.rect.x < (gv.windowWidth - gv.paddleWidth):
        paddle.moveRight()
    if keys[pygame.K_LEFT] and paddle.rect.x > 0:
        paddle.moveLeft()
    if keys[pygame.K_SPACE] and ball.velocity[0] == 0 and ball.velocity[1] == 0:
        ball.respawn()

    # COLLISION
    if pygame.sprite.collide_rect(ball, paddle):
        ball.bounce()

    if pygame.sprite.spritecollide(ball, bricks, True):
        ball.bounce()
        gv.brickHitCounter += 1
        gv.score += 1
        print("Brick Hit Counter: " + str(gv.brickHitCounter))

        if gv.brickHitCounter % 24 == 0:
            gv.level += 1
            if gv.level == 2:
                brickColor = gv.red
            elif gv.level == 3:
                brickColor = gv.blue
            elif gv.level == 4:
                brickColor = gv.yellow
            else:
                brickColor = gv.green

            Brick.spawnBricks(Brick)

    # DRAW AND UPDATE
    pygame.draw.line(screen, gv.white, (0, gv.upperBoundY), (gv.windowWidth, gv.upperBoundY), 5)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    bricks.draw(screen)
    bricks.update()
    ball.update()

    if ball.rect.y <= gv.upperBoundY or ball.rect.y >= (gv.windowHeight - gv.ballHeight):
        ball.velocity[1] = -ball.velocity[1]

    if ball.rect.x <= 0 or ball.rect.x >= (gv.windowWidth - gv.ballWidth):
        ball.velocity[0] = -ball.velocity[0]

    if ball.rect.y >= (gv.windowHeight - gv.ballHeight):
        ball.respawn()
        gv.lives -= 1


    text = font.render("Score: " + str(gv.score), 1, gv.white)
    screen.blit(text, (15, 7))

    text = font.render("Lives: " + str(gv.lives), 1, gv.white)
    screen.blit(text, (gv.windowWidth - 150, 7))

    if(gv.lives == 0):
        gv.score = 0
        gv.lives = 10

    pygame.display.flip()
    clock.tick(60)
