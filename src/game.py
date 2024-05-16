import numpy as np
import pygame

from src.utils import get_state

from .box import Box, Obstacle
from .floor import Floor, Goal
from .player import Player, ReversePlayer


class PuzzleElement:
    def __init__(self, char, obj=None, ground=None):
        """Khởi tạo một phần tử trong mê cung.

        Parameters:
            char (str): Ký tự đại diện cho loại phần tử.
            obj (object): Đối tượng trong phần tử (VD: Hộp, Người chơi).
            ground (object): Đối tượng mặt đất (VD: Mục tiêu, Tường).

        Attributes:
            char (str): Ký tự đại diện cho loại phần tử.
            ground (object): Đối tượng mặt đất.
            obj (object): Đối tượng trong phần tử.
        """
        self.char = char
        self.ground = ground
        self.obj = obj

    def __str__(self): 
        """Trả về ký tự đại diện cho phần tử."""
        return self.char

class Game:
    def __init__(self, window=None, width=1216, height=640, level=None, seed=None, path=None):
        """Khởi tạo một trò chơi mới.

        Parameters:
            window (pygame.Surface): Cửa sổ pygame.
            width (int): Chiều rộng của cửa sổ.
            height (int): Chiều cao của cửa sổ.
            level (int): Cấp độ của trò chơi.
            seed (int): Hạt giống cho việc tạo ngẫu nhiên.
            path (str): Đường dẫn tới file lưu trữ mê cung.

        Attributes:
            seed (int): Hạt giống cho việc tạo ngẫu nhiên.
            window (pygame.Surface): Cửa sổ pygame.
            level (int): Cấp độ của trò chơi.
            width (int): Chiều rộng của cửa sổ.
            height (int): Chiều cao của cửa sổ.
            puzzle (np.ndarray): Mảng lưu trữ phần tử của mê cung.
            floor_group (pygame.sprite.Group): Nhóm sprite cho mặt sàn.
            object_group (pygame.sprite.Group): Nhóm sprite cho các đối tượng trong mê cung.
            player_group (pygame.sprite.Group): Nhóm sprite cho người chơi.
            goal_group (pygame.sprite.Group): Nhóm sprite cho mục tiêu.
            player (object): Đối tượng người chơi.
            puzzle_size (tuple): Kích thước của mê cung.
            pad_x (int): Lề ngang cho mê cung.
            pad_y (int): Lề dọc cho mê cung.
            path (str): Đường dẫn tới file lưu trữ mê cung.
        """
        self.seed = seed
        self.window = window
        self.level = level
        self.width = width
        self.height = height
        self.puzzle = np.empty((height // 64, width // 64), dtype=PuzzleElement)
        self.floor_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.goal_group = pygame.sprite.Group()
        self.player = None
        self.puzzle_size = None
        self.pad_x = 0
        self.pad_y = 0
        self.path = path or f'levels/lvl{level}.dat'
        self.load_floor()
        if type(self) == Game:
            self.load_puzzle()

    def __del__(self):
        """Hủy các đối tượng khi kết thúc trò chơi."""
        self.clear_objects()

    def get_matrix(self):
        """Trả về ma trận biểu diễn cho mê cung."""
        slice_x = slice(self.pad_x, self.pad_x + self.puzzle_size[1])
        slice_y = slice(self.pad_y, self.pad_y + self.puzzle_size[0])
        sliced = self.puzzle[slice_y, slice_x]
        matrix = np.empty((self.puzzle_size), dtype='<U1')
        for h in range(len(sliced)):
            for w in range(len(sliced[0])):
                matrix[h, w] = sliced[h, w].char
        return matrix
    
    def get_curr_state(self):
        """Trả về trạng thái hiện tại của mê cung."""
        return get_state(self.get_matrix())

    def print_puzzle(self):
        """In ra mê cung."""
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w]:
                    print(self.puzzle[h, w].char, end=' ')
                else:
                    print(' ', end=' ')
            print(' ')

    def is_level_complete(self):
        """Kiểm tra xem cấp độ đã hoàn thành chưa."""
        boxes_left = 0
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w] and self.puzzle[h, w].char == '@':
                    boxes_left += 1
        return boxes_left == 0

    def clear_objects(self):
        """Xóa các đối tượng trong mê cung."""
        for sprite in self.object_group:
            del sprite
        for sprite in self.floor_group:
            del sprite

    def load_floor(self):
        """Tải mặt sàn của mê cung."""
        for i in range(self.width // 64):
            for j in range(self.height // 64):
                Floor(self.floor_group, x=i, y=j)

    def load_puzzle(self):
        """Tải mê cung từ file lưu trữ."""
        try:
            with open(self.path) as f:
                lines = f.readlines()
                self.puzzle_size = (len(lines), len(lines[0].strip().split()))
                pad_x = (self.width // 64 - self.puzzle_size[1] - 2) // 2
                pad_y = (self.height // 64 - self.puzzle_size[0]) // 2
                self.pad_x, self.pad_y = pad_x, pad_y
            with open(self.path) as f:
                for i, line in enumerate(f):
                    for j, c in enumerate(line.strip().split()):
                        new_elem = PuzzleElement(c)
                        self.puzzle[i + pad_y, j + pad_x] = new_elem
                        if c == '+':  # wall
                            new_elem.obj = Obstacle(self.object_group, x=j + pad_x, y=i + pad_y)
                        elif c == '@':  # box
                            new_elem.obj = Box(self.object_group, x=j + pad_x, y=i + pad_y, game=self)
                        elif c == '*':  # player
                            new_elem.obj = Player(
                                self.object_group, self.player_group, 
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            self.player = new_elem.obj
                        elif c == 'X':  # goal
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                        elif c == '$':  # box on goal
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                            new_elem.obj = Box(self.object_group,  x=j + pad_x, y=i + pad_y, game=self)
                        elif c == '%':  # player on goal
                            new_elem.obj = Player(
                                self.object_group, self.player_group, 
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                            self.player = new_elem.obj
                        elif c not in ' -':
                            raise ValueError(
                                f'Invalid character on file lvl{self.level}.dat: {c}'
                            )
        except (OSError, ValueError) as e:
            print(f'{e}')
            self.clear_objects()
            return


class ReverseGame(Game):
    def __init__(self, window=None, width=1216, height=640, level=None, seed=None):
        # Gọi hàm khởi tạo của lớp cha với các đối số tương ứng
        super().__init__(window, width, height, level, seed)
        # Đặt giá trị mặc định cho đệm x và y
        self.pad_x = 0
        self.pad_y = 0

    def load_puzzle(self, puzzle):
        # Tính toán giá trị đệm x và y dựa trên kích thước của bản đồ và cửa sổ trò chơi
        pad_x = (self.width // 64 - len(puzzle[0]) - 2) // 2
        pad_y = (self.height // 64 - len(puzzle)) // 2
        self.pad_x, self.pad_y = pad_x, pad_y
        # Lặp qua từng hàng và cột trong bản đồ
        for i, row in enumerate(puzzle):
            for j, c in enumerate(row):
                new_elem = PuzzleElement(c)
                # Thêm phần tử mới vào bản đồ tại vị trí tương ứng với đệm x và y
                self.puzzle[i + pad_y, j + pad_x] = new_elem
                # Xử lý từng loại phần tử trong bản đồ
                if c == '+':  # tường
                    new_elem.obj = Obstacle(self.object_group, x=j + pad_x, y=i + pad_y)
                elif c == '@':  # hộp
                    new_elem.obj = Box(self.object_group, x=j + pad_x, y=i + pad_y, game=self)
                elif c == '*':  # người chơi
                    new_elem.obj = ReversePlayer(
                        self.object_group, self.player_group, 
                        x=j + pad_x, y=i + pad_y, game=self
                    )
                    self.player = new_elem.obj
                elif c == 'X':  # mục tiêu
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                elif c == '$':  # hộp trên mục tiêu
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                    new_elem.obj = Box(self.object_group,  x=j + pad_x, y=i + pad_y, game=self)
                elif c == '%':  # người chơi trên mục tiêu
                    new_elem.obj = ReversePlayer(
                        self.object_group, self.player_group, 
                        x=j + pad_x, y=i + pad_y, game=self
                    )
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                    self.player = new_elem.obj


    
    