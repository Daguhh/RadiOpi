#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 12:40:03 2017

@author: david
"""
import RPi.GPIO as GPIO

# Initialisation de la numerotation et des E/S

class Button :
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        
    def State(self) :
        self.state = GPIO.input(self.pin)
        return self.state
        
    
class RotaryEncoder :
    def __init__(self) :
        GPIO.setmode(GPIO.BOARD)
        
        self.encoderPosCount = 0
        self.pinALast = 0
        self.direction = "None"
        
        self.btnSW = Button(23)
        self.btnCLK = Button(24)
        self.btnDT = Button(25)
        
        self.prev_state = btnCLK.State()
        
    def State(self) :
        if self.btnCLK.State() != self.prev_state :
            # le bouton à tourné
            if self.btnDT.State() == self.prev_state :
                self.direction = "clk" # sens horaire
                self.encoderPosCount += 1
            else :
                self.direction = "aclk" # sens anti-horaire
                self.encoderPosCount -= 1
        self.prev_state = btnCLK.State()
        
        return self.encoderPosCount, self.direction

    def Reset(self) :
        self.encoderPosCount = 0
        self.direction = "None"        

