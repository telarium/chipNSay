#!/usr/bin/env python
#
# CHIP 'n SAY by Next Thing Co 2015
# Powered by C.H.I.P., the world's first $9 computer!
# This sets the state of various GPIO pins

import os
import time
import subprocess
from threading import Thread

class GPIO:
    def __init__(self):
        self.pins = []
        self.inputPins = []
        self.outputPins = []
        
    def setup(self,pin,direction):
        cmd = "echo " + str(pin) + " > /sys/class/gpio/export"
        subprocess.call(cmd,shell=True, stdout=subprocess.PIPE)
        cmd = "echo \"" + direction + "\" > /sys/class/gpio/gpio" + str(pin) + "/direction" 
        subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
        self.pins.append([pin,0,0])
        if( direction == "in"):
            self.inputPins.append([pin,0,0])
        else:
            self.outputPins.append([pin,0,0])
            self.set( pin, 0 )

    def readAll(self):
        results = []
        cmd = "cat"
        for pinObject in self.inputPins:
            cmd = cmd + " /sys/class/gpio/gpio" + str(pinObject[0]) + "/value"

        result = subprocess.check_output(cmd,shell=True)
        result = result.split('\n')
        for i in result:
            try:
                results.append(int(i))
            except:
                result = None

        return results

    def read(self,pin):
        cmd = "cat /sys/class/gpio/gpio" + str(pin) + "/value"
        result = subprocess.check_output(cmd,shell=True)
        return( int(result) )
        
    def set(self,pin, val):
        if ( self.pins != None ):
            for pinObject in self.outputPins:
                if(pinObject[0]==pin and pinObject[1]!=val):
                    pinObject[1]=val
                    cmd = "echo " + str(val) + " > /sys/class/gpio/gpio" + str(pinObject[0]) + "/value"
                    subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
        
    def cleanup(self):
        for pinObject in self.pins:
            cmd = "echo " + str(pinObject[0]) + " > /sys/class/gpio/unexport"
            subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
            self.pins = None