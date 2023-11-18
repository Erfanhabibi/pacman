import numpy as np
import itertools
import copy
import random
from collections import deque
import tkinter as tk
from PIL import Image, ImageTk


class Game:
    VALID_DIRECTIONS = ['u', 'd', 'l', 'r']
    NUMBER_OF_GHOSTS = 2
    PACMAN = 'P'
    EMPTY = ' '
    FOOD = '.'
    WALL = '#'
    GHOST_ON_FOOD = 'GF'
    GHOST = 'G'

    def __init__(self, field):
        self.field = field
        self.score = 0
        self.won = None
        self.pacman_position = None
        self.ghost_positions = []
        self._initialize_positions()

    def _initialize_positions(self):
        position_indicators = {
            self.PACMAN: self._set_pacman_position,
            self.GHOST: self._add_ghost_position,
            self.GHOST_ON_FOOD: self._add_ghost_position,
        }

        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                indicator = self.field[i, j]
                position_handler = position_indicators.get(indicator)
                if position_handler:
                    position_handler((i, j))

    def _set_pacman_position(self, position):
        self.pacman_position = position

    def _add_ghost_position(self, position):
        self.ghost_positions.append(position)


def initialize_game():
    field = np.array([
        [Game.GHOST_ON_FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD,
            Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.GHOST_ON_FOOD],
        [Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.WALL,
            Game.WALL, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD,
            Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD,
            Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD,
            Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD],
        [Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.WALL,
            Game.WALL, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD,
            Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.WALL,
            Game.WALL, Game.WALL, Game.WALL, Game.FOOD, Game.WALL, Game.FOOD, Game.WALL, Game.WALL, Game.FOOD],
        [Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD,
            Game.PACMAN, Game.FOOD, Game.FOOD, Game.FOOD, Game.WALL, Game.FOOD, Game.FOOD, Game.FOOD, Game.FOOD]
    ])

    return Game(field)


def get_permutations(lst, n):
    return [p for p in itertools.product(lst, repeat=n)]



def print_ground(game, canvas):
    element_to_color = {
        Game.EMPTY: 'white',
        Game.PACMAN: 'yellow',
        Game.GHOST: 'red',
        Game.GHOST_ON_FOOD: 'red',
        Game.FOOD: 'green',
        Game.WALL: 'black',
    }

    rows, cols = game.field.shape
    cell_size = 40

    for i in range(rows):
        for j in range(cols):
            element = game.field[i, j]
            color = element_to_color.get(element, 'white')
            canvas.create_rectangle(
                j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)

    canvas.create_text(cols * cell_size // 2, rows * cell_size +
                       20, text=f'Score: {game.score}', font=('Helvetica', 14))


def check_win_or_lost(game):
    flat_ground = game.field.flatten()

    food_and_ghosts = np.isin(flat_ground, [Game.FOOD, Game.GHOST_ON_FOOD])
    ghost_count = np.count_nonzero(
        np.isin(flat_ground, [Game.GHOST, Game.GHOST_ON_FOOD]))

    if np.sum(food_and_ghosts) == 0:
        game.won = True
    elif ghost_count != Game.NUMBER_OF_GHOSTS or np.sum(flat_ground == Game.PACMAN) != 1:
        game.won = False


def move_pacman(game, direction):
    pacman_position = game.pacman_position

    if pacman_position is None:
        return False

    new_position = get_new_position(pacman_position, direction)

    if is_valid_position(game, new_position):
        if game.field[new_position] == Game.FOOD:
            game.score += 10

        game.score -= 1 
        game.field[new_position] = Game.PACMAN
        game.field[pacman_position] = Game.EMPTY
        game.pacman_position = new_position

        return True

    return False



def move_ghosts(game, directions):
    for index, ghost_position in enumerate(game.ghost_positions):
        new_position = get_new_position(ghost_position, directions[index])

        if is_valid_position(game, new_position):
            if game.field[new_position] not in [Game.GHOST, Game.GHOST_ON_FOOD]:
                if game.field[ghost_position] == Game.GHOST_ON_FOOD:
                    game.field[ghost_position] = Game.FOOD
                else:
                    game.field[ghost_position] = Game.EMPTY

                if game.field[new_position] == Game.FOOD:
                    game.field[new_position] = Game.GHOST_ON_FOOD
                else:
                    game.field[new_position] = Game.GHOST

                game.ghost_positions.remove(ghost_position)
                game.ghost_positions.append(new_position)


