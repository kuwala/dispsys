import pygame, os
import time, random

# my modules
from lcdDisp import DispSys
from oscServ import oscServerGuy
from models import synthState

    
# Creat the Objects and Start the ~Game
dispsys = DispSys()
dispsys.test()
clock = pygame.time.Clock()

# Create the oscServer


stateText = "start"
state = synthState()
oscServer = oscServerGuy(state)

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
      dunce = "troll"
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
      elif event.key == pygame.K_ESCAPE:
        done = True

  # LOGIC LOGIC
  if state.fresh == "hot":
    if state.txt == "/d":
      dispsys.drawDrums()
    elif state.txt == "/s":
      dispsys.drawSynth()
    elif state.txt == "/q":
      dispsys.drawSequencer()
    state.setCold()

  #if counter > 100:
  #  counter = 0
  #  if miniState % 2 == 0:
  #    dispsys.drawSynth()
  #  else :
  #    dispsys.drawDrums()
  #  miniState +=1

  dispsys.update()
  clock.tick(50)
  #counter += 1

print "Closing pygame"
pygame.quit()
print "Closing OSCServer"
oscServer.close()
print "Exited Gracefully"

