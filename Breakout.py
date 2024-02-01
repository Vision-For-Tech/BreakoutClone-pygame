import pygame
import sys

pygame.init()

WHITE = (255,255,255)
WIDTH, HEIGHT  = 300, 500
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 20
ball_radius = 7
BRICK_WIDTH = 70
BRICK_HEIGHT = 10
BRICK_ROWS = 4
BRICK_COLS = 4
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

won_font = pygame.font.SysFont('arial.ttf', 36)


bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(
            round(col + 0.1) * (BRICK_ROWS + BRICK_WIDTH),
            round(row + 0.5) * round(BRICK_COLS + BRICK_HEIGHT - 5),
            BRICK_WIDTH,
            BRICK_HEIGHT,
        )
        bricks.append(brick)









class Paddle:
    VEL = 2



    
    def __init__(self,x,y,width,height,color):
        self.x = self.original_x = x
        self.y = self.original_y =  y
        self.width = width
        self.height = height
        self.color = color



    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height))

    def move(self, right=True):
        if right:
            self.x += self.VEL
        else:
            self.x -= self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y



class Ball:
    MAX_VEL = 5

    
    def __init__(self,x,y,radius,color):
        self.x = self.original_x =  x
        self.y = self.original_y = y
        self.radius = radius
        self.color = color
        self.x_vel = self.MAX_VEL
        self.y_vel = 5
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)



    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.center = (self.x, self.y)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 5
        self.x_vel *= 1


def handle_events(keys, paddle):
    if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
        paddle.move(right=True)
    if keys[pygame.K_LEFT] and paddle.x + paddle.VEL >= 0:
        paddle.move(right=False)


def handle_collisions(ball,paddle, bricks):
    if ball.x + ball.radius >= WIDTH:
        ball.x_vel = -1 * ball.x_vel
    elif ball.x - ball.radius <= 0:
        ball.x_vel = -1 * ball.x_vel


    if ball.y_vel > 0:
        if ball.y + ball.radius >= paddle.y and ball.y <= HEIGHT:
            if ball.x + ball.radius >= paddle.x and ball.x - ball.radius <= paddle.x + paddle.width:
                ball.y_vel *= -1


    for brick in bricks[:]:
        if ball.rect.colliderect(brick):
            print("Collision detected with a brick!")
            collided = True
            if collided:
                bricks.remove(brick)
                ball.y_vel = -ball.y_vel
                break

    pygame.display.update()

  
               



def draw_bricks(win, bricks):
        for brick in bricks:
            if brick.x >= 0 and brick.y >= 0:
                pygame.draw.rect(win,WHITE,brick)
            





def draw(win, paddle, ball, bricks):
    win.fill((0,0,0))
    paddle.draw(win)
    ball.draw(win)
    draw_bricks(win,bricks)
    pygame.display.update()





def main():
    run = True

    paddle = Paddle(HEIGHT // 2 - PADDLE_HEIGHT,HEIGHT - 10,PADDLE_WIDTH,PADDLE_HEIGHT,WHITE)
    ball = Ball(WIDTH // 2,HEIGHT // 2,ball_radius,WHITE)
   

    
    while run:
        won = False
        clock.tick(60)
        draw(win, paddle, ball, bricks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        handle_events(keys,paddle)
        ball.move()
        handle_collisions(ball,paddle,bricks)
        won_text = "YOU WON!!!!"


        if ball.y <= 0:
            ball.reset()
        if ball.y >= HEIGHT:
            ball.x = paddle.x + paddle.width // 2
            ball.y = paddle.y - 5
            ball.y_vel = -5


        if len(bricks) == 0:
            won = True

            

        if won:
            label = won_font.render(won_text, 1 , WHITE)
            win.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
            pygame.display.update() 
            pygame.time.delay(5000)
            draw(win,paddle,ball,bricks)
            ball.reset()
            ball.move
            paddle.reset()
            won = False
            
            

        pygame.display.update()

        

    pygame.quit()


main()
