import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle

from .events import *

# Hàm tạo các widget cho thanh bên (sidebar) của cửa sổ
def sidebar_widgets(window):
    # Tạo nút để chuyển về cấp độ trước đó
    prev_button = Button(
        window,  # cửa sổ để vẽ nút
        1030, 12, 22, 40,  # tọa độ và kích thước của nút (x, y, width, height)
        text='<',  # văn bản hiển thị trên nút
        radius=2,  # độ cong của các góc nút
        font=pygame.font.SysFont('Verdana', 18, bold=True),  # phông chữ cho văn bản trên nút
        onClick=lambda: pygame.event.post(pygame.event.Event(PREVIOUS_EVENT)),  # hành động khi nút được nhấn
        borderColor='black',  # màu của viền nút
        borderThickness=2,  # độ dày của viền nút
    )
    # Tạo nhãn để hiển thị thông tin cấp độ hiện tại
    label = Label(window, f'Level 0', 1055, 10, 30)
    # Tạo nút để chuyển sang cấp độ tiếp theo
    next_button = Button(
        window,  # cửa sổ để vẽ nút
        1188, 12, 22, 40,  # tọa độ và kích thước của nút
        text='>',  # văn bản hiển thị trên nút
        radius=2,  # độ cong của các góc nút
        font=pygame.font.SysFont('Verdana', 18, bold=True),  # phông chữ cho văn bản trên nút
        onClick=lambda: pygame.event.post(pygame.event.Event(NEXT_EVENT)),  # hành động khi nút được nhấn
        borderColor='black',  # màu của viền nút
        borderThickness=2,  # độ dày của viền nút
    )
    # Tạo nút để khởi động lại trò chơi
    restart = Button(
        window,  # cửa sổ để vẽ nút
        1055, 130, 130, 40,  # tọa độ và kích thước của nút
        text='Restart',  # văn bản hiển thị trên nút
        radius=5,  # độ cong của các góc nút
        font=pygame.font.SysFont('Verdana', 18, bold=True),  # phông chữ cho văn bản trên nút
        onClick=lambda: pygame.event.post(pygame.event.Event(RESTART_EVENT)),  # hành động khi nút được nhấn
        borderColor='black',  # màu của viền nút
        borderThickness=2,  # độ dày của viền nút
    )
    # Tạo nút để chọn trò chơi ngẫu nhiên
    random_game = Button(
        window,  # cửa sổ để vẽ nút
        1055, 220, 130, 40,  # tọa độ và kích thước của nút
        text='Random',  # văn bản hiển thị trên nút
        radius=5,  # độ cong của các góc nút
        font=pygame.font.SysFont('Verdana', 18, bold=True),  # phông chữ cho văn bản trên nút
        onClick=lambda: pygame.event.post(pygame.event.Event(RANDOM_GAME_EVENT)),  # hành động khi nút được nhấn
        borderColor='black',  # màu của viền nút
        borderThickness=2,  # độ dày của viền nút
    )
    # Tạo nhãn để hiển thị tùy chọn trực quan hóa
    visualizer = Label(window, f'Visualize', 1055, 450, 16)
    # Tạo toggle để bật/tắt trực quan hóa
    toggle = Toggle(window, 1160, 455, 18, 22, handleRadius=11)
    
    # Tạo nút để khởi động giải thuật A* với heuristic Manhattan
    astarman_button = Button(
        window,  # cửa sổ để vẽ nút
        1055, 300, 130, 40,  # tọa độ và kích thước của nút
        text='A* Manhattan',  # văn bản hiển thị trên nút
        radius=5,  # độ cong của các góc nút
        font=pygame.font.SysFont('Verdana', 14, bold=True),  # phông chữ cho văn bản trên nút
        onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_ASTARMAN_EVENT)),  # hành động khi nút được nhấn
        borderColor='black',  # màu của viền nút
        borderThickness=2,  # độ dày của viền nút
    )

    # Tạo nhãn và TextBox để nhập seed cho trò chơi ngẫu nhiên
    seed = Label(window, f'Seed', 1055, 190, 16)
    seedbox = TextBox(
        window,  # cửa sổ để vẽ TextBox
        1110, 191, 75, 28,  # tọa độ và kích thước của TextBox
        placeholderText='Seed',  # văn bản hiển thị khi TextBox trống
        borderColour=(0, 0, 0),  # màu của viền TextBox
        textColour=(0, 0, 0),  # màu của văn bản trong TextBox
        onSubmit=lambda: pygame.event.post(pygame.event.Event(RANDOM_GAME_EVENT)),  # hành động khi người dùng nhập xong
        borderThickness=1,  # độ dày của viền TextBox
        radius=2,  # độ cong của các góc TextBox
        font=pygame.font.SysFont('Verdana', 14),  # phông chữ cho văn bản trong TextBox
    )
    # Tạo nhãn để hiển thị số lần di chuyển
    moves = Label(window, f' Moves - 0 ', 1055, 75, 20)
    # Tạo nhãn đa dòng để hiển thị độ sâu của giải pháp
    paths = MultilineLabel(window, f'Solution Depth: 0\n', 64, 0, 20)
    # Tạo nhãn để hiển thị thông báo khi hoàn thành cấp độ
    level_clear = LevelClear(window, f'Level Clear!')
    return {
        'restart': restart,  # nút khởi động lại
        'random_button': random_game,  # nút chơi ngẫu nhiên
        'moves_label': moves,  # nhãn số lần di chuyển
        'prev_button': prev_button,  # nút chuyển về cấp độ trước
        'next_button': next_button,  # nút chuyển sang cấp độ tiếp theo
        'label': label,  # nhãn cấp độ hiện tại
        'level_clear': level_clear,  # nhãn hoàn thành cấp độ
        'toggle': toggle,  # toggle bật/tắt trực quan hóa
        'visualizer': visualizer,  # nhãn trực quan hóa
        'paths': paths,  # nhãn đa dòng hiển thị độ sâu giải pháp
        'seedbox': seedbox,  # TextBox nhập seed
        'seed': seed,  # nhãn seed
        'astarman': astarman_button,  # nút giải thuật A* Manhattan
    }

