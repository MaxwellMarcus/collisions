from tkinter import *
import math
import random

#Initializing the window
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
canvas = Canvas(root,width=width,height=height)
canvas.pack()

mouse_x = 0
mouse_y = 0
last_mouse_x = 0
last_mouse_y = 0

colors = ['#ff0000','#00ff00','#0000ff','#990000','#009900','#000099']

class Particle:
    def __init__(self,x,y,radius,velocity,color,mouse=False):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.original_color = color
        self.color_vel = 1
        self.mass = 1
        self.mouse = mouse
        if self.mouse:
            self.mass = 100

        c = list(self.color)
        r = get_dec(self.color[1:3])
        g = get_dec(self.color[3:5])
        b = get_dec(self.color[5:7])
        self.rgb = [r,g,b]
        self.original_rgb = [r,g,b]

    def update(self,particles):
        if not self.mouse:
            self.x += self.velocity[0]
            self.y += self.velocity[1]

        for i in particles:
            if not i == self:
                if get_dist(i.x,i.y,self.x,self.y) < self.radius+i.radius:
                    resolve_collision(self,i)
                    if not self.mouse:
                        self.x += self.velocity[0]
                        self.y += self.velocity[1]
                    i.x += i.velocity[0]
                    i.y += i.velocity[1]

        if not self.mouse:
            if self.x - self.radius <= 0:
                self.velocity[0] = -self.velocity[0]
            if self.x + self.radius >= width:
                self.velocity[0] = -self.velocity[0]
            if self.y - self.radius <= 0:
                self.velocity[1] = -self.velocity[1]
            if self.y + self.radius >= height:
                self.velocity[1] = -self.velocity[1]

        #self.rgb = self.original_rgb.copy()
        self.color = self.original_color
        dist = get_dist(mouse_x,mouse_y,self.x,self.y)
        if dist < 150:
            if self.original_rgb[0] == 0:
                if self.rgb[0] < 150:
                    self.rgb[0] += 1
            if self.original_rgb[1] == 0:
                if self.rgb[1] < 150:
                    self.rgb[1] += 1
            if self.original_rgb[2] == 0:
                if self.rgb[2] < 150:
                    self.rgb[2] += 1

        r = get_hex(self.rgb[0])
        while len(r) < 2:
            r = '0'+r
        g = get_hex(self.rgb[1])
        while len(g) < 2:
            g = '0'+g
        b = get_hex(self.rgb[2])
        while len(b) < 2:
            b = '0'+b

        self.color = '#'+r+g+b

        self.render()

    def render(self):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,self.x+self.radius,self.y+self.radius,fill=self.color,outline=self.original_color)

#keeping track of mouse
def mouse_move(event):
    global mouse_x,mouse_y,last_mouse_x,last_mouse_y
    last_mouse_x = mouse_x
    last_mouse_y = mouse_y
    mouse_x = event.x
    mouse_y = event.y

def get_hex(n):
    hex = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
    rs = []
    q = n
    r = n
    while n > 0:
        q = n // 16
        r = n % 16
        n = q
        rs.append(r)
    ans = ''
    for i in rs:
        ans += str(hex[i])
    return ans

def get_dec(n):
    dec = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    n1 = list(n)
    for i in range(len(n1)):
        n1[i] = dec[n1[i]]

    new = 0
    for i in range(len(n1)):
        m = 16 ** (len(n1)-i-1)
        new += n1[i] * m

    return new

def get_dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def rotate(velocity, angle):
    x = velocity[0] * math.cos(angle) - velocity[1] * math.sin(angle)
    y = velocity[1] * math.sin(angle) + velocity[0] * math.cos(angle)

    return [x,y]

def resolve_collision(p1,p2):
    xVelDiff = p1.velocity[0] - p2.velocity[0]
    yVelDiff = p1.velocity[1] - p2.velocity[1]

    xDist = p2.x - p1.x
    yDist = p2.y - p1.y

    if xVelDiff * xDist + yVelDiff * yDist >= 0:
        a = -math.atan2(p2.y - p1.y,p2.x - p1.x)

        m1 = p1.mass
        m2 = p2.mass

        u1 = rotate(p1.velocity, a)
        u2 = rotate(p2.velocity, a)

        v1 = [u1[0] * (m1-m2) / (m1+m2) + u2[0] * 2 * m2 / (m1 + m2), u1[1]]
        v2 = [u2[0] * (m1-m2) / (m1+m2) + u1[0] * 2 * m2 / (m1 + m2), u2[1]]

        final_v1 = rotate(v1, -a)
        final_v2 = rotate(v2, -a)

        p1.velocity = final_v1
        p2.velocity = final_v2

root.bind('<Motion>',mouse_move)

#creating circles
particles = []
for i in range(100):
    r = 30
    x = random.randint(r,width-r)
    y = random.randint(r,height-r)

    if not i == 0:
        j = 0
        while j < len(particles):
            l = particles[j]
            if get_dist(l.x,l.y,x,y) < r+l.radius:
                x = random.randint(r,width-r)
                y = random.randint(r,height-r)
                j = -1
            j += 1

    particles.append(Particle(x,y,r,[random.randint(-10,10),random.randint(-10,10)],colors[random.randint(0,len(colors)-1)]))



while True:
    #clearing the canvas
    canvas.delete(ALL)

    #render particles
    for i in particles:
        i.update(particles)

    #updating the screen
    root.update()
