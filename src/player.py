import random
from collections import defaultdict

import pygame
from pygame.sprite import Sprite

from .box import Box, Obstacle


class Player(Sprite):
    """Lớp đại diện cho nhân vật người chơi trong trò chơi."""
    
    def __init__(self, *groups, x, y, game):
        """
        Khởi tạo một đối tượng người chơi.
        
        Args:
            *groups: Các nhóm mà nhân vật người chơi sẽ tham gia.
            x (int): Tọa độ x ban đầu của nhân vật.
            y (int): Tọa độ y ban đầu của nhân vật.
            game (object): Tham chiếu đến đối tượng trò chơi.
        """
        super().__init__(*groups)
        self.game = game
        # Tải hình ảnh cho các hướng di chuyển của nhân vật
        self.up = pygame.image.load('img/playerU.png')
        self.up = pygame.transform.scale(self.up, [64, 64])
        self.down = pygame.image.load('img/playerD.png')
        self.down = pygame.transform.scale(self.down, [64, 64])
        self.left = pygame.image.load('img/playerL.png')
        self.left = pygame.transform.scale(self.left, [64, 64])
        self.right = pygame.image.load('img/playerR.png')
        self.right = pygame.transform.scale(self.right, [64, 64])
        self.image = self.down  # Hình ảnh mặc định là hướng xuống
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)  # Vị trí và kích thước ban đầu của nhân vật
        self.x = x
        self.y = y

    def update(self, key=None):
        """
        Cập nhật vị trí của nhân vật dựa trên phím được nhấn.
        
        Args:
            key (str): Phím được nhấn để di chuyển nhân vật ('R', 'L', 'U', 'D').

        Returns:
            int: 1 nếu di chuyển thành công, 0 nếu không di chuyển.
        """
        move = None
        # Xác định hướng di chuyển dựa trên phím được nhấn
        if key:
            if key == 'R':
                self.image = self.right
                move = (64, 0)  # Di chuyển sang phải
            elif key == 'L':
                self.image = self.left
                move = (-64, 0)  # Di chuyển sang trái
            elif key == 'U':
                self.image = self.up
                move = (0, -64)  # Di chuyển lên trên
            elif key == 'D':
                self.image = self.down
                move = (0, 64)  # Di chuyển xuống dưới
        if move:
            curr = self.y, self.x
            target = self.y + move[1] // 64, self.x + move[0] // 64
            target_elem = self.game.puzzle[target]
            # Kiểm tra xem có thể di chuyển đến ô đích hay không
            if not (target_elem and target_elem.obj and isinstance(target_elem.obj, Obstacle)):
                is_box = isinstance(target_elem.obj, Box)
                # Nếu ô đích không có hộp hoặc có thể đẩy được hộp
                if not is_box or (is_box and target_elem.obj.can_move(move)):
                    curr_elem = self.game.puzzle[curr]
                    # Cập nhật vị trí và trạng thái của nhân vật và hộp
                    self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
                    self.y, self.x = target
                    curr_elem.char = '-' if not curr_elem.ground else 'X'
                    curr_elem.obj = None
                    target_elem.char = '*' if not target_elem.ground else '%'
                    target_elem.obj = self
                    return 1  # Trả về 1 nếu di chuyển thành công
        return 0  # Trả về 0 nếu không thực hiện di chuyển
    
    def __del__(self):
        self.kill()


