"""
All work was split equally amongst group members

Air Hockey game with options to play with your friend (locally) or with AI

Github Project: https://github.com/anxnas26/che120proj

*Some debugging was done with the aid of ChatGPT. It is commented where it was used.

"""

__authors__ = "Anas Alsaid Ahmad, Aayan Asghar"
__date__ = "05/12/2023"

import pygame
import sys
import os
from random import randint

pygame.init()

black = (0,0,0)
white = (255, 255, 255)
blue = (0,0,255)
red = (255, 0, 0)

font1 = pygame.font.Font(None, 70)

#seeting up the screen
screenWidth =  1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
squaresize = 100
screenSize = (screenWidth, screenHeight)
screenCenter = (screenWidth//2 , screenHeight//2)

# Get the directory of the program
script_dir = os.path.dirname(os.path.abspath(__file__)) #debugged with ChatGPT. It came up with this idea for the file paths


pygame.display.set_caption("Air Hockey Game")
screenfill = pygame.display.set_mode((screenWidth, screenHeight))

# Load background image
background_path = os.path.join(script_dir, 'resources', 'Graphics', 'Wooden.jpeg')
background_surface = pygame.image.load(background_path).convert()
background_surface = pygame.transform.scale(background_surface, (screenWidth, screenHeight))

# Load settings background image
settings_background_path = os.path.join(script_dir, 'resources', 'Graphics', 'Wooden.jpeg')
settings_background = pygame.image.load(settings_background_path).convert()
settings_background = pygame.transform.scale(settings_background, (screenWidth, screenHeight))

# Load font
font_path = os.path.join(script_dir, 'resources', 'Font', 'FFF_Tusj.ttf')
font = pygame.font.Font(font_path, 36)

pygame.mixer.init()

# Load and play the background music
music_path = os.path.join(script_dir, 'resources', 'Audio', 'onlymp3.to - Air Hockey Challenge OST Main Theme-VcNI_-82h9g-192k-1701818078.mp3')
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

sound_on = True


def toggle_sound(): #toggles the music on and off
    global sound_on
    sound_on = not sound_on
    if sound_on:
        pygame.mixer.music.set_volume(1.0)  # Set volume to maximum (1.0)
    else:
        pygame.mixer.music.set_volume(0.0)  # Set volume to minimum (0.0)


def draw_button(text, position): #draws the buttons
    button_text = font.render(text, True, white)
    button_rect = button_text.get_rect(center=position)
    screenfill.blit(button_text, button_rect)


def return_button(): #return button (for settings)
    return_text = font.render("Return", True, white)
    return_rect = return_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
    screenfill.blit(return_text, return_rect)
    return return_rect


def settings_menu(): #menu for modifying game settings
    global sound_on
    while True:
        screenfill.blit(settings_background, (0, 0))

        title_text = font.render("Settings", True, white)
        screenfill.blit(title_text, (screenWidth // 2 - title_text.get_width() // 2, 50))

        sound_text = font.render(f"Adjust Sound [{'ON' if sound_on else 'OFF'}]", True, white)
        sound_rect = sound_text.get_rect(center=(screenWidth // 2, 200))
        screenfill.blit(sound_text, sound_rect)

        return_text = font.render("Return", True, white)
        return_rect = return_text.get_rect(center=(screenWidth // 2, 300))
        screenfill.blit(return_text, return_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_rect.collidepoint(event.pos):
                        return
                    elif sound_rect.collidepoint(event.pos):
                        toggle_sound()


#Game functions

#variables for setting up the game
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
            if self.x < (stickWidth*10):
                self.x += self.speed

    def move_left(self):
        if self.player == 2:
            if self.x > (screenWidth - (stickWidth*10)):
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

    def startPuck(self): #sets the pucks intial position and reset position (when someone scores)
        if self.x == 0 or self.x == screenWidth:
            #place the puck in the middle
            self.x = screenWidth // 2
            self.y = screenHeight // 2
            # Generate random speeds for the puck
            self.speed_x = randint(3, 7) * (-1 if randint(0, 1) == 0 else 1)
            self.speed_y = randint(3, 7) * (-1 if randint(0, 1) == 0 else 1)
        else:
            pass

        self.x += self.speed_x
        self.y += self.speed_y

    def checkWallCollisions(self): #checks for any wall collisions
        if self.x - self.size < 0 or self.x + self.size > screenWidth:
            return self.x

        if self.y - self.size < 0 or self.y + self.size > screenHeight:
            self.speed_y = -self.speed_y


#these 2 functions check for a score on either side of the map
def puckScoreRight(puck: AirHockeyPuck) -> bool:
    if puck.checkWallCollisions() == screenWidth:
        puck.startPuck()
        return True
    else:
        pass


def puckScoreLeft(puck: AirHockeyPuck) -> bool:
    if puck.checkWallCollisions() == 0:
        puck.startPuck()
        return True
    else:
        return False


def scoreboard(counter1, counter2): #keeps track of player's scores
    score_text = font1.render(f" {counter1}   {counter2}", True, red)
    text_rect = score_text.get_rect(center=(screenWidth // 2, 50))
    screen.blit(score_text, text_rect.topleft)


def checkCollisions(stick1: AirHockeyStick, stick2:AirHockeyStick, puck: AirHockeyPuck) -> None:
    puck.startPuck()
    puck.checkWallCollisions()

    # Check collisions with the sticks
    if stick1.check_collision(puck) or stick2.check_collision(puck):
        puck_speed = pygame.math.Vector2(puck.speed_x, puck.speed_y)

        # Calculate the collision normal vector based on the stick's orientation
        if stick1.check_collision(puck):
            collision_normal = pygame.math.Vector2(1, 0)
        else:
            collision_normal = pygame.math.Vector2(-1, 0)

        # Reflect the puck's velocity vector based on the collision normal
        puck_speed.reflect_ip(collision_normal) #debugged with ChatGPT
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

def aiControls(stick: AirHockeyStick, puck: AirHockeyPuck):

    if stick.y + stick.height // 2 < puck.y:
        stick.move_down()
    elif stick.y + stick.height // 2 > puck.y:
        stick.move_up()


def drawBoard():
    screen.fill(white)
    pygame.draw.rect(screen, white, (0, 0, screenWidth, squaresize))
    pygame.draw.circle(screen, red, (screenWidth//2, screenHeight//2), 100)


def draw_button(text, position):
    button_text = font.render(text, True, white)
    button_rect = button_text.get_rect(center=position)
    screenfill.blit(button_text, button_rect)


# ---- Game

stick1 = AirHockeyStick((screenWidth - (stickWidth*2)), stick_y, 2)
stick2 = AirHockeyStick((stickWidth), stick_y, 1)
puck = AirHockeyPuck((screenWidth//2),(screenHeight//2), 20, 5, 5)

counter1 = 0
counter2 = 0

def player_vs_player_screen():
    running = True
    global counter1, counter2 #debugged with ChatGPT assistance
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

        if counter1 == 1 or counter2 == 1:
            screen.fill(black)
            celebration_text = font1.render("Player {} wins!".format(1 if counter1 >= 1 else 2), True, white)
            text_rect = celebration_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
            screen.blit(celebration_text, text_rect.topleft)
            print("Game ends")
            pygame.display.flip()

            pygame.time.delay(3000)
            sys.exit()


        drawBoard()
        scoreboard(counter1, counter2)
        pygame.draw.rect(screen, black, (stick1.x, stick1.y, stick1.width, stick1.height))
        pygame.draw.rect(screen, black, (stick2.x, stick2.y, stick2.width, stick2.height))
        pygame.draw.circle(screen, puck.colour, (int(puck.x), int(puck.y)), puck.size)
        pygame.display.flip()


def player_vs_ai_screen():
    running = True
    global counter1, counter2
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()


        stickControls(stick2, 'wasd')
        aiControls(stick1, puck)


        checkCollisions(stick1, stick2, puck)

        if puckScoreRight(puck):
            counter1 += 1
            
        if puckScoreLeft(puck):
            counter2 += 1

        if counter1 == 1 or counter2 == 1:
            screen.fill(black)
            celebration_text = font1.render("Player {} wins!".format(1 if counter1 >= 1 else 2), True, white) #debugged with ChatGPT
            text_rect = celebration_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
            screen.blit(celebration_text, text_rect.topleft)
            print("Game ends")
            pygame.display.flip()

            pygame.time.delay(3000)
            sys.exit()


        drawBoard()
        scoreboard(counter1, counter2)
        pygame.draw.rect(screen, black, (stick1.x, stick1.y, stick1.width, stick1.height))
        pygame.draw.rect(screen, black, (stick2.x, stick2.y, stick2.width, stick2.height))
        pygame.draw.circle(screen, puck.colour, (int(puck.x), int(puck.y)), puck.size)
        pygame.display.flip()


def main():
    while True:
        screenfill.blit(background_surface, (0, 0))

        title_text = font.render("Air Hockey Game", True, white)
        screenfill.blit(title_text, (screenWidth // 2 - title_text.get_width() // 2, 50))

        button_positions = [(screenWidth // 2, 200), (screenWidth // 2, 250), (screenWidth // 2, 300)]
        options = ["Player vs AI", "Player vs Player", "Settings"]
        for option, position in zip(options, button_positions):
            draw_button(option, position)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for option, position in zip(options, button_positions):
                        button_rect = font.render(option, True, white).get_rect(center=position)
                        if button_rect.collidepoint(event.pos):
                            if option == "Player vs AI":
                                player_vs_ai_screen()
                            elif option == "Player vs Player":
                                player_vs_player_screen()
                            elif option == "Settings":
                                settings_menu()


if __name__ == "__main__":
    main()
