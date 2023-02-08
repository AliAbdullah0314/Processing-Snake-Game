import random
import time
import os 
resolution= 600
tileres=resolution/20
startsize=3

isRestart=False

#direction aspect of the snake's movement (positive means right or up, and negative means left or down)
xdir=1
ydir=0

path = os.getcwd()
leftsnake = loadImage(path + "/images/head_left.png")
upsnake=loadImage(path + "/images/head_up.png")
apple= loadImage(path + "/images/apple.png")
banana= loadImage(path + "/images/banana.png")

#the rgb values for all possible snake colours:
greentail='080,153,032'
redtail='173,048,032'
yellowtail= '251,226,076'

#dictionary which helps keep track of the order of colours in the snake
mapping={}

#counter to keep track of elements in the dictionary
counter=3

class Snaketile():
    
    def __init__(self, row, col, clr):
        
        self.r=row
        self.c=col
        self.clr=clr
    
    
class Snake(list):
    def __init__(self, size):
        self.size=size
        for i in range (size):
            self.append(Snaketile(10, 10-i, '080,153,032'))  #creates the initial part of the snake's body
    
    def move(self, clr):
        if(not(isRestart)):
            self.insert(0,Snaketile(snake[0].r-ydir, snake[0].c+xdir, clr)) #inserts a new head for the snake every time the snake moves
            self.pop() #pops out the last element in the snake list, so as to give the trailing effect
            
        
        #assigns each tile of the snake a color value from the dictionary 'mapping'
        i=3
        while(i<len(snake)):
            snake[i].clr=mapping[i]
            i+=1
        
    #checks if the fruit is in the same row as the snake         
    def checkrow(self, target):
        present=False
        for i in range(len(self)):
            if(self[i].r==target):
                present=True
        return present
   
    #checks if the fruit is in the same column as the snake          
    def checkcol(self, target):
        present=False
        for i in range(len(self)):
            if(self[i].c==target):
                present=True
        return present
    
    
    def addtail(self, clr ):
        global counter
        if(clr=='red'):
            self.append(Snaketile(snake[len(snake)-1].r, snake[len(snake)-1].c, redtail))
            mapping[counter]=redtail
            counter+=1
        if(clr=='yellow'):
            self.append(Snaketile(snake[len(snake)-1].r, snake[len(snake)-1].c, yellowtail))
            mapping[counter]=yellowtail
            counter+=1
        


        
        


class Fruit():
    def __init__(self, type):
        self.type=type
        self.r=-2
        self.c=-2
        
    def display(self,snake):
        
        if(self.type=='apple'):
            image(apple,self.c*tileres-15,self.r*tileres-15)
            
        if(self.type=='banana'):
            image(banana,self.c*tileres-15,self.r*tileres-15)
    
        
            
        




class Game():
    
    def __init__(self, score):
        self.score=score

    #runs when the game is over
    def over(self):
        global xdir
        global ydir
        xdir=0
        ydir=0
        textSize(50)
        fill(0,0,0)
        text("GAME OVER",140,50)
        text("Your score was "+str(self.score), 90,100 )
       

    
    
        
#creates a snake object, and a game object
snake=Snake(3)
game=Game(0)

#runs when the mouse is clicked after the game is over. Resets all values to default
def restart():
    global xdir
    global ydir
    xdir=1
    ydir=0 
    
    global mapping
    global counter
    mapping.clear()
    counter=3
    
    global snake
    global game
    snake=Snake(3)
    game=Game(0)
    
    global isRestart
    isRestart=False
    
    
    
        
    
    

        

fruitshow=False

#controls the movement of the snake
def keyPressed():
    global xdir
    global ydir
    if(keyCode==UP and ydir!=-1):
        xdir=0
        ydir=1
    
    if(keyCode==DOWN and ydir!=1):
        xdir=0
        ydir=-1
    
    if(keyCode==LEFT and xdir!=1):
        xdir=-1
        ydir=0
        
    if(keyCode==RIGHT and xdir!=-1):
        xdir=1
        ydir=0


def mouseClicked():
    if(isRestart):
        restart()

