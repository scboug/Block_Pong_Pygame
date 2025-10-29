import random
from multiprocessing.util import log_to_stderr
import pygame
from pygame.examples.grid import TITLE

pygame.init()

"""Screen dimensions"""
screen_width = 1080
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) #Creating the GUI window size.
pygame.display.set_caption("Block Pong") #Labelling the GUI window.

class Paddle:
    """Class for all functionality for the paddle."""
    def __init__(self, x, y, width, height, colour):
        """The dimensions of the paddle."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def create_paddle(self, screen):
        """Draws the paddle on the screen."""
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def collision(self):
        """Used to check if the paddle collides."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def paddle_left(self, cx):
        """
        Moves the paddle left.
        cx = defines how much the paddle moves left
        """
        if self.x > 0: #Checks if the paddle is at the left edge of the screen.
            self.x += cx

    def paddle_right(self, cx):
        """
        Moves the paddle right.
        cx = defines how much the paddle moves right.
        """
        if self.x < 1080 - self.width: #Checks if the paddle is at the right edge of the screen.
            self.x += cx

class Ball:
    """Class for all functionality for the ball."""
    def __init__(self, x, y, radius, width, colour, sx, sy):
        """The dimensions of the ball."""
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.colour = colour
        self.sx = sx
        self.sy = sy

    def create_ball(self, screen):
        """Draws the ball on the screen."""
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius, self.width)

    def collision(self):
        """Used to check if the ball collides."""
        return pygame.Rect(self.x, self.y, self.radius, self.width)

    def movement(self):
        """Constantly moves the ball."""
        self.x += self.sx
        self.y += self.sy

    def direction_change_vertical(self):
        """Changes the balls direction along the y-axis"""
        self.sy *= -1

    def direction_change_horizontal(self):
        """Changes the ball direction along the x-axis"""
        self.sx *= -1

    def speed_increase(self):
        """Increases the speed of the ball by 5%"""
        self.sy *= 1.05
        self.sx *= 1.05

    def speed_reset(self):
        """Resets the speed of the ball."""
        self.sx = 5
        self.sy = 5

    def ball_reset(self, x, y):
        """Resets the ball position."""
        self.x = x
        self.y = y

class Block:
    """Class for all functionality for the block."""
    def __init__(self, x, y, width, height, colour):
        """The dimensions of the block."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def create_block(self, screen):
        """Draws the block on the screen."""
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def collision(self):
        """Used to check if the block collides."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def relocate(self, s_width, s_height):
        """Relocates the block randomly in the top half of the screen."""
        self.x = random.randint(0, s_width - self.width) #generates a random x value between 0 and the screen width
        # - the block width so its fully in side.
        self.y = random.randint(0, s_height // 2) #generates a random y value between 0 and half the screen height.


ball = Ball(300, 200, 15, 15, (255, 255, 255), 5, 5) #Defining the ball.
user_paddle = Paddle(400, 700, 250,50, colour=(255, 255, 255)) #Defining the paddle.
block = Block(300, 50, 50, 50, colour=(255, 255, 255)) #Defining the block.

"""Loading in Sounds."""
pygame.mixer.init()
block_hit = pygame.mixer.Sound("Block_smash.mp3")
bounce = pygame.mixer.Sound("Ball_bounce.mp3")
ball_dropped = pygame.mixer.Sound("ball_dropped.mp3")
wrong_input = pygame.mixer.Sound("error-126627.mp3")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 100) #Font used.
player_score = 0

game_loop = True
run = False

while game_loop:
    """The home menu/ navigation menu loop."""
    menu_display = font.render("Press the Space bar to start", True,(255, 255, 255))
    screen.blit(menu_display, (screen_width / 10, screen_height / 2))
    menu1_display = font.render("or Escape to quit", True, (255, 255, 255))
    screen.blit(menu1_display, (screen_width / 10, screen_height / 1.5))

    """Checks the User input and checks if to start of exit the application."""
    menu_key = pygame.key.get_pressed()
    if menu_key[pygame.K_SPACE]:
        run = True
        player_score = 0
    elif menu_key[pygame.K_ESCAPE]:
        game_loop = False

    pygame.display.update()

    while run:
        """The game loop"""
        screen.fill((0, 0, 0)) #Resets the window with black every frame.
        clock.tick(60) #Controls the frames per second.

        score_display = font.render("Player Score: " + str(player_score),
                                    True, (255, 255, 255)) #Defines how the scoreboard looks.
        screen.blit(score_display, (screen_width / 3, screen_height / 2)) #Draws the score board on the screen.

        user_paddle.create_paddle(screen) #Draws the paddle on screen.
        ball.create_ball(screen) #Draws the ball on screen.
        block.create_block(screen) #Draws the ball on screen.

        keys = pygame.key.get_pressed() #Taking in the user key input.

        """Check if the user input is <- or -> arrow keys."""
        if keys[pygame.K_LEFT]:
            user_paddle.paddle_left(-5) #Moves paddle left -5 on the x-axis.
        elif keys[pygame.K_RIGHT]:
            user_paddle.paddle_right(5) #Moves the paddle right +5 on the x-axis.

        ball.movement() #Makes the ball constantly move.

        """Checks if the ball hits the top of the screen."""
        if ball.y <= 0 + 15:
            ball.direction_change_vertical() #Changes the ball vertical direction (bounces ball off top).
            bounce.play() #Plays sound.

        """Checks if the ball hits the bottom of the screen."""
        if ball.y > screen_height:
            game_over = font.render("Game Over!", True, "firebrick1")
            screen.blit(game_over, (screen_width / 3, screen_height / 3)) #Displays "Game Over"
            ball_dropped.play() #Plays sound.
            run = False

        """Checks if the ball hit the left or right of the screen."""
        if ball.x >= screen_width - 15 or ball.x <= 0 + 15:
            ball.direction_change_horizontal() #Changes the ball horizontal direction (bounces ball off sides).
            bounce.play() #Plays sound.

        """Checks if the ball collides with the paddle."""
        if user_paddle.collision().colliderect(ball.collision()):
            ball.direction_change_vertical() #Changes the balls vertical direction (bounces the bal up off the paddle).
            bounce.play() #Plays sound.

        """Checks if the ball collides with the block."""
        if ball.collision().colliderect(block.collision()):
            block.relocate(screen_width, screen_height) #Places the ball in a new random location.
            player_score += 1 #Adds a point to player score.
            block_hit.play() #Plays sound.
            if player_score < 10:
                ball.speed_increase()

        """Checks to end the game by clicking the X button."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             run = False

        pygame.display.update()  # Refreshes the screen.

    """Checks to end the game by clicking the X button."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             game_loop = False


    screen.fill((0, 0, 0))
    score_display = font.render("Player Score: " + str(player_score),
                                True,(255, 255, 255))  #Defines how the scoreboard looks.
    screen.blit(score_display, (screen_width / 10, screen_height /8)) #Displays the scoreboard.
    ball.ball_reset(300, 200) #Reset the ball location.
    block.relocate(screen_width, screen_height) #Changes blocks location.
    ball.speed_reset() #Resets the balls speed.

pygame.quit()