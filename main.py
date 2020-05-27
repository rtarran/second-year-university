# importing third party libraries
import pygame

# importing the ball class from ball file
from ball import Ball

# initialising Pygame mixer for music
pygame.mixer.pre_init(44100, 16, 2, 4096)

# Initialising Pygame library
pygame.init()

# Globals are capitalised
# Creating colour variables for ease. These are tuples
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Screen width and height variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_MIDDLE = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# Frames per second variable
# How fast the snake moves
# Difficulty variables
EASY = 5
MEDIUM = 10
HARD = 15

# This sets the canvas for the game to be played on
GAME_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game title
pygame.display.set_caption("Pong")

# Clock variable for tracking time
CLOCK = pygame.time.Clock()

# Font variable for printing to canvas
FONT = pygame.font.SysFont("Calibri", 15)
LARGE_FONT = pygame.font.SysFont("Calibri", 40)

# Pong paddle sizes in pixels
PONG_PADDLE_PIXELS = 10
PONG_PADDLE_HEIGHT = 100

# Ball variables
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# creating a list to store the ball in
sprites_list = pygame.sprite.Group()

# adding the ball to the sprites list
sprites_list.add(ball)


# function to make a list to store the range of paddle coordinates
# this will be used to check against the ball coordinates for collision detection
def create_a_list(r1, r2):
    return list(range(r1, r2))


# Function to draw a start screen with objective of the game and an option to begin or quit
def start_screen():
    intro = True

    while intro:
        GAME_SCREEN.fill(RED)
        message("Welcome to Pong, press X to begin or Y for instructions", BLACK)
        pygame.display.update()
        CLOCK.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    intro = False
            if event.type == pygame.QUIT:
                quit()


# function for displaying the winner
# user can choose to start the game again or quit
def winner_screen(winner):
    carry_on = True

    while carry_on:
        GAME_SCREEN.fill(RED)
        message(str(winner) + " wins! To play again press X", BLACK)
        pygame.display.update()
        CLOCK.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    main_game_loop()
            if event.type == pygame.QUIT:
                quit()


# Function for making a text box
def text_objects(text, colour):
    text_surface = FONT.render(text, True, colour)
    return text_surface, text_surface.get_rect()


# Function for displaying a message to the screen
def message(msg, colour):
    text_surface, text_rect = text_objects(msg, colour)
    text_rect.center = SCREEN_MIDDLE
    GAME_SCREEN.blit(text_surface, text_rect)


# Function for displaying the users score to the screen
def scoring(score, x_coordinate, y_coordinate):
    score_text = LARGE_FONT.render(str(score), True, WHITE)
    GAME_SCREEN.blit(score_text, (x_coordinate, y_coordinate))
    pygame.display.update()


# main game loop and logic
def main_game_loop():
    paddle_a = pygame.Rect(0, 300, PONG_PADDLE_PIXELS, PONG_PADDLE_HEIGHT)
    paddle_b = pygame.Rect(690, 300, PONG_PADDLE_PIXELS, PONG_PADDLE_HEIGHT)
    carry_on = True
    paddle_a_up = False
    paddle_a_down = False
    paddle_b_up = False
    paddle_b_down = False
    player_a_score = 0
    player_b_score = 0

    # calling the start screen function declared above
    start_screen()

    while carry_on:
        # event handling
        # by using booleans here we can keep the paddles moving while the key is held down
        # W and S for paddle A
        # Up and Down for paddle B
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_a_up = True
                elif event.key == pygame.K_s:
                    paddle_a_down = True
                elif event.key == pygame.K_UP:
                    paddle_b_up = True
                elif event.key == pygame.K_DOWN:
                    paddle_b_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    paddle_a_up = False
                elif event.key == pygame.K_s:
                    paddle_a_down = False
                elif event.key == pygame.K_UP:
                    paddle_b_up = False
                elif event.key == pygame.K_DOWN:
                    paddle_b_down = False

        # moving the paddle up and down
        # additional conditionals for boundary checking
        # if the paddles y coordinate equals the edge of the screen y coord then the paddle will move no further
        if paddle_a_up and paddle_a.y != 0:
            paddle_a.y -= PONG_PADDLE_PIXELS
        if paddle_a_down and paddle_a.y != 400:
            paddle_a.y += PONG_PADDLE_PIXELS
        if paddle_b_up and paddle_b.y != 0:
            paddle_b.y -= PONG_PADDLE_PIXELS
        if paddle_b_down and paddle_b.y != 400:
            paddle_b.y += PONG_PADDLE_PIXELS

        # storing paddle a and b's y coordinates
        # x coordinates not needed as they're always the same since the paddles do not move left and right
        # this will be used to check ball collision
        paddle_a_coordinates = create_a_list(paddle_a.y, (paddle_a.y + 101))
        paddle_b_coordinates = create_a_list(paddle_b.y, (paddle_b.y + 101))

        # updating sprite list
        sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 690:
            # checks to see if the ball is colliding with the paddle
            if any(x == ball.rect.y for x in paddle_b_coordinates):
                ball.bounce()
                continue
            # checks to see if the ball is colliding with the paddle
            if any(x != ball.rect.y for x in paddle_b_coordinates):
                ball.velocity[0] = -ball.velocity[0]
                player_a_score += 1
        if ball.rect.x <= 0:
            # checks to see if the ball is colliding with the paddle
            if any(x == ball.rect.y for x in paddle_a_coordinates):
                ball.bounce()
                continue
            # checks to see if the ball is colliding with the paddle
            if any(x != ball.rect.y for x in paddle_a_coordinates):
                ball.velocity[0] = -ball.velocity[0]
                player_b_score += 1
        # checks to see if the ball is hitting the top of the screen
        # if it is then make it bounce off the boundary
        if ball.rect.y > 490:
            ball.velocity[1] = -ball.velocity[1]
        # checks to see if the ball is hitting the top of the screen
        # if it is then make it bounce off the boundary
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        # checking which player has won
        if player_a_score == 10:
            winner_screen("Player A")
        if player_b_score == 10:
            winner_screen("Player B")

        # delete the two paddle coordinate lists to start a fresh list on the next pass
        del paddle_b_coordinates, paddle_a_coordinates

        # paint game screen black
        GAME_SCREEN.fill(BLACK)

        # draw the net
        pygame.draw.line(GAME_SCREEN, WHITE, [350, 0], [350, 600])

        # draw paddle a
        pygame.draw.rect(GAME_SCREEN, WHITE, paddle_a)

        # draw paddle b
        pygame.draw.rect(GAME_SCREEN, WHITE, paddle_b)

        # draw score to screen
        scoring(player_a_score, (SCREEN_WIDTH / 4), 10)
        scoring(player_b_score, (SCREEN_WIDTH / 4) * 3, 10)

        # draw ball
        sprites_list.draw(GAME_SCREEN)

        # update the display
        pygame.display.update()

        # 60 frames per second
        CLOCK.tick(60)


# calling the main game loop
main_game_loop()
