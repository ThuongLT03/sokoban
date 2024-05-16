import pygame

# Định nghĩa lớp Floor để tạo các ô sàn trong trò chơi
class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        # Tải hình ảnh cho ô sàn dựa trên vị trí x của nó
        if x <= 15:
            self.image = pygame.image.load('img/floor.png')  # Sàn bình thường
        else:
            self.image = pygame.image.load('img/sidefloor.png')  # Sàn ở cạnh
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x
        self.y = y
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Vẽ hình ảnh của ô sàn lên màn hình

    def __del__(self):
        self.kill()  # Loại bỏ sprite khỏi tất cả các nhóm mà nó thuộc về


# Định nghĩa lớp Goal là một loại đặc biệt của ô sàn để đại diện cho mục tiêu trong trò chơi
class Goal(Floor):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y)
        self.image = pygame.image.load('img/goal.png')  # Tải hình ảnh của mục tiêu
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)  # Thiết lập vị trí và kích thước của hình chữ nhật cho mục tiêu
