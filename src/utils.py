from heapq import heappop, heappush
import numpy as np
import pygame
import pygame_widgets 

def play_solution(solution, game, widgets, show_solution, moves):
    """
    Phát lại giải pháp cho trò chơi.

    Parameters:
        - solution (list): Danh sách các bước di chuyển để giải quyết trò chơi.
        - game: Đối tượng trò chơi.
        - widgets (dict): Tập hợp các widget của giao diện người dùng.
        - show_solution (bool): Cờ hiển thị giải pháp trên màn hình.
        - moves (int): Số lượng bước di chuyển.
    """
    for move in solution:
        events = pygame.event.get()  # Lấy các sự kiện từ hàng đợi sự kiện của pygame.
        moves += game.player.update(move)  # Cập nhật trạng thái của người chơi dựa trên bước di chuyển.
        game.floor_group.draw(game.window)  # Vẽ các ô mặt đất lên màn hình trò chơi.
        game.goal_group.draw(game.window)  # Vẽ các mục tiêu lên màn hình trò chơi.
        game.object_group.draw(game.window)  # Vẽ các đối tượng khác lên màn hình trò chơi.
        pygame_widgets.update(events)  # Cập nhật trạng thái của các widget trong giao diện người dùng.
        widgets['label'].draw()  # Vẽ nhãn trên màn hình.
        widgets['seed'].draw()  # Vẽ hạt giống (seed) trên màn hình.
        widgets['visualizer'].draw()  # Vẽ trình visualizer trên màn hình.
        widgets['moves_label'].set_moves(f' Moves - {moves} ', 20)  # Thiết lập số lượt di chuyển trên màn hình.
        if show_solution:
            widgets['paths'].draw()  # Nếu cờ hiển thị giải pháp được bật, vẽ đường đi của giải pháp trên màn hình.
        pygame.display.update()  # Cập nhật màn hình.
        pygame.time.delay(130)  # Tạm dừng thực thi trong 130 milliseconds để giữ trò chơi chạy mượt mà.
    return moves  # Trả về tổng số lượt di chuyển sau khi phát lại giải pháp.

def print_state(state, shape):
    """
    In ra trạng thái của trò chơi.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
        - shape (tuple): Dạng của bản đồ trò chơi.
    """
    if not state:
        return
    m, n = shape
    matrix = np.array(list(state)).reshape(m, n)  # Chuyển đổi chuỗi thành ma trận để in ra trạng thái của trò chơi.
    print(matrix)

