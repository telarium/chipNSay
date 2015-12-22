#!/usr/bin/python
# CHIP 'n Say by Next Thing Co
# Powered by C.H.I.P., the world's first $9 computer!

# sudo apt-get install python-pygame

import pygame
import pygame.mixer
import sys
import time
import subprocess
from pygame.locals import *
from threading import Thread
from chipNSay_gpio import GPIO

# Declare CHIP's IO pins for each slot on the See 'n Say

SLOT1 = 101 # LCD-D5
SLOT2 = 115 # LCD-D19
SLOT3 = 116 # LCD-D20
SLOT4 = 114 # LCD-D18
SLOT5 = 118 # LCD-D22
SLOT6 = 117 # LCD-D21
SLOT7 = 111 # LCD-D15
SLOT8 = 119 # LCD-D23
SLOT9 = 109 # LCD-D13
SLOT10 = 107 # LCD-D11
SLOT11 = 103 # LCD-D7
SLOT12 = 99 # LCD-D3

io = GPIO() #Establish connection to our GPIO pins.

pygame.init()
pygame.mixer.init()
pygame.audio = None
pygame.pressed = None
pygame.isRunning = True
pygame.timeSinceLastPlay = time.time()
pygame.slots = [SLOT1,SLOT2,SLOT3,SLOT4,SLOT5,SLOT6,SLOT7,SLOT8,SLOT9,SLOT10,SLOT11,SLOT12]

for i in range(len(pygame.slots)):
    io.setup( pygame.slots[i], "in" )

def main(args):

    subprocess.Popen('amixer cset numid=1 100%' ,shell=True, stdout=subprocess.PIPE ) # Set PA mixer volume to 100%
    subprocess.Popen('amixer cset numid=4 1' ,shell=True, stdout=subprocess.PIPE ) # Set DAC self.output to be "Mixed"

    while pygame.isRunning:
        try:
            if( pygame.pressed != None and io.read(pygame.slots[pygame.pressed]) == 1 ):
                pygame.isRunning = True
            elif( pygame.pressed != None and io.read(pygame.slots[pygame.pressed]) == 0 ):
                if( time.time() - pygame.timeSinceLastPlay > 1.2 ):
                    pygame.timeSinceLastPlay = time.time()
                    pygame.sound.play()

                pygame.pressed = None
            else:
                pygame.pressed = None
                i = -1
                for pin in io.readAll():
                    i = i + 1
                    if( pin == 1 ):
                        pygame.timeSinceLastPlay - time.time()
                        pygame.pressed = i
                        print( i+1 )
                        pygame.sound = pygame.mixer.Sound(str(i+1) + ".wav")
                        break

        except KeyboardInterrupt:
            pygame.isRunning = False
            io.cleanup()
            pygame.quit()
            sys.exit(1)
             
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


