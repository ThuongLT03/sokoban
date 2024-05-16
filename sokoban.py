import random
import time

import pygame
import pygame_widgets

from src.astar import solve_astar
from src.events import * 
from src.game import Game
from src.generator import generate
from src.utils import play_solution
from src.widgets import sidebar_widgets

random.seed(10)  # Thiết lập seed cho thư viện random để đảm bảo kết quả ngẫu nhiên nhất quán

def play_game(window, level=1, random_game=False, random_seed=None, **widgets):
    moves = runtime = 0  # Khởi tạo biến moves (số nước di chuyển) và runtime (thời gian chạy) bằng 0
    show_solution = False  # Khởi tạo biến show_solution (hiển thị giải pháp) thành False
    widgets['paths'].transparency = False  # Đặt độ trong suốt của đường đi là False
    # Kiểm tra xem trò chơi có phải là trò chơi ngẫu nhiên không
    if random_game:
        # Nếu là trò chơi ngẫu nhiên, sinh bản đồ mới với seed ngẫu nhiên hoặc seed được chỉ định
        if not random_seed:
            random_seed = random.randint(0, 99999)
        generate(window, seed=random_seed, visualizer=widgets['toggle'].getValue())
    # Hiển thị trạng thái của nút Previous nếu level > 1, ngược lại ẩn nút đó
    if level <= 1:
        widgets['prev_button'].hide()
    else:
        widgets['prev_button'].show()
    # Hiển thị trạng thái của nút Next nếu level < 10, ngược lại ẩn nút đó
    if level >= 10:
        widgets['next_button'].hide()
    else:
        widgets['next_button'].show()
    # Hiển thị seed nếu là trò chơi ngẫu nhiên hoặc level là 0, ngược lại hiển thị level
    if random_game or level == 0:
        widgets['label'].set_text(f'Seed {random_seed}', 18)
    else:
        widgets['label'].set_text(f'Level {level}', 30)
    # Tạo một đối tượng Game mới với level và cửa sổ được chỉ định
    game = Game(level=level, window=window)
    game_loop = True  # Khởi tạo biến game_loop thành True
    # Vòng lặp chính của trò chơi
    while game_loop:
        events = pygame.event.get()  # Lấy tất cả các sự kiện từ pygame
        for event in events:
            if event.type == pygame.QUIT:  # Kiểm tra sự kiện thoát khỏi trò chơi
                game_loop = False  # Kết thúc vòng lặp
                return {
                    'keep_playing': False,  # Không tiếp tục chơi
                    'reset': -1,  # Không có reset
                    'random_game': False,  # Không phải trò chơi ngẫu nhiên
                }
            # Xử lý các sự kiện nhấn nút Restart, Previous, Next, Random Game và Solve A*
            elif event.type in [RESTART_EVENT, PREVIOUS_EVENT, NEXT_EVENT, RANDOM_GAME_EVENT, SOLVE_ASTARMAN_EVENT]:
                game_loop = False  # Kết thúc vòng lặp
                # Trả về thông tin để xử lý tiếp theo
                return {
                    'keep_playing': True,
                    'reset': level if event.type != RANDOM_GAME_EVENT else 0,  # Trở về level hoặc trò chơi ngẫu nhiên
                    'random_game': event.type == RANDOM_GAME_EVENT,  # Đánh dấu là trò chơi ngẫu nhiên hay không
                    'random_seed': random_seed if event.type != RANDOM_GAME_EVENT else None,  # Seed của trò chơi ngẫu nhiên
                }
            elif event.type == SOLVE_ASTARMAN_EVENT:  # Kiểm tra sự kiện Solve A*
                # Tìm giải pháp cho bản đồ hiện tại bằng thuật toán A*
                print('Finding a solution for the puzzle\n')
                widgets['paths'].reset('Solving with [A*]')  # Đặt lại thông báo trên đường đi
                show_solution = True  # Hiển thị giải pháp
                start = time.time()  # Bắt đầu đo thời gian
                solution, depth = solve_astar(  # Gọi hàm solve_astar
                    game.get_matrix(),  # Lấy ma trận từ trò chơi
                    widget=widgets['paths'],  # Đường đi sẽ được hiển thị trên widget 'paths'
                    visualizer=widgets['toggle'].getValue(),  # Lấy giá trị của toggle button
                    heuristic='manhattan',  # Sử dụng hàm heuristic Manhattan
                )
                runtime = round(time.time() - start, 5)  # Tính thời gian chạy và làm tròn
                if solution:  # Nếu tìm thấy giải pháp
                    widgets['paths'].solved = True  # Đánh dấu là đã tìm thấy giải pháp
                    widgets['paths'].transparency = True  # Đặt độ trong suốt của đường đi
                    # Hiển thị thông báo với giải pháp và thời gian chạy
                    widgets['paths'].set_text(f'[A*] Solution Found in {runtime}s!\n{solution}', 20)
                    # Phát giải pháp để di chuyển người chơi
                    moves = play_solution(solution, game, widgets, show_solution, moves)
                else:  # Nếu không tìm thấy giải pháp
                    widgets['paths'].solved = False  # Đánh dấu là không tìm thấy giải pháp
                    # Hiển thị thông báo với lý do không tìm thấy giải pháp
                    widgets['paths'].set_text('[A*] Solution Not Found!\n' + ('Deadlock Found!' if depth < 0 else f'Depth {depth}'), 20)
            elif event.type == pygame.KEYDOWN:  # Xử lý sự kiện nhấn phím
                if event.key in (pygame.K_d, pygame.K_RIGHT):  # Di chuyển sang phải
                    moves += game.player.update(key='R')
                elif event.key in (pygame.K_a, pygame.K_LEFT):  # Di chuyển sang trái
                    moves += game.player.update(key='L')
                elif event.key in (pygame.K_w, pygame.K_UP):  # Di chuyển lên trên
                    moves += game.player.update(key='U')
                elif event.key in (pygame.K_s, pygame.K_DOWN):  # Di chuyển xuống dưới
                    moves += game.player.update(key='D')
        # Vẽ các nhóm đối tượng trên cửa sổ
        game.floor_group.draw(window)
        game.goal_group.draw(window)
        game.object_group.draw(window)
        pygame_widgets.update(events)  # Cập nhật các widget pygame
        widgets['label'].draw()  # Vẽ nhãn
        widgets['seed'].draw()  # Vẽ hộp văn bản cho seed
        widgets['visualizer'].draw()  # Vẽ toggle button cho visualizer
        # Cập nhật nhãn hiển thị số nước di chuyển
        widgets['moves_label'].set_moves(f' Moves - {moves} ', 20)
        if show_solution:  # Nếu cần hiển thị giải pháp
            widgets['paths'].draw()  # Vẽ đường đi
        pygame.display.update()  # Cập nhật cửa sổ
        # Kiểm tra xem level đã hoàn thành chưa
        if game.is_level_complete():
            print(f'Level Complete! - {moves} moves')  # In thông báo level đã hoàn thành
            widgets['level_clear'].draw()  # Hiển thị thông báo trên cửa sổ
            pygame.display.update()  # Cập nhật cửa sổ
            game_loop = False  # Kết thúc vòng lặp
            wait = True  # Khởi tạo biến wait thành True
            while wait:  # Vòng lặp chờ sự kiện từ người chơi
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        wait = False  # Kết thúc vòng lặp
            print('Objects cleared!\n')  # In thông báo đã xóa các đối tượng
    del game  # Xóa đối tượng game
    return {
        'keep_playing': True,  # Tiếp tục chơi
        'reset': 0 if random_game else -1,  # Đặt lại level hoặc không
        'random_game': random_game,  # Đánh dấu là trò chơi ngẫu nhiên hay không
    }

