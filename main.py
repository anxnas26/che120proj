import pygame
import sys

pygame.init()

black = (0,0,0)
white = (255, 255, 255)


screenWidth =  1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
squaresize = 100
size = (screenWidth, screenHeight)

stickWidth = 20
stickHeight = 100
stickSpeed = 5
stick_x = screenWidth - stickWidth #set intitial x-coordinate
stick_y = (screenHeight - stickHeight) // 2  # set initial y-coordinate

class AirHockeyStick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.speed = 5

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y < screenHeight - self.height:
            self.y += self.speed

stick1 = AirHockeyStick((screenWidth - (stickWidth*2)), ((screenHeight - stickHeight) // 2))
stick2 = AirHockeyStick((stickWidth), ((screenHeight - stickHeight) // 2))

            
def stickControls(stick: AirHockeyStick, controls: str):
    keys = pygame.key.get_pressed()

    if controls == 'arrows':
        if keys[pygame.K_UP]:
            stick.move_up()
        if keys[pygame.K_DOWN]:
            stick.move_down()

    elif controls == 'wasd':
        if keys[pygame.K_w]:
            stick.move_up()
        if keys[pygame.K_s]:
            stick.move_down()
    
    else:
        print("error")


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    stickControls(stick1, 'arrows')
    stickControls(stick2, 'wasd')

    screen.fill(white)
    pygame.draw.rect(screen, white, (0, 0, screenWidth, squaresize))
    pygame.draw.rect(screen, black, (stick1.x, stick1.y, stick1.width, stick1.height))
    pygame.draw.rect(screen, black, (stick2.x, stick2.y, stick2.width, stick2.height))

    pygame.display.flip()