# Lớp Label để hiển thị nhãn văn bản trên cửa sổ
class Label:
    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        self.x = x  # tọa độ x của nhãn
        self.y = y  # tọa độ y của nhãn
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)  # thiết lập phông chữ cho nhãn
        self.image = self.font.render(text, 1, color)  # tạo hình ảnh văn bản của nhãn
        self.max_width = self.image.get_width()  # chiều rộng tối đa của nhãn
        self.total_height = self.image.get_height()  # chiều cao tối đa của nhãn
        self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)  # tạo hình chữ nhật bao quanh nhãn
        self.window = window  # cửa sổ để vẽ nhãn
        self.transparency = transparency  # thiết lập độ trong suốt của nhãn
        self.solved = False  # trạng thái của nhãn (chưa giải quyết)

    # Phương thức để cập nhật văn bản của nhãn
    def set_text(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)  # cập nhật phông chữ
        self.image = self.font.render(new_text, 1, color)  # cập nhật hình ảnh văn bản
        self.draw()  # vẽ lại nhãn

    # Phương thức để cập nhật số lần di chuyển
    def set_moves(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)  # cập nhật phông chữ
        self.image = self.font.render(new_text, 1, color)  # cập nhật hình ảnh văn bản
        _, _, w, h = self.image.get_rect()  # lấy kích thước của hình ảnh văn bản
        self.rect.width = max(130, w)  # cập nhật chiều rộng của nhãn
        self.rect.height = max(40, h)  # cập nhật chiều cao của nhãn
        self.draw()  # vẽ lại nhãn

    # Phương thức để vẽ nhãn lên cửa sổ
    def draw(self):
        # Vẽ hình chữ nhật màu xám làm nền cho nhãn
        pygame.draw.rect( 
            self.window, 
            pygame.Color('gray'), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height) 
        ) 
        # Vẽ viền đen cho nhãn
        pygame.draw.rect( 
            self.window, 
            (0, 0, 0), 
            (self.rect.x, 
            self.rect.y, 
            self.rect.width, 
            self.rect.height), 
            width=3 
        ) 
        # Tính toán vị trí để vẽ văn bản bên trong nhãn
        text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x 
        text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y 
        # Vẽ văn bản lên nhãn
        self.window.blit(self.image, (text_pos_x, text_pos_y))

