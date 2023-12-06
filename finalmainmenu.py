import pygame
import sys

pygame.init()

width, height = 800, 600
pygame.display.set_caption("Air Hockey Game")
screenfill = pygame.display.set_mode((width, height))

background_surface = pygame.image.load('/Users/aayan/Desktop/Final/Graphics/Wooden.jpeg').convert()
background_surface = pygame.transform.scale(background_surface, (width, height))

settings_background = pygame.image.load('/Users/aayan/Desktop/Final/Graphics/Wooden.jpeg').convert()
settings_background = pygame.transform.scale(settings_background, (width, height))

white = (255, 255, 255)
font = pygame.font.Font("/Users/aayan/Desktop/Final/Font/FFF_Tusj.ttf", 36)

# Initialize the mixer module
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load('/Users/aayan/Desktop/Final/Audio/onlymp3.to - Air Hockey Challenge OST Main Theme-VcNI_-82h9g-192k-1701818078.mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Initialize sound state
sound_on = True

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        pygame.mixer.music.set_volume(1.0)  # Set volume to maximum (1.0)
    else:
        pygame.mixer.music.set_volume(0.0)  # Set volume to minimum (0.0)

def draw_button(text, position):
    button_text = font.render(text, True, white)
    button_rect = button_text.get_rect(center=position)
    screenfill.blit(button_text, button_rect)

def return_button():
    return_text = font.render("Return", True, white)
    return_rect = return_text.get_rect(center=(width // 2, height // 2))
    screenfill.blit(return_text, return_rect)
    return return_rect

def player_vs_ai_screen():
    while True:
        screenfill.fill((0, 0, 0))

        return_rect = return_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_rect.collidepoint(event.pos):
                        return

def player_vs_player_screen():
    while True:
        screenfill.fill((0, 0, 0))

        return_rect = return_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_rect.collidepoint(event.pos):
                        return

def main_menu():
    while True:
        screenfill.blit(background_surface, (0, 0))

        title_text = font.render("Air Hockey Game", True, white)
        screenfill.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

        button_positions = [(width // 2, 200), (width // 2, 250), (width // 2, 300)]
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

def settings_menu():
    global sound_on
    while True:
        screenfill.blit(settings_background, (0, 0))

        title_text = font.render("Settings", True, white)
        screenfill.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

        sound_text = font.render(f"Adjust Sound [{'ON' if sound_on else 'OFF'}]", True, white)
        sound_rect = sound_text.get_rect(center=(width // 2, 200))
        screenfill.blit(sound_text, sound_rect)

        return_text = font.render("Return", True, white)
        return_rect = return_text.get_rect(center=(width // 2, 300))
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

if __name__ == "__main__":
    main_menu()
