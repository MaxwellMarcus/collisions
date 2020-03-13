try:
    from tkinter import *
except ImportError:
    from Tkinter import *

root = Tk()
canvas = Canvas(root,width=500,height=500)
canvas.pack()

class Box:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_x -= self.vel_x/100.0
        self.vel_y -= self.vel_y/100.0

        self.render()

    def render(self):
        canvas.create_rectangle(self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2)

b1 = Box(250,25,25,25)
b2 = Box(250,250,50,50)

keys = []

def key_press(event):
    global keys
    keys.append(event.keysym)

def key_release(event):
    global keys
    while event.keysym in keys:
        keys.remove(event.keysym)

root.bind('<KeyPress>',key_press)
root.bind('<KeyRelease>',key_release)

def collision(x,y,w,h,x1,y1,w1,h1):
    if x-w < x1+w and x+w > x1-w1 and y-h < y1+h1 and y+h > y1-h1:
        return True
    else:
        return False

while True:
    canvas.delete(ALL)

    if 'Up' in keys:
        b1.vel_y = -1
    if 'Down' in keys:
        b1.vel_y = 1
    if 'Left' in keys:
        b1.vel_x = -1
    if 'Right' in keys:
        b1.vel_x = 1

    if b1.x-b1.w/2 < b2.x+b2.w/2 and b1.x+b1.w/2 > b2.x-b2.w/2 and b1.y-b1.h/2 < b2.y+b2.h/2 and b1.y+b1.h/2 > b2.y-b2.h/2:
        if collision(b1.x+b1.vel_x,b1.y+b1.vel_y,b1.w/2,b1.h/2,b2.x,b2.y,b2.w/2,b2.h/2):
            b1.vel_x = 0
            b1.vel_y = 0

    print()


    b1.update()
    b2.update()

    root.update()
