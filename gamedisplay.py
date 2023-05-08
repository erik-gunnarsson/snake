import pygame
from gamestate import GameState

# This class draws the actual graphics of the game
# Without much understanding of the actual mechanics

# Colors (Red, Green, Blue)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
RUST = pygame.Color(195, 98, 65)

class GameDisplay:
    def __init__(self, game_resolution_x: int,  game_resolution_y: int) -> None:
        # game resolution
        self.game_resolution_x = game_resolution_x
        self.game_resolution_y = game_resolution_y

        # Initialise game window
        self.game_window = pygame.display.set_mode((self.game_resolution_x, self.game_resolution_y))
        pygame.display.set_caption('Snake for Business')

    def draw(self, state: GameState) -> None:
        if state.is_game_over():
            self.draw_game_over()
        else:
            self.game_window.fill(BLACK)
            self._draw_obstacles(state)
            self._draw_snake(state)
            self._draw_apple(state)
            self._draw_score(state)
        pygame.display.update()

    def draw_game_over(self) -> None:
        my_font = pygame.font.SysFont('ARIAL', 90)
        game_over_surface = my_font.render('YOU DIED', True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.game_resolution_x/2, self.game_resolution_y/4)
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

    def _draw_snake(self, state: GameState) -> None:
        for pos in state.snake[:-1]:
            self.draw_square(state, GREEN, pos) # The snake is green except for the head
        # Draw the snakes head in red, so to see where it's going
        self.draw_square(state, RED, state.get_snake_head())

    def _draw_apple(self, state: GameState) -> None:
        self.draw_square(state, WHITE, state.apple) # Draw a white dot, which is food

    def _draw_obstacles(self, state: GameState) -> None:
        for y, row in enumerate(state.map):
            for x, column in enumerate(row):
                if column:
                    self.draw_square(state, RUST, (x, y)) # Draw a white dot, which is food

    def _draw_score(self, state: GameState) -> None:
        score_font = pygame.font.SysFont('ARIAL', 20)
        score_surface = score_font.render('Score : ' + str(len(state.snake)), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.game_resolution_x/10, 15)    
        self.game_window.blit(score_surface, score_rect)

    def draw_square(self, state: GameState, color, coordinate: tuple):
        # Convert the board size to actual game solution
        width = self.game_resolution_x / state.board_size_x
        height = self.game_resolution_y / state.board_size_y 
        new_x = coordinate[0] * width
        new_y =  (state.board_size_y - coordinate[1] - 1) * height # Flips the y axis so starting is lower left corner instead of top left
        pygame.draw.rect(self.game_window, color, pygame.Rect(new_x, new_y, width, height))
        