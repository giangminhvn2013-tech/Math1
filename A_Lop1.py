import pygame
import random
import sys
import time

# --- Khởi tạo ---
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1080, 2400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toán Lớp 1 Vui Nhộn")

# --- Âm thanh ---
click_sound = pygame.mixer.Sound("click.wav")
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")

# --- Màu sắc ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BACKGROUND = (230, 240, 255)
LIGHT_BLUE = (200, 220, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 200, 200)

# --- Font ---
title_font = pygame.font.SysFont("arial", 80, bold=True)
main_font = pygame.font.SysFont("arial", 60)
small_font = pygame.font.SysFont("arial", 45)
large_font = pygame.font.SysFont("arial", 90, bold=True)
xlarge_font = pygame.font.SysFont("arial", 100, bold=True)

# --- Biến toàn cục ---
current_screen = "main_menu"
score = 0
current_question = {"a": 0, "b": 0, "operator": "+", "answer": 0}
user_answer = ""
feedback = ""
feedback_time = 0
question_count = 0
total_questions = 10
current_mode = ""
completed = False
pressed_buttons = {}

# --- Sinh câu hỏi ---
def generate_question(mode):
    operator = random.choice(["+", "-"])
    if mode == "mode1":
        if operator == "+":
            a = random.randint(0, 9)
            b = random.randint(0, 9 - a)
            answer = a + b
        else:
            a = random.randint(1, 9)
            b = random.randint(0, a)
            answer = a - b
    elif mode == "mode2":
        if operator == "+":
            a = random.randint(10, 99)
            b = random.randint(0, 9)
            answer = a + b
        else:
            a = random.randint(10, 99)
            b = random.randint(0, a % 10)
            answer = a - b
    else:
        if operator == "+":
            a = random.randint(10, 99)
            b = random.randint(0, 99)
            answer = a + b
        else:
            a = random.randint(10, 99)
            b = random.randint(0, a)
            answer = a - b
    return {"a": a, "b": b, "operator": operator, "answer": answer}

# --- Vẽ nút có hiệu ứng ---
def draw_button(text, x, y, width, height, color, hover_color,
                action=None, font=main_font, icon=None, icon_font_size=None):
    global pressed_buttons
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)
    button_id = (x, y, width, height)

    if button_id in pressed_buttons:
        if time.time() - pressed_buttons[button_id] < 0.15:
            current_color = (180, 180, 180)
        else:
            del pressed_buttons[button_id]
            current_color = color
    elif rect.collidepoint(mouse):
        if click[0] == 1:
            pressed_buttons[button_id] = time.time()
            click_sound.play()
            if action:
                action()
        current_color = hover_color
    else:
        current_color = color

    pygame.draw.rect(screen, current_color, rect, border_radius=25)
    pygame.draw.rect(screen, BLACK, rect, 3, border_radius=25)

    if icon:
        font_obj = pygame.font.SysFont("segoeuisymbol",
                                       icon_font_size if icon_font_size else font.get_height() + 20,
                                       bold=True)
        text_surf = font_obj.render(icon, True, BLACK)
    else:
        text_surf = font.render(text, True, BLACK)

    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# --- Menu chính ---
def draw_main_menu():
    screen.fill(BACKGROUND)
    title = title_font.render("Toán Lớp 1 Vui Nhộn", True, BLUE)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 100))

    draw_button("Cộng trừ 1 chữ số", WIDTH/2 - 400, 300, 800, 150,
                GREEN, LIGHT_GREEN, lambda: go_to_question_count("mode1"))
    draw_button("Cộng trừ 2 chữ số với 1 chữ số", WIDTH/2 - 400, 500, 800, 150,
                BLUE, LIGHT_BLUE, lambda: go_to_question_count("mode2"))
    draw_button("Cộng trừ 2 chữ số", WIDTH/2 - 400, 700, 800, 150,
                PURPLE, (200, 150, 255), lambda: go_to_question_count("mode3"))

    draw_button("Thoát", WIDTH/2 - 200, 900, 400, 120, RED, LIGHT_RED, exit_game)

