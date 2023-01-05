import pygame
import random
import time
from enum import Enum

# TODO:
# 1) show dice score
# 2) show current player
# 3) add clickable button to roll and text instructions
# 4) animate player movement
# 5) implement player ladder interaction
# 6) implement player snake interaction
# 7) show winner and end game

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (160, 82, 45)
purple = (128, 0, 128)
orange = (255, 160, 122)
screen_height = 510  # height and width is 510 as using 40 pixel squares and 10 pixel gaps we can have a 10 by 10 grid meaning 100 squares
screen_width = 710
space_height = 40  # height and width is 510 as using 40 pixel squares and 10 pixel gaps we can have a 10 by 10 grid meaning 100 squares
space_width = 40
all_spaces = []
player_colours = [red, blue, purple, orange]
player_colour_names = ["red", "blue", "purple", "orange"]

spaces_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    [40, 39, 38, 37, 36, 35, 34, 33, 32, 31],
    [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    [60, 59, 58, 57, 56, 55, 54, 53, 52, 51],
    [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
    [80, 79, 78, 77, 76, 75, 74, 73, 72, 71],
    [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
    [100, 99, 98, 97, 96, 95, 94, 93, 92, 91]
]
snake_ladder_positions = [
    [[3, 21], [15, 30], [34, 84], [41, 62], [74, 93], [80, 98], [69, 91], [23, 56], [68, 49], [27, 9], [64, 99],
     [43, 5]],
    [[3, 21], [15, 30], [34, 84], [41, 62], [74, 93], [80, 98], [69, 91], [23, 56], [68, 49], [27, 9], [64, 99],
     [43, 5]]
]


def cell_top(row, space_height, space_gap):
    return space_gap + ((10 - row - 1) * space_height + (10 - row - 1) * space_gap)


def cell_left(column, space_width, space_gap):
    return space_gap + (column * space_width + column * space_gap)


def play_game():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    grid_positions = create_grid_positions()
    snakes_and_ladders = create_snakes_and_ladders()
    player_positions = [1, 1]
    current_player = 0
    while True:
        for event in pygame.event.get():
            draw_grid(screen, grid_positions, snakes_and_ladders, player_positions)
            pygame.draw.rect(screen, white, pygame.Rect(520, 10, 180, 490))
            font = pygame.font.Font("seguisym.ttf", 20)
            text_image = font.render(str("its " + player_colour_names[current_player] + "'s turn"), True, player_colours[current_player])
            text_rect = text_image.get_rect(center=(610, 255))
            screen.blit(text_image, text_rect)
            button = pygame.draw.rect(screen, player_colours[current_player], pygame.Rect(560, 295, 100, 40))
            button_text = font.render(str("roll"), True, black)
            screen.blit(button_text, button_text.get_rect(center=button.center))
            if event.type == pygame.MOUSEBUTTONDOWN:
                dice_roll = random.randint(1, 6)
                player_positions[current_player] += dice_roll
                if player_positions[current_player] > 100:
                    player_positions[current_player] = 100
                current_player += 1
                if current_player >= len(player_positions):
                    current_player = 0
            if event.type == pygame.QUIT:
                return
            pygame.display.update()


class GridPosition:
    def __init__(self, left, top, row, column):
        self.top = top
        self.left = left
        self.row = row
        self.column = column
        self.middle = (left + (space_width / 2), top + (space_height / 2))


def create_grid_positions():
    grid_positions = {}
    for row in reversed(range(10)):
        for column in range(10):
            grid_positions[spaces_grid[row][column]] = GridPosition(cell_left(column, 40, 10), cell_top(row, 40, 10),
                                                                    row, column)
    return grid_positions


def draw_grid(screen, grid_positions, snakes_or_ladders, player_positions):
    screen.fill(black)
    font = pygame.font.Font("seguisym.ttf", 20)
    for key, position in grid_positions.items():
        space = pygame.Rect(position.left, position.top, space_width, space_height)
        text_image = font.render(str(key), True, (10, 10, 10))
        text_rect = text_image.get_rect(center=space.center)
        pygame.draw.rect(screen, white, space)
        screen.blit(text_image, text_rect)
    for snake_or_ladder in snakes_or_ladders:
        pygame.draw.line(screen,
                         brown if snake_or_ladder.type == Type.LADDER else green,
                         grid_positions[snake_or_ladder.bottom].middle,
                         grid_positions[snake_or_ladder.top].middle,
                         10)
    for key, player_position in enumerate(player_positions):
        pygame.draw.circle(screen,
                           player_colours[key],
                           (grid_positions[player_position].left + space_width / 2 - key * 2,
                            grid_positions[player_position].top + space_height / 2 - key * 2),
                           10)


class Type(Enum):
    LADDER = 1
    SNAKE = 2


class LadderOrSnake:
    def __init__(self, indexes, type):
        sorted_indexes = indexes
        self.bottom = sorted_indexes[0]
        self.top = sorted_indexes[1]
        self.type = type


def create_snakes_and_ladders():
    snakes_and_ladders = []
    choice = random.choice(snake_ladder_positions)
    random.shuffle(choice)
    for index, position in enumerate(choice):
        snakes_and_ladders.append(LadderOrSnake(position, Type.LADDER if index % 2 == 0 else Type.SNAKE))
    return snakes_and_ladders


play_game()
