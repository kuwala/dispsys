# DispSys for SynthOS - Daanniieell
# this is the main app file. Run this !!
# python dispSys.py
# you may need sudo to access the FrameBuffer ??
# it has the game loop and the application
#
# imports the OSC Server wich passes data to the 
# syntState wich is the model

import pygame, os
import time, random

# my code modules
from lcdDisp import LcdDisp # RENAME to MODULE MANAGER
from oscServ import oscServerGuy
from models import synthState

# Create OSCContainer obj
savedOSC = synthState()

# Create the oscServer
oscServer = oscServerGuy(savedOSC)

# Creat the Objects and Start the ~Game
moduleManager = LcdDisp()
moduleManager.setState(savedOSC)
moduleManager.drawHello()
clock = pygame.time.Clock()

done = False
clock = pygame.time.Clock()

# ~Game Loop
while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.MOUSEBUTTONUP:
      #done = True
      pass
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        savedOSC.receive("/s", "tags go here", [-1])
        savedOSC.setHot()
      elif event.key == pygame.K_d:
        savedOSC.receive("/d", "tags go here", [-1])
        savedOSC.setHot()
        moduleManager.drawDrums()
      elif event.key == pygame.K_1:
        moduleManager.drawGrid(64)
      elif event.key == pygame.K_2:
        moduleManager.drawGrid(32)
      elif event.key == pygame.K_3:
        moduleManager.drawGrid(16)
      elif event.key == pygame.K_q:
        moduleManager.drawSequencer()
      elif event.key == pygame.K_r:
        moduleManager.recMod.randomPercent()
        moduleManager.drawRecMod()
      elif event.key == pygame.K_v:
        moduleManager.visModTest()
      elif event.key == pygame.K_ESCAPE:
        done = True


  # Does Logic & Routes Input from state
  # sends CPU Tick update to active module(s)
  moduleManager.update()
  
  # Draws screen to the Display
  # with pygame
  moduleManager.drawScreen()
  clock.tick(50)

print "Closing pygame"
pygame.quit()
print "Closing OSCServer"
oscServer.close()
print "Exited Gracefully"

