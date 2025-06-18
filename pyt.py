import pygame
import sys
import random

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Random AI")

# 顏色
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

class Grid:
    def __init__(self):
        self.grid_lines = [
            ((0, 200), (600, 200)), ((0, 400), (600, 400)),
            ((200, 0), (200, 600)), ((400, 0), (400, 600))
        ]
        self.grid = [[-1 for _ in range(3)] for _ in range(3)]  # -1 = 空格，1=叉叉，0=圈圈
        self.game_over = False
        self.winner = None

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def set_move(self, x, y, player):
        if self.grid[y][x] == -1:
            self.grid[y][x] = player
            self.check_winner(player)
            return True
        return False

    def check_winner(self, player):
        # 檢查列、欄、斜線
        for i in range(3):
            if all(self.grid[i][j] == player for j in range(3)) or \
               all(self.grid[j][i] == player for j in range(3)):
                self.game_over = True
                self.winner = player
                return

        if all(self.grid[i][i] == player for i in range(3)) or \
           all(self.grid[i][2 - i] == player for i in range(3)):
            self.game_over = True
            self.winner = player
            return

        if self.is_full():
            self.game_over = True
            self.winner = None

    def is_full(self):
        for row in self.grid:
            if -1 in row:
                return False
        return True

    def clear(self):
        self.grid = [[-1 for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.winner = None

    def draw(self, surface):
        surface.fill(WHITE)
        for line in self.grid_lines:
            pygame.draw.line(surface, GRAY, line[0], line[1], 2)

        for y in range(3):
            for x in range(3):
                val = self.grid[y][x]
                if val == 1:  # 叉叉
                    pygame.draw.line(surface, BLACK, (x * 200 + 30, y * 200 + 30), (x * 200 + 170, y * 200 + 170), 10)
                    pygame.draw.line(surface, BLACK, (x * 200 + 170, y * 200 + 30), (x * 200 + 30, y * 200 + 170), 10)
                elif val == 0:  # 圈圈
                    pygame.draw.circle(surface, BLACK, (x * 200 + 100, y * 200 + 100), 70, 10)

# 隨機 AI 選擇空格
def random_move(grid):
    empty_cells = [(x, y) for y in range(3) for x in range(3) if grid.grid[y][x] == -1]
    return random.choice(empty_cells) if empty_cells else None

def main():
    grid = Grid()
    running = True
    player_turn = True

    while running:
        grid.draw(screen)
        pygame.display.flip()

        if not grid.game_over and not player_turn:
            pygame.time.wait(500)
            move = random_move(grid)
            if move:
                grid.set_move(move[0], move[1], 0)  # AI = 0 = 圈圈
                player_turn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not grid.game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x = mx // 200
                y = my // 200
                if grid.set_move(x, y, 1):  # Player = 1 = 叉叉
                    player_turn = False

            if grid.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                grid.clear()
                player_turn = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
