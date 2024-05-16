import pygame
from pygame.sprite import Sprite

# Định nghĩa một lớp cho các phần tử trong trò chơi gọi là Box
class Box(Sprite):
    # Phương thức khởi tạo để khởi tạo đối tượng Box
    def __init__(self, *groups, x, y, game=None):
        super().__init__(*groups)  # Gọi phương thức khởi tạo của lớp cha (Sprite)
        self.game = game  # Tham chiếu đến đối tượng trò chơi
        # Tải hình ảnh cho Box:
        self.sprite = pygame.image.load('img/box.png')
        self.sprite = pygame.transform.scale(self.sprite, [64, 64])
        self.spriteg = pygame.image.load('img/boxg.png')
        self.spriteg = pygame.transform.scale(self.spriteg, [64, 64])
        # Thiết lập hình ảnh ban đầu của Box dựa trên vị trí của nó trên lưới
        self.image = self.sprite if game and not game.puzzle[y, x].ground else self.spriteg
        # Thiết lập vị trí và kích thước của Box
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x  # Tọa độ x
        self.y = y  # Tọa độ y

    # Phương thức để kiểm tra xem Box có thể di chuyển theo một hướng nào đó không
    def can_move(self, move):
        # Tính toán vị trí đích sau khi di chuyển
        target_x, target_y = self.x + move[0] // 64, self.y + move[1] // 64
        target = target_y, target_x
        curr = self.y, self.x
        target_elem = self.game.puzzle[target]  # Phần tử tại vị trí đích
        # Kiểm tra xem vị trí đích có trống không
        if not isinstance(target_elem.obj, Box):
            curr_elem = self.game.puzzle[curr]  # Phần tử hiện tại
            # Cập nhật vị trí và hình dạng của Box
            self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
            self.y, self.x = target
            curr_elem.char = '-' if not curr_elem.ground else 'X'
            curr_elem.obj = None
            target_elem.char = '@' if not target_elem.ground else '$'
            target_elem.obj = self
            self.update_sprite()  # Cập nhật sprite
            return True  # Trả về True nếu di chuyển thành công
        return False  # Trả về False nếu di chuyển không khả thi
    
    # Phương thức để đảo ngược một bước di chuyển đã thực hiện
    def reverse_move(self, move):
        target = self.y + move[0] // 64, self.x + move[1] // 64
        curr_pos = self.y, self.x
        # Cập nhật lưới trò chơi để phản ánh bước di chuyển đảo ngược
        self.game.puzzle[curr_pos].obj = None
        self.game.puzzle[target].obj = self
        self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
        self.y, self.x = target
        self.game.puzzle[curr_pos].char = 'X' if self.game.puzzle[curr_pos].ground else '-'
        self.game.puzzle[target].char = '$' if self.game.puzzle[target].ground else '@'
        self.update_sprite()  # Cập nhật sprite
    
    # Phương thức để cập nhật sprite của Box dựa trên vị trí hiện tại của nó
    def update_sprite(self):
        curr_obj = self.game.puzzle[self.y, self.x]
        self.image = self.spriteg if curr_obj and curr_obj.ground else self.sprite

    # Phương thức hủy được gọi khi đối tượng Box bị xóa
    def __del__(self):
        self.kill()  # Loại bỏ sprite khỏi tất cả các nhóm mà nó thuộc về


# Định nghĩa một lớp con của Box gọi là Obstacle
class Obstacle(Box):
    # Phương thức khởi tạo để khởi tạo đối tượng Obstacle
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y)  # Gọi phương thức khởi tạo của lớp cha (Box)
        # Tải hình ảnh cho Obstacle
        self.image = pygame.image.load('img/obs.png')
        self.image = pygame.transform.scale(self.image, [64, 64])
        # Thiết lập vị trí và kích thước của Obstacle
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
