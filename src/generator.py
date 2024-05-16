import random
import numpy as np
import pygame

from .game import ReverseGame

# Kích thước tối thiểu và tối đa của mê cung và số lượng hộp
MIN_W = 6
MIN_H = 6
MAX_W = 15
MAX_H = 10
MIN_BOXES = 4
MAX_BOXES = 10

def num_boxes(puzzle_area):
    """Tính số lượng hộp dựa trên diện tích của mê cung"""
    # Tính hệ số và sai số để tính toán số lượng hộp dựa trên diện tích của mê cung
    m = (MAX_BOXES - MIN_BOXES) / (MAX_W * MAX_H - MIN_W * MIN_H)
    b = MIN_BOXES - m * MIN_W * MIN_H
    # Áp dụng phương trình tuyến tính để tính số lượng hộp
    return int(m * puzzle_area + b)

def random_valid(width=10, height=10):
    """Tạo một vị trí ngẫu nhiên hợp lệ trong mê cung"""
    return random.randrange(1, width - 1), random.randrange(1, height - 1)

def visualize(reverse_game, puzzle_size):
    """Hiển thị trạng thái của trò chơi"""
    pygame.event.pump()
    reverse_game.player.update(puzzle_size)
    reverse_game.floor_group.draw(reverse_game.window)
    reverse_game.goal_group.draw(reverse_game.window)
    reverse_game.object_group.draw(reverse_game.window)
    pygame.display.update()
    pygame.time.delay(1)

def generate(window=None, seed=3, visualizer=False, path=None):
    """Tạo một mê cung mới"""
    path = path or 'levels/lvl0.dat'
    random.seed(seed)
    valid = False
    while not valid:
        # Tạo kích thước mê cung ngẫu nhiên
        width = random.randint(MIN_W, MAX_W)
        height = random.randint(MIN_H, MAX_H)
        puzzle = np.full((height, width), '+', dtype='<U1')
        # Tính toán số lượng hộp cần tạo
        boxes = num_boxes(width * height)
        boxes_seen = set()
        player_pos = random_valid(width, height)
        puzzle_size = height, width
        puzzle[player_pos[1], player_pos[0]] = '*'  # Đặt vị trí của người chơi
        boxes_created = 0
        while boxes_created < boxes:
            # Tạo hộp ở vị trí ngẫu nhiên
            box_pos = random_valid(height, width)
            if puzzle[box_pos] == '+':
                puzzle[box_pos] = '$'
                boxes_created += 1
                boxes_seen.add(box_pos)
        # Tạo một trò chơi mới với mê cung và vị trí người chơi đã tạo
        reverse_game = ReverseGame(window, level=0, seed=seed)
        reverse_game.load_floor()
        reverse_game.load_puzzle(puzzle)
        player = reverse_game.player
        counter = round(height * width * random.uniform(1.8, 3.6))
        # Tạo trạng thái của trò chơi nếu visualizer được kích hoạt
        while counter > 0:
            if visualizer:
                visualize(reverse_game, puzzle_size)
            else:
                reverse_game.player.update(puzzle_size)
            if player.states[player.curr_state] >= 20:
                break
            counter -= 1
        # Cắt ra phần mê cung từ trò chơi
        slice_x = slice(reverse_game.pad_x, reverse_game.pad_x + width)
        slice_y = slice(reverse_game.pad_y, reverse_game.pad_y + height)
        matrix = reverse_game.puzzle[slice_y, slice_x]
        player.print_puzzle(matrix)
        player.kill()
        # Kiểm tra xem có đủ số lượng hộp ở những vị trí không đúng hay không
        out_of_place_boxes = np.sum([str(x) == '@' for x in matrix.flatten()])
        if out_of_place_boxes >= boxes // 2:
            # Nếu có đủ hộp không đúng, lưu mê cung và kết thúc quá trình tạo
            np.savetxt(path, matrix, fmt='%s')
            valid = True
            del reverse_game
        else:
            # Nếu không đủ, tăng giá trị hạt giống và tạo lại mê cung mới
            seed += 1
            del reverse_game
            print(f'Not enough boxes out of place, generating new seed... [{out_of_place_boxes}]')

if __name__ == '__main__':
    generate()  # Tạo một mê cung mới khi chạy script này