def main():
    pygame.init()  # Khởi tạo pygame
    displayIcon = pygame.image.load('img/icon.png')  # Tải biểu tượng cửa sổ
    pygame.display.set_icon(displayIcon)  # Đặt biểu tượng cửa sổ
    window = pygame.display.set_mode((1216, 640))  # Tạo cửa sổ với kích thước 1216x640
    pygame.display.set_caption('Sokoban')  # Đặt tiêu đề cửa sổ
    level = 1  # Khởi tạo level
    keep_playing = True  # Khởi tạo biến keep_playing thành True
    random_game = False  # Khởi tạo biến random_game thành False
    random_seed = None  # Khởi tạo biến random_seed thành None
    widgets = sidebar_widgets(window)  # Tạo các widget cho sidebar
    # Vòng lặp chính của trò chơi
    while keep_playing:
        print(f'Loading level {level}\n' if level > 0 else 'Loading random game')
        # Chạy trò chơi và nhận thông tin trạng thái của trò chơi
        game_data = play_game(window, level, random_game, random_seed, **widgets)
        keep_playing = game_data.get('keep_playing', False)  # Cập nhật trạng thái keep_playing
        if not keep_playing:  # Nếu không tiếp tục chơi
            pygame.quit()  # Dừng pygame
            quit()  # Thoát chương trình
        reset = game_data.get('reset', -1)  # Lấy thông tin reset
        random_game = game_data.get('random_game', False)  # Lấy thông tin random_game
        random_seed = game_data.get('random_seed')  # Lấy thông tin random_seed
        level = reset if reset >= 0 else min(level + 1, 7)  # Cập nhật level

if __name__ == '__main__':
    main()  # Chạy hàm main khi script được chạy
