#This program is by Yoyo Liu 
#Completed: 12/31/2021 
#Uploaded to Github: 1/21/2024

import random
import time #for wait time

class Frame: 
  def __init__(self, frame_num, choice):#construct each frame
    self.frame_num = frame_num #make sure the frame number is clear
    self.throw_ball = 0 #make sure doesn't throw more than two times
    self.total_pin = 0 #total pins knock down eacj frame
    self.pin_limit = 10 #make sure does knock down more than pins available
    self.choice = choice #pass in the chosen game mode
  
  def make_pins(self):#specialized for 2D game
    print("\nHere is the board, each X represents an available pin, each O represents a pin that is knocked out.")#make the pin board
    board = [] #start with a blank board
    for x in range(4):
      board.append(["X"] * 7)#get the 2D array board
    for x in range(0, 4, 2):
      for y in range(1, 7, 2):#make places without pin empty, this is for the odd number rows
        board[x][y] = ' '
    for x in range(1, 4, 2):
      for y in range(0, 7, 2):#make places without pin empty, this is for the even number rows
        board[x][y] = ' '
    #extra space without pins identified
    board[2][0] = ' '
    board[2][6] = ' '
    board[3][1] = ' '
    board[3][5] = ' '
    for row in board:
      print(" ".join(row))#print board without the [] and stuff
    return board #return board for further use
  
  def knock(self, board):#specialized for 2D game
    prob_list = ["left", "center", "right"]#get the probability right (I spent at least 2 hours trying to figure out how to make sure the pins are not chaotic, so for example two pins on the very opposite side got knock down but not the middle ones, and I came up with this solution. It is definitely not the best as it sometimes still gave very chaotic solutions, but it is the best I can think of without implementing the paths of balls, probability of each pin getting knocked over when the near by pin falls, the skill of the bowler, etc.)
    side = random.choice(prob_list) #decide on a side that is mostly impacted
    collection = []#collection of the location of the pins
    pin = random.randint(0, self.pin_limit)#generate number of pins being knocked over
    for i in range(4):
      for j in range(7):
        if board[i][j] == 'X' or board[i][j] == 'O':
          location = [i,j]
          collection.append(location)#get every pin's location, whether available or not
    if side == "left":
      out = random.choices(collection, weights = (50, 20, 10, 5, 40, 10, 5, 30, 10, 20), k = pin)#if the ball comes from the left side, the probability of the pins on the left side being knocked down is higher than the ones on the right. With the right corner having the least possibility. It will choose location base on the number of pins that is being knocked over. The probability is not a percentage, but rather relative probability so it does not add up to 100. Also, to make sure a strike and a spare is still possible, I did not make the probability of the very right corner one 0, but it may cause some chaotic result like two corner ones being knocked over but not the middle, but the small probability helps to minimize that. 
    if side == "center":
      out = random.choices(collection, weights = (10, 20, 20, 10, 15, 30, 15, 30, 30, 50), k = pin)#similar to the one above, but the center ones now have higher probability. 
    if side == "right":
      out = random.choices(collection, weights = (5, 10, 20, 50, 5, 10, 40, 10, 30, 20), k = pin)#similar to the left one
    for i in out:#for every pin that is being knocked out
      if board[i[0]][i[1]] == 'X':#if it is not being knocked out before during the first throw
        board[i[0]][i[1]] = 'O'#mark it as knocked out
      elif board[i[0]][i[1]] == 'O':#if it has already been knocked over
        pin -= 1#decrease the number of pins knocked over in this throw by 1. I use this instead of just calculating the pins NOT being knocked over in the previous step because I think in real life, it is more difficult second throw than first throw, and since I want this to be as close as to real life bowling experience, making second throw harder is more accurate. 
    
    for row in board:
      print(" ".join(row))#print the board again. 
    return pin, board#return the number of pins being knocked down this throw, and the board so second throw is based on first throw's board. 
  
  def throw(self, the_board):#this is the general throwing method for both games
    word = '' #set the word, later identity the types of throw
    global points #get poins from outside the class
    if self.throw_ball < 2: #only throw if the throw number is less than 2 times
      self.throw_ball += 1 #identify which throw this is
      if self.choice == 1: #if choose the Pure Chance Game
        pin = random.randint(0, self.pin_limit)#generate a number for knocked down pins
      elif self.choice == 2: #if want the more complex game
        if self.throw_ball == 1: #generate new board if first throw in frame
          the_board = self.make_pins()
        pin, the_board = self.knock(the_board)#use the board (just newly generated OR passed in from the first thrwo)
      self.pin_limit -= pin #decrease the amount of pins available 
      self.total_pin += pin #increase the amount of pins being knocked down
      if self.throw_ball == 1 and self.total_pin == 10: #if strick
        points += 20 #get 20 points
        word = "Strike! You get 20 points! " #Key word to strike
        self.throw_ball += 1#no need second throw so change it to second throw already finished
      elif self.throw_ball == 2 and self.total_pin == 10: #if spare
        points += 15 #add 15 points
        points -= 10-pin #make sure the amount does not exceed 15 points
        word = "Spare! You get 15 points this frame! " #key word to spare
      elif self.total_pin != 10: #if not spare nor strike
        points += pin #get points = to pins being knocked over
      if pin == 0:
        notice = "Aww, you hit 0 pins. It's okay! You can do this!" #display sadness for user
        the_throw_num = str(self.throw_ball)#identify throw num
      else:
        notice = "Great job! You hit " + str(pin) + " pins in this throw." #congrat user
        if word == "Strike! You get 20 points! ":
          the_throw_num = str(self.throw_ball-1)#make sure to display throw one and not throw 2
        else: 
          the_throw_num = str(self.throw_ball)#identify throw num
      print("\nFrame " + str(self.frame_num) + " Throw " + the_throw_num)#show current frame + throw
      print(word + notice) #tell them how they did
      print("The current score is: " + str(points) + " points.")#show score
    return the_board #return board for second throw (if first throw)



