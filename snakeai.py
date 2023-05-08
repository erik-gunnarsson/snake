import random
from gamestate import GameState

UP = (0,1)
DOWN = (0,-1)
RIGHT = (1,0)
LEFT = (-1,0)

class SnakeAI:
    def get_next_move(self, state: GameState) -> tuple:
        head = state.get_snake_head()
        apple_direction = self.direction_to_apple(head, state.apple)
        safe_options = self.filter_options(state)
        
        if random.random() < 0 and safe_options: # 50% chance of choosing a random safe direction
            return random.choice(safe_options)

        ai_decision = self.choose_best_direction(state.snake_direction, apple_direction, safe_options)
        return ai_decision

    def direction_to_apple(self, head: tuple, apple: tuple) -> tuple:
        x_direction = apple[0] - head[0]
        y_direction = apple[1] - head[1]

        if x_direction > 0:
            x_direction = 1
        elif x_direction < 0:
            x_direction = -1

        if y_direction > 0:
            y_direction = 1
        elif y_direction < 0:
            y_direction = -1

        return (x_direction, y_direction)

    def choose_best_direction(self, current_direction: tuple, apple_direction: tuple, safe_options: list) -> tuple:
        options = [DOWN, UP, RIGHT, LEFT]

        # Remove the opposite direction of the current direction from options
        opposite_direction = (-current_direction[0], -current_direction[1])
        options.remove(opposite_direction)

        for direction in options:
            if direction == apple_direction and direction in safe_options:
                return direction

        # Prioritize the direction with the same X or Y component as the apple direction
        for direction in options:
            if direction[0] == apple_direction[0] or direction[1] == apple_direction[1]:
                if direction in safe_options:
                    return direction

        # If no suitable direction is found, continue in the current direction if it's safe
        if current_direction in safe_options:
            return current_direction
        # If no safe options are available, return a random direction (inevitable death)
        return random.choice([DOWN, UP, RIGHT, LEFT])

    def filter_options(self, state: GameState) -> list:
        options = [DOWN, UP, RIGHT, LEFT]
        safe_options = []

        for direction in options:
            simulated_state = simulate_move(state, direction)
            if not simulated_state.is_game_over():
                safe_options.append(direction)

        return safe_options
    

# This function creates a copy the current state, given a state and a direction you wish to test
# In this new copy, the snake will have moved one step in that direction
# You don't need to understand the code inside the function to be able to use it.
def simulate_move(state: GameState, direction: tuple) -> GameState:
    head = state.get_snake_head()
    new_pos_of_head = (head[0] + direction[0], head[1] + direction[1])

    # Create a copy of the current state that we can then modify and play with
    new_simulated_state = GameState()
    new_simulated_state.apple = state.apple
    new_simulated_state.snake = [*state.snake, new_pos_of_head]
    new_simulated_state.board_size_x = state.board_size_x
    new_simulated_state.board_size_y = state.board_size_y
    new_simulated_state.map = state.map

    # This extends the snake
    new_simulated_state.snake_direction = direction
    # Check if the new position of the head is on the same spot as the apple
    # Once the snakes moves, the tail is removed, unless it eats an apple
    is_eating_apple = new_pos_of_head == state.apple
    if not is_eating_apple:
        new_simulated_state.snake.pop(0) # deletes the first element of the list
    return new_simulated_state
