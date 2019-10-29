from tkinter import *
import math
import random

#Initializing the window
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
canvas = Canvas(root,width=width,height=height)
canvas.pack()

class Square:
    def __init__(self,x,mass):
        self.x = x
        self.vel_x = 0
        self.mass = mass
        self.keys = []

    def update(self):
        self.x += self.vel_x

        if 'a' in self.keys:
            self.vel_x -= .1
        if 'd' in self.keys:
            self.vel_x += .1

        self.render()

    def keypress(self,event):
        self.keys.append(event.keysym)

    def keyrelease(self,event):
        while event.keysym in self.keys:
            self.keys.remove(event.keysym)


    def render(self):
        canvas.create_rectangle(self.x+self.mass/2,0,self.x-self.mass/2,0+self.mass)

class Player:
    def __init__(self,x,mass):
        self.x = x
        self.vel_x = 0
        self.mass = mass
        self.keys = []

    def update(self):
        self.x += self.vel_x
        self.vel_x -= self.vel_x/10

        if 'a' in self.keys:
            self.vel_x -= .1
        if 'd' in self.keys:
            self.vel_x += .1

        for i in squares:
            if abs(self.x-i.x) < s1.mass/2+i.mass/2:
                collision(s1,i)

        self.render()

    def keypress(self,event):
        self.keys.append(event.keysym)

    def keyrelease(self,event):
        while event.keysym in self.keys:
            self.keys.remove(event.keysym)


    def render(self):
        canvas.create_rectangle(self.x+self.mass/2,0,self.x-self.mass/2,0+self.mass)

def collision(s1,s2):
    v1 = s1.vel_x
    v2 = s2.vel_x

    m1 = s1.mass
    m2 = s2.mass

    s1.vel_x = v1 * (m1-m2) / (m1+m2) + v2 * 2 * m2 / (m1+m2)
    s2.vel_x = v2 * (m2-m1) / (m1+m2) + v1 * 2 * m1 / (m1+m2)


s1 = Player(50,100)
squares = []
squares.append(Square(500,50))

root.bind('<KeyPress>',s1.keypress)
root.bind('<KeyRelease>',s1.keyrelease)

while True:
    canvas.delete(ALL)

    s1.update()
    for i in squares:
        i.update()

    root.update()
