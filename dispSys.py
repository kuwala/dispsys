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
from lcdDisp import DispSys
from oscServ import oscServerGuy
from models import synthState

    
# Create state obj
state = synthState()

# Create the oscServer
oscServer = oscServerGuy(state)

# Creat the Objects and Start the ~Game
dispsys = DispSys()
dispsys.setState(state)
dispsys.drawHello()
clock = pygame.time.Clock()

done = False
clock = pygame.time.Clock()
counter = 0
miniState = 0

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
        dispsys.drawSynth()
      elif event.key == pygame.K_d:
        dispsys.drawDrums()
      elif event.key == pygame.K_1:
        dispsys.drawGrid(64)
      elif event.key == pygame.K_2:
        dispsys.drawGrid(32)
      elif event.key == pygame.K_3:
        dispsys.drawGrid(16)
      elif event.key == pygame.K_q:
        dispsys.drawSequencer()
      elif event.key == pygame.K_w:
        dispsys.testNewSeq()
      elif event.key == pygame.K_v:
        dispsys.visModTest()
      elif event.key == pygame.K_ESCAPE:
        done = True


  # Does Logic & Routes Input
  #dispsys.visModTest()
  dispsys.update()

  dispsys.drawScreen()
  clock.tick(50)
  #counter += 1

print "Closing pygame"
pygame.quit()
print "Closing OSCServer"
oscServer.close()
print "Exited Gracefully"