def find_boxes_and_goals(state, shape):
    """
    Tìm các hộp và mục tiêu trong trạng thái của trò chơi.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
        - shape (tuple): Dạng của bản đồ trò chơi.

    Returns:
        - boxes (list): Danh sách các vị trí của các hộp.
        - goals (list): Danh sách các vị trí của các mục tiêu.
        - boxes_on_goal (list): Danh sách các vị trí của các hộp đặt trên mục tiêu.
    """
    _, width = shape
    boxes, goals, boxes_on_goal = [], [], []
    for pos, char in enumerate(state):
        if char == '@':
            boxes.append((pos // width, pos % width))
        elif char in 'X%':
            goals.append((pos // width, pos % width))
        elif char == '$':
            boxes_on_goal.append((pos // width, pos % width))
    return boxes, goals, boxes_on_goal

def get_state(matrix):
    """
    Chuyển đổi ma trận thành chuỗi biểu diễn trạng thái của trò chơi.

    Parameters:
        - matrix (numpy.ndarray): Ma trận biểu diễn trạng thái của trò chơi.

    Returns:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
    """
    return matrix.tobytes().decode('utf-8').replace('\x00', '')

def is_solved(state):
    """
    Kiểm tra xem trạng thái của trò chơi đã được giải quyết hay chưa.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.

    Returns:
        - bool: True nếu trạng thái đã được giải quyết, False nếu ngược lại.
    """
    return '@' not in state

def manhattan_sum(state, player_pos, shape):
    """
    Tính tổng khoảng cách Manhattan giữa các hộp và mục tiêu cũng như giữa người chơi và các hộp.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
        - player_pos (tuple): Vị trí của người chơi.
        - shape (tuple): Dạng của bản đồ trò chơi.

    Returns:
        - int: Tổng khoảng cách Manhattan.
    """
    height, width = shape
    player_x, player_y = player_pos
    boxes, goals, _ = find_boxes_and_goals(state, shape)
    boxes_cost = len(boxes) * height * width
    player_cost = 0
    for box_x, box_y in boxes:
        boxes_cost += min(abs(box_x - goal_x) + abs(box_y - goal_y) for goal_x, goal_y in goals)
    player_cost = min(abs(box_x - player_x) + abs(box_y - player_y) for box_x, box_y in boxes) if boxes else 0
    return boxes_cost + player_cost

def is_deadlock(state, shape):
    """
    Kiểm tra xem trạng thái của trò chơi có bị kẹt không.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
        - shape (tuple): Dạng của bản đồ trò chơi.

    Returns:
        - bool: True nếu trạng thái bị kẹt, False nếu ngược lại.
    """
    height, width = shape
    if not state or len(state) != height * width:
        return False
    boxes, _, _ = find_boxes_and_goals(state, shape)
    for bx, by in boxes:
        box = bx * width + by
        if ((state[box - 1] == '+' and state[box - width] == '+') or
            (state[box + 1] == '+' and state[box + width] == '+') or
            (state[box + 1] == '+' and state[box - width] == '+') or
            (state[box - 1] == '+' and state[box + width] == '+')):
            return True
    double_box_positions = [
        (0, -1, -width, -width - 1),
        (0, 1, -width, -width + 1),
        (0, -1, width - 1, width),
        (0, 1, width + 1, width),
    ]
    for bx, by in boxes:
        box = bx * width + by
        for pos in double_box_positions:
            pos_set = set()
            for dir in pos:
                pos_set.add(state[box + dir])
            if pos_set in ({'@', '+'}, {'@'}, {'@', '$'}, {'@', '$', '+'}):
                return True
    box = goal = 0
    for i in range(width + 1, 2 * width - 1):
        if state[i] == '@':
            box += 1
        elif state[i] in 'X%':
            goal += 1
    if box > goal:
        return True
    box = goal = 0
    for i in range(width * (height - 2) + 1, width * (height - 2) + width - 1):
        if state[i] == '@':
            box += 1
        elif state[i] in 'X%':
            goal += 1
    if box > goal:
        return True
    box = goal = 0
    for i in range(width + 1, width * (height - 1) + 1, width):
        if state[i] == '@':
            box += 1
        elif state[i] in 'X%':
            goal += 1
    if box > goal:
        return True
    box = goal = 0
    for i in range(2 * width - 2, width * height - 2, width):
        if state[i] == '@':
            box += 1
        elif state[i] in 'X%':
            goal += 1
    if box > goal:
        return True
    return False

def can_move(state, shape, player_pos, move):
    """
    Kiểm tra xem có thể thực hiện bước di chuyển cho người chơi không.

    Parameters:
        - state (str): Chuỗi biểu diễn trạng thái của trò chơi.
        - shape (tuple): Dạng của bản đồ trò chơi.
        - player_pos (tuple): Vị trí hiện tại của người chơi.
        - move (tuple): Bước di chuyển cần kiểm tra.

    Returns:
        - new_state (str): Chuỗi biểu diễn trạng thái mới nếu bước di chuyển có thể được thực hiện, None nếu không thể.
        - move_cost (int): Chi phí của bước di chuyển.
    """
    new_state = list(state)
    x, y = player_pos
    _, width = shape
    move_cost = 0
    target = x + move[0], y + move[1]
    boxtarget = x + move[0] * 2, y + move[1] * 2
    curr1d = x * width + y
    target1d = target[0] * width + target[1]
    boxtarget1d = boxtarget[0] * width + boxtarget[1]
    if state[target1d] == '+':
        return None, move_cost
    elif state[target1d] in '-X':
        new_state[curr1d] = '-' if new_state[curr1d] == '*' else 'X'
        new_state[target1d] = '*' if new_state[target1d] == '-' else '%'
        move_cost = 3
    elif state[target1d] in '@$':
        if state[boxtarget1d] in '+@$':
            return None, move_cost
        elif state[boxtarget1d] in '-X':
            new_state[boxtarget1d] = '@' if new_state[boxtarget1d] == '-' else '$'
            new_state[target1d] = '*' if new_state[target1d] == '@' else '%'
            new_state[curr1d] = '-' if new_state[curr1d] == '*' else 'X'
            move_cost = 0 if new_state[boxtarget1d] == '$' else 2
    return ''.join(new_state), move_cost
