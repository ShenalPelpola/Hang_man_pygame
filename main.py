import math
import random
import pygame
import Utilities.colors as colors
from Models.Letter import Letter

pygame.init()

# setting the width and height for the screen
WIDTH, HEIGHT = 900, 550
window = pygame.display.set_mode((WIDTH, HEIGHT))
# setting the name of the game
pygame.display.set_caption("Hangman Game GUESS THE WORD!")

# load images
images = []
for i in range(7):
    image = pygame.image.load("images/hangman" + str(i) + ".png")
    images.append(image)

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# game variables
hangman_status = 0
game_words = ["HELLO", "PYTHON", "WORLD", "DEVELOPER"]
word = random.choice(game_words)
guessed = []

# button variables
RADIUS = 25
GAP = 18
startX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
startY = 415
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters = []

for i in range(26):
    x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letter = Letter(x, y, ALPHABET[i], True)
    letters.append(letter)


def reset():
    global hangman_status
    global game_words
    global word
    global guessed
    global letters

    hangman_status = 0
    word = random.choice(game_words)
    guessed = []

    for ltr in letters:
        ltr.visible = True


def draw():
    window.fill(colors.background)
    # draw title
    title = TITLE_FONT.render("HANGMAN!", 1, colors.letterColor)
    window.blit(title, (WIDTH / 2 - title.get_width() / 2, 20))
    # draw word
    display_word = ""
    for ler in word:
        if ler in guessed:
            display_word += ler + "  "
        else:
            display_word += "_  "
    text = WORD_FONT.render(display_word, 1, colors.letterColor)
    window.blit(text, (425, 200))
    # draw buttons
    for letter in letters:
        pos_x = letter.x
        pos_y = letter.y
        ltr = letter.ltr
        isVisible = letter.visible
        if isVisible:
            pygame.draw.circle(window, colors.buttonColor, (pos_x, pos_y), RADIUS)
            text = LETTER_FONT.render(ltr, 1, colors.letterColor)
            window.blit(text, (pos_x - text.get_width() / 2, pos_y - text.get_height() / 2))

    window.blit(images[hangman_status], (150, 125))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    window.fill(colors.buttonColor)
    text = WORD_FONT.render(message, 1, colors.letterColor)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    # The game loop - game loops checks for events
    # e.g: clicks, double clicks, timers collisions etc
    FPS = 60  # speed of the game
    clock = pygame.time.Clock()
    run = True
    global hangman_status
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x = letter.x
                    y = letter.y
                    ltr = letter.ltr
                    isVisible = letter.visible
                    if isVisible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter.visible = False
                            guessed.append(ltr)

                            if ltr not in word:
                                hangman_status += 1
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            display_message("You won!")
            break

        elif hangman_status == 6:
            display_message("You lost!")
            break


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        else:
            reset()
            main()

