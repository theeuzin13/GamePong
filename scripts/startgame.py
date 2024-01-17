import pygame
pygame.init()


WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_HEIGHT, PLAYER_WIDTH = 100, 20

BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNIG_SCORE = 3

class Player:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y-= self.VEL
        else: 
            self.y+= self.VEL
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


    


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0 

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x , self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

        

def draw(win, players, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width()//2, 20))

    for player in players:
        player.draw(win)

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_player, right_player):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_player.y and ball.y <= left_player.y + left_player.height:
            if ball.x - ball.radius <= left_player.x + left_player.width:
                ball.x_vel *= -1

                middle_y = left_player.y + left_player.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_player.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_player.y and ball.y <= right_player.y + right_player.height:
            if ball.x + ball.radius >= right_player.x:
                ball.x_vel *= -1

                middle_y = right_player.y + right_player.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_player.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_player_movement(keys, left_player, right_player):
    if keys[pygame.K_w] and left_player.y - left_player.VEL >= 0:
        left_player.move(up=True)
    if keys[pygame.K_s] and left_player.y + left_player.VEL + left_player.height <= HEIGHT:
        left_player.move(up=False)

    if keys[pygame.K_UP] and right_player.y - right_player.VEL >= 0 :
        right_player.move(up=True)
    if keys[pygame.K_DOWN]and right_player.y + right_player.VEL + right_player.height <= HEIGHT:
        right_player.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()

    left_Player = Player(10, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
    right_Player = Player(WIDTH - 10 - PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    
    while run:
        clock.tick(FPS)
        draw(WIN, [left_Player, right_Player], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_player_movement(keys, left_Player , right_Player)

        ball.move()
        handle_collision(ball, left_Player, right_Player)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()


        won = False
        if left_score >= WINNIG_SCORE:
            won = True
            win_text = "Left Player Won!" 
        elif right_score >= WINNIG_SCORE:
            won = True
            win_text = "Right Player Won!"


        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width()//2 , HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_Player.reset()
            right_Player.reset()
            left_score = 0
            right_score = 0

    pygame.QUIT()

if __name__ == '__main__':
    main()