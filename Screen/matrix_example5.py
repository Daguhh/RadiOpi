#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

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
from Methodes import animations, parcourir_menu
            
def demo2(w, h, block_orientation, rotate): 
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded= 4, rotate=rotate, block_orientation=block_orientation)
    device.contrast(1)
    
    b = animations.tXt2(device)
    print("=(=(=(==(==(=(==(=(=(=(=(==(==========================((((((((((((")
    a = animations.makeFigure(device)
    a.slIce()
    b.slIce()
    a.slIce()
    b.slIce()
    a.slIce()
#    b.slIce(txt="david", side=[0,-1])
#    a.spiRal()
#    a.textFall()
    a.baLlrebond()
    a.siNus()
#    a.baLl()
#    a.maGnetism()
#    a.waTer()

    menus = parcourir_menu.ScreenMatrix(device)
    while 1 :
        menus.menuNavigation()
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('--width', type=int, default=8, help='Width')
    parser.add_argument('--height', type=int, default=8, help='height')
    parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotation factor')

    args = parser.parse_args()

    try:
        demo2(args.width, args.height, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        pass
