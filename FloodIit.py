#for github
###############################################
# Flood it game using turtle                  #
# ProfEvans                                   #
# Total time spent on editing:> 06:24:19 HMS  #
###############################################

#run pip install pyscreenshot
#run pip install pyautogui
#run pip install for any other red imports

import turtle as trtl # trtl is the GUI
import random as rand #randomizes color choice
import threading # less lag I think
from PIL import Image #analizes screenshot specifically RGB
import pyscreenshot #takes a screenshot
import pyautogui #get position for Screenshot
import time as t #I didnt use this

#INIT trtl
wn = trtl.Screen()
wn.delay(0) #this makes the display update as fast as your computer allows.

writer = trtl.Turtle()
writer.hideturtle()
writer.penup()

Move_writer = trtl.Turtle()
Move_writer.hideturtle()
Move_writer.penup()

#var assignment for the most part
colorID_list = ['purple','orange','blue','red','green','yellow','tan']
#basic flood it colors

#board Creation
BD_size = (15,15) # I could add a title screen that sets this var based on how large you want your grid.
BD = []
for r in range(BD_size[0]):
    BD.append([])
    for c in range(BD_size[1]):
        BD[r].append([])
#keeps track of moves
move_count = 0
moves = round(BD_size[0]*BD_size[1]/len(colorID_list))


''' Example Board And locations, used with debugging, does not currently work
BD = [
#    A B C D E
    [0,0,0,0,0], #1
    [0,0,0,0,0], #2
    [0,0,0,0,0], #3
    [0,0,0,0,0], #4
    [0,0,0,0,0]  #5
]
'''
#list of total colors, and all owned
colors = []
owned = []

#creates colors for easy assignment
class Color():
    def __init__(self, id, location):
        self.id = id
        self.location = location
        BD[location[0]][location[1]] = self
        colors.append(self)
        #Im using separate turtles for each square to make screen updates faster
        self.color = trtl.Turtle()
        self.color.shape('square')
        self.color.color(id)
        self.color.penup()
        self.color.speed(0)
        self.color.goto(0-(BD_size[1]*10),0+(BD_size[0]*10)) #helps center the board
        self.color.fd(location[1]*20)
        self.color.rt(90)
        self.color.fd(location[0]*20)
        #multiply its BD location by 20 to help with spacing 
    
    def take(self,clr, location): #clr normally means clear but in this case it means color. I didnt want to write color.color(color)
        #print(self.id)
        owned.append(self)
        self.color.color(clr)
        self.id = clr #I use color and id almost interchangeably, but id is callable. color is not
        self.check(self.id) #it rechecks the board but the new position in case more of the same colors are connected.
        # print(self.id)
        # print(self.location[0] - BD[self.location[0]+1][self.location[1]].location[0], self.location[0] - BD[self.location[0]+1][self.location[1]].location[0] )

    def check(self,color):
        #used try and except because it uses +1 for index and could pose errors towards the ends of the list 
        self.color.color(color)
        self.id = (color) 
        for I in range(2): #did this because I was getting overlap and it wasn't assigning and now it is so shrug
            try:
                if BD[self.location[0]+1][self.location[1]].id == self.id: #checks to see if they are the same
                    if BD[self.location[0]+1][self.location[1]] not in owned: #double checks it doesn't double up on owned
                        BD[self.location[0]+1][self.location[1]].take(self.id, self.location) #takes that tile as its own
                        print('took bottom')
                        print(f'bottom {self.location[0]} trying at {self.location[0]+1}')
            except IndexError:
                print('error in 1') #so I can see when its at a wall
                #pass
            
            try:
                if BD[self.location[0]-1][self.location[1]].id == self.id and self.location[0]-1 >=0: #added self.location[0]-1 >=0 because [-1] returns the last in a list
                    if BD[self.location[0]-1][self.location[1]] not in owned:
                        BD[self.location[0]-1][self.location[1]].take(self.id, self.location)
            except IndexError:
                print('error in 2')
                #pass
            
            try:
                if BD[self.location[0]][self.location[1]+1].id == self.id:
                    if BD[self.location[0]][self.location[1]+1] not in owned:
                        BD[self.location[0]][self.location[1]+1].take(self.id, self.location)
            except IndexError:
                print('error in 3')
                #pass

            try:
                if BD[self.location[0]][self.location[1]-1].id == self.id and self.location[1]-1 >=0:
                    if BD[self.location[0]][self.location[1]-1] not in owned:
                        BD[self.location[0]][self.location[1]-1].take(self.id, self.location)
            except IndexError:
                print('error in 4')
                #pass
            #I modified my maze solver algorithm to make the check function, it looks at the space above, below, lef, and right of the current square.

        get_win_state()
        
        # for i in owned:
        #     print(i.location)

