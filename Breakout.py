import pygame
from random import randint

pygame.init()

windowWidth = 1000
windowHeight = 600
ballStartPosX = int(windowWidth / 2)
ballStartPosY = 350
ballWidth = 15
ballHeight = 15
brickWidth = 100
brickHeight = 50
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
paddleWidth = 200
paddleHeight = 25
paddleVelocity = 5
upperBoundY = 50

paddleStartingPositionX = int((windowWidth - paddleWidth) / 2)
paddleStartingPositionY = 500

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super(Brick, self).__init__()
        self.image = pygame.Surface((brickWidth, brickHeight))
        self.image.fill(white)
        pygame.draw.rect(self.image, white, (brickWidth, brickHeight, 0, 0))

        self.rect = self.image.get_rect()


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle, self).__init__()
        self.image = pygame.Surface((paddleWidth, paddleHeight))
        self.image.fill(white)
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, white, (0, 0, paddleWidth, paddleHeight))

        self.rect = self.image.get_rect()

    def moveRight(self):
        self.rect.x += paddleVelocity

    def moveLeft(self):
        self.rect.x -= paddleVelocity


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.image = pygame.Surface((ballWidth, ballHeight))
        self.image.fill(green)
        self.image.set_colorkey(white)
        pygame.draw.rect(self.image, green, (0, 0, ballWidth, ballHeight))

        self.rect = self.image.get_rect()
        self.velocity = [randint(-4, 4), randint(-4, -2)]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

    def respawn(self):
        self.rect.x = ballStartPosX
        self.rect.y = ballStartPosY
        self.setVelocity(-6, -2)

    def setVelocity(self, lowerBound, upperBound):
        self.velocity = [randint(lowerBound, upperBound), randint(lowerBound, upperBound)]

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
# bricks.add(brick1)
# bricks.add(brick2)
# bricks.add(brick3)

paddle.rect.x = paddleStartingPositionX
paddle.rect.y = paddleStartingPositionY

ball.rect.x = ballStartPosX
ball.rect.y = ballStartPosY

# Attempt to have all of the bricks in a list, rather than each one as an individual object
brickObjects = []

for x in range(24):
    brickObjects.append(Brick())

brickCounter = 0
heightMultiplier = 1
brickWidthPadding = 75;

for brick in brickObjects:
    brick.rect.x = brickWidthPadding + (brickCounter * (brickWidth + 10))

    if brick.rect.x >= windowWidth - brickWidth:
        heightMultiplier += 1
        brickCounter = 0
        brick.rect.x = brickWidthPadding

    brick.rect.y = 100 * heightMultiplier
    bricks.add(brick)
    brickCounter += 1
    print("Brick: " + str(brickCounter))

# GAME LOOP
active = True
while (active):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    screen.fill(black)

    # KEY ACTIONS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and paddle.rect.x < (windowWidth - paddleWidth):
        paddle.moveRight()
    if keys[pygame.K_LEFT] and paddle.rect.x > 0:
        paddle.moveLeft()

    # COLLISION
    if pygame.sprite.collide_rect(ball, paddle):
        ball.bounce()

    if pygame.sprite.spritecollide(ball, bricks, True):
        ball.bounce()

    # DRAW AND UPDATE
    pygame.draw.line(screen, white, (0, upperBoundY), (windowWidth, upperBoundY), 5)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    bricks.draw(screen)
    bricks.update()
    ball.update()

    if ball.rect.y <= upperBoundY or ball.rect.y >= (windowHeight - ballHeight):
        ball.velocity[1] = -ball.velocity[1]

    if ball.rect.x <= 0 or ball.rect.x >= (windowWidth - ballWidth):
        ball.velocity[0] = -ball.velocity[0]

    pygame.display.flip()
    clock.tick(60)
