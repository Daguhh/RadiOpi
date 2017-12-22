#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 12:43:39 2017

@author: david
"""

import time
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import  proportional
from myfont import MINI_FONT, DRAWING_FONT
import numpy as np
from PIL import Image
# PIL.ImageFont.truetype(font=None, size=10, index=0, encoding='', layout_engine=None)



def getMatFromFont(txt):
    font = MINI_FONT
    size_font = 5
    x, y = 0, 0
    mat=0*np.ones((8,len(txt)*size_font))
    for ch in txt:
        for byte in font[ord(ch)]:
            for j in range(8):
                if byte & 0x01 > 0:
                    mat[y+j,x] = 1
                byte >>= 1
            x += 1
        mat[:,x] = 0
        x += 1
    return(mat.astype(np.uint8))
        
    

    
    
class tXt() :
    def __init__(self,device) :
        self.device = device
        self.FONT = DRAWING_FONT
     
    def printImage(self, mat, x=0, y=0) :
        im1 = Image.fromarray(255*mat, mode='L')
        with canvas(self.device) as draw:
            draw.bitmap((x,y), im1, fill="white")    
            
    def slIce(self) :
        
        mat_aff = 0*np.ones((8,32)).astype(np.uint8)
        mat_txt = getMatFromFont("david")
        pixel_liste = []
        
        for col in np.arange(np.size(mat_txt,1)):
            for row in np.arange(np.size(mat_txt,0)):
                
                if mat_txt[row,col] == 1:
                    new_pixel = self.SlicingPixel(row,col)
                    pixel_liste.append( new_pixel )
                    
                for l in np.arange(4) : # do x4 times
                    mat_aff = np.zeros((8,32)).astype(np.uint8) # reset : =0
                    for pixel in pixel_liste :
                        tic = time.time()
                        xmin, xmax, ymin, ymax = pixel.move() 
                        toc = time.time()
                        mat_aff[xmin:xmax, ymin:ymax] = 1
                    self.printImage(mat_aff,0,-2)
        
        print("toc3 = " +str(toc-tic))
        print(len(pixel_liste))
        self.printImage(mat_txt,0,-2)
        time.sleep(3)
        
    class SlicingPixel() :
        def __init__(self, x, y) :
            self.dest_x = x
            self.dest_y = y
            self.xmin = x
            self.xmax = self.xmin+1
            self.ymin = 31
            self.ymax = 0
           
            
        def move(self) :
            if self.dest_y != self.ymin :
                self.ymin -= 1# move left
                if self.ymin+8 < 32 : self.ymax = self.ymin+8 # slice = 8px large
                else : self.ymax = 31
            else :
                if self.ymax != self.dest_y+1: # contract slice
                    self.ymax-=1
                    
            return self.xmin, self.xmax, self.ymin, self.ymax      
        
class tXt2() :
    def __init__(self,device) :
        self.device = device
        self.FONT = DRAWING_FONT
     
    def printImage(self, mat, x=0, y=0) :
        im1 = Image.fromarray(255*mat, mode='L')
        with canvas(self.device) as draw:
            draw.bitmap((x,y), im1, fill="white")    
            
    def slIce(self, txt="test", side=[0,-1]) :
        
        mat_aff = np.zeros((8,32)).astype(np.uint8)
        mat_txt = getMatFromFont(txt)
        pixel_liste = []
        
        if side[1] == 1:
            c1 = np.arange(np.size(mat_txt,1),0,-1)-1
#            r1 = np.arange(np.size(mat_txt,0),0,-1)-1
        else :
            c1 = np.arange(np.size(mat_txt,1))
        r1 = np.arange(np.size(mat_txt,0))
            
        for col in c1 : 
            for row in r1 :
                
                if mat_txt[row,col] == 1:
                    new_pixel = self.SlicingPixel(xy=[row,col], direction=side)
                    pixel_liste.append( new_pixel )
                    
                for x4_times in np.arange(16) : # do x4 times
                    mat_aff = np.zeros((8,32)).astype(np.uint8) # reset : =0
                    for pixel in pixel_liste :
                        tic = time.time()
                        xymin, xymax = pixel.move() 
                        toc = time.time()
                        mat_aff[ xymin[0]:xymax[0], xymin[1]:xymax[1] ] = 1
                    self.printImage(mat_aff,0,-2)
#            time.sleep(0.005)
        self.printImage(mat_txt,0,-2)
        
        print("toc1 = " +str(toc-tic))
        time.sleep(1)
        print(len(pixel_liste))
                
    class SlicingPixel() :
        def __init__(self, xy, direction=[0, 1]) :
            self.dest = np.array(xy)
            self.direction = np.array(direction)
            self.bound = np.array([8,32]) 
            self.slice_width = np.array([2,8])
            self.xy_min = self.dest*(self.direction==0) + self.bound*(self.direction<0)
            self.xy_max = self.dest+1
            
        def move(self) :
            side = self.direction
            slc_w = self.slice_width
            bnd = self.bound
            dest = self.dest
            if (self.dest != self.xy_min).any() :
                self.xy_min += side
                if (self.xy_min + slc_w*(-side) > bnd).any() :
                    self.xy_max = bnd*(np.abs(side)) + (dest+1)*(side==0) 
                elif (self.xy_min + slc_w*(-side) < 0).any() : 
                    self.xy_max = np.array([0,0]) + (dest+1)*(side==0) 
                else : 
                    self.xy_max = self.xy_min + (side==0) + slc_w*(-side)
            else :
                if (self.xy_max != dest-side).all(): # contract slice
                    self.xy_max += side
            
            a = self.xy_min.copy()
            b = self.xy_max.copy()
            if a[0]>b[0] : a[0],b[0] = b[0],a[0]
            if a[1]>b[1] : a[1],b[1] = b[1],a[1]
            return a,b


    



class makeFigure() :
    def __init__(self, device) :
        self.device = device
        self.txt = "abcd"
        self.pos = ord("a")
        self.FONT = DRAWING_FONT
        self.mat = 0*np.ones((8,32)).astype(np.uint8)
        tmp = self.mat2byte(self.mat)
        self.printMat(tmp)
        
     #   self.mat=1*(np.random.rand(8,32)>1)

    def mat2byte(self, Amat) :       
        k=0
        for chnb in np.arange(0,25,8) :
            mat = Amat[:,chnb:chnb+8]
            for i in np.arange(8) :
                byte = 0
                for j in np.arange(8) :
                    byte <<= 1
                    byte += (mat[j][i])
              #  byte = format(byte,'#04x' )
                self.FONT[ord(self.txt[k])][i] = byte
            k+=1
        
    def spiRal(self) :
        self.mat = 1*np.ones((8,32)).astype(np.uint8)
        for l in np.arange(4) :
            print(l)
            x=0;y=0
            x = np.append(x,np.arange(l,32-l,1))
            x = np.append(x,(31-l)*np.ones(8-2*l).astype(np.uint8))
            x = np.append(x,np.arange(32-l,0+l,-1)-1)
            x = np.append(x,(l)*np.ones(7-2*l).astype(np.uint8))
            
            y = np.append(y,l*np.ones(32-2*l).astype(np.uint8))
            y = np.append(y, np.arange(l,8-l,1))
            y = np.append(y, (7-l)*np.ones(32-2*l).astype(np.uint8))
            y = np.append(y, np.arange(8-l,1+l,-1)-1)
    
            for i in np.arange(np.size(x)) :    
                if 1 :
                    self.mat[y[i],x[i]] = 0
                    self.printImage(self.mat)
                    time.sleep(0.003)
                    
    def siNus(self) :
        mat = 0*np.ones((8,32)).astype(np.int8)
        for l in np.arange(1000) :
            x = np.arange(32).astype(np.int8)
            freq = 0.6
            noise = 1/freq*np.random.rand(32)
            noise2 = 1*(np.random.rand(32)>0.5)+1
            y = 3+noise2*np.round(1.7*np.sin((x-l+noise)*freq)).astype(np.int8)
            mat=0*np.ones((8,32)).astype(np.int8)
            for i in np.arange(32) :
                mat[:y[i]:,x[i]] = 1
            self.printImage(mat.astype(np.uint8))   
            
            time.sleep(0.03)
    
    def baLl(self):
        self.mat = 0*np.ones((8,32)).astype(np.uint8)
        
        x=0; y=0; vx=1; vy=1
        ball_list=[]
        balle1 = Ball(x,y,vx,vy)
        ball_list.append(balle1)
        k = 0
        for l in np.arange(10000) :
            self.mat = 0*np.ones((8,32)).astype(np.uint8)
            for balle in ball_list :
                x,y = balle.move()
                self.mat[x,y] = 1
                if k >500 :
                    x = np.random.randint(0,4,1,dtype='int')
                    y = np.random.randint(0,27,1,dtype='int')
                    vx = np.random.randint(1,3,1,dtype='int')
                    vy = np.random.randint(1,3,1,dtype='int')
                    new_ball = Ball(x,y,vx,vy)
                    ball_list.append(new_ball)
                    k=0
                k+=1
            self.printImage(self.mat)   
            time.sleep(0.01)
            
       
    def printImage(self, mat, x=0, y=0) :
#        print(mat)
        im1 = Image.fromarray(255*mat, mode='L')#.convert('1')
        with canvas(self.device) as draw:
            draw.bitmap((x,y), im1, fill="white")
        
        
    def maGnetism(self) :
        mat = ( 2*(np.random.rand(8,32)>0.5)-1 ).astype(np.int8)  
        print(mat)
        ind = [1,0],[-1,0],[0,1],[0,-1]     
        while 1 :        
            self.printImage(((mat+1)/2).astype(np.uint8))
            time.sleep(2)
            for x in np.arange(8) :
                for y in np.arange(32) :
                    summ = mat[x,y]
                    for k in ind :
                        summ += mat[(x+k[0])%8, (y+k[1])%32]
                    if summ > 0 :
                        mat[x,y]=1
                    else :
                        mat[x,y]=-1
            
                    
    def printMat(self,mat) :
        with canvas(self.device) as draw:  
            #text(draw, (0,-2), "radio", fill="white", font=proportional(MINI_FONT))
            text(draw, (0,0), "a", fill="white", font=proportional(self.FONT))
            text(draw, (8,0), "b", fill="white", font=proportional(self.FONT))
            text(draw, (16,0), "c", fill="white", font=proportional(self.FONT))
            text(draw, (24,0), "d", fill="white", font=proportional(self.FONT))
            
    def waTer(self) :
        mat = 0*np.ones((8,32)).astype(np.uint8)
        water_list=[]
        new_goutte = Water()
        water_list.append(new_goutte)
        k = 0
        for l in np.arange(10000) :
            mat = 0*np.ones((8,32)).astype(np.uint8)
            for goutte in water_list :
                x,y = goutte.fall(mat)
                mat[x,y] = 1
                if k > 2 :
                    new_goutte = Water()
                    water_list.append(new_goutte)
                    k=0
            k+=1*(np.random.rand(1)>0.7)
            self.printImage(mat)   
            time.sleep(0.05)
            
            if len(water_list) >256 :
                break
            
    def slIce(self) :
        
        mat0 = 0*np.ones((8,32)).astype(np.uint8)
#        im1 = ImageFont.truetype(font=MINI_FONT, size=10, index=0, encoding='', layout_engine=None)
        mat = getMatFromFont("david")
        pixel_liste = []
        for j in np.arange(np.size(mat,1)):
            for i in np.arange(np.size(mat,0)):
                if mat[i,j] == 1:
                    
                    new_pixel = MovingPixelText(i,j)
                    pixel_liste.append(new_pixel)
                for l in np.arange(4) :
                    mat0 = 0*np.ones((8,32)).astype(np.uint8)
                    for pixel in pixel_liste :
                        tic = time.time()
                        x,ymin, ymax = pixel.move()
                        toc = time.time()
                        mat0[x,ymin:ymax] = 1
                    self.printImage(mat0,0,-2)
        
        print("toc = " +str(toc-tic))
        time.sleep(1)
        print(len(pixel_liste))
        
    def baLlrebond(self) :
        g=-1
        v0=10
        x=np.zeros(500)
        t = np.arange(500)
        i=0
        for j in t :
            x[j] = g*i**2/2+v0*i
            v_t = g*i
            if x[j] < 0 :
                if x[j-1]>=0 :
                    print("============")
                    v0 = -(v_t+v0)*0.9
                    i=0
            i+=0.5
        x=(np.round(x/np.max(x)*31)).astype(np.uint8)
        for x2 in x :
            mat = 0*np.ones((8,32)).astype(np.uint8)
            for y in np.arange(8) :
                mat[y,x2] = 1
                self.printImage(mat)
            time.sleep(0.03)    
            
    def textFall(self) :
        mat = 0*np.ones((8,32)).astype(np.uint8)
        mat_t = getMatFromFont("test22")
        tmp=mat_t
        mat_t = 0*np.ones((8,32)).astype(np.uint8)
        for i in np.arange(np.size(tmp,0)) :
            for j in np.arange(np.size(tmp,1)) :
                mat_t[i,j] = tmp[i,j]
        
        pos_x = np.zeros(32).astype(np.int8)
        for i in np.arange(np.size(mat,1)) :
            for j in np.arange(np.size(mat,0)-1,-1,-1) :
                if mat_t[j,i] == 1 :
                    pos_x[i] = j
                    
#        new_pixel = BouncingPixel(pos_x[1],1) 
#        for i in np.arange(31) :
#            x,y = new_pixel.move()
#            print(x,y)
#            print("========================================================")
#            
        pixel_liste = []
        
        for i in np.arange(np.size(mat,1)) :
            new_pixel = BouncingPixel(pos_x[i],i)
            pixel_liste.append(new_pixel)
        for i in np.arange(200) :
            mat = 0*np.ones((8,32)).astype(np.uint8)
#            mat2 = 0*np.ones((8,32)).astype(np.uint8)
#            
            for px in np.random.randint(0,32,8) :
                pixel_liste[px].init = 1
                
            for pixel in pixel_liste :
                x,y = pixel.move()
                mat_t[x,y] = 0
                mat[x,y] = 1
                mat2 = mat+mat_t
                self.printImage(mat2)
            time.sleep(0.05)
            
class BouncingPixel() :
    def __init__(self,x,y) :
        self.x0 = 7
        self.y0 = y
        self.ind = 0
        self.init = 0
        g=-1; v0=0; tps = np.arange(200); x=0*tps; t=0
        for j in tps :
            x[j] = g*t**2/2+v0*t + self.x0
            v_t = g*t
            if x[j] < 0 :
                if x[j-1]>=0 :
                    v0 = -(v_t+v0)*0.8
                    t=0
                    self.x0=0
            t+=0.5
        self.x= 7-x
        self.x = (self.x<8)*self.x + 7*(self.x>=8)  
        
    def move(self) :
        if self.init == 1 :
            self.x2 = self.x[self.ind]
            self.ind+=1
            return self.x2, self.y0
        else :
            return self.x0, self.y0
 


        
class MovingPixelText() :
    def __init__(self, x, y) :
        self.dest_x = x
        self.dest_y = y
        self.pos_x = x
        self.y_min = 31
        
    def move(self) :
        if self.dest_y != self.y_min :
            self.y_min -= 1
            self.y_max = self.y_min+8
            if self.y_max>31 :
                self.y_max = 31
        else :
            if self.y_max != self.dest_y+1:
                self.y_max-=1
        return self.pos_x, self.y_min, self.y_max
        

class Water() :
    def __init__(self) :
        self.x = np.random.randint(0,8,1,dtype='int')
        self.y = 31
        
    def fall(self,mat) :
        if self.y==0 :
            pass
        elif mat[self.x,self.y-1] == 0 :
            self.y-=1
        elif self.x!=7 and mat[self.x+1,self.y-1] == 0:
            self.x+=1
            self.y-=1
        elif self.x!=0 and mat[self.x-1,self.y-1] == 0 :
            self.x-=1
            self.y-=1
        else :
            pass
        return self.x, self.y
        
            
class Ball() :
    def __init__(self,x,y,vx,vy) :
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        
    def move(self) :
        self.x += self.vx
        self.y += self.vy
        if self.x+self.vx >= 8 or self.x+self.vx <= -1 :
            self.vx = - self.vx
        if self.y+self.vy >= 32 or self.y+self.vy<=-1 :
            self.vy = - self.vy
        return self.x, self.y
    
    