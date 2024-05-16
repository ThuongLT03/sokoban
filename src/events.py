import pygame

# Định nghĩa các sự kiện tùy chỉnh bằng cách sử dụng các sự kiện người dùng của Pygame
RESTART_EVENT = pygame.USEREVENT + 1  # Sự kiện khởi động lại trò chơi
PREVIOUS_EVENT = pygame.USEREVENT + 2  # Sự kiện chuyển đến trò chơi trước đó
NEXT_EVENT = pygame.USEREVENT + 3      # Sự kiện chuyển đến trò chơi tiếp theo
RANDOM_GAME_EVENT = pygame.USEREVENT + 4  # Sự kiện chuyển đến một trò chơi ngẫu nhiên
SOLVE_ASTARMAN_EVENT = pygame.USEREVENT + 5  # Sự kiện giải trò chơi bằng thuật toán A* Man
