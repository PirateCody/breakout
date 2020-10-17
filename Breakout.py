import pygame
from random import randint

pygame.init()

level = 1
windowWidth = 1000
windowHeight = 600
ballStartPosX = int(windowWidth / 2)
ballStartPosY = 400
ballWidth = 10
ballHeight = 10
brickWidth = 100
brickHeight = 50
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brickColor = white
paddleWidth = 200
paddleHeight = 25
paddleVelocity = 5
upperBoundY = 50
brickHitCounter = 0

paddleStartingPositionX = int((windowWidth - paddleWidth) / 2)
paddleStartingPositionY = 550

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super(Brick, self).__init__()
        self.image = pygame.Surface((brickWidth, brickHeight))
        self.image.fill(brickColor)
        pygame.draw.rect(self.image, brickColor, (brickWidth, brickHeight, 0, 0))

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
        self.velocity = [0,0]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

    def respawn(self):
        self.rect.x = ballStartPosX
        self.rect.y = ballStartPosY
        self.setVelocity(-2, 2)

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

paddle.rect.x = paddleStartingPositionX
paddle.rect.y = paddleStartingPositionY

ball.rect.x = ballStartPosX
ball.rect.y = ballStartPosY

Brick.spawnBricks(Brick)

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
    if keys[pygame.K_SPACE] and ball.velocity[0] == 0 and ball.velocity[1] == 0:
        ball.respawn()

    # COLLISION
    if pygame.sprite.collide_rect(ball, paddle):
        ball.bounce()

    if pygame.sprite.spritecollide(ball, bricks, True):
        ball.bounce()
        brickHitCounter+=1

        if brickHitCounter % 24 == 0:
            level += 1
            if level == 2:
                brickColor = red
            elif level == 3:
                brickColor == blue
            else:
                brickColor = green

            Brick.spawnBricks(Brick)

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

    if ball.rect.y >= (windowHeight-ballHeight):
        ball.respawn()

    pygame.display.flip()
    clock.tick(60)