#determines the orientation and layout of the head image    
def headDesign(xd, yd):
    if(xd==1):  
        pushMatrix() #this is done to contain the properties of rotate and translate for this image only
        translate((snake[0].c)*tileres-15,(snake[0].r)*tileres-15)
        rotate(PI)
        translate(-(snake[0].c)*tileres-30,-(snake[0].r)*tileres-30)
        image(leftsnake,(snake[0].c)*tileres,(snake[0].r)*tileres)
        popMatrix()
        
    
    if(yd==1):
        image(upsnake,(snake[0].c)*tileres-15,(snake[0].r)*tileres-15)
        
    if(yd==-1):
        pushMatrix() #this is done to contain the properties of rotate and translate for this image only
        translate((snake[0].c)*tileres-15,(snake[0].r)*tileres-15)
        rotate(PI)
        translate(-(snake[0].c)*tileres-30,-(snake[0].r)*tileres-30)
        image(upsnake,(snake[0].c)*tileres,(snake[0].r)*tileres)
        popMatrix()
    if(xd==-1):
        image(leftsnake,(snake[0].c)*tileres-15,(snake[0].r)*tileres-15)

def setup():
    size(resolution,resolution)


randchoice=random.randint(0,1)  #helps in choosing a fruit randonly
appleobj=Fruit('apple')
bananaobj=Fruit('banana')
over=False
def draw():
    if(frameCount%12 == 0):    #slows down the game
        global appleobj
        global bananaobj
        global fruitshow
        global randchoice
        background(200,200,200)
        stroke(1,0.0)
        headDesign(xdir, ydir)
        snaketiles=[]
        for i in range(1,len(snake)):
            elements=[snake[i].r, snake[i].c]
            snaketiles.append(elements)
            
        head=[snake[0].r, snake[0].c]
        
        for i in range(1,len(snake)):
            stroke(1,0.0)
            fill(int((snake[i].clr)[0:3]), int((snake[i].clr)[4:7]), int((snake[i].clr)[8:11]))
            circle((snake[i].c)*tileres,(snake[i].r)*tileres, tileres )
        
        #adds a tail if the snake eats an apple
        if(snake[0].r==appleobj.r and snake[0].c==appleobj.c ):
            snake.addtail('red')
            snake.move(redtail)
            appleobj.r=-1
            appleobj.c=-1
            game.score+=1
            fruitshow=False
            
        #adds a tail if the snake eats a banana     
        elif(snake[0].r==bananaobj.r and snake[0].c==bananaobj.c ):
            snake.addtail('yellow')
            snake.move(yellowtail)
            bananaobj.r=-1
            bananaobj.c=-1
            game.score+=1
            fruitshow=False
        else:
            snake.move(greentail)
        
        
        
            
            
    
        
        #shows the the score
        textSize(20)
        fill(0,0,0)
        text("Score: "+str(game.score),500,20)
        
        
        if(fruitshow==False):    #runs if there is no fruit showing (either at the start or after the snake has eaten one)
            randchoice=random.randint(0,1)
            if(randchoice==0):   #this means that the fruit is an apple
                conflict=True
                while(conflict):
                    randrow=random.randint(1,19)
                    randcol=random.randint(1,19)
                    if((not snake.checkrow(randrow)) and (not(snake.checkcol(randcol)))):
                        appleobj.r=randrow
                        appleobj.c=randcol
                        appleobj.display(snake)
                        fruitshow=True
                        conflict=False
            else:    #this means that the fruit is a banana
                conflict=True
                while(conflict):
                    randrow=random.randint(1,19)
                    randcol=random.randint(1,19)
                    if((not snake.checkrow(randrow)) and (not(snake.checkcol(randcol)))):
                        bananaobj.r=randrow
                        bananaobj.c=randcol
                        bananaobj.display(snake)
                        fruitshow=True
                        conflict=False
            
        
        else:
            if(randchoice==0):    #this means that the fruit is an apple
                appleobj.display(snake)
                
            
            else:    #this means that the fruit is a banana
                bananaobj.display(snake)
    
        global over
        
        #runs if the snake is exceeding the boundaries or if the snake is 400 units long
        if((head in snaketiles) or (snake[0].c==-1) or(snake[0].r==-1) or (snake[0].c==21) or (snake[0].r==21) or (len(snake)==400)):
            game.over()
            over=True
            global isRestart
            isRestart=True
