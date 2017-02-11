#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  puissance4.py
#  Created by CLOVIS
#  More about me on clovis-cyclone.blogspot.fr (actually in english)
#  
#  All the informations about the creation and managing of bots, and of
#  all the others options is on this project's github page :
#  github.com/CLOVIS-AI/connect-4
#  
#  Sharing this file is allowed whatever the usage might be. In this case,
#  all the places where my name is mentionned and this header should
#  remain unchanged (except for the file name, coding and path). You are
#  free to change any other line.

import os
import time
import random



# --------------------- PLAYERS

# ----------- GENERAL
player_turn = 2
manches = 3
empty_char = " "

# ----------- PLAYER 1
play1_isPlayer = 0 #Typo : isNotPlayer
play1_name = "Player 1"
play1_score = 0
play1_symbol = "X"
play1_tournamentName = ""


# ----------- PLAYER 2
play2_isPlayer = 0 #Typo : isNotPlayer
play2_name = "Player 2"
play2_score = 0
play2_symbol = "O"
play2_tournamentName = ""

# ----------- Bots
AI_list = []
AI_data = []
def AI_data_refresh():
	AI_data.append(randomBot_infos())
	AI_list.append(randomBot_infos()[0])

# ----------- Tournament
players = [] # players[][0] = name | players[][1] = isPlayer | players[][2] = score | players[][3] = symbol
def newPlayer(name, isPlayer, symbol):
	players.append([name, isPlayer, 0, symbol])


# --------------------- BOARDS

# ----------- BOARD
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
board_width = 9
board_height = 9

# ----------- SCREEN
screen = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
spaces = []
for i in range(50):
	s = ""
	for j in range(i):
		if j%2 == 1:
			s = s+" "
		else:
			s = s+"|"
	spaces.append(s)



# --------------------- FUNCTIONS

def replaceChar(string, replaceBy, index):
	return string[:index] + replaceBy + string[index + 1:]

# ----------- GET SYMBOL
def getSymbol(player):
	if(player == 1):
		return play1_symbol
	elif(player == 2):
		return play2_symbol
	elif(player == 0):
		return empty_char
	else:
		return player

# ----------- REFRESH BOARD
def refreshBoard():
	drawBoard()
	time.sleep(0.1)
	wasUseful = False
	# 1. Find pawns
	for i in range(board_width):
		for j in range(board_height-1):
			if(str(board[i][j+1]) != "0"):
				# 2. Is that pawn floating ?
				if(board[i][j] == 0): # it is floating
					board[i][j] = board[i][j+1]
					board[i][j+1] = 0
					wasUseful = True
	return wasUseful
			
# ----------- CHECK IF 4 ALIGNED
def check():
	global play1_score
	global play2_score
	wasUseful = False
	# 1. Find pawns
	for i in range(board_width):
		for j in range(board_height):
			if(board[i][j] != 0):
				# 2. Is it aligned with something ?
				if(i <= board_width -4 and board[i][j] == board[i+1][j] and board[i][j] == board[i+2][j] and board[i][j] == board[i+3][j]):
					# Horizontally !
					if(board[i][j] == 1):
						play1_score = play1_score + 1
					elif(board[i][j] == 2):
						play2_score = play2_score + 1
					board[i][j] = 0
					board[i+1][j] = 0
					board[i+2][j] = 0
					board[i+3][j] = 0
					wasUseful = True
				elif(j <= board_height -4 and board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2] and board[i][j] == board[i][j+3]):
					# Vertically !
					if(board[i][j] == 1):
						play1_score = play1_score + 1
					elif(board[i][j] == 2):
						play2_score = play2_score + 1
					board[i][j] = 0
					board[i][j+1] = 0
					board[i][j+2] = 0
					board[i][j+3] = 0
					wasUseful = True
				elif(j <= board_height -4 and i <= board_width -4 and board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2] and board[i][j] == board[i+3][j+3]):
					# Diagonally right-top
					if(board[i][j] == 1):
						play1_score = play1_score + 1
					elif(board[i][j] == 2):
						play2_score = play2_score + 1
					board[i][j] = 0
					board[i+1][j+1] = 0
					board[i+2][j+2] = 0
					board[i+3][j+3] = 0
					wasUseful = True
				elif(j <= board_height -4 and i >= 3 and board[i][j] == board[i-1][j+1] and board[i][j] == board[i-2][j+2] and board[i][j] == board[i-3][j+3]):
					# Diagonally left-top
					if(board[i][j] == 1):
						play1_score = play1_score + 1
					elif(board[i][j] == 2):
						play2_score = play2_score + 1
					board[i][j] = 0
					board[i-1][j+1] = 0
					board[i-2][j+2] = 0
					board[i-3][j+3] = 0
					wasUseful = True
	while refreshBoard():
		pass
	return wasUseful