# --- Màn hình chọn số câu hỏi ---
def draw_question_count_selection(mode):
    screen.fill(BACKGROUND)
    title = title_font.render("Chọn số câu hỏi", True, BLUE)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 100))

    mode_titles = {
        "mode1": "Cộng trừ 1 chữ số",
        "mode2": "Cộng trừ 2 chữ số với 1 chữ số",
        "mode3": "Cộng trừ 2 chữ số"
    }
    mode_text = main_font.render(f"Chế độ: {mode_titles[mode]}", True, BLACK)
    screen.blit(mode_text, (WIDTH/2 - mode_text.get_width()/2, 200))

    question_counts = [10, 20, 30, 40, 50]
    for i, count in enumerate(question_counts):
        x = WIDTH/2 - 350 + (i % 3) * 250
        y = 300 + (i // 3) * 180
        draw_button(str(count), x, y, 200, 150,
                    GREEN, LIGHT_GREEN, lambda c=count: set_question_count(c, mode))

    draw_button("Menu", WIDTH/2 - 200, 800, 400, 120,
                YELLOW, (255, 255, 150), go_to_main_menu)

# --- Vẽ phép toán theo cột ---
def draw_vertical_math_operation():
    a = current_question['a']
    b = current_question['b']
    operator = current_question['operator']

    a_str, b_str = str(a), str(b)
    max_len = max(len(a_str), len(b_str))

    digit_width = 70
    start_x = WIDTH/2 - (max_len * digit_width) / 2

    # --- Vẽ số a (từng chữ số) ---
    for i, digit in enumerate(reversed(a_str)):
        digit_text = xlarge_font.render(digit, True, BLACK)
        x = start_x + (max_len - 1 - i) * digit_width
        screen.blit(digit_text, (x, 300))

    # --- Vẽ toán tử ---
    operator_text = xlarge_font.render(operator, True, BLACK)
    operator_x = start_x - 80
    screen.blit(operator_text, (operator_x, 400))

    # --- Vẽ số b (từng chữ số) ---
    for i, digit in enumerate(reversed(b_str)):
        digit_text = xlarge_font.render(digit, True, BLACK)
        x = start_x + (max_len - 1 - i) * digit_width
        screen.blit(digit_text, (x, 400))

    # --- Vẽ đường ngang ---
    line_start_x = start_x - 40
    line_end_x = start_x + max_len * digit_width
    pygame.draw.line(screen, BLACK, (line_start_x, 500), (line_end_x, 500), 5)

    return line_start_x, max_len, line_end_x

# --- Game ---
def draw_game():
    screen.fill(BACKGROUND)
    progress_text = main_font.render(f"Câu: {question_count}/{total_questions}", True, BLACK)
    screen.blit(progress_text, (50, 50))
    score_text = main_font.render(f"Điểm: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 50, 50))

    line_start_x, max_digits, line_end_x = draw_vertical_math_operation()

    min_digits = 2 if current_mode in ["mode1", "mode2"] else 3
    answer_box_width = max(min_digits, max_digits) * 70 + 20
    answer_box_x = line_end_x - answer_box_width
    answer_box_y = 540

    pygame.draw.rect(screen, WHITE, (answer_box_x, answer_box_y,
                                     answer_box_width, 120), border_radius=15)
    pygame.draw.rect(screen, BLACK, (answer_box_x, answer_box_y,
                                     answer_box_width, 120), 4, border_radius=15)

    # --- Vẽ user_answer theo cột ---
    for i, digit in enumerate(reversed(user_answer)):
        digit_text = xlarge_font.render(digit, True, BLACK)
        x = line_end_x - (i + 1) * 70
        y = answer_box_y + (120 - digit_text.get_height()) // 2
        screen.blit(digit_text, (x, y))

    if feedback and time.time() - feedback_time < 2.5:
        feedback_color = GREEN if feedback.startswith("Đúng") else RED
        feedback_text = large_font.render(feedback, True, feedback_color)
        screen.blit(feedback_text, (WIDTH/2 - feedback_text.get_width()/2, answer_box_y + 300))

    draw_number_pad(answer_box_y + 400)

# --- Bàn phím số ---
def draw_number_pad(start_y=900):
    cols = 3
    spacing = 30
    button_width = (WIDTH - (cols + 1) * spacing) / cols
    button_height = 160
    start_x = spacing

    rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]]
    for row_idx, row in enumerate(rows):
        for col_idx, num in enumerate(row):
            x = start_x + col_idx * (button_width + spacing)
            y = start_y + row_idx * (button_height + spacing)
            draw_button(num, x, y, button_width, button_height,
                        WHITE, LIGHT_BLUE, lambda n=num: number_click(n), xlarge_font)

    y_last = start_y + 3 * (button_height + spacing)
    draw_button("0", start_x, y_last, button_width, button_height,
                WHITE, LIGHT_BLUE, lambda: number_click("0"), xlarge_font)
    draw_button("", start_x + (button_width + spacing), y_last,
                button_width, button_height, PINK, LIGHT_RED, backspace, None, "⌫", 80)
    draw_button("", start_x + 2 * (button_width + spacing), y_last,
                button_width, button_height, GREEN, LIGHT_GREEN, check_answer, None, "✓", 80)

    y_menu = y_last + button_height + spacing
    draw_button("Menu", start_x, y_menu,
                button_width * 3 + spacing * 2, button_height,
                YELLOW, (255,255,150), go_to_main_menu)

