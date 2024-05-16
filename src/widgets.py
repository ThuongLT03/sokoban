import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
from .events import *

# Tạo các widget bên trái của giao diện người dùng.
def sidebar_widgets(window):
    
    # Tạo nút "Previous" để chuyển đến cấp độ trước đó.
    prev_button = Button(
        window, 1030, 12, 22, 40, text='<', radius=2,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(PREVIOUS_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(150, 150, 150)  # Màu nền của nút
    )
    # Label hiển thị thông tin về cấp độ hiện tại của trò chơi.
    label = Label(window, f'Level 0', 1055, 10, 30, color='blue')  # Màu văn bản của nhãn
    
    # Tạo nút "Next" để chuyển đến cấp độ tiếp theo.
    next_button = Button(
        window, 1188, 12, 22, 40, text='>', radius=2,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(NEXT_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(150, 150, 150)  # Màu nền của nút
    )
    
    # Nút "Restart" để khởi động lại cấp độ hiện tại.
    restart = Button(
        window, 1055, 130, 130, 40, text='Restart', radius=5,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(RESTART_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(255, 0, 0)  # Màu nền của nút
    )
    
    # Nút "Random" để tạo một trò chơi ngẫu nhiên mới.
    random_game = Button(
        window, 1055, 220, 130, 40, text='Random', radius=5,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(RANDOM_GAME_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(0, 255, 0)  # Màu nền của nút
    )
    
    # Label hiển thị văn bản "Visualize".
    visualizer = Label(window, f'Visualize', 1055, 450, 16, color='green')  # Màu văn bản của nhãn
    # Toggle để bật/tắt chức năng visualize.
    toggle = Toggle(window, 1160, 455, 18, 22, handleRadius=11, startOn=True)  # Bật toggle mặc định
    
    # Nút "A* Solution" để tìm kiếm và hiển thị giải pháp sử dụng thuật toán A*.
    astarman_button = Button(
        window, 1055, 300, 130, 40, text='A* Solution', radius=5,
        font=pygame.font.SysFont('Verdana', 14, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_ASTARMAN_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(0, 0, 255)  # Màu nền của nút
    )
    
    # Label hiển thị văn bản "Seed".
    seed = Label(window, f'Seed', 1055, 190, 16, color='purple')  # Màu văn bản của nhãn
    # Hộp văn bản để nhập giá trị hạt giống cho trò chơi ngẫu nhiên.
    seedbox = TextBox(
        window, 1110, 191, 75, 28, placeholderText='Seed',
        borderColour=(0, 0, 0), textColour=(0, 0, 0), backgroundColour=(255, 255, 255),
        onSubmit=lambda: pygame.event.post(pygame.event.Event(RANDOM_GAME_EVENT)),
        borderThickness=1, radius=2,
        font=pygame.font.SysFont('Verdana', 14),
    )
    
    # Label hiển thị số lượt di chuyển.
    moves = Label(window, f' Moves - 0 ', 1055, 75, 20, color='orange')  # Màu văn bản của nhãn
    # Label đa dòng hiển thị thông tin về độ sâu giải pháp.
    paths = MultilineLabel(window, f'Solution Depth: 0\n', 64, 0, 20, color='black')  # Màu văn bản của nhãn
    # Label hiển thị thông báo khi hoàn thành cấp độ.
    level_clear = LevelClear(window, f'Level Clear!', color='green')  # Màu văn bản của nhãn
    
    return {
        'restart': restart,
        'random_button': random_game,
        'moves_label': moves,
        'prev_button': prev_button, 
        'next_button': next_button, 
        'label': label, 
        'level_clear': level_clear,
        'toggle': toggle,
        'visualizer': visualizer,
        'paths': paths,
        'seedbox': seedbox,
        'seed': seed,
        'astarman': astarman_button,
    }

# Lớp Label để tạo các nhãn trong giao diện người dùng.
class Label:

    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        """
        Khởi tạo một nhãn mới.

        Parameters:
            - window: Cửa sổ pygame để vẽ nhãn.
            - text (str): Nội dung của nhãn.
            - x (int): Tọa độ x của nhãn.
            - y (int): Tọa độ y của nhãn.
            - font_size (int): Kích thước font chữ.
            - transparency (bool): Cờ chỉ định tính trong suốt của nhãn.
            - color (str hoặc tuple): Màu của nhãn.
        """
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(text, 1, color)
        self.max_width = self.image.get_width()
        self.total_height = self.image.get_height()
        self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)
        self.window = window
        self.transparency = transparency
        self.solved = False

    def set_text(self, new_text, font_size, color='black'):
        """
        Thiết lập văn bản mới cho nhãn.

        Parameters:
            - new_text (str): Nội dung văn bản mới.
            - font_size (int): Kích thước font chữ mới.
            - color (str hoặc tuple): Màu của văn bản mới.
        """
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(new_text, 1, color)
        self.draw()

    def set_moves(self, new_text, font_size, color='black'):
        """
        Thiết lập số lượt di chuyển mới cho nhãn.

        Parameters:
            - new_text (str): Số lượt di chuyển mới.
            - font_size (int): Kích thước font chữ.
            - color (str hoặc tuple): Màu của văn bản.
        """
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(new_text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect.width = max(130, w)
        self.rect.height = max(40, h)
        self.draw()

    def draw(self): # Vẽ nhãn trên cửa sổ pygame.
        pygame.draw.rect( 
            self.window, 
            pygame.Color('gray'), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height) 
        ) 
        pygame.draw.rect( 
            self.window, 
            (0, 0, 0), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height), 
            width=3 
        ) 
        text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x 
        text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y 
        self.window.blit(self.image, (text_pos_x, text_pos_y))


class MultilineLabel(Label): # Lớp MultilineLabel để tạo các nhãn đa dòng trong giao diện người dùng.
    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        """
        Khởi tạo một nhãn đa dòng mới.

        Parameters:
            - window: Cửa sổ pygame để vẽ nhãn.
            - text (str): Nội dung của nhãn.
            - x (int): Tọa độ x của nhãn.
            - y (int): Tọa độ y của nhãn.
            - font_size (int): Kích thước font chữ.
            - transparency (bool): Cờ chỉ định tính trong suốt của nhãn.
            - color (str hoặc tuple): Màu của nhãn.
        """
        super().__init__(window, text, x, y, font_size, transparency)
        self.lines = text.split('\n')
        if len(self.lines) == 1:
            self.image = self.font.render(text, 1, color)
        self.images = [self.font.render(line, 1, color) for line in self.lines]
        self.max_width = max(image.get_width() for image in self.images)
        self.total_height = (sum(image.get_height() for image in self.images) + 
                                (len(self.lines) - 1) * 5)
        self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)
        self.color = color
        self.draw()

    def draw(self):
        pygame.draw.rect(
            self.window, 
            pygame.Color('gray'), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height) 
        ) 
        pygame.draw.rect(
            self.window, 
            (0, 0, 0), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height), 
            width=3 
        ) 
        y_offset = self.rect.y + 5
        for image in self.images:
            text_pos_x = (self.rect.width - image.get_width()) // 2 + self.rect.x
            self.window.blit(image, (text_pos_x, y_offset))
            y_offset += image.get_height() + 5


class LevelClear(Label): # Lớp LevelClear kế thừa từ lớp Label
    def __init__(self, window, text, color='black'):
        """
        Khởi tạo một nhãn hiển thị khi cấp độ được hoàn thành.

        Parameters:
            - window: Cửa sổ pygame để vẽ nhãn.
            - text (str): Nội dung của nhãn.
            - color (str hoặc tuple): Màu của nhãn.
        """
        super().__init__(window, text, 1000, 300, 50, color=color)
        self.font = pygame.font.SysFont('Verdana', 50, bold=True)
        self.image = self.font.render(text, 1, color)
        self.rect = pygame.Rect(1000, 300, self.image.get_width() + 10, self.image.get_height() + 10)
        self.window = window
        self.draw()

    def draw(self):
        pygame.draw.rect(
            self.window, 
            pygame.Color('gray'), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height)
        ) 
        pygame.draw.rect(
            self.window, 
            (0, 0, 0), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height), 
            width=3 
        ) 
        text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x 
        text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y 
        self.window.blit(self.image, (text_pos_x, text_pos_y))
