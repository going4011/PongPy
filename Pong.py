#http://www.codeskulptor.org/#user39_o0lSChNw6g_6.py
#Implementation of classic arcade game Pong
#W and S control up and down on the left paddle.
#Up and Down control up and down on the right paddle.
#Use the "Restart" button to start a new game.
import simplegui
import random

#initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel = [0, 0]
score1 = 0
score2 = 0

def spawn_ball(direction):
    '''
    Initialize ball in the middle of the canvas.
    Picks a random velocity depending on the
    direction specified.
    '''    
    global ball_pos, ball_vel #these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == "right":
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -(random.randrange(1, 3))
    if direction == "left":
        ball_vel[0] = -(random.randrange(2, 4))
        ball_vel[1] = -(random.randrange(1, 3))

def new_game():
    '''
    Starts a new game. Resets paddle positions, scores
    and spawns a new ball in the middle of the canvas.
    '''
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  #these are numbers
    global score1, score2  #these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball("left")

def draw(canvas):
    '''
    Draws ball, paddles, lines to the canvas.
    Updates ball and paddles and checks their position
    and collision detection.
    '''
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    #draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    #update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #collision detection for gutters and paddle
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT) and (ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball("right")
            score2 += 1
    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if (ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball("left")
            score1 += 1
        
    #draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    #bounces the ball off the top and bottom of the screen
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    #update paddle's vertical position
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    #keep paddle on the screen
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    if paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    
    #draw paddles
    canvas.draw_line([0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH * 2, 'White')  
    canvas.draw_line([WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH * 2, 'White')
    
    #draw scores
    canvas.draw_text(str(score1), (140, 40), 48, "White")
    canvas.draw_text(str(score2), (450, 40), 48, "White")
        
def keydown(key):
    '''
    Keydown handler for game controls.
    W and A control left paddle
    Up and Down control right paddle
    '''
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
            paddle1_vel -= 6
    if key == simplegui.KEY_MAP["up"]:
            paddle2_vel -= 6
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 6
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 6

def keyup(key):
    '''
    Keyup handler for game controls.
    When the key is released, the paddle's
    velocity is set to 0. (It is stopped)
    '''
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
    
def restart():
    '''
    Button handler for starting a new game
    with the "Reset" button.
    '''
    new_game()

#create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart)


#start frame
new_game()
frame.start()