# ----------- DISPLAY SCREEN
def drawBoard():
	resetScreen()
	# Windows clear :
	# os.system('CLS')
	# Linux clear :
	os.system('clear')
	# Print the screen :
	print("# ----------------------------- #")
	for i in range(len(screen)):
		if len(players) == 0:
			print("# "+screen[i]+" #")
		else:
			if i == 0:
				print("# "+screen[i]+" # Tournament Mode")
			elif i-1 < len(players):
				if players[i-1][0] == play1_tournamentName:
					if play1_isPlayer != 0:
						print("# "+screen[i]+" # "+"1~  "+spaces[int(players[i-1][2]*2)]+players[i-1][0]+" ("+players[i-1][3]+")")
					else:
						print("# "+screen[i]+" # "+"1-  "+spaces[int(players[i-1][2]*2)]+players[i-1][0]+" ("+players[i-1][3]+")")
				elif players[i-1][0] == play2_tournamentName:
					if play2_isPlayer != 0:
						print("# "+screen[i]+" # "+"2~  "+spaces[int(players[i-1][2]*2)]+players[i-1][0]+" ("+players[i-1][3]+")")
					else:
						print("# "+screen[i]+" # "+"2-  "+spaces[int(players[i-1][2]*2)]+players[i-1][0]+" ("+players[i-1][3]+")")
				else:
					print("# "+screen[i]+" # "+"    "+spaces[int(players[i-1][2]*2)]+players[i-1][0]+" ("+players[i-1][3]+")")
			else:
				print("# "+screen[i]+" #")
	print("# ----------------------------- #")

def resetScreen():
	# Line 0
	screen[0] = "     V S     "
	if(play1_isPlayer == False):
		screen[0] = play1_name + screen[0]
	else:
		screen[0] = "<AI/>   " + screen[0]
	if(play2_isPlayer == False):
		screen[0] = screen[0] + play2_name
	else:
		screen[0] = screen[0] + "   <AI/>"
	# Line 1
	screen[1] = str(play1_symbol) + ":" + str(play1_score) + "   1 2 3 4 5 6 7 8 9   " + str(play2_score) + ":" + str(play2_symbol)
	# Line 2
	screen[2] = "                             "
	# Line 3&...
	for j in range(board_height-1, -1, -1):
		stri = ""
		for i in range(board_width):
			stri = stri + getSymbol(board[i][j]) + " "
			#print("["+str(i)+";"+str(j)+"] > "+getSymbol(board[i][j]))
		screen[2+(board_width - j)] = "      " + stri + "     "
		
	screen[12] = "                             "
	screen[13] = "      1 2 3 4 5 6 7 8 9      "
	# Add the score
	for i in range(9):
		if i+1 > manches:
			pass
		elif i+1 > play1_score:
			screen[11-i] = replaceChar(screen[11-i], ".", 2)
		else:
			screen[11-i] = replaceChar(screen[11-i], play1_symbol, 2)
	for i in range(9):
		if i+1 > manches:
			pass
		elif i+1 > play2_score:
			screen[11-i] = replaceChar(screen[11-i], ".", len(screen[11-1])-3)
		else:
			screen[11-i] = replaceChar(screen[11-i], play2_symbol, len(screen[11-1])-3)

resetScreen()

# --------------------- FUNCTIONS

def askNumber(text, lowerLimit, upperLimit):
	#Asks an input from the user, checked
	lowerLimit, upperLimit = float(lowerLimit), float(upperLimit)
	while True:
		a = float(checkIfNumber(text))
		if a >= lowerLimit and a <= upperLimit:
			break
		else:
			print("It appears this input is incorrect. It is either because :\n\tThe input is not a number,\n\tThe input does not validate : "+str(lowerLimit)+"<=x<="+str(upperLimit)+"\nPlease try again.\n")
	return a

def checkIfNumber(text):
	a=(raw_input(text))
	try:
		int(a)
	except ValueError:
		try:
			float(a)
		except ValueError:
			a= 450
	if a== 450:
		a= 450
		return False
	else:
		return a

def playBot(bot_ID, player):
	if bot_ID == 1:
		return randomBot_play(player)

def play(player, column):
	s = ""
	if(player == 1):
		s = 1
	elif(player == 2):
		s = 2
	else:
		s = player
	if(board[column][board_height-1] == 0):
		board[column][board_height-1] = s
		return True
	else:
		return False