class ReversePlayer(Player):
    """Lớp đại diện cho nhân vật người chơi có khả năng kéo hộp."""
    
    def __init__(self, *groups, x, y, game=None, puzzle=None):
        """
        Khởi tạo một đối tượng người chơi có khả năng kéo hộp.
        
        Args:
            *groups: Các nhóm mà nhân vật người chơi sẽ tham gia.
            x (int): Tọa độ x ban đầu của nhân vật.
            y (int): Tọa độ y ban đầu của nhân vật.
            game (object): Tham chiếu đến đối tượng trò chơi.
            puzzle (object): Tham chiếu đến ma trận của trò chơi.
        """
        super().__init__(*groups, x=x, y=y, game=game)
        self.puzzle = puzzle  # Ma trận của trò chơi
        self.curr_state = ''  # Trạng thái hiện tại của trò chơi
        self.states = defaultdict(int)  # Danh sách các trạng thái đã gặp
        self.prev_move = (0, 0)  # Biến lưu trữ bước di chuyển trước đó

    def print_puzzle(self, matrix=None):
        """
        In ma trận trò chơi ra màn hình.

        Args:
            matrix (list): Ma trận trò chơi.

        Returns:
            None
        """
        matrix = matrix if matrix is not None else self.game.puzzle
        height, width = len(matrix), len(matrix[0])
        for h in range(height):
            for w in range(width):
                if matrix[h, w]:
                    print(matrix[h, w], end=' ')
                else:
                    print('F', end=' ')
            print(' ')
        print('\n')

    def get_state(self):
        """
        Trả về trạng thái hiện tại của trò chơi dưới dạng chuỗi.

        Returns:
            str: Trạng thái hiện tại của trò chơi.
        """
        state = ''
        height, width = len(self.game.puzzle), len(self.game.puzzle[0])
        for row in range(height):
            for col in range(width):
                if self.game.puzzle[row, col]:
                    state += str(self.game.puzzle[row, col])
        return state 

    def update(self, puzzle_size):
        """
        Cập nhật vị trí của người chơi và hộp theo chiến lược ngẫu nhiên.

        Args:
            puzzle_size (tuple): Kích thước ma trận của trò chơi.

        Returns:
            None
        """
        height, width = puzzle_size
        quick_chars = {
            '*': '-',
            '%': 'X',
            '+': '*',
            '-': '*',
            'X': '%',
            '@': '-',
            '$': 'X',
        }
        moves_tuples = [(64, 0), (-64, 0), (0, -64), (0, 64)]  # Các bước di chuyển có thể
        moves = random.choices(
            moves_tuples, 
            weights=[0.1 if m == self.prev_move else 1 for m in moves_tuples],
            k=1
        )  # Chọn ngẫu nhiên một bước di chuyển
        self.curr_state = self.get_state()  # Lấy trạng thái hiện tại của trò chơi
        for move in moves:
            self.states[self.curr_state] += 1  # Đếm số lần xuất hiện của trạng thái hiện tại
            curr_pos = self.y, self.x
            target = self.y + move[0] // 64, self.x + move[1] // 64
            reverse_target = self.y - move[0] // 64, self.x - move[1] // 64
            # Kiểm tra xem có đến vị trí có thể di chuyển không
            if (target[1] == self.game.pad_x or 
                target[0] == self.game.pad_y or
                target[1] >= self.game.pad_x + width - 1 or 
                target[0] >= self.game.pad_y + height - 1 or
                (self.game.puzzle[target] and self.game.puzzle[target].char in '@$')):
                self.prev_move = move
                return
            self.prev_move = -move[0], -move[1]
            # Cập nhật vị trí và trạng thái của người chơi và hộp
            self.game.puzzle[curr_pos].char = quick_chars[self.game.puzzle[curr_pos].char]
            self.game.puzzle[curr_pos].obj = None
            self.game.puzzle[target].char = quick_chars[self.game.puzzle[target].char]
            if self.game.puzzle[target].obj:
                self.game.puzzle[target].obj.kill()
            self.game.puzzle[target].obj = self
            # Nếu có hộp ở vị trí mới, thực hiện di chuyển đảo ngược
            if (c := self.game.puzzle[reverse_target].char) in '@$':
                self.game.puzzle[reverse_target].char = quick_chars[c]
                self.game.puzzle[reverse_target].obj.reverse_move(move)
            self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
            self.y, self.x = target
            # Xác định hướng nhân vật để chọn hình ảnh tương ứng
            if move == (64, 0):
                self.image = self.down
            elif move == (-64, 0):
                self.image = self.up
            elif move == (0, 64):
                self.image = self.right
            else:
                self.image = self.left

