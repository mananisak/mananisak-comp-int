#Final Breakout Controller. The breakout game preloaded with the maximum fitness chromosome. Due to issues with pygame it the visuals stop very quickly but the score continues to increase in the background.
#Manan Isak and Kate Le
#05/10/2022

import sys, pygame, random, math
import numpy as np


class Breakout():   
    def activationSigmoid(self,x):
        return 1/(1+ np.exp(x))

    def activation(self,x):
        if x >= 0:
            return 1
        else:
            return 0

    #The neural network algorithm
    def ANN(self, weights, inputs):
        threshold = -1
        hiddenOut = [0]*5   # The hidden outputs for five hidden nodes
        finalOut = [0]*3 # The final outputs of the three output nodes
        # Find outputs of the five hidden nodes first
        for j in range(len(hiddenOut)):
            x = 0
           
            for k in range(len(inputs)):  # Take an input from an array of the 5 breakout inputs
                x = x + (float(inputs[k]) * weights[j][k])
            hiddenOut[j] = self.activation(x + (threshold * weights[j][5])) # Or some other activation function

        # Find the outputs of the three output nodes
        for j in range(len(finalOut)):
            x = 0
           
            for k in range(len(hiddenOut)):  # Take an input from an array of the 5 hidden outputs
                x = x + (float(hiddenOut[k]) * weights[j+5][k])
            finalOut[j] = self.activation(float(x) + (threshold * weights[j+5][5])) # Or some other activation function
       
        return finalOut

    def main(self):
        #000100110001101111101101001110001001110101100001011100010100001101011101101011101110010001100100000111100100001010101101001100001011011000111000011100100111000010111101010000100011110010000101
        weights = [[-3, -1, -3, 7, 10, 9], [-1, 4, 5, 9, 2, -3], [3, -3, 0, -1, 1, 9], [6, 10, 10, 0, 2, 0], [-3, 10, 0, -2, 6, 9], [-1, -4, 7, 2, -1, 4], [3, -2, 3, -4, 7, 9], [0, -2, -1, 8, 4, 1]]
        
        xspeed_init = 6
        yspeed_init = 6
        max_lives = 1
        score = 1
        bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey        
        size = width, height = 640, 480

        pygame.init()            
        screen = pygame.display.set_mode(size)
        #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        bat = pygame.image.load("bat.png").convert()
        batrect = bat.get_rect()

        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballrect = ball.get_rect()
       
        pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
        pong.set_volume(10)        
       
        wall = Wall()
        wall.build_wall(width)

        # Initialise ready for game loop
        batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
        ballrect = ballrect.move(width / 2, height / 2)      
        xspeed = xspeed_init
        yspeed = yspeed_init
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)      
        pygame.mouse.set_visible(0)       # turn off mouse pointer
        #timeElapsed = 0 #Counts the frames

        while 1:
            # 60 frames per second
            #print(score)
            clock.tick(240)
            #timeElapsed += 1

            #if timeElapsed > 7200: # After 7200 frames or 2 minutes at 60 frames per second
                #f = open("fit.txt", "w")
                #f.write(str(score))
                #f.close()
                #print(score)
                #break
            # bat_speed = random.randrange(1, 20)
            # move_left = random.random()
            # move_right = random.random()

            bat_x = (batrect.left + batrect.right)/2
            ball_x = (ballrect.left + ballrect.right)/2
            ball_y = (ballrect.top + ballrect.bottom)/2

            # Inputs for neural network
            inputList = [bat_x, ball_x, ball_y, xspeed, yspeed]

            # use NN to get 3 outputs
            outputList = self.ANN(weights, inputList) #ouputList = [moveLeft, moveRight, speed]
            move_left, move_right, bat_speed = outputList[0], outputList[1], outputList[2]*10

            # print('PRINTING Three outputs')
            # print(move_left)
            # print(move_right)
            # print(bat_speed)

            if bat_speed > 20:
                bat_speed = 20
            elif bat_speed < 0:
                bat_speed = 0

            # process key presses
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_ESCAPE:
        #             sys.exit()
            #         if event.key == pygame.K_LEFT:                        
            #             batrect = batrect.move(-bat_speed, 0)    
            #             if (batrect.left < 0):                          
            #                 batrect.left = 0      
            #         if event.key == pygame.K_RIGHT:                    
            #             batrect = batrect.move(bat_speed, 0)
            #             if (batrect.right > width):                            
            #                 batrect.right = width

            # Move bat without keys
            if move_left > move_right and batrect.left > 0: # move left
                batrect = batrect.move(-bat_speed, 0)
            elif move_left <= move_right and batrect.right < width: # move right
                batrect = batrect.move(bat_speed, 0)
            # freeze bat if it hits either walls

            # check if bat has hit ball    
            if ballrect.bottom >= batrect.top and \
               ballrect.bottom <= batrect.bottom and \
               ballrect.right >= batrect.left and \
               ballrect.left <= batrect.right:
                yspeed = -yspeed                
                pong.play(0)                
                offset = ballrect.center[0] - batrect.center[0]                          
                # offset > 0 means ball has hit RHS of bat                  
                # vary angle of ball depending on where ball hits bat                      
                if offset > 0:
                    if offset > 30:  
                        xspeed = 7
                    elif offset > 23:                
                        xspeed = 6
                    elif offset > 17:
                        xspeed = 5
                else:  
                    if offset < -30:                            
                        xspeed = -7
                    elif offset < -23:
                        xspeed = -6
                    elif xspeed < -17:
                        xspeed = -5    
                     
            # move bat/ball
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed                
                pong.play(0)            
            if ballrect.top < 0:
                yspeed = -yspeed                
                pong.play(0)              

            # check if ball has gone past bat - lose a life
            if ballrect.top > height:
                lives -= 1
                # start a new ball
                xspeed = xspeed_init
                rand = random.random()                
                if random.random() > 0.5:
                    xspeed = -xspeed
                yspeed = yspeed_init            
                ballrect.center = width * random.random(), height / 3                                
                if lives == 0:
                    # save score to fitness text file
                    #f = open("fit.txt", "w")
                    #f.write(str(score))
                    #f.close()
                    break                    
                    # msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)
                    # msgrect = msg.get_rect()
                    # msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    # screen.blit(msg, msgrect)
                    # pygame.display.flip()
                    # # process key presses
                    # #     - ESC to quit
                    # #     - any other key to restart game
                    # while 1:
                    #     restart = False
                    #     for event in pygame.event.get():
                    #         if event.type == pygame.QUIT:
                    #             sys.exit()
                    #         if event.type == pygame.KEYDOWN:
                    #             if event.key == pygame.K_ESCAPE:
                    #            sys.exit()()
                    #             if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                    #                 restart = True      
                    #     if restart:                  
                    #         screen.fill(bgcolour)
                    #         wall.build_wall(width)
                    #         lives = max_lives
                    #         score = 0
                    #         break
           
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed                                
                pong.play(0)

            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed                              
                pong.play(0)
           
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
            index = ballrect.collidelist(wall.brickrect)      
            if index != -1:
                if ballrect.center[0] > wall.brickrect[index].right or \
                   ballrect.center[0] < wall.brickrect[index].left:
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed                
                pong.play(0)              
                wall.brickrect[index:index + 1] = []
                score += 10
                         
            screen.fill(bgcolour)
            scoretext = pygame.font.Font(None,40).render(str(score), True, (0,255,255), bgcolour)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
            screen.blit(scoretext, scoretextrect)

            for i in range(0, len(wall.brickrect)):
                screen.blit(wall.brick, wall.brickrect[i])    

            # # if wall completely gone then rebuild it
            # if wall.brickrect == []:              
            #     wall.build_wall(width)                
            #     xspeed = xspeed_init
            #     yspeed = yspeed_init                
            #     ballrect.center = width / 2, height / 3


            # # if wall completely gone then break and save fitness as the highest (1000)
            if wall.brickrect == []:    
                #f = open("fit.txt", "w")
                #f.write(str(1000+score))
                #f.close()
                print(score)
                break
                #wall.build_wall(width)                
                #xspeed = xspeed_init
                #yspeed = yspeed_init                
                #ballrect.center = width / 2, height / 3
         
            screen.blit(ball, ballrect)
            screen.blit(bat, batrect)
            pygame.display.flip()

class Wall():
    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left      
        self.brickheight = brickrect.bottom - brickrect.top            

    def build_wall(self, width):        
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):          
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
               
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
    print("Running main")
    br = Breakout()
    br.main()