def game(player_turn):
	global play1_score
	global play2_score
	play1_score = 0
	play2_score = 0
	gameOn = True
	while gameOn:
		drawBoard()
		print("")
		# Swap player's turn
		if(player_turn == 1):
			player_turn = 2
		else:
			player_turn = 1
		# Ask where the player wants to play
		good = False
		a = 0
		while good == False:
			if player_turn == 1 and play1_isPlayer == 0 or player_turn == 2 and play2_isPlayer == 0:
				if play1_tournamentName == "" and play2_tournamentName == "":
					a = int(askNumber("It's player "+str(player_turn)+"'s turn (" + getSymbol(player_turn) + ").\nWhere do you want to play ? ", 1, 9))
				elif player_turn == 1:
					a = int(askNumber("It's "+play1_tournamentName+"'s turn (" + getSymbol(player_turn) + ").\nWhere do you want to play ? ", 1, 9))
				elif player_turn == 2:
					a = int(askNumber("It's "+play2_tournamentName+"'s turn (" + getSymbol(player_turn) + ").\nWhere do you want to play ? ", 1, 9))
				else :
					print("Error in game()")
			elif player_turn == 1 and play1_isPlayer != 0:
				a = playBot(play1_isPlayer, player_turn)
			elif player_turn == 2 and play2_isPlayer != 0:
				a = playBot(play2_isPlayer, player_turn)
			else:
				a = 1
			if a != None and play(player_turn, a-1):
				good = True
		while refreshBoard():
			pass
		# Check if no 4s aligned
		while check() == True:
			pass
		time.sleep(0.0)
		if play1_score >= manches:
			break
		elif play2_score >= manches:
			break
		# Checking if full
		full = True
		for i in range(board_width):
			if board[i][board_height-1] == 0:
				full = False
		if full:
			drawTextQuick(False)
	

def drawText(line1, line2, line3, line4, line5, line6, line7, line8, line9, erase):
	for i in range(board_width+9):
		if(i < board_width):
			play(line9[i], i)
		if(i > 0 and i < board_width+1):
			play(line8[i-1], i-1)
		if(i > 1 and i < board_width+2):
			play(line7[i-2], i-2)
		if(i > 2 and i < board_width+3):
			play(line6[i-3], i-3)
		if(i > 3 and i < board_width+4):
			play(line5[i-4], i-4)
		if(i > 4 and i < board_width+5):
			play(line4[i-5], i-5)
		if(i > 5 and i < board_width+6):
			play(line3[i-6], i-6)
		if(i > 6 and i < board_width+7):
			play(line2[i-7], i-7)
		if(i > 7 and i < board_width+8):
			play(line1[i-8], i-8)
		refreshBoard()
	if(erase == False):
		return
	time.sleep(1.0)
	for j in range(board_height):
		for i in range(board_width):
			board[i][0] = 0
		refreshBoard()

def drawTextQuick(t):
	if(t == False):
		drawText("         ", "         ", "         ", "         ", "         ", "         ", "         ", "         ", "         ", True)
	elif(t == True):
		drawText("#########", "#########", "#########", "#########", "#########", "#########", "#########", "#########", "#########", True)

# --------------------- BOT API

# Explanations
# Each bot is qualified by a <name>_play() function and a <name>_infos() function.

# getBoardSize()
def API_getBoardHeight():
	return board_height

def API_getBoardWidth():
	return board_width

# getStateAt(player, x, y)
# player - your player ID
# x, y - coordinates
def API_getStateAt(player, x, y):
	if x >= 0 and x < board_width and y >= 0 and y < board_height:
		if player == board[x][y]:
			return "you"
		elif player != board[x][y]:
			return "other"
		else:
			return "none"
	else:
		return "error"

# getColumn(player, x)
# player - your player ID
# x - coordinates
def API_getColumn(player, x):
	t = []
	for i in range(board_height):
		t.append(API_getStateAt(player, x, i))
	return t

# getLength()
def API_getLength():
	return manches

# getScores(player)
# player - your player ID
def API_getScores(player):
	if player == 1:
		return play1_score, play2_score
	else:
		return play2_score, play1_score

# You also need to provide :
# <name>_infos()
#   return ["your name", "your creator", <do you allow for multiple instances ?>]

# --------------------- BOTS

# ----------- Random
def randomBot_play(player):
	return random.randrange(0, API_getBoardWidth())
def randomBot_infos():
	return ["random", "CLOVIS", True]

# --------------------- THE ACTUAL GAME