# --- Các hàm phụ ---
def number_click(number):
    global user_answer
    max_length = 3 if current_mode == "mode3" else 2
    if len(user_answer) < max_length:
        user_answer += number

def backspace():
    global user_answer
    if user_answer:
        user_answer = user_answer[:-1]

def check_answer():
    global score, user_answer, feedback, feedback_time, current_question, question_count, completed, current_screen
    if user_answer and user_answer.isdigit():
        if int(user_answer) == current_question["answer"]:
            feedback = "Đúng!"
            score += 1
            correct_sound.play()
        else:
            feedback = f"Sai! Đáp án: {current_question['answer']}"
            wrong_sound.play()
        feedback_time = time.time()
        question_count += 1
        user_answer = ""
        if question_count >= total_questions:
            completed = True
            current_screen = "results"
        else:
            current_question = generate_question(current_mode)

def go_to_main_menu():
    global current_screen, score, question_count, completed
    current_screen = "main_menu"
    score = 0
    question_count = 0
    completed = False

def exit_game():
    pygame.quit()
    sys.exit()

def go_to_question_count(mode):
    global current_screen, current_mode
    current_screen = "question_count"
    current_mode = mode

def set_question_count(count, mode):
    global total_questions
    total_questions = count
    start_game(mode)

def start_game(mode):
    global current_screen, current_question, user_answer, current_mode, question_count, score, completed
    current_screen = "game"
    current_mode = mode
    current_question = generate_question(mode)
    user_answer = ""
    question_count = 0
    score = 0
    completed = False

# --- Kết quả ---
def draw_results():
    screen.fill(BACKGROUND)
    title = title_font.render("Kết Quả Học Tập", True, BLUE)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 200))

    score_text = main_font.render(f"Điểm: {score}/{total_questions}", True, BLACK)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 350))

    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    percent_text = main_font.render(f"Tỷ lệ đúng: {percentage:.1f}%", True, BLACK)
    screen.blit(percent_text, (WIDTH/2 - percent_text.get_width()/2, 450))

    if percentage >= 90:
        comment = "Xuất sắc! Em học rất giỏi!"
        color = GREEN
    elif percentage >= 70:
        comment = "Tốt! Em đã hiểu bài rất tốt!"
        color = BLUE
    elif percentage >= 50:
        comment = "Khá! Em cần luyện tập thêm nhé!"
        color = ORANGE
    else:
        comment = "Cần cố gắng hơn! Em hãy luyện tập lại nhé!"
        color = RED

    comment_text = main_font.render(comment, True, color)
    screen.blit(comment_text, (WIDTH/2 - comment_text.get_width()/2, 550))

    draw_button("Menu", WIDTH/2 - 300, 750, 600, 150,
                YELLOW, (255, 255, 150), go_to_main_menu)

# --- Main loop ---
def main():
    global current_screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_screen == "main_menu":
            draw_main_menu()
        elif current_screen == "question_count":
            draw_question_count_selection(current_mode)
        elif current_screen == "game":
            draw_game()
        elif current_screen == "results":
            draw_results()

        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
