from sense_hat import SenseHat
import time, random

sense = SenseHat()

#COLORS
white = (255, 255, 255)
clear = (0, 0, 0)
red = (255, 0, 0)
blue =(0, 0, 255)
green= (0, 255, 0)

#list for generateUniqueX function
numbers = []

#VARIABLES
#setting start values for players position, health, score
playerPosLeft = 3
playerPosRight = 4
health = 3
score = 0

#varibale what counts seconds
seconds = time.time()

#boolean variable which turns True if players fails the game
failed = False

#boolean variable which checks, if meteorite is spawned first time
firstMeteor2 = False
firstMeteor3 = False

#FUNCTIONS
#function which turns pixels on from players position
def movePlayer():
  sense.set_pixel(playerPosLeft, 7, blue)
  sense.set_pixel(playerPosRight, 7, blue)
  
#clears players previous position
def clearPreviousPos():
  sense.set_pixel(playerPosLeft, 7, clear)
  sense.set_pixel(playerPosRight, 7, clear)

#function which keeps up the healthbar
def healthBar(currentHealth):
  i = currentHealth * 2 + 1
#turning pixels of from healthbar based on current health
  while i < 7:
    sense.set_pixel(i, 0, clear)
    i += 1
#setting pixels on to healthbar, only used first time this function is called
  i = currentHealth * 2
  while i > 0:
    sense.set_pixel(i, 0, red)
    i -= 1
  sense.set_pixel(7, 0, green)
  sense.set_pixel(0, 0, green)
  
#generates three x-values to meteorites that are unique from each other
def generateUniqueX(min, max):
    x = None
    while x in numbers or x is None:
        x = random.randint(min, max)
    numbers.append(x)
    if len(numbers) >= 3:
        numbers.pop(0)
    return x

#class for meteorites which player is supposed to catch
class Meteorite:
  def __init__(self, x, y):
    self.firstTime = True
    self.x = x
    self.y = y
#function which refresh meteorites position (making them constantly fall)
#and regenerates them if they go out of borders
  def refresh(self):
    global health
    global score
    
    if not self.firstTime:
      self.y += 1
    else:
      self.firstTime = False
    if self.x != playerPosLeft and self.x != playerPosRight and self.y >= 7:
      self.y = 1
      self.x = generateUniqueX(0, 7)
      health -= 1
      healthBar(health)
    elif (self.x == playerPosLeft or self.x == playerPosRight) and self.y >= 7:
      self.y = 1
      self.x = generateUniqueX(0, 7)
      score += 1
    sense.set_pixel(self.x, self.y, white)

#generating random positions for meteorites first time
meteorite1 = Meteorite(generateUniqueX(0, 7), 1)
meteorite2 = Meteorite(generateUniqueX(0, 7), 1)
meteorite3 = Meteorite(generateUniqueX(0, 7), 1)

#adding healthbar to senseHat screen
healthBar(health)

#starting the game
while True:
  
#checks if players health is gone, makes failed variable True
  if health == 0:
    failed = True
  
#check if player has failed the game
  if failed:
#shows your score in senseHat screen
    sense.show_message("Score:", text_colour=red)
    sense.show_message((str(score)), text_colour=white)
#restores default values to variables which can change during game
    firstMeteor2 = False
    firstMeteor3 = False
    playerPosLeft = 3
    playerPosRight = 4
    health = 3
    score = 0
#makes new starting positons for meteorites
    meteorite1 = Meteorite(generateUniqueX(0, 7), 1)
    meteorite2 = Meteorite(generateUniqueX(0, 7), 1)
    meteorite3 = Meteorite(generateUniqueX(0, 7), 1)
    healthBar(health)
    
    time.sleep(0.2)
#changes the value of failed back to True
    failed = False
    
  for event in sense.stick.get_events():
    if event.action == "pressed":
      if event.direction == "left":
        clearPreviousPos()
#makes sure player isn't alredy in edge of the screen
        if playerPosLeft <= 0:
          playerPosLeft = 0
#if it's not, changes players position
        else:
          playerPosLeft -= 1
          playerPosRight -= 1
      elif event.direction == "right":
        clearPreviousPos()
#makes sure player isn't alredy in edge of the screen
        if playerPosRight >= 7:
          playerPosRight = 7
#if it's not, changes players position
        else:
          playerPosLeft += 1
          playerPosRight += 1
#calls movePlayer() function to refresh players position
  movePlayer()
  
#check if 0.5 seconds has passed to make meteorites falling slower
  if time.time() - seconds >= 0.5:
#resets seconds variable back to 0 so previous if statment works correctly next time
    seconds = 0
    sense.set_pixel(meteorite1.x, meteorite1.y, clear)
    meteorite1.refresh()
#check if the first meteorite y position is already 4 or is meteor2 already spawned first time
    if meteorite1.y >= 3 or firstMeteor2:
      sense.set_pixel(meteorite2.x, meteorite2.y, clear)
      meteorite2.refresh()
      firstMeteor2 = True
#check if the second meteorite y position is already 4 or is meteor3 already spawned first time
    if meteorite2.y >= 3 or firstMeteor3:
      sense.set_pixel(meteorite3.x, meteorite3.y, clear)
      meteorite3.refresh()
      firstMeteor3 = True
#starts counting seconds again
    seconds = time.time()
