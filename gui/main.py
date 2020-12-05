import math
import os.path
import random
import sys
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 500

pygame.display.set_caption("Hangman Game")
project_directory = os.path.dirname(__file__)

"""Author https://www.iconbros.com/icons/ib-g-hangman for icon"""
ICON = pygame.image.load(os.path.join(project_directory, "images/icon.png"))
pygame.display.set_icon(ICON)

# Font
COMICSHANNS = os.path.join(project_directory, "font/comic-shanns.otf")

TITLE_FONT = pygame.font.Font(COMICSHANNS, 70)
LETTER_FONT = pygame.font.Font(COMICSHANNS, 30)
WORD_FONT = pygame.font.Font(COMICSHANNS, 40)

# Game variables
HANGMAN_STATUS = 0
WORDS = ["IDE", "PYTHON", "DEVELOPER", "PYGAME", "VIM", "STRAGER", "RUBY",
         "CPLUSPLUS", "TWITCH", "JAVASCRIPT", "HTML", "CSS", "NODEJS"]
WORD = random.choice(WORDS)
GUESSED = ["D", "Y", "I", "J", "A", "H"]
CLICK = False

# Buttons
RADIUS = 20
GAP = 15
letters = []
STARTX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)  # answer = 42
STARTY = 400
A = 65
for i in range(26):
    x = STARTX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = STARTY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_GREY = (60, 60, 90)
GREEN = (66, 244, 66)
RED = (255, 0, 0)


def draw():
    screen.fill(WHITE)

    # Text
    text = TITLE_FONT.render("DEVELOPER HANGMAN", True, BLACK)
    screen.blit(text, (int(WIDTH / 2) - int(text.get_width() / 2), 20))

    # Hangman image
    screen.blit(images[HANGMAN_STATUS], (150, 100))

    # Draw buttons
    for letter in letters:
        a, b, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, BLACK, (a, b), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            screen.blit(text, (int(a - text.get_width() / 2), int(b
                                                                  - text.get_height() / 2)))

    # Draw word
    display_word = ""
    for letter in WORD:
        if letter in GUESSED:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    screen.blit(text, (400, 200))


def display_message(message):
    global WORD

    screen.fill(WHITE)

    # You won or You lose
    text = WORD_FONT.render(message, True, BLACK)
    screen.blit(text, (int(WIDTH / 2 - text.get_width() / 2), int(HEIGHT / 2
                                                                  - text.get_height() / 2)))

    # The was word
    display_word = WORD_FONT.render(f"The word was {WORD}", True, BLACK)
    screen.blit(display_word, (int(WIDTH / 2 - display_word.get_width() / 2),
                               int(
                                   HEIGHT / 2 - display_word.get_height() / 2 + 50)))
    pygame.display.update()


def menu():
    global CLICK, HANGMAN_STATUS, GUESSED, WORDS, WORD

    # FPS
    fps = 60
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)
        pos_x, pos_y = pygame.mouse.get_pos()

        # Position of buttons
        pos_play_button = (100, 400, 120, 50)
        pos_quit_button = (550, 400, 120, 50)

        # Create the buttons
        button_play = pygame.Rect(pos_play_button)
        button_quit = pygame.Rect(pos_quit_button)

        # Create text inside the buttons
        text_play = WORD_FONT.render("Play", True, BLACK)
        text_quit = WORD_FONT.render("Quit", True, BLACK)

        # Check collision
        if button_play.collidepoint(pos_x, pos_y):
            pygame.draw.rect(screen, BRIGHT_GREY, pos_play_button)
            if CLICK:
                HANGMAN_STATUS = 0
                WORDS = ["IDE", "PYTHON", "DEVELOPER", "PYGAME", "VIM"]
                WORD = random.choice(WORDS)
                GUESSED = ["D", "Y", "I"]
                CLICK = False
                for letter in letters:
                    letter[3] = True
                main()
        if button_quit.collidepoint(pos_x, pos_y):
            pygame.draw.rect(screen, BRIGHT_GREY, pos_quit_button)
            if CLICK:
                sys.exit()

        # Draw the buttons
        pygame.draw.rect(screen, GREEN, button_play)
        pygame.draw.rect(screen, RED, button_quit)

        screen.blit(text_play, (120, 405))
        screen.blit(text_quit, (570, 405))

        CLICK = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    CLICK = True

        pygame.display.update()


def main():
    global HANGMAN_STATUS

    # FPS
    fps = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        # FPS
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    j, k, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((j - m_x) ** 2 + (k - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            GUESSED.append(ltr)
                            if ltr not in WORD:
                                HANGMAN_STATUS += 1
        draw()

        won = True
        for letter in WORD:
            if letter not in GUESSED:
                won = False
                break

        if won:
            display_message("You won")
            menu()
            break

        if HANGMAN_STATUS == 6:
            display_message("You lose")
            menu()
            break

        pygame.display.update()


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Images
    images = []
    for i in range(7):
        image = os.path.join(project_directory, "images/hangman")
        image = pygame.image.load(image + str(i) + ".png")
        images.append(image)

    main()
