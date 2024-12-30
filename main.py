import pygame
import sys

import pygame.image


right_walking, left_walking = False, False

def main():
    global right_walking, left_walking

    # Initialize Pygame
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Guardians of Al-Qalaa: Legacy of Qatar")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # Fonts
    font = pygame.font.Font("font/Amiri-Regular.ttf", 25)
    large_font = pygame.font.Font("font/Amiri-Regular.ttf", 40)

    # Game states
    START_SCREEN = 0
    QUIZ = 1
    GATE_OPENING = 2
    FINISHED = 3
    DEFEAT = 4
    WALKING = 5

    state = START_SCREEN
    
    # Game loop state
    running = True

    # Sprites
    desert_background = pygame.image.load("images/desert_bg.png")
    knight = pygame.image.load("images/knight.png")
    falcon = pygame.image.load("images/falcon.png")
    gate = pygame.image.load("images/gate.png")
    without_falcon = pygame.image.load("images/without_falcon.png")
    castle = pygame.image.load("images/castle.png")

    # Audio
    desert_theme = pygame.mixer.Sound("audio/desert_theme.mp3")
    desert_theme.play(-1)

    # Knight
    knight_x = 1
    knignt_speed = 2

    # UI
    retry = pygame.image.load("images/retry.png")
    retry_rect = retry.get_rect()
    retry_rect.center = (screen.get_width() - 50, screen.get_height() - 50)

    # Time management
    clock = pygame.time.Clock()

    # Game variables
    current_question = 0
    questions = [
        {
            "question": "أخبرني، أيها الفارس—ما الرمز الذي كان يمثل الولاء، والحرية، والبصيرة الحادة اللازمة لقيادة القبيلة عبر الصحراء الشاسعة؟"[::-1],
            "options": ["A. اللؤلؤ"[::-1], "B. الصقر"[::-1], "C. السيف"[::-1], "D. النخيل"[::-1]],
            "correct": 1  # Index of correct option
        },
        {
            "question": "البوابة لم تفتح بعد، لدخول القلعة يجب ان تخبرني أيها الفارس ما هي الصفة التي يجب ان يتمتع بها القائد لتوحيد وحماية شعبه؟"[::-1],
            "options": ["A. الكرم"[::-1], "B. القوة"[::-1], "C. الحكمة"[::-1], "D. الشجاعة"[::-1]],
            "correct": 2  # Index of correct option
        },
    ]


    # Gate variables
    gate_y = screen.get_height() - gate.get_height() + 150
    gate_speed = 2
    gate_target_position = gate_y  # Target position of the gate
    gate_increment = 150  # Amount to move the gate per correct answer
    gate_moving = False

    
    # User's answer
    user_answer = -1
    
    rotated_image = knight
    # Main game loop
    while running:  
        

        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and state == QUIZ:

                if event.key == pygame.K_a:
                    user_answer = 0
                elif event.key == pygame.K_b:
                    user_answer = 1
                elif event.key == pygame.K_c:
                    user_answer = 2
                elif event.key == pygame.K_d:
                    user_answer = 3

                if user_answer != -1:
                    if check_answer(questions[current_question], user_answer):
                        if current_question < len(questions) - 1:
                            current_question += 1
                            gate_target_position -= gate_increment  # Move gate a bit
                            gate_moving = True
                            user_answer = -1  # Reset the answer
                        else:
                            gate_target_position = 100  # Open gate fully after last question
                            gate_moving = True
                            state = GATE_OPENING  # Proceed to gate opening phase
                    else:
                        state = DEFEAT


            elif event.type == pygame.KEYDOWN and state == WALKING:
                if event.key == pygame.K_RIGHT:
                    right_walking = True
                elif event.key == pygame.K_LEFT:
                    left_walking = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_walking = False
                elif event.key == pygame.K_LEFT:
                    left_walking = False
                elif event.key == pygame.K_f:
                    right_walking = False
                    left_walking = False

                    state = QUIZ

        if state == START_SCREEN:
            draw_text(screen, "حراس القلعة – تراث قطر"[::-1],
                      (screen.get_width() - large_font.size("حراس القلعة – تراث قطر"[::-1])[0]) // 2,
                      (screen.get_height() - large_font.size("حراس القلعة – تراث قطر"[::-1])[0] // 2 - 120),
                      large_font, BLUE)

            draw_text(screen, "اضغط على "[::-1] + " Enter " + " للبدء.."[::-1],
                      (screen.get_width() - font.size("اضغط على  Enter  للبدء..")[0]) // 2,
                      ((screen.get_height() - large_font.size("حراس القلعة – تراث قطر"[::-1])[0] // 2) + 100),
                      font, BLACK)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = WALKING

        elif state == WALKING:
            
            if right_walking and not knight_x > 100:
                rotated_image = pygame.transform.flip(knight, False, False)
                knight_x += knignt_speed
            elif left_walking and not knight_x < 0:
                rotated_image = pygame.transform.flip(knight, True, False)
                knight_x -= knignt_speed

            screen.blit(desert_background, ((screen.get_width() - desert_background.get_width()) // 2,
                                            (screen.get_height() - desert_background.get_height()) // 2))
            

            screen.blit(rotated_image, (knight_x, (screen.get_height() - knight.get_height())))
            
            screen.blit(without_falcon,((screen.get_width() - 320), (screen.get_height() - falcon.get_height() + 10)))
            screen.blit(castle, ((screen.get_width() - 120), (screen.get_height() - castle.get_height())))
            screen.blit(gate, ((screen.get_width() - 200), gate_y))
                        
            draw_text(screen, "اضغط F للبدء"[::-1], (screen.get_width() - font.size("اضغط F للبدء"[::-1])[0]) // 2, 30, font, WHITE)


        elif state == QUIZ:  
            screen.blit(desert_background, ((screen.get_width() - desert_background.get_width()) // 2,
                                            (screen.get_height() - desert_background.get_height()) // 2))
            screen.blit(knight, (knight_x, (screen.get_height() - knight.get_height())))
            screen.blit(falcon, ((screen.get_width() - 320), (screen.get_height() - falcon.get_height())))
            screen.blit(castle, ((screen.get_width() - 120), (screen.get_height() - castle.get_height())))
            screen.blit(gate, ((screen.get_width() - 200), gate_y))

            display_question(screen, questions[current_question], font, WHITE, BLACK)

        elif state == GATE_OPENING:
            
            knight_x += knignt_speed

            screen.blit(desert_background, ((screen.get_width() - desert_background.get_width()) // 2,
                                            (screen.get_height() - desert_background.get_height()) // 2))
            screen.blit(falcon, ((screen.get_width() - 320), (screen.get_height() - falcon.get_height())))
            screen.blit(castle, ((screen.get_width() - 120), (screen.get_height() - castle.get_height())))
            screen.blit(gate, ((screen.get_width() - 200), gate_y))
            screen.blit(rotated_image, (knight_x, (screen.get_height() - knight.get_height())))
            
            draw_text(screen, "تم فتح البوابة. يمكنك الدخول أيها الفارس الشجاع"[::-1], (screen.get_width() - font.size("تم فتح البوابة. يمكنك الدخول أيها الفارس الشجاع"[::-1])[0]) // 2, 30, font, WHITE)

            if gate_y > -100:
                gate_y -= gate_speed  # Continue moving gate until it's fully opened

        elif state == FINISHED:
            pygame.quit()
            sys.exit()

        elif state == DEFEAT:
            screen.blit(desert_background, ((screen.get_width() - desert_background.get_width()) // 2,
                                        (screen.get_height() - desert_background.get_height()) // 2))

            screen.blit(without_falcon,((screen.get_width() - 300), (screen.get_height() - falcon.get_height() + 10)))
            screen.blit(castle, ((screen.get_width() - 120), (screen.get_height() - castle.get_height())))
            screen.blit(gate, ((screen.get_width() - 200), gate_y))

            draw_text(screen, 'أنت تهزم الفارس'[::-1], (screen.get_width() - font.size("أنت تهزم الفارس"[::-1])[0]) // 2, 30, font, WHITE)


        if gate_moving:
            if gate_y > gate_target_position:  # Move the gate until it reaches the target position
                gate_y -= gate_speed
            else:
                gate_moving = False  # Stop moving when the gate reaches its target

        screen.blit(retry, retry_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_rect.collidepoint(event.pos):
                user_answer = -1
                current_question = 0
                gate_y = screen.get_height() - gate.get_height() + 150
                gate_target_position = gate_y
                desert_theme.stop()
                desert_theme.play(-1)
                knight_x = 1

                state = WALKING

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_text(screen, text, x, y, font, color=()):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_text_wrapped_centered(screen, text, y, font, color, max_width):
    """Render wrapped and centered text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = words[0]
    
    # Break the text into lines
    for word in words[1:]:
        # Test line width with the new word
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    # Render each line centered
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_width = text_surface.get_width()
        x = (screen.get_width() - text_width) // 2  # Center the line horizontally
        screen.blit(text_surface, (x, y + i * font.get_height()))

def display_question(screen, question_data, font, question_color, option_color):
    """Display the question and options."""
    draw_text_wrapped_centered(screen, question_data["question"], 20, font, question_color, 800)
    
    for i, option in enumerate(question_data["options"]):
        draw_text(screen, option, (screen.get_width() - font.size(option)[0]) // 2, 150 + i * 50, font, option_color)

def check_answer(question_data, answer):
    return answer == question_data['correct']

if __name__ == '__main__':
    main()
