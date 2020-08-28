import os
import random
import pygame
import pygame.gfxdraw


# background configuration
WIDTH = 720
HEIGHT = 720
GRID_WIDTH = WIDTH // 20
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# define font name
# font_name = pygame.font.match_font('华文黑体')
FONT_NAME = pygame.font.get_default_font() 

USER, AI = 1, 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gomoku")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    base_folder = os.path.dirname(__file__)

    # load resources
    img_folder = os.path.join(base_folder, 'images')
    background_img = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()

    background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    back_rect = background.get_rect()

    movements = []
    remain = set(range(1, 19**2 + 1))

    color_metrix = [[None] * 20 for i in range(20)]

    game_over = True
    running = True
    winner = None
    while running:
        if game_over:
            show_go_screen(screen, background, back_rect, clock, winner)
            game_over = False
            movements = []
            remain = set(range(1, 19**2 + 1))

            color_metrix = [[None] * 20 for i in range(20)]

        # 设置屏幕刷新频率
        clock.tick(FPS)

        # 处理不同事件
        for event in pygame.event.get():

            # 检查是否关闭窗口
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                response = move(screen, event.pos, clock, movements, color_metrix)
                if response is not None and response[0] is False:
                    game_over = True
                    winner = response[1]
                    continue

        # Update
        all_sprites.update()

        # Draw / render
        # screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_background(screen, background, back_rect)
        draw_movements(screen, movements)

        # After drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()


# draw background lines
def draw_background(surf, background, back_rect):
    # 加载背景图片
    surf.blit(background, back_rect)
    
    # 画网格线，棋盘为 19行 19列的
    # 1. 画出边框
    rect_lines = [
        ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
        ((GRID_WIDTH, HEIGHT - GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((WIDTH - GRID_WIDTH, GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
    ]
    for line in rect_lines:
        pygame.draw.line(surf, BLACK, line[0], line[1], 2)

    for i in range(17):
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH * (2 + i), GRID_WIDTH),
                         (GRID_WIDTH * (2 + i), HEIGHT - GRID_WIDTH))
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH, GRID_WIDTH * (2 + i)),
                         (HEIGHT - GRID_WIDTH, GRID_WIDTH * (2 + i)))

    circle_center = [
        (GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 10, GRID_WIDTH * 10)
    ]
    for cc in circle_center:
        pygame.draw.circle(surf, BLACK, cc, 5)


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def move(surf, pos, clock, movements, color_metrix):
    '''
    Args:
        surf: 我们的屏幕
        pos: 用户落子的位置
    Returns a tuple or None:
        None: if move is invalid else return a
        tuple (bool, player):
            bool: True is game is not over else False
            player: winner (USER or AI)
    '''
    grid = (int(round(pos[0] / (GRID_WIDTH + .0))),
            int(round(pos[1] / (GRID_WIDTH + .0))))

    if grid[0] <= 0 or grid[0] > 19:
        return
    if grid[1] <= 0 or grid[1] > 19:
        return

    pos = (grid[0] * GRID_WIDTH, grid[1] * GRID_WIDTH)

    if color_metrix[grid[0]][grid[1]] is not None:
        return None

    curr_move = (pos, BLACK)
    add_coin(surf, BLACK, grid, clock, movements, color_metrix, USER)

    # judge is game over
    if game_is_over(grid, BLACK, color_metrix):
        return (False, USER)

    return (True, USER)  # AI turn


def add_coin(surf, color, pos, clock, movements, color_metrix, ident=USER, radius=16):
    num_pos = gridpos_2_num(pos)
    movements.append(((pos[0] * GRID_WIDTH, pos[1] * GRID_WIDTH), color))

    color_metrix[pos[0]][pos[1]] = color
    # pygame.draw.circle(surf, color, movements[-1][0], radius)
    pygame.gfxdraw.aacircle(surf, movements[-1][0][0], movements[-1][0][1], radius, color)
    pygame.gfxdraw.filled_circle(surf, movements[-1][0][0], movements[-1][0][1], radius, color)
    clock.tick(FPS)


def game_is_over(pos, color, color_metrix):
    hori = 1
    verti = 1
    slash = 1
    backslash = 1
    left = pos[0] - 1
    while left > 0 and color_metrix[left][pos[1]] == color:
        left -= 1
        hori += 1

    right = pos[0] + 1
    while right < 20 and color_metrix[right][pos[1]] == color:
        right += 1
        hori += 1

    up = pos[1] - 1
    while up > 0 and color_metrix[pos[0]][up] == color:
        up -= 1
        verti += 1

    down = pos[1] + 1
    while down < 20 and color_metrix[pos[0]][down] == color:
        down += 1
        verti += 1

    left = pos[0] - 1
    up = pos[1] - 1
    while left > 0 and up > 0 and color_metrix[left][up] == color:
        left -= 1
        up -= 1
        backslash += 1

    right = pos[0] + 1
    down = pos[1] + 1
    while right < 20 and down < 20 and color_metrix[right][down] == color:
        right += 1
        down += 1
        backslash += 1

    right = pos[0] + 1
    up = pos[1] - 1
    while right < 20 and up > 0 and color_metrix[right][up] == color:
        right += 1
        up -= 1
        slash += 1

    left = pos[0] - 1
    down = pos[1] + 1
    while left > 0 and down < 20 and color_metrix[left][down] == color:
        left -= 1
        down += 1
        slash += 1

    if max([hori, verti, backslash, slash]) >= 5:
        return True


def gridpos_2_num(grid):
    return (grid[1] - 1) * 19 + grid[0] - 1


def draw_movements(surf, movements):
    for move in movements[:-1]:
        pygame.gfxdraw.aacircle(surf, move[0][0], move[0][1], 16, move[1])
        pygame.gfxdraw.filled_circle(surf, move[0][0], move[0][1], 16, move[1])
        # pygame.draw.circle(surf, move[1], move[0], 16)
    if movements:
        pygame.gfxdraw.aacircle(surf, movements[-1][0][0], movements[-1][0][1], 16, GREEN)
        pygame.gfxdraw.filled_circle(surf, movements[-1][0][0], movements[-1][0][1], 16, GREEN)
        # pygame.draw.circle(surf, GREEN, movements[-1][0], 16)


def show_go_screen(surf, background, back_rect, clock, winner=None):
    note_height = 10
    if winner is not None:
        draw_text(surf, 'You {0} !'.format('win!' if winner == USER else 'lose!'),
                  64, WIDTH // 2, note_height, RED)
    else:
        surf.blit(background, back_rect)

    draw_text(surf, 'Gomuku', 64, WIDTH // 2, note_height + HEIGHT // 4, BLACK)
    draw_text(surf, 'Press any key to start', 22, WIDTH // 2, note_height + HEIGHT // 2,
              BLUE)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


if __name__ == "__main__":
    main()