def MOVES(): #updates move counter
    global move_count, moves
    Move_writer.clear()
    Move_writer.goto(0,0+(BD_size[1]*10)+10)
    Move_writer.write(f'{move_count}/{moves}', align='center', font=('Arial',10,'normal')) #f strings are wonderful
    move_count += 1

def get_win_state(): # this tests if every color is the same color 
    global colors, BD_size
    last = colors[0].id
    counter = 0
    for c in colors:
        if last == c.id:
            counter += 1
            if counter == BD_size[0]*BD_size[1]:
                WIN()
        else:
            #print(f'last:{last} new:{c.id}') #debugging
            break

def WIN():
    global BD_size, move_count, moves
    if move_count <= moves: #you can still play on after you max out on moves but this will put you in your place
        writer.clear()
        writer.goto(0,0+(BD_size[1]*-10)-10)
        writer.write('WIN!!!!', align='center', font=('Arial',10,'normal'))
    else:
        writer.clear()
        writer.goto(0,0+(BD_size[1]*-10)-10)
        writer.write('You suck Nerd', align='center', font=('Arial',10,'normal'))
        
def get_board(): #debugging
    for c in BD:
        print(c)

def click(x,y): #test screen clicks
#make colors
    global running
    if not running:
        print('start')
        running != running #as to not overload the system
        #could have made a dict that way it could be expandable
        blue = (0,0,255)
        red = (255,0,0)
        tan = (210,180,140)
        orange = (255,165,0)
        purple = (128,0,128)
        yellow = (255,255,0)
        green = (0,128,0)

        pad = 5 #is the buffer on each side of the screen shot
        location = pyautogui.position() #so it can test the color of where the mouse is
        box = (location[0]-pad, location[1]-pad, location[0]+pad, location[1]+pad) #just better for the screenshot in my opinion
        image = pyscreenshot.grab(box) #takes a 10x10 pixl screen shot at mouse location
        image.save('i1.png') #saves it because we need to switch to a different function
        im = Image.open('i1.png') #calls the save
        pix = im.load() #its a part of the PIL image. See PIL reference page
        
        #could have made a dict that way it could be expandable
        if pix[5,5] == blue:
            clr = 'blue'
        elif pix[5,5] == red:
            clr = 'red'
        elif pix[5,5] == tan:
            clr = 'tan'
        elif pix[5,5] == orange:
            clr = 'orange'
        elif pix[5,5] == purple:
            clr = 'purple'
        elif pix[5,5] == yellow:
            clr = 'yellow'
        elif pix[5,5] == green:
            clr = 'green'
        #print(clr)
        for i in owned:
            #used threading for each ownded that way it can do it all at once instead of one by one
            x = threading.Thread(target=i.check, args=[clr])
            x.start()
            #i.check(clr)
        running != running #toggle from running to not running
        MOVES() #updates move counter
        #print('end') #debugging
    else:
        print('Slow Down') #incase you have an auto clicker

Rl = 0
Cl = 0
#sets location in 2d list BD
wn.tracer(False) # so it all shows up at once
for r in BD:
    Cl = 0
    for c in r:
        c = Color(rand.choice(colorID_list), (Rl,Cl)) #creates a color with random color and relative location in 2d list 
        #c = Color('blue', (Rl,Cl)) 
        #adds color to the 2d list
        BD[Rl][Cl] = c
        Cl += 1
    Rl += 1
#You need to define a start square. I chose the top left like the actual game flood it
owned.append(BD[0][0])
BD[0][0].check(BD[0][0].id) #has to run through incase it spawns with other colors around it that are the same
MOVES() #starts move counter
wn.update() #updates the screen so the GUI shows up
wn.tracer(True) #so it updates as it goes instead of waiting which was slower

#starts scanning for a click on the gui, if you click off of it, nothing will happen and it wont add to the move list
wn.listen()
running = False
wn.onscreenclick(click)

wn.mainloop()