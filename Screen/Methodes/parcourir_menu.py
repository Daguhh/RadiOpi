#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 12:39:55 2017

@author: david
"""

import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message, textsize
# from myinitfont import text, show_message, textsize
from luma.core.legacy.font import  proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from myfont import MINI_FONT, DRAWING_FONT
import numpy as np
from arborescence_menu import MENU_TREE
from PIL import Image, ImageDraw, ImageFont
# PIL.ImageFont.truetype(font=None, size=10, index=0, encoding='', layout_engine=None)



class OutOfBoundExcept(Exception):
    def __init__(self,raison):
        self.raison = raison
    def __str__(self):
        return self.raison
    
class ScreenMatrix() :
    def __init__(self,device) :
        self.device = device
        self.menus = MENU_TREE
        self.menu_ind = [1,0,0]
        self.sous_menu = 0
        self.y_offset = -2
        self.printText()
        
    def menuNavigation(self) :
        key=input("=====  zqsd  =====")     
        try :         
            # move direction
            if key == "z" : 
                xdir=0; ydir=1 
                self.device.contrast(15)
            elif key ==  "s" :
                self.device.contrast(0)
                xdir=0; ydir=-1
            elif key == "d" :
                xdir=1; ydir=0
            elif key == "q" : 
                xdir=-1; ydir=0
                
            # test border
            self.test_bound(self.menu_ind[:], self.sous_menu, xdir, ydir) 
            
            # calcul des nouveaux indices
            old = self.menu_ind[:]  
            if key in {"z","s"} :
                self.menu_ind[self.sous_menu] += xdir+ydir
            elif key in {"d"} :
                self.sous_menu += xdir
                self.menu_ind[self.sous_menu] += xdir+ydir
            elif key in {"q"} :
                self.menu_ind[self.sous_menu]=0
                self.sous_menu += xdir    
            new = self.menu_ind[:]
            
            # deplacement de old vers new
            self.slideText(old, new, xdir, ydir)
            
        except OutOfBoundExcept as e:
                print(e)
                
    
    def get_text(self,i) :
        txt = self.menus[i[0]][i[1]][i[2]]
        return txt
    
    def test_bound(self, ind, sous_menu, xdir, ydir) :
        out = 0
        sous_menu += xdir
        if sous_menu<0 or sous_menu>2 : out = 1
        else : ind[sous_menu] += ydir 
        if ind[self.sous_menu]<=0 : out = 1
        try : self.get_text(ind)
        except : out = 1
        if out == 1 : self.boundEffect(xdir,ydir); raise OutOfBoundExcept("Out Of Bound") 
        else : return out
           
    def printText(self) :
        txt = self.get_text(self.menu_ind)
        with canvas(self.device) as draw:        
            text(draw, (0, self.y_offset), txt, fill="white", font=proportional(MINI_FONT))
            
    def slideText(self, old_ind, new_ind, xdir, ydir) :
        new_text = self.get_text(new_ind)
        old_text = self.get_text(old_ind)
        if xdir!=0 : mouvement = xdir*(-1-np.arange(32))
        if ydir!=0 : mouvement = ydir*(-1-np.arange(6))
        for step in mouvement :
            with canvas(self.device) as draw:     
                # coordonnées des déplacments
                x_new = (xdir!=0) * (step+xdir*32)
                y_new = (ydir!=0) * (step + 6*ydir) + self.y_offset
                x_old = (xdir!=0) * step
                y_old = (ydir!=0) * (step) + self.y_offset               
                # dessine texte
                text(draw, (x_old, y_old), old_text, fill="white", font=proportional(MINI_FONT))
                text(draw, (x_new, y_new), new_text, fill="white", font=proportional(MINI_FONT))
            time.sleep(0.03)
    
    def boundEffect(self, xdir, ydir):
        texte = self.get_text(self.menu_ind)
        for step in [0,1,2,1,0] :
            with canvas(self.device) as draw:     
                # coordonnées des déplacments
                x_new = (xdir!=0) * -xdir * (step)
                y_new = (ydir!=0) * -ydir * (step) + self.y_offset             
                # dessine texte
                text(draw, (x_new, y_new), texte, fill="white", font=proportional(MINI_FONT))
                time.sleep(0.06)
