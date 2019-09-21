import pygame, random
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)

# Set the width and height of the screen [width, height]

size = (900, 450)
frame = 0
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chase")

# Loop until the user clicks the close button.
done = False

#Loading Pictures
PlayButtonRef= pygame.image.load("play.png").convert_alpha()
GameoverRef= pygame.image.load("gameover.jpg").convert_alpha()
WinRef= pygame.image.load("win.jpg").convert_alpha()
blockRef= pygame.image.load("block1.png").convert_alpha()
cheeseRef= pygame.image.load("cheese.png").convert_alpha()
mainRef= pygame.image.load("Title.jpg").convert_alpha()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Initializing global variables
surface=1
score=0
mouse_down=False

#Creating class that defines the player
class Snake():

    #Initializing variables in class with self
    def __init__(self, x, y):
        self.x = 100
        self.y = 100
        self.w = 25
        self.h = 25
        self.change = 50

        # if true then right or left
        self.dir = True
        self.body = False

    #Gets the x value of the player
    def get_x(self):
        return self.x

    # Gets the x value of the player
    def get_y(self):
        return self.y

    #Function that controls the player and moves the object on screen + sets boundaries around screen
    def control(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_DOWN]:
            self.change = 50
            self.dir = False

        if key[pygame.K_UP]:
            self.change = -50
            self.dir = False

        if key[pygame.K_RIGHT]:
            self.change = 50
            self.dir = True

        if key[pygame.K_LEFT]:
            self.change = -50
            self.dir = True

        if self.y > 450:
            surface = 3
        if self.y < 0:
            surface = 3
        if self.x < 0:
            surface = 3
        if self.x > 900:
            surface = 3

    #Function that draws the player and calls on the control function to check if player direction changes
    def draw(self):
        screen.fill(BLACK)

        #calls on control method
        self.control()

        #changes self.x/y depending on if direction is right/left or up/down
        if self.dir == True:
            self.x += self.change

        elif self.dir == False:
            self.y += self.change

        #displays player
        screen.blit(blockRef,[self.x,self.y])

    #checking if the player collides with the cheese
    def check_collision(self, other):
        if self.x + self.w >= other.x and self.x <= other.x + other.w:
            if self.y + self.h >= other.y and self.y <= other.y + other.h:
                self.body = True
                return True

        return False

#Creating class that defines the cheese
class cheese():
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 300)
        self.w = 25
        self.h = 25
        self.change = 20

    #Displays cheese
    def draw(self):
        screen.blit(cheeseRef,[self.x,self.y])

    #randomly resets in another location
    def reset(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 300)


#creating instances for classes
snake = Snake(100, 100)
c1 = cheese()

#Main while loop
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #checking if the mouse is being pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            pposition_x = pygame.mouse.get_pos()[0]
            pposition_y = pygame.mouse.get_pos()[1]

            #switching to main screen once certain x/y clicked
            if surface == 1 and (380 <= pposition_x <= 530) and (160 <= pposition_y <= 310):
                surface = 2

            # switching to main screen once certain x/y clicked
            if surface == 3 and (130 <= pposition_x <= 400) and (250 <= pposition_y <= 280):
                surface = 1

            #switching to main screen once certain x/y clicked
            if surface == 3 and (620 <= pposition_x <= 820) and (250 <= pposition_y <= 290):
                done=True

    #Initializing FPS and how timer behaves
    frame += 10
    time = frame / 100
    Initial_Time=60
    Final_Time=Initial_Time-int(time)

    #How game changes to Win Screen
    if score==10 and Final_Time>0:
        surface=4
        snake = Snake(100, 100)

    #How game changes to game over screen
    if (snake.get_x() < 0 or snake.get_x() > 900) or (snake.get_y() < 0 or snake.get_y() > 450) or (Final_Time==0):
        surface = 3
        snake=Snake(100,100)

    #What takes place in initial surface
    if surface==1:
        screen.blit(mainRef,[0,-20])
        screen.blit(PlayButtonRef, [380,160])

    #What takes place in game surface --- call draw and control for player + draw for cheese
    if surface == 2:
        # Game code goes here
        snake.draw()
        snake.control()
        c1.draw()

        #How cheese reset and addition of score gets called
        if snake.check_collision(c1) == True:
            c1.reset()
            score+=1

        font = pygame.font.SysFont('Arial', 20, True, False)
        score_title = font.render("Score: "+str(score), False, WHITE)
        screen.blit(score_title, [20, 0])

        font = pygame.font.SysFont('Arial', 20, True, False)
        time_title = font.render("Time: " + str(Final_Time), False, WHITE)
        screen.blit(time_title, [100, 0])

    # What takes place in game over surface --- reset score/time
    if surface == 3:
        screen.blit(GameoverRef, [-195, -130])
        mouse_down=False
        surface=3
        score=0
        frame=0

    # What takes place in winner surface
    if surface == 4:
        screen.blit(WinRef, [0, 0])
        mouse_down=False

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 10 frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()