def get_new_position(position, direction):
    x, y = position
    if direction == 'u':
        return x - 1, y
    elif direction == 'd':
        return x + 1, y
    elif direction == 'l':
        return x, y - 1
    elif direction == 'r':
        return x, y + 1
    else:
        return position


def is_valid_position(game, position):
    x, y = position
    return 0 <= x < len(game.field) and 0 <= y < len(game.field[0]) and game.field[x, y] != Game.WALL


def move(game, direction, is_pacman_turn):
    if is_pacman_turn:
        move_pacman(game, direction)
    else:
        move_ghosts(game, direction)
    check_win_or_lost(game)
    return game


def len_shortest_path_to_food(game):
    x, y = game.pacman_position
    field = game.field
    queue = deque([(x, y, 0)])
    visited = set()

    while queue:
        x, y, distance = queue.popleft()

        if field[x, y] == Game.FOOD:
            return distance

        if (x, y) not in visited:
            visited.add((x, y))

            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                new_x, new_y = x + dx, y + dy
                if is_valid_position(game, (new_x, new_y)):
                    queue.append((new_x, new_y, distance + 1))

    return len(game.field) * len(game.field[0])


def neighbors_have_food(game, x, y):
    field = game.field
    valid_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for new_x, new_y in valid_positions:
        if is_valid_position(game, (new_x, new_y)) and field[new_x, new_y] == Game.FOOD:
            return True

    return False


def count_single_foods(game):
    field = game.field
    count = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i, j] == Game.FOOD and not neighbors_have_food(game, i, j):
                count += 1
    return count


def evaluate_game(game):
    if game.won:
        return float('inf')
    elif game.won is not None:
        return float('-inf')

    score = game.score
    shortest_path_length = len_shortest_path_to_food(game)
    single_foods_penalty = 5 * count_single_foods(game)

    return score - shortest_path_length - single_foods_penalty


def minimax(game, depth, alpha, beta, is_pacman_turn, last_best_move=None):
    if depth == 0 or game.won is not None:
        return evaluate_game(game), last_best_move

    if is_pacman_turn:
        maxEval = float('-inf')
        best_moves = []

        for direction in Game.VALID_DIRECTIONS:
            new_game = move(copy.deepcopy(game),
                            direction, is_pacman_turn=True)

            if new_game is not None:
                eval, _ = minimax(new_game, depth - 1, alpha, beta,
                                  is_pacman_turn=False, last_best_move=last_best_move)

                if eval > maxEval:
                    maxEval = eval
                    best_moves = [direction]
                elif eval == maxEval:
                    best_moves.append(direction)

                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

        return maxEval, random.choice(best_moves) if best_moves else None
    else:
        minEval = float('inf')

        for directions in get_permutations(Game.VALID_DIRECTIONS, Game.NUMBER_OF_GHOSTS):
            new_game = move(copy.deepcopy(game), directions,
                            is_pacman_turn=False)

            if new_game is not None:
                eval, _ = minimax(new_game, depth - 1, alpha, beta,
                                  is_pacman_turn=True, last_best_move=last_best_move)

                if eval < minEval:
                    minEval = eval

                beta = min(beta, eval)

                if beta <= alpha:
                    break

        return minEval, None


def play():
    game = initialize_game()

    root = tk.Tk()
    root.title("Pacman Game")

    canvas = tk.Canvas(root, width=len(
        game.field[0]) * 40, height=len(game.field) * 40, bg='white')
    canvas.pack()

    score_label = tk.Label(
        root, text=f"Score: {game.score}", font=('Helvetica', 14))
    score_label.pack()

    while game.won is None:
        print_ground(game, canvas)
        _, direction = minimax(game, 3, float(
            '-inf'), float('inf'), is_pacman_turn=True)
        move(game, direction, is_pacman_turn=True)

        ghost_directions = [random.choice(
            Game.VALID_DIRECTIONS) for _ in range(Game.NUMBER_OF_GHOSTS)]
        move(game, ghost_directions, is_pacman_turn=False)


        score_label.config(text=f"Score: {game.score}") 

        root.update()
        root.after(1)  # Pause for 10 milliseconds
        check_win_or_lost(game)

    result_label = tk.Label(
        root, text="You won!" if game.won else "You lost!", font=('Helvetica', 16))
    result_label.pack()

    root.mainloop()


play()
