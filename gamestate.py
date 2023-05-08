class GameState:
    # The apple is stored as a tuple with to coordinates representing x and y 
    # Example (40, 50)
    apple: tuple

    # the snake is stored a list of tuples,
    # Each tuple represents a position on 
    # the game board that the snake occupies
    # The first position of the list is the snakes tail
    # the last position of the list of the snakes head
    # Example [ (10,11), (10, 12), (10, 13), (11,13) ]
    snake: list[tuple]
    map: list[list[int]]
    # The direction is a tuple representing x and y,
    # The direction is -1, 0 or 1 in the two dimension
    # Example (1, 0) represents "RIGHT", going 1 step in x direction and 0 steps in y
    snake_direction: tuple
    
    board_size_x: int # The size of the board in tiles in the x direction
    board_size_y: int # The size of the board in tiles in the y direction

    # A help function that find the head and return a tuple representing the head 
    def get_snake_head(self) -> tuple:
        return self.snake[-1] # Returns the coordinate at the last position of the list, which is the head
    
    # A help function that checks if the head is on the same position as any other part of the snake
    def is_snake_crossing_itself(self) -> bool:
        return self.get_snake_head() in self.snake[:-1]

    # returns true if the coordinate is an obstacle, false otherwise
    def coordinate_is_wall(self, coordinate: tuple) -> bool:
        return self.map[coordinate[1]][coordinate[0]] == 1
    
    # returns if true if the game is over (you have died), false otherwise
    # The gamne is over if the snake has run into a wall or into itself
    def is_game_over(self) -> bool:    
        return self.coordinate_is_wall(self.get_snake_head()) or self.is_snake_crossing_itself()

