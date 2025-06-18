import pygame
import sys
import math

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Player vs AI")

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
        self.search_dirs = [ (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1) ]
        self.game_over = False
        self.winner = None

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def is_within_bounds(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def set_move(self, x, y, player):
        if self.grid[y][x] == -1:
            self.grid[y][x] = player
            self.check_winner(x, y, player)
            return True
        return False

    def check_winner(self, x, y, player):
        # 檢查8個方向是否有連3
        for i in range(4):  # 只需檢查四個方向及其相反方向即可 (避免重複)
            dx, dy = self.search_dirs[i]
            count = 1

            # 向一邊檢查
            cx, cy = x + dx, y + dy
            while self.is_within_bounds(cx, cy) and self.grid[cy][cx] == player:
                count += 1
                cx += dx
                cy += dy

            # 向相反方向檢查
            dx, dy = -dx, -dy
            cx, cy = x + dx, y + dy
            while self.is_within_bounds(cx, cy) and self.grid[cy][cx] == player:
                count += 1
                cx += dx
                cy += dy

            if count >= 3:
                self.game_over = True
                self.winner = player
                return

        # 若格子滿了且無人贏，判和
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
        # 畫格線
        for line in self.grid_lines:
            pygame.draw.line(surface, GRAY, line[0], line[1], 2)

        # 畫叉叉和圈圈
        for y in range(3):
            for x in range(3):
                val = self.grid[y][x]
                if val == 1:  # 叉叉
                    pygame.draw.line(surface, BLACK, (x * 200 + 30, y * 200 + 30), (x * 200 + 170, y * 200 + 170), 10)
                    pygame.draw.line(surface, BLACK, (x * 200 + 170, y * 200 + 30), (x * 200 + 30, y * 200 + 170), 10)
                elif val == 0:  # 圈圈
                    pygame.draw.circle(surface, BLACK, (x * 200 + 100, y * 200 + 100), 70, 10)

# Minimax 演算法
def minimax(grid, depth, is_maximizing):
    if grid.winner == 0:  # AI圈圈贏
        return 1
    elif grid.winner == 1:  # 玩家叉叉贏
        return -1
    elif grid.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for y in range(3):
            for x in range(3):
                if grid.grid[y][x] == -1:
                    grid.grid[y][x] = 0
                    grid.check_winner(x, y, 0)
                    score = minimax(grid, depth + 1, False)
                    grid.grid[y][x] = -1
                    grid.game_over = False
                    grid.winner = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for y in range(3):
            for x in range(3):
                if grid.grid[y][x] == -1:
                    grid.grid[y][x] = 1
                    grid.check_winner(x, y, 1)
                    score = minimax(grid, depth + 1, True)
                    grid.grid[y][x] = -1
                    grid.game_over = False
                    grid.winner = None
                    best_score = min(score, best_score)
        return best_score

def best_move(grid):
    best_score = -math.inf
    move = None
    for y in range(3):
        for x in range(3):
            if grid.grid[y][x] == -1:
                grid.grid[y][x] = 0
                grid.check_winner(x, y, 0)
                score = minimax(grid, 0, False)
                grid.grid[y][x] = -1
                grid.game_over = False
                grid.winner = None
                if score > best_score:
                    best_score = score
                    move = (x, y)
    return move

def main():
    grid = Grid()
    running = True
    player_turn = True

    while running:
        grid.draw(screen)
        pygame.display.flip()

        if not grid.game_over and not player_turn:
            pygame.time.wait(500)
            move = best_move(grid)
            if move:
                grid.set_move(move[0], move[1], 0)  # AI用0 (圈圈)
                player_turn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not grid.game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x = mx // 200
                y = my // 200
                if grid.set_move(x, y, 1):  # 玩家用1 (叉叉)
                    player_turn = False

            if grid.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                grid.clear()
                player_turn = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
