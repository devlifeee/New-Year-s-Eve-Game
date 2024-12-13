#подключние бибилиотек
import pygame 
import random

#инициализация Pygame
pygame.init()

#константы-параметры окна
display_width = 1200
display_height = 700

#pygame.mixer.music.load("lvl1/music/music.mp3")
#pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(0.3)



#класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #компоненты скорости по оси X и Y
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        # Обновление позиции игрока
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity




display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Новогодняя игра")



# Иконку можно добавить используя следующий код
#icon = pygame.image.load("img\catikonka.png")
#pygame.display.set_icon(icon)

# Класс для представления камней
stone_img = [pygame.image.load("img/rock 2.png"), pygame.image.load("img/rock 2.png"), pygame.image.load("img/rock 2.png")]
stone_option = [110, 470, 130, 450, 70, 510]

cate_img = [pygame.image.load("img/cat stand 1 (1).png"),pygame.image.load("img/cat stand 3 (1).png"), 
            pygame.image.load("img/cat stand 4.png"),pygame.image.load("img/cat stay 2.png") ]

jump_count = 0
img_counter = 0
player_speed = 5
player_x = 150

class Stone:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y 
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


user_width = 90
user_height = 60
user_x = display_width // 3
user_y = display_height - user_height - 100

clock = pygame.time.Clock()
stone_width = 60
stone_height = 50
stone_x = display_width - 100
stone_y = display_height - stone_height + 300

make_jump = False
jump_counter = 30

def run_game():
    global make_jump
    game = True

    stone_arr = []
    create_stone_arr(stone_arr)
    land = pygame.image.load("img\Background.jpg")
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()
        if jump_count >= 15:
            game = game_over()
        display.blit(land, (0, 0))
        draw_array(stone_arr)
        draw_cat()
        if cheak_collision(stone_arr):
            game = game_over()
        pygame.display.update()
        clock.tick(60)
    return game_over()

def jump():
    global user_y, jump_counter, make_jump
    if jump_counter >= -30:
        user_y -= jump_counter / 1.7
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False
    
    def jump():
        global user_y, jump_counter, make_jump, jump_count
        jump_count += 1

def create_stone_arr(array):
    choice = random.randrange(0, 3)
    img = stone_img[choice]
    width = stone_option[choice * 2]
    height = stone_option[choice * 2 + 1]
    array.append(Stone(display_width + 60, height + 7, width, img, 4))

def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    
    if maximum < display_width:
        radius = display_width
        if radius - maximum < 100:
            radius += 200
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(15, 20)
    else:
        radius += random.randrange(200, 360)

    return radius

#вывод текста
def print_text(massage, x , y , font_color= (0,0,0) , font_type = "shrifts/Indico.otf" , font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(massage, True, font_color)
    display.blit (text, (x , y))

#барьеры
def cheak_collision(barriers):
    cat_rect = pygame.Rect(user_x, user_y, user_width, user_height)
    for barrier in barriers:
        barrier_rect = pygame.Rect(barrier.x, barrier.y, barrier.width, barrier.image.get_height())
        if cat_rect.colliderect(barrier_rect):
            run_game = False  # Завершение игры
            return  # Выход из функции, чтобы не проверять другие камни

    return  # Нет столкновений
#пауза
def pause():

    pygame.mixer.music.pause()
    
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Paused. Press enter to continue", 320, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pause = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()

def draw_array(array):
    for stone in array:
        check = stone.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = stone_img[choice]
            width = stone_option[choice * 2]
            height = stone_option[choice * 2 + 1]

            stone.return_self(radius, height, width, img)
#моделька кота
def draw_cat():
    global img_counter
    if img_counter == 20:
        img_counter = 0
    display.blit(cate_img[img_counter // 5], (user_x , user_y - 20))
    img_counter += 1

#завершение игры при проигрыше
def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("The game is over. Press Enter to play again or Esc to exit.", 50, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)

while run_game():
    pass
pygame.quit()
quit()