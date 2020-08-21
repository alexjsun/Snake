""" Snake game implementation in Python """
import random
import pygame

class Square():
    """ Square object for making the snake segments and food """
    def __init__(self, x_pos, y_pos, horizontal, vertical, color, width=20, height=20):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.horizontal = horizontal
        self.vertical = vertical
        self.color = color
        self.width = width
        self.height = height

    def draw_square(self, surface):
        """ Draws an individual square """
        pygame.draw.rect(surface, self.color, (self.x_pos, self.y_pos, self.width, self.height))

    def move_square(self, x_pos, y_pos, horizontal, vertical):
        """ Moves individual squares based on position """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.horizontal = horizontal
        self.vertical = vertical

class Snake():
    """ Snake Object """
    def __init__(self, color, dis_width, dis_height):
        self.color = color
        self.head = Square(dis_width // 2, dis_height // 2, 0, 1, color)
        self.body = []
        self.body.append(self.head)
        self.horizontal = 0 # Snake is not moving horizontally (1 denotes right, -1 denotes left)
        self.vertical = 1 # Snake is moving up (-1 denotes down, 0 denotes no vertical movement)

    def move(self):
        """ Moves the snake using key buttons """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.horizontal == 0:
                    self.horizontal = -1
                    self.vertical = 0
                if event.key == pygame.K_RIGHT and self.horizontal == 0:
                    self.horizontal = 1
                    self.vertical = 0
                if event.key == pygame.K_UP and self.vertical == 0:
                    self.horizontal = 0
                    self.vertical = 1
                if event.key == pygame.K_DOWN and self.vertical == 0:
                    self.horizontal = 0
                    self.vertical = -1
        for i in range(len(self.body)):
            tmp_x = self.body[i].x_pos
            tmp_y = self.body[i].y_pos
            tmp_h = self.body[i].horizontal
            tmp_v = self.body[i].vertical
            if i == 0:
                prev_x = self.head.x_pos
                prev_y = self.head.y_pos
                prev_h = self.head.horizontal
                prev_v = self.head.vertical
                dx = self.horizontal * self.head.width
                dy = self.vertical * self.head.height
                self.head.move_square(prev_x + dx, prev_y - dy, self.horizontal, self.vertical)
            else: 
                self.body[i].move_square(prev_x, prev_y, prev_h, prev_v)
                prev_x = tmp_x
                prev_y = tmp_y
                prev_h = tmp_h
                prev_v = tmp_v

    def draw_snake(self, surface):
        """ Draws the snake """
        for i in range(len(self.body)):
            self.body[i].draw_square(surface)

    def reset(self, dis_width, dis_height, color):
        """ Resets the game """
        self.head = Square(dis_width // 2, dis_height // 2, 0, 1, color)
        self.body = []
        self.body.append(self.head)
        self.horizontal = 0
        self.vertical = 1

    def check_collision(self, dis_width, dis_height):
        """ Checks if the snake collides with itself or the display boundaries
            (True if collision occurs, False otherwise) """
        if (self.head.x_pos < 0 or self.head.x_pos > dis_width - self.head.width or
                self.head.y_pos < 0 or self.head.y_pos > dis_height - self.head.height):
            return True
        for i in range(1, len(self.body)):
            if (self.head.x_pos == self.body[i].x_pos and self.head.y_pos == self.body[i].y_pos):
                return True
        return False

    def add_square(self, width, height):
        """ Adds a square to the tail of the snake """
        last = self.body[-1]
        if last.horizontal == 1 and last.vertical == 0:
            self.body.append(Square(last.x_pos - width, last.y_pos, 1, 0, last.color))
        if last.horizontal == -1 and last.vertical == 0:
            self.body.append(Square(last.x_pos + width, last.y_pos, -1, 0, last.color))
        if last.horizontal == 0 and last.vertical == 1:
            self.body.append(Square(last.x_pos, last.y_pos + height, 0, 1, last.color))
        if last.horizontal == 0 and last.vertical == -1:
            self.body.append(Square(last.x_pos, last.y_pos - height, 0, -1, last.color))

def new_snack(nrows, snake, color):
    """ Generates a new snack at a random location """
    invalid_pos = 0
    while True:
        new_x = random.randrange(nrows) * snake.body[0].width
        new_y = random.randrange(nrows) * snake.body[0].height
        for i in range(len(snake.body)):
            if new_x == snake.body[i].x_pos and new_y == snake.body[i].y_pos:
                invalid_pos += 1
                break
        if invalid_pos == 0:
            break
    return Square(new_x, new_y, 0, 0, color)


def draw_gridlines(dis_len, side_len, surface):
    """ Draws the gridlines on the surface """
    x = 0
    y = 0
    lines = (dis_len // side_len) - 1
    for line in range(lines):
        x += side_len
        y += side_len
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, dis_len))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (dis_len, x))

def main():
    """ Runs the game loop """
    pygame.init()
    dis_x = 600
    dis_y = 600
    dis = pygame.display.set_mode((dis_x, dis_y))
    green = (0, 255, 0)
    black = (0, 0, 0)
    red = (255, 0, 0)

    snake = Snake(green, dis_x, dis_y)
    snack = new_snack(dis_x // snake.head.width, snake, red)
    pygame.display.update()
    pygame.display.set_caption('Snake by alexjsun')

    clock = pygame.time.Clock()

    game_over = False
    while not game_over:
        pygame.time.delay(60)
        clock.tick(10)
        snake.move()
        score = 0
        if snake.head.x_pos == snack.x_pos and snake.head.y_pos == snack.y_pos:
            score = score + 1
            snake.add_square(snake.head.width, snake.head.height)
            snack = new_snack(30, snake, red)
        if snake.check_collision(dis_x, dis_y):
            print("Your score: " + str(score))
            snake.reset(dis_x, dis_y, green)
        dis.fill(black)
        snake.draw_snake(dis)
        snack.draw_square(dis)
        draw_gridlines(dis_x, snack.width, dis)
        pygame.display.update()

    pygame.quit()
    quit()

main()
