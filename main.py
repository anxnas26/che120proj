import pygame
import sys
from random import randint

pygame.init()

black = (0,0,0)
white = (255, 255, 255)
blue = (0,0,255)
red = (255, 0, 0)


screenWidth =  1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
squaresize = 100
screenSize = (screenWidth, screenHeight)
screenCenter = (screenWidth//2 , screenHeight//2)

stickWidth = 20
stickHeight = 100
stickSpeed = 5
stick_x = screenWidth - stickWidth #set intitial x-coordinate
stick_y = (screenHeight - stickHeight) // 2  # set initial y-coordinate

class AirHockeyStick:
    def __init__(self, x: int, y: int, player: int):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.speed = 5
        self.player = player

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y < screenHeight - self.height:
            self.y += self.speed
    
    def move_right(self):
        if self.player == 2:
            if self.x < (screenWidth - stickWidth):
                self.x += self.speed
        else:
            if self.x < (stickWidth*4):
                self.x += self.speed

    def move_left(self):
        if self.player == 2:
            if self.x > (screenWidth - (stickWidth*4)):
                self.x -= self.speed
        else:
            if self.x > 0:
                self.x -= self.speed

    def check_collision(self, puck):
        return (
            self.x < puck.x + puck.size and
            self.x + self.width > puck.x and
            self.y < puck.y + puck.size and
            self.y + self.height > puck.y
        )

class AirHockeyPuck:
    def __init__(self, x: int, y: int, size: int, speed_x: int, speed_y: int, colour = black) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.colour = colour

    def startPuck(self):
        if self.checkWallCollisions() == 0 or self.checkWallCollisions() == screenWidth:
            self.x = screenWidth // 2
            self.y = screenHeight // 2
        else:
            pass

        self.x += self.speed_x
        self.y += self.speed_y


    def checkWallCollisions(self):
        if self.x - self.size < 0 or self.x + self.size > screenWidth:
            return self.x - self.size

        if self.y - self.size < 0 or self.y + self.size > screenHeight:
            self.speed_y = -self.speed_y


def puckScoreRight(puck: AirHockeyPuck) -> bool:
    if puck.checkWallCollisions() == 0:
        return True
    else:
        pass

def puckScoreLeft(puck: AirHockeyPuck) -> bool:
    if puck.checkWallCollisions() == screenWidth:
        return True
    else:
        pass

def scoreboard():
    pass


def checkCollisions(stick1: AirHockeyStick, stick2:AirHockeyStick, puck: AirHockeyPuck) -> None:
    puck.startPuck()
    puck.checkWallCollisions()

    # Check collisions with the sticks
    if stick1.check_collision(puck) or stick2.check_collision(puck):
        puck_speed = pygame.math.Vector2(puck.speed_x, puck.speed_y)

        # Calculate the collision normal vector based on the stick's orientation
        if stick1.check_collision(puck):
            collision_normal = pygame.math.Vector2(1, 0)  # Right stick
        else:
            collision_normal = pygame.math.Vector2(-1, 0)  # Left stick

        # Reflect the puck's velocity vector based on the collision normal
        puck_speed.reflect_ip(collision_normal)
        puck.speed_x = puck_speed.x
        puck.speed_y = puck_speed.y


def stickControls(stick: AirHockeyStick, controls: str):
    keys = pygame.key.get_pressed()

    if controls == 'arrows':
        if keys[pygame.K_UP]:
            stick.move_up()
        if keys[pygame.K_DOWN]:
            stick.move_down()
        if keys[pygame.K_RIGHT]:
            stick.move_right()
        if keys[pygame.K_LEFT]:
            stick.move_left()

    elif controls == 'wasd':
        if keys[pygame.K_w]:
            stick.move_up()
        if keys[pygame.K_s]:
            stick.move_down()
        if keys[pygame.K_d]:
            stick.move_right()
        if keys[pygame.K_a]:
            stick.move_left()
    
    else:
        print("error")


def drawBoard():
    screen.fill(white)
    pygame.draw.rect(screen, white, (0, 0, screenWidth, squaresize))
    pygame.draw.circle(screen, red, (screenWidth//2, screenHeight//2), 100)


stick1 = AirHockeyStick((screenWidth - (stickWidth*2)), stick_y, 2)
stick2 = AirHockeyStick((stickWidth), stick_y, 1)
puck = AirHockeyPuck((screenWidth//2),(screenHeight//2), 20, 5, 5)

counter1 = 0
counter2 = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    stickControls(stick1, 'arrows')
    stickControls(stick2, 'wasd')


    checkCollisions(stick1, stick2, puck)

    if puckScoreRight(puck):
        counter1 += 1
    if puckScoreLeft(puck):
        counter2 += 1

    if counter1 == 5 or counter2 == 5:
        print("Game ends")
        running = False


    drawBoard()
    pygame.draw.rect(screen, black, (stick1.x, stick1.y, stick1.width, stick1.height))
    pygame.draw.rect(screen, black, (stick2.x, stick2.y, stick2.width, stick2.height))
    pygame.draw.circle(screen, puck.colour, (int(puck.x), int(puck.y)), puck.size)
    pygame.display.flip()