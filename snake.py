try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

WIDTH = 600
HEIGHT = 600
GRID = 10
GRID_COLOR = "DarkGreen"
BACKGROUND_COLOR = "Green"
SNAKE_COLOR = "Yellow"
game_over_text = ""
points = 0
speed = 80


class Snake:
    def __init__(self):
        self.segment_list = []
        self.position = [(WIDTH // 20, HEIGHT // 20), (WIDTH // 20, HEIGHT // 20),
                         (WIDTH // 20, HEIGHT // 20), (WIDTH // 20, HEIGHT // 20)]
        self.dir = [1, 0]
        self.eat = False

    def change_dir(self, direction):
        if direction == "right":
            self.dir[0] = 1
            self.dir[1] = 0
        elif direction == "left":
            self.dir[0] = -1
            self.dir[1] = 0
        elif direction == "up":
            self.dir[0] = 0
            self.dir[1] = -1
        elif direction == "down":
            self.dir[0] = 0
            self.dir[1] = 1

    def move(self):
        if self.position[-1][0] + self.dir[0] > WIDTH // GRID:
            self.position.append((1, self.position[-1][1] + self.dir[1]))
        elif self.position[-1][0] + self.dir[0] < 1:
            self.position.append((60, self.position[-1][1] + self.dir[1]))
        elif self.position[-1][1] + self.dir[1] > HEIGHT // GRID:
            self.position.append((self.position[-1][0] + self.dir[0], 1))
        elif self.position[-1][1] + self.dir[1] < 1:
            self.position.append((self.position[-1][0] + self.dir[0], 60))
        else:
            self.position.append((self.position[-1][0] + self.dir[0], self.position[-1][1] + self.dir[1]))

    def is_collide(self):
        global game_over_text
        for pos in self.position[0: -1]:
            if pos == self.position[-1]:
                timer.stop()
                game_over_text = "Game Over"

    def eat_apple(self):
        global apple_pos, apple_seg, points, speed
        if apple_pos == self.position[-1]:
            self.eat = True
            points += 1
            apple_pos, apple_seg = place_apple()


def place_apple():
    apple = (random.randrange(1, WIDTH // GRID), random.randrange(1, HEIGHT // GRID))
    apple_segment = [(apple[0] * GRID - GRID, apple[1] * GRID),
                     (apple[0] * GRID, apple[1] * GRID),
                     (apple[0] * GRID, apple[1] * GRID - GRID),
                     (apple[0] * GRID - GRID, apple[1] * GRID - GRID)]
    return apple, apple_segment

snake = Snake()
apple_pos, apple_seg = place_apple()


def new_game():
    global snake
    timer.stop()
    del snake
    snake = Snake
    timer.start()


def exit_button():
    timer.stop()
    quit()


def key_down(key):
    if key == simplegui.KEY_MAP['right'] and snake.dir[0] == 0:
        snake.change_dir("right")
    elif key == simplegui.KEY_MAP['left'] and snake.dir[0] == 0:
        snake.change_dir("left")
    elif key == simplegui.KEY_MAP['up'] and snake.dir[1] == 0:
        snake.change_dir("up")
    elif key == simplegui.KEY_MAP['down'] and snake.dir[1] == 0:
        snake.change_dir("down")


def timer_handler():
    snake.move()
    snake.is_collide()
    snake.eat_apple()

    if not snake.eat:
        snake.position.pop(0)
    snake.eat = False

    label.set_text("Points = " + str(points))


def draw(canvas):

    a, b, c, d = GRID, GRID, GRID, GRID
    for i in range(WIDTH // GRID):
        canvas.draw_line((a, 0), (b, HEIGHT), 1, GRID_COLOR)
        a, b = a + GRID, b + GRID
    for j in range(HEIGHT // GRID):
        canvas.draw_line((0, c), (WIDTH, d), 1, GRID_COLOR)
        c, d = c + GRID, d + GRID
    for k in snake.segment_list:
        canvas.draw_polygon(k, 1, "DarkRed", SNAKE_COLOR)

    snake.segment_list = []
    for pos in snake.position:
        segment = [(pos[0] * GRID - GRID, pos[1] * GRID),
                   (pos[0] * GRID, pos[1] * GRID),
                   (pos[0] * GRID, pos[1] * GRID - GRID),
                   (pos[0] * GRID - GRID, pos[1] * GRID - GRID)]
        snake.segment_list.append(segment)

    canvas.draw_polygon(apple_seg, 1, "DarkRed", "DarkRed")
    canvas.draw_text(game_over_text, (WIDTH // 3 - 30, HEIGHT // 3), 60, 'Red', 'serif')

# create frame and add a button and labels
frame = simplegui.create_frame("Snake", WIDTH, HEIGHT)
frame.set_canvas_background(BACKGROUND_COLOR)
frame.add_button("Exit", exit_button)

label = frame.add_label("Points = " + str(points))
timer = simplegui.create_timer(speed, timer_handler)

# register event handlers
frame.set_keydown_handler(key_down)
frame.set_draw_handler(draw)

# get things rolling
timer.start()
frame.start()
