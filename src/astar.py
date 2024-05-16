import time
from collections import defaultdict
from heapq import heappop, heappush

import numpy as np
import pygame

# Nhập các hàm tiện ích từ tệp utils
from .utils import (can_move, get_state, is_deadlock, is_solved,
                    manhattan_sum, print_state)

# Hàm A* để tìm đường đi ngắn nhất
def astar(matrix, player_pos, widget=None, visualizer=False, heuristic='manhattan'):
    # In ra kiểu heuristic đang sử dụng
    print(f'A* - {heuristic.title()} Heuristic')
    heur = '[A*]' if heuristic == 'manhattan' else '[Dijkstra]'
    # Lấy kích thước của ma trận
    shape = matrix.shape
    # Lấy trạng thái ban đầu của ma trận
    initial_state = get_state(matrix)
    initial_cost = curr_depth = 0
    if heuristic == 'manhattan':
        # Tính chi phí hiện tại theo heuristic Manhattan
        curr_cost = manhattan_sum(initial_state, player_pos, shape)
    # Khởi tạo tập hợp để lưu trữ các trạng thái đã thấy
    seen = {None}
    # Khởi tạo hàng đợi ưu tiên
    heap = []
    # Thêm trạng thái ban đầu vào hàng đợi ưu tiên
    heappush(heap, (initial_cost, curr_cost, initial_state, player_pos, curr_depth, ''))
    # Các hướng di chuyển có thể (xuống, lên, trái, phải)
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    # Từ điển ánh xạ từ hướng di chuyển sang ký tự đại diện
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U', 
        (0, -1): 'L',
        (0, 1): 'R',
    }
    # Vòng lặp chính của A*
    while heap:
        # Nếu có widget, cập nhật các sự kiện của pygame
        if widget:
            pygame.event.pump()
        # Lấy phần tử có chi phí thấp nhất từ heap
        _, curr_cost, state, pos, depth, path = heappop(heap)
        # Đánh dấu trạng thái hiện tại đã được thấy
        seen.add(state)
        # Thử các hướng di chuyển có thể
        for move in moves:
            # Kiểm tra nếu di chuyển có thể thực hiện được và không dẫn đến deadlock
            new_state, move_cost = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            if new_state in seen or deadlock:
                continue
            # Tính toán vị trí mới
            new_pos = pos[0] + move[0], pos[1] + move[1]
            if heuristic == 'manhattan':
                # Tính chi phí mới nếu sử dụng heuristic Manhattan
                new_cost = manhattan_sum(new_state, new_pos, shape)
            # Nếu chi phí mới là vô cực, bỏ qua
            if new_cost == float('inf'):
                continue
            # Thêm trạng thái mới vào heap
            heappush(heap, (
                move_cost + curr_cost,
                new_cost,
                new_state,
                new_pos,
                depth + 1,
                path + direction[move],
            ))
            # Kiểm tra nếu trạng thái mới là lời giải
            if is_solved(new_state):
                print(f'{heur} Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'{heur} Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return (path + direction[move], depth + 1)
            # Cập nhật giao diện đồ họa nếu có
            if widget and visualizer:
                widget.set_text(f'{heur} Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    # Nếu không tìm thấy lời giải
    print(f'{heur} Solution not found!\n')
    if widget and visualizer:
        widget.set_text(f'{heur} Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return (None, -1 if not heap else depth + 1)

# Hàm giải quyết câu đố sử dụng thuật toán A*
def solve_astar(puzzle, widget=None, visualizer=False, heuristic='manhattan'):
    # Ma trận đại diện cho câu đố
    matrix = puzzle
    # Tìm vị trí của người chơi trong ma trận
    where = np.where((matrix == '*') | (matrix == '%'))
    player_pos = where[0][0], where[1][0]
    # Gọi hàm astar để giải quyết câu đố
    return astar(matrix, player_pos, widget, visualizer, heuristic)

# Đoạn mã chính để chạy thuật toán
if __name__ == '__main__':
    # Đo thời gian bắt đầu
    start = time.time()
    # Tải câu đố từ tệp và giải quyết bằng thuật toán A* với heuristic Manhattan
    solve_astar(np.loadtxt('levels/lvl5.dat', dtype='<U1'), heuristic='manhattan')
    # In ra thời gian chạy của thuật toán
    print(f'Runtime: {time.time() - start} seconds')
