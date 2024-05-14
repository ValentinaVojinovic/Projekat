import pygame
from pygame.locals import *
import random

pygame.init()

# Ekran igrice
width = 480
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Snake Game')

# Grid varijable
grid_size = 20
num_rows = width // grid_size
num_cols = height // grid_size

# Pravac kretanja
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

# Boje
black = (0, 0, 0)
blue = (25, 103, 181)
dark_green = (67, 160, 71)
light_green = (129, 199, 132)
red = (200, 0, 0)
white = (255, 255, 255)

# Varijable igrice
score = 0
gameover = False

# Sat
clock = pygame.time.Clock()
fps = 10

class Apple:

    def __init__(self):
        self.randomize_location()

    def randomize_location(self):
        random_x = random.randint(0, num_cols - 1) * grid_size
        random_y = random.randint(0, num_rows - 1) * grid_size
        self.location = (random_x, random_y)

    def draw(self):
        square = pygame.Rect(self.location, (grid_size, grid_size))
        pygame.draw.rect(screen, red, square)

class Snake:

    def __init__(self):
        self.body = [(width / 2, height / 2)]
        self.direction = right
        self.head = self.body[0]

    def turn(self, direction):

        # Zmija moze da se pomjera u svakom pravcu ako je duzina 1
        if len(self.body) == 1:
            self.direction = direction
        else:

            # Ako se pomjera lijevo ili desno , osigurati pravac
            # Prva dva "body parta" kvadrata nijesu u istoj y osi
            if direction == left or direction == right:
                if self.body[0][1] != self.body[1][1]:
                    self.direction = direction

            # Ako se pomjera gore ili dolje, osigurati isto pravac
            # Prva dva "body parta" kvadrata nijesu u istoj x osi
            if direction == up or direction == down:
                if self.body[0][0] != self.body[1][0]:
                    self.direction = direction


    def move(self):

        # Odrediti sledecu lokaciju glave
        x, y = self.direction
        next_x = (self.head[0] + x * grid_size)
        next_y = (self.head[1] + y * grid_size)

        # Ako sledeca lokacija udari u zid, prebaci se na suprotni zid
        next_x = next_x % width
        next_y = next_y % height
        next_location = (next_x, next_y)

        # Dodaj novu lokaciju glave na pocetak liste
        self.body.insert(0, next_location)
        self.head = self.body[0]

        # Proveri da li je jabuka na lokaciji glave
        if self.head == apple.location:

            # Pomjeriti jabuku na sledecu lokaciju
            apple.randomize_location()

            # Osigurajte da nova lokacija jabuke nije tamo gde je zmija
            while apple.location in self.body:
                apple.randomize_location()

        else:

            # Ukloniti poslednji deo tela iz liste
            self.body.pop()

    def check_collision(self):

        # Proveriti da li je glava udarila u deo tela
        if self.head in self.body[1:]:
            return True
        else:
            return False


    def draw(self):
        for body_part in self.body:
            square = pygame.Rect(body_part, (grid_size, grid_size))
            pygame.draw.rect(screen, blue, square)
            pygame.draw.rect(screen, white, square, 1)

# Jabuka
apple = Apple()

# Zmija
snake = Snake()

# Loop
running = True
while running:

    clock.tick(fps)

    # Proveriti akcije dogadjaja
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:

            # Strelice za pomjeranje zmije
            if event.key == K_UP:
                snake.turn(up)
            elif event.key == K_DOWN:
                snake.turn(down)
            elif event.key == K_LEFT:
                snake.turn(left)
            elif event.key == K_RIGHT:
                snake.turn(right)

    # Pozadina
    for x in range(num_cols):
        for y in range(num_rows):

            # Stvaranje kvadrata za grid
            square = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))

            # Naizmenične boje za pozadinu
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, dark_green, square)
            else:
                pygame.draw.rect(screen, light_green, square)

    # Jabuka
    apple.draw()

    # Pomjeranje zmije
    snake.move()

    # Zmija
    snake.draw()

    # Display za score
    font = pygame.font.SysFont('monoface', 16)
    text = font.render("Score: {0}".format(len(snake.body)), 1, black)
    screen.blit(text, (5, 10))

    # Provera sudara
    collision = snake.check_collision()
    if collision:
        gameover = True

    # Stanje kada je igra završena
    while gameover:

        clock.tick(fps)

        # Nacrtate gameover tekst
        pygame.draw.rect(screen, black, (0, height / 2 - 50, width, 100))
        text = font.render("Game over! Press SPACE to play again", 1, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, height / 2)
        screen.blit(text, text_rect)
        pygame.display.update()

        # Provjera da li je korisnik izašao ili pritisnuo taster razmaknice
        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            elif event.type == KEYDOWN and event.key == K_SPACE:

                # Reset igrice
                gameover = False
                score = 0
                snake.body = [(width / 2, height / 2)]
                snake.direction = right
                snake.head = snake.body[0]
                apple.randomize_location()

    pygame.display.update()

pygame.quit()