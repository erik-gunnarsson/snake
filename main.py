# Snake for business
# Author Joel Smedberg
# joel.smedberg@hhs.se



# game_speed difficulty settings
# Easy               ->  7
# Medium             ->  15
# Hard               ->  50
# Mission impossible ->  120
GAME_SPEED = 7

# Change here to switch between A.I and human
# Set this to True to let the AI function play the game
USE_AI = True

# ALL CODE BELOW THIS POINT IS ONLY TO MAKE THE GAME RUN AND DOESN'T NEED TO BE UNDERSTOOD TO WRITE THE AI
# ------------
print("Starting snake for business")
import time, copy, random, json
import pygame
import gamedisplay
from gamestate import GameState
from snakeai import SnakeAI


map_matrix:list[list[int]] = json.load(open("map.json", "r"))

# These are the dimensions of the game board
BOARD_SIZE_X = len(map_matrix[0])
BOARD_SIZE_Y = len(map_matrix)
STARTING_POS_Y = int(BOARD_SIZE_Y / 2)

# These are the directions which a snake can go. 
# Each tuple can be added to the heads position before 
# and you'll get the position of the head in the next instance
# this is duplicated in the AI module to make avoid dependencies
UP = (0,1)
DOWN = (0,-1)
RIGHT = (1,0)
LEFT = (-1,0)


# This gives a random position somewhere on the board given the board x and y size
def random_board_position(board_size_x, board_size_y) -> tuple:
        random_x_position = random.randint(1, board_size_x - 2)
        random_y_position = random.randint(1, board_size_y - 2)
        return (random_x_position, random_y_position)

# This picks a random position on the board that is not within the snake
# used to decide where to put a random apple
def generate_new_apple(state: GameState) -> tuple:
        state.apple = random_board_position(state.board_size_x, state.board_size_y)
        # If that place happens to on the actual snake
        # then run the function again until it lands on a spot not occupied
        while state.apple in state.snake or state.map[state.apple[1]][state.apple[0]] == 1: 
            # Randomly select a position on the map and place an apple there
            state.apple = random_board_position(state.board_size_x, state.board_size_y)

# Sets up the starting position for the game, where the snake starts in the middel to left
state = GameState()
state.board_size_x = BOARD_SIZE_X
state.map = map_matrix
state.board_size_y = BOARD_SIZE_Y
state.snake_direction = RIGHT
state.snake = [(3, STARTING_POS_Y ), (4, STARTING_POS_Y ), (5, STARTING_POS_Y )]
generate_new_apple(state)


# This determins the resolution of the game
# Pixels per game tile 
RESOLUTION_MULTIPLIER = 10


# this creates a new game display,
# this handles anything that is graphical
display = gamedisplay.GameDisplay( 
    game_resolution_x= BOARD_SIZE_X * RESOLUTION_MULTIPLIER,
    game_resolution_y= BOARD_SIZE_Y * RESOLUTION_MULTIPLIER
)

# PyGame the framework that does most of the heavy lifting for us
pygame.init()
# Initiates the A.I
ai = SnakeAI()

# FPS (frames per second) controller
game_speed_control = pygame.time.Clock()

# This capures a keystroke by a human player
def get_human_next_move():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return UP
            if event.key == pygame.K_DOWN:
                return DOWN
            if event.key == pygame.K_LEFT:
                return LEFT
            if event.key == pygame.K_RIGHT:
                return RIGHT


# Calculates the determinant of a matrix. The determinant is non 0 if the snake has made a turn
def determinant(a: tuple, b: tuple):
    return (a[0] * b[1] - b[0] * a[1])

# Checks if the snake wishes to turn compared to the last direction
# If the snake does not wish to turn or make a 180 turn, the determinant will be 0
# and no update will be required since 180 turns are not allowed
def has_turned(next_move: tuple, direction: tuple) -> bool:
    if next_move is None:
        return False
    return determinant(next_move, direction) != 0

# Move the snake 1 step in the travel direction
# Adds a new apple if the head is on the old one
# Extends the snake 1 step if the apple is eaten
def move_snake(state:GameState):
    head = state.get_snake_head()
    new_head_position = (head[0] + state.snake_direction[0], head[1] + state.snake_direction[1])
    state.snake.append(new_head_position)
    # Check if the new position of the head is on the same spot as the apple
    is_eating_apple = new_head_position == state.apple
    if is_eating_apple:
        generate_new_apple(state)
    else:
        state.snake.pop(0)  # Remove the first element of a list
display.draw(state)
while not state.is_game_over():
    next_move = get_human_next_move()
    if USE_AI: 
        # make a copy of the state so that it's not modified in the ai function
        next_move = ai.get_next_move(copy.deepcopy(state))
    if has_turned(next_move, state.snake_direction):
        state.snake_direction = next_move
    move_snake(state)
    # update the visible part of the game
    display.draw(state)
    # make sure the game pauses for a long enough time between each step
    game_speed_control.tick(GAME_SPEED)

# Sleep for 4 seconds before exiting the game
time.sleep(4)
# Make sure everything shuts down in an orderily fashion
pygame.display.quit()
pygame.quit()
time.sleep(1)
exit()