# Lớp MultilineLabel để hiển thị nhãn đa dòng trên cửa sổ
class MultilineLabel(Label):
    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        super().__init__(window, text, x, y, font_size, transparency)  # kế thừa từ lớp Label
        self.lines = text.split('\n')  # tách văn bản thành các dòng
        if len(self.lines) == 1:  # nếu chỉ có một dòng
            self.image = self.font.render(text, 1, color)  # tạo hình ảnh văn bản
        self.images = [self.font.render(line, 1, color) for line in self.lines]  # tạo hình ảnh cho từng dòng
        self.max_width = max(image.get_width() for image in self.images)  # lấy chiều rộng lớn nhất của các dòng
        self.total_height = (sum(image.get_height() for image in self.images) + 
                              (len(self.lines) - 1) * font_size // 2)  # tính tổng chiều cao của các dòng
        self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)  # tạo hình chữ nhật bao quanh nhãn
        self.max_lines = len(self.lines)  # số dòng tối đa

    # Phương thức để đặt lại văn bản của nhãn
    def reset(self, text=''):
        self.max_width = self.total_height = 1  # đặt lại chiều rộng và chiều cao
        self.transparency = False  # đặt lại độ trong suốt
        self.solved = False  # đặt lại trạng thái
        self.max_lines = 2  # đặt lại số dòng tối đa
        self.set_text(f'{text}\n', 20)  # đặt lại văn bản
        pygame.display.update()  # cập nhật màn hình

    # Phương thức để cập nhật văn bản của nhãn
    def set_text(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)  # cập nhật phông chữ
        self.new_lines = new_text.split('\n')  # tách văn bản thành các dòng mới
        path_split = []  # danh sách chứa các đoạn văn bản
        for i in range(0, len(self.new_lines[1]), 60):  # tách dòng văn bản thứ hai thành các đoạn nhỏ hơn
            path_split.append(self.new_lines[1][i:i + 60])
        self.lines = [self.new_lines[0]] + path_split  # cập nhật các dòng văn bản
        self.max_lines = max(self.max_lines, len(self.lines))  # cập nhật số dòng tối đa
        while len(self.lines) < self.max_lines:  # thêm các dòng trống nếu cần
            self.lines.append('')
        self.images = [self.font.render(line, 1, color) for line in self.lines]  # tạo hình ảnh cho từng dòng
        self.max_width = max(self.max_width, max(image.get_width() for image in self.images))  # cập nhật chiều rộng lớn nhất
        self.total_height = (sum(image.get_height() for image in self.images) + 
                             (len(self.lines) - 1) * font_size // 2)  # tính tổng chiều cao
        self.rect = pygame.Rect(self.x, self.y, self.max_width + 10, self.total_height + 10)  # cập nhật hình chữ nhật bao quanh
        self.draw()  # vẽ lại nhãn

    # Phương thức để vẽ nhãn đa dòng lên cửa sổ
    def draw(self):
        # Tạo bề mặt trong suốt để vẽ nhãn
        transparent_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        transparent_surface.set_alpha(110)  # đặt độ trong suốt
        transparent_surface.fill((200, 0, 0) if not self.solved else (0, 255, 0))  # đặt màu nền
        if not self.transparency:  # nếu không cần trong suốt
            pygame.draw.rect(
                self.window,
                (200, 0, 0) if not self.solved else (0, 255, 0),  # màu nền
                (self.rect.x,
                self.rect.y,
                self.rect.width,
                self.rect.height)
            )
        # Vẽ viền đen cho nhãn
        pygame.draw.rect(
            self.window,
            (0, 0, 0),
            (self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height),
            width=3
        )
        # Tính toán vị trí để vẽ văn bản bên trong nhãn
        offset = ((self.rect.height - sum(image.get_height() for image in self.images) - 
                   (len(self.images) - 1)) // 2 + self.rect.y)
        if self.transparency:  # nếu cần trong suốt
            self.window.blit(transparent_surface, (self.rect.x, self.rect.y))
        for image in self.images:  # vẽ từng dòng văn bản
            text_pos_x = (self.rect.width - image.get_width()) // 2 + self.rect.x
            text_pos_y = offset
            offset += image.get_height()
            self.window.blit(image, (text_pos_x, text_pos_y))

# Lớp LevelClear để hiển thị thông báo khi hoàn thành cấp độ
class LevelClear(Label):
    def __init__(self, window, text, x=256, y=192, font_size=60, color='black'):
        super().__init__(window, text, x, y, font_size, color)  # kế thừa từ lớp Label
        self.w, self.h = 512, 256  # đặt kích thước của nhãn
        self.rect = pygame.Rect(x, y, self.w, self.h)  # tạo hình chữ nhật bao quanh nhãn
        self.image = self.font.render(text, 1, color)  # tạo hình ảnh văn bản của nhãn

    # Phương thức để vẽ thông báo hoàn thành cấp độ lên cửa sổ
    def draw(self):
        # Tạo bề mặt trong suốt để vẽ nhãn
        transparent_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        transparent_surface.set_alpha(100)  # đặt độ trong suốt
        transparent_surface.fill((0, 255, 0))  # đặt màu nền
        # Vẽ viền xanh lá cho nhãn
        pygame.draw.rect(
            self.window,
            '#008000',
            (self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height),
            width=4
        )
        # Tính toán vị trí để vẽ văn bản bên trong nhãn
        text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x
        text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y
        # Vẽ bề mặt trong suốt và văn bản lên cửa sổ
        self.window.blit(transparent_surface, (self.rect.x, self.rect.y))
        self.window.blit(self.image, (text_pos_x, text_pos_y))