game_on = input("Hello, welcome to Yoyo's Bowling Game! Press enter to continue. Press 'q' to quit.")#greet user when first entered the game

while game_on != 'q':#if user do not want to quit
  game_selection = False #for game selection while loop
  game_type = ''#not define game mode
  points = 0 #points start at zero
  rule_or_not = input("\nAre you ready? Press 'R' to get the rules. Press enter to choose a game mode!\n")#ask whether want to see the rules
  if rule_or_not == 'R' or rule_or_not == 'r':
    print("\nRules:\nA game of bowling consists of ten frames. In each frame, the bowler will have two chances to knock down as many pins (total of 10 pins) as possible with their bowling ball. \n\nPoints: \nIf you throw a strike, (when all ten pins are knocked over on the first throw of a frame), you get 20 points and no second throw. \nIf you throw a spare (when all ten pins are knocked over within the two throws of a frame), you get 15 points. \nIf you did not knock over all ten, the amount of pins you knock down is the points you will gain in this round.\n\nThere are two game modes: \nPure Chance: You won't be able to see which pins are knocked down. - Great for fast game. \n2D Visual Game: You can see which pins you knock down each throw, BUT you won't be able to control how the ball goes. - Great for people who would like some frustration and a better experience.")#display rules
    time.sleep(3)#allow user to read
    quit_rules= input("\nPress enter to continue.")#quit rule page

  while game_selection == False:
    game_type = input("\nWould you like to playe Pure Chance Game or 2D Visual Game? Press '1' for Pure Chance Game, '2' for 2D Visual Game. Please enter 1 or 2.")#ask user which mode to play
    if game_type == "1" or game_type == "2":#if user input a correct mode
      game_selection = True #exit the loop (loop will not run again)
    else: 
      game_selection = False#if user did not input the correct selection, run it again
  frames = [Frame(i+1, int(game_type)) for i in range(10)]#make all 10 frames

  for i in range(10): 
    board = ' '#make the board empty so we can change later in each frame
    first_throw = frames[i].throw(board)#get first throw
    time.sleep(2)#wait between throws
    frames[i].throw(first_throw)#get second throw base on first throw
    if i == 9: #if 10 frames all finished
      print("\nWow this game went by so fast!")#feel happy for the user
      time.sleep(1)#wait a second, creates mood
      print("\nAmazing job! You have a total of " + str(points) + " points!\n")#give them their points
      time.sleep(1)#wait another second
      game_on = input("Do you want to start another game? Press any key to start a new game, or 'Q' to quiz this game.")#ask if they want to play again
    else: 
      input("Great, press enter to continue to the next frame!\n")#if 10 frame did not finish, continue to the next frame

print("\nThank you so much for playing this game! Don't forget to check out Meme's Yahtzee Game as well! See you soon!")#Express gratefulness for playing the game, ask them to buy more product, jk. 