AI_data_refresh()
close = True
while close == True:
	drawText("         ", #1
	         "CONNECT-4", #2
			 "         ", #3
			 "   ***   ", #4
			 "         ", #5
			 "A GAME BY", #6
			 "         ", #7
			 "  CLOVIS ", #8
			 "         ", True) #9
	drawText(" * Menu *", #1
			 "         ", #2
			 "1-Play   ", #3
			 "2-Players", #4
			 "3-Tourna-", #5
			 "    -ment", #6
			 "4-Length ", #7
			 "   of the", #8
			 "    games", False) #9
	c = int(askNumber("Your choice : ", 1, 4))
	if(c == 1):
		drawTextQuick(False)
		play1_symbol = "O"
		play2_symbol = "X"
		game(player_turn)
		if play1_score > play2_score:
			drawTextQuick(False)
			drawText(" And the ", #1
			    	 "winner is", #2
					 "   ...   ", #3
					 "         ", #4
					 "         ", #5
					 "         ", #6
					 " Player1 ", #7
					 "   !!!   ", #8
				 	 "         ", True) #9
		elif play1_score < play2_score:
			drawTextQuick(False)
			drawText(" And the ", #1
			    	 "winner is", #2
					 "   ...   ", #3
					 "         ", #4
					 "         ", #5
					 "         ", #6
					 " Player2 ", #7
					 "   !!!   ", #8
				 	 "         ", True) #9
		else:
			drawTextQuick(False)
			drawText(" And the ", #1
			    	 "winner is", #2
					 "   ...   ", #3
					 "         ", #4
					 "         ", #5
					 "   IT'S  ", #6
					 "  A DRAW ", #7
					 "   !!!   ", #8
				 	 "         ", True) #9
	elif(c == 2):
		drawTextQuick(False)
		drawText(" Players ", #1
				 "         ", #2
				 "1-Player1", #3
				 "2-Player2", #4
				 "         ", #5
				 "         ", #6
				 "         ", #7
				 "         ", #8
				 "         ", False) #9
		c2 = int(askNumber("Your choice : ", 1, 4))
		if(c2 == 1):
			drawTextQuick(False)
			drawText(" Player1 ", #1
			    	 "         ", #2
					 "1-AI     ", #3
					 "2-Player ", #4
					 "         ", #5
					 "         ", #6
					 "         ", #7
					 "         ", #8
				 	 "         ", False) #9
			c3 = int(askNumber("Your choice : ", 1, 2))
			if(c3 == 1):
				print("Choose your AI:")
				for i in range(len(AI_list)):
					print(str(i+1) + ". "+AI_list[i])
				c4 = int(askNumber("Your choice : ", 1, len(AI_list)))
				play1_isPlayer = c4
			else:
				play1_isPlayer = 0
		else:
			drawTextQuick(False)
			drawText(" Player2 ", #1
			    	 "         ", #2
					 "1-AI     ", #3
					 "2-Player ", #4
					 "         ", #5
					 "         ", #6
					 "         ", #7
					 "         ", #8
				 	 "         ", False) #9
			c3 = int(askNumber("Your choice : ", 1, 2))
			if(c3 == 1):
				print("Choose your AI:")
				for i in range(len(AI_list)):
					print(str(i+1) + ". "+AI_list[i])
				c4 = int(askNumber("Your choice : ", 1, len(AI_list)))
				play2_isPlayer = c4
			else:
				play2_isPlayer = 0
	elif(c == 3):
		drawTextQuick(False)
		drawText("         ", #1
				 " Welcome ", #2
				 "  to the ", #3
				 "         ", #4
				 "  CLASH  ", #5
				 "   MODE  ", #6
				 "         ", #7
				 "   ***   ", #8
				 "Settings:", True) #9
		print("\n\nWelcome to the Tournament Mode.\nYou first need to choose the general settings.\n")
		manches = askNumber("How many points are needed to get a win ? ", 1, 9)
		print("Good. Now, choose the players.")
		usedSymbols = []
		usedNames = []
		while True:
			if len(players) != 0:
				print("Do you want to add an other player ? If so, type his/her name, otherwise type a single 'enter'")
				if len(players) > 12:
					print("\n\n\t-- IMPORTANT NOTE. --\nBecause of the way the displaying is done, if you go on adding players,\nthey won't be displayed at the side of the board.\nThey will, however, be included in the tournament, and everything will work fine.\nYou just won't see them.\nThis will be fixed in nexts versions.")
				name = "The cake is a lie."
				while name == "The cake is a lie." or usedNames.count(name) > 0:
					name = raw_input("Your choice : ")
					if usedNames.count(name) > 0:
						print("It appears this name is already used. You need to choose an other one.")
				if len(name) == 0:
					break
				print("\nPlayer " + str(len(players)) + " : ")
				print("\tName : "+str(name))
			else:
				print("\nPlayer " + str(len(players)) + " : ")
				name = ""
				while len(name) == 0:
					name = raw_input("\tName : ")
					if name == "":
						print("\tYou have to choose a name !")
			usedNames.append(name)
			symbol = ""
			turnAgain = True
			while len(symbol) > 1 or turnAgain:
				turnAgain = False
				symbol = raw_input("\tChoose your symbol (1 character only) : ")
				if symbol != "" and usedSymbols.count(symbol) > 0:
					print("\tThis symbol is already used by an other player, you need to choose an other one.\n\tType a single 'enter' if you don't care about it.")
					turnAgain = True
			usedSymbols.append(symbol)
			print("\tChoose your type :")
			print("\t0. Human player")
			for i in range(len(AI_list)):
				print("\t"+str(i+1) + ". "+AI_list[i])
			isPlayer = int(askNumber("\tYour choice : ", 0, len(AI_list)))
			newPlayer(name, isPlayer, symbol)
		drawTextQuick(False)
		#Randomize the order
		pList = []
		for i in range(len(players)):
			pList.append(i)
		random.shuffle(pList)
		winners = []
		rows = 0
		while True :
			for i in range(0, len(pList)-1, 2):
				play1_symbol = players[pList[i]][3]
				if play1_symbol == "" or play1_symbol == None:
					play1_symbol = "X"
				play1_isPlayer = players[pList[i]][1]
				play1_tournamentName = players[pList[i]][0]
				play2_symbol = players[pList[i+1]][3]
				if play2_symbol == "" or play2_symbol == None:
					play2_symbol = "O"
				play2_isPlayer = players[pList[i+1]][1]
				play2_tournamentName = players[pList[i+1]][0]
				drawText("         ", #1
						"         ", #2
						"         ", #3
						"         ", #4
						" BEGIN ! ", #5
						"         ", #6
						"         ", #7
						"         ", #8
						"         ", True) #9
				game(player_turn)
				drawTextQuick(True)
				if play1_score > play2_score:
					players[pList[i]][2] = players[pList[i]][2] + 1
					winners.append(pList[i])
				elif play1_score < play2_score:
					players[pList[i+1]][2] = players[pList[i+1]][2] + 1
					winners.append(pList[i+1])
				else:
					players[pList[i]][2] = players[pList[i]][2] + 0.5
					players[pList[i+1]][2] = players[pList[i+1]][2] + 0.5
					winners.append(pList[i])
					winners.append(pList[i+1])
			if len(pList)%2 == 1:
				winners.append(pList[len(pList)-1])
			del pList
			pList = []
			winners.sort()
			for i in range(len(winners)):
				if i == 0:
					pList.append(winners[i])
				elif winners[i] != winners[i-1]:
					pList.append(winners[i])
			random.shuffle(pList)
			if len(pList) <= 1:
				break
			del winners
			winners = []
			rows = rows +1
		#Display of the winner
		drawBoard()
		print("\n\nThe Tournament has ended ...")
		time.sleep(2.0)
		scores = []
		for i in range(len(players)):
			scores.append(players[i][2])
		list(set(scores))
		scores.sort()
		for i in range(len(scores)-1):
			if i >=0 and i < len(scores)-1 and scores[i] == scores[i+1]:
				del scores[i]
		for i in range(len(scores)):
			if scores[i] == 1:
				print("\nWith 1 point, ranked #"+str(len(scores)-i))
			elif len(scores)-i == 3:
				print("\nNow entering the podium !")
				print("\nWith "+str(scores[i])+" points, ranked #"+str(len(scores)-i))
			else:
				print("\nWith "+str(scores[i])+" points, ranked #"+str(len(scores)-i))
			for j in range(len(players)):
				if players[j][2] == scores[i]:
					print(" " + players[j][0])
			time.sleep(3.0 + 1.1*i*2)
		players = []
		play1_isPlayer = 0
		play1_symbol = "O"
		play2_isPlayer = 0
		play2_symbol = "X"
		raw_input("\n\nPress 'enter' to return to the main menu.")
	else:
		drawTextQuick(False)
		drawText(" Length  ", #1
				 "   of the", #2
				 "  games  ", #3
				 "         ", #4
				 "   choose", #5
				 "a value  ", #6
				 "between 1", #7
				 " and 9   ", #8
				 "         ", False) #9
		c2 = int(askNumber("Your choice : ", 1, 9))
		if(c2 > 0 and c2 < 10):
			manches = c2
		else:
			print("\nThis choice is not allowed.")
	time.sleep(1)



