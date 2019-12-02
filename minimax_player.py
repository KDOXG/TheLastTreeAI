# -*- coding: utf-8 -*-
import urllib.request
import sys
import random
import time
import copy

class mmTree:
    def __init__(self,rule,animal,land,Animal,Land,goal):
        mmValue = 0
        gameCopy = Game()
        gameCopy.init_board_def(2,Animal,Land,goal[0],goal[1])
        self.rule = rule
        self.animal = animal
        self.land = land
        mmNext = []

    def Minimax(self):
        branching = self.mmNext
        #if random.randint(1,2) % 2 == 0 or len(self.mmNext) == 0:
        #    return (self.rule,self.animal,self.land)
        #else:
        #    i = random.randint(0,len(self.mmNext)-1)
        #    return Minimax(self.mmNext[i])

def minimaxMake(board):
    game = Game(board)

class Animal:
	land = 2
	fruits = 0

class Land:
	def __init__(self,trees):
		self.seeds = 0
		self.plants = 0
		self.trees = trees

class Game:
	NUMGOALS = 8
	NUMPLAYERS = 2
	animals = []
	lands = []
	goals = []
	player = 0
	ended = False
	movements = 0
	last_rule = 0
	last_animal = 0
	last_land = 0
	previous_land = 0

	def init_board_def(self, numplayers, A, L, g1, g2):
		self.NUMGOALS = 8
		self.NUMPLAYERS = numplayers
		self.animals = A
		self.lands = L
		availableGoals = []
		for g in range(self.NUMGOALS):
			availableGoals.append(10+g)
		random.shuffle(availableGoals)
		self.goals = []
		# Mudar o goals
		self.goals.append(g1)
		self.goals.append(g2)
		#self.goals.extend(availableGoals[0:self.NUMPLAYERS])
		self.player = 0
		self.ended = False
		self.movements = 0
		self.last_rule = 0
		self.last_animal = 0
		self.last_land = 0
		self.previous_land = 0

    # Initialize the board.
	def init_board(self,numplayers):
		self.NUMGOALS = 8
		self.NUMPLAYERS = numplayers
		self.animals = [Animal(),Animal(),Animal(),Animal()]
		self.lands = [Land(0),Land(0),Land(1),Land(0),Land(0)]
		availableGoals = []
		for g in range(self.NUMGOALS):
			availableGoals.append(10+g)
		random.shuffle(availableGoals)
		self.goals = []
		self.goals.extend(availableGoals[0:self.NUMPLAYERS])
		self.player = 0
		self.ended = False
		self.movements = 0
		self.last_rule = 0
		self.last_animal = 0
		self.last_land = 0
		self.previous_land = 0

	def get_info(self, infoID, num):
		if infoID=='land': #which land the animal[num] is at?
			return self.animals[num].land
		elif infoID=='fruit': #how much fruits does the animal[num] have?
			return self.animals[num].fruits
		elif infoID=='seed': #how much seeds at land[num]?
			return self.lands[num].seeds
		elif infoID=='plant': #how much plants at land[num]?
			return self.lands[num].plants
		elif infoID=='tree': #how much trees at land[num]?
			return self.lands[num].trees
		else:
			return -1
	
	def preview_board(self, modifications):
		newAnimals = copy.deepcopy(self.animals)
		newLands = copy.deepcopy(self.lands)
		for modification in (modifications):
			if modification[0]=='land':
				newAnimals[modification[1]].land = modification[2]
			elif modification[0]=='fruit':
				newAnimals[modification[1]].fruits = modification[2]
			elif modification[0]=='seed':
				newLands[modification[1]].seeds = modification[2]
			elif modification[0]=='plant':
				newLands[modification[1]].plants = modification[2]
			elif modification[0]=='tree':
				newLands[modification[1]].trees = modification[2]
			else:
				return None
		return (newAnimals,newLands)
	
	def preview_move(self, player, rule, animal, land):
		if rule == 0: #move (displace an animal to an adjacent land)
			if self.animals[animal].land+1 == land or self.animals[animal].land-1 == land:
				if self.last_rule==0 and self.last_animal==animal and self.last_land==self.animals[animal].land and self.previous_land==land:
					return None #(-5, "Can't reverse last action")
				else:
					return self.preview_board([('land',animal,land)])
			else:
				return None #(-3.0, "Invalid move, input land is not adjacent to the land of input animal")
		elif rule == 1: #gather (create a fruit picking it from a tree)
			if self.lands[self.animals[animal].land].trees > 0:
				return self.preview_board([('fruit',animal,self.animals[animal].fruits+1)])
			else:			
				return None #(-3.1, "Invalid move, not enough trees")
		elif rule == 2: #eat (destroy a fruit and spit out its seed)
			if self.animals[animal].fruits > 0:
				return self.preview_board([('fruit',animal,self.animals[animal].fruits-1),('seed',self.animals[animal].land,self.lands[self.animals[animal].land].seeds+1)])
			else:
				return None # (-3.2, "Invalid move,  not enough fruits")
		elif rule == 3: #plant (create a plant by planting a seed)
			if self.lands[self.animals[animal].land].seeds > 0:
				return self.preview_board([('seed',self.animals[animal].land,self.lands[self.animals[animal].land].seeds-1),('plant',self.animals[animal].land,self.lands[self.animals[animal].land].plants+1)])
			else:
				return None # (-3.3, "Invalid move,  not enough seeds")
		elif rule == 4: #fertilize (create a tree by fertilizing a plant with a fruit)
			if self.lands[self.animals[animal].land].plants > 0:
				if self.animals[animal].fruits > 0:
					return self.preview_board([('fruit',animal,self.animals[animal].fruits-1),('plant',self.animals[animal].land,self.lands[self.animals[animal].land].plants-1),('tree',self.animals[animal].land,self.lands[self.animals[animal].land].trees+1)])
				else:
					return None # (-3.2, "Invalid move,  not enough fruits")
			else:
				return None # (-3.4, "Invalid move,  not enough plants")
		elif rule == 5: #devour (destroy 2 fruits)
			if self.animals[animal].fruits > 1:
				return self.preview_board([('fruit',animal,self.animals[animal].fruits-2)])
			else:
				return None # (-3.2, "Invalid move, not enough fruits")
		elif rule == 10: #the fruit king (an animal with 5+ fruits is the only one with fruits)
			if self.goals[player] == rule:
				if self.animals[animal].fruits > 4:
					if self.animals[animal].fruits == self.animals[0].fruits+self.animals[1].fruits+self.animals[2].fruits+self.animals[3].fruits:
	            				return (self.animals,self.lands)
					else:
						return None # (-3.8, "Invalid move, too much fruits")
				else:
					return None # (-3.2, "Invalid move, not enough fruits")
			else:
				return None # (-4, "Not your goal")
		elif rule == 11: #grove symmetry (all self.lands have the same amount of trees)
			if self.goals[player] == rule:
				if self.lands[0].trees==self.lands[1].trees and self.lands[0].trees==self.lands[2].trees and self.lands[0].trees==self.lands[3].trees and self.lands[0].trees==self.lands[4].trees:
					return (self.animals,self.lands)
				else:
					return None # (-3.6, "Invalid move, all numbers should be equal")
			else:
				return None # (-4, "Not your goal")
		elif rule == 12: #ecosystem (the same amount (>0) of fruits, seeds, plants and trees in one place/animal)
			if self.goals[player] == rule:
				if self.animals[animal].fruits == self.lands[self.animals[animal].land].plants and self.animals[animal].fruits == self.lands[self.animals[animal].land].seeds and self.animals[animal].fruits == self.lands[self.animals[animal].land].trees:
					if self.animals[animal].fruits > 0:
	            				return (self.animals,self.lands)
					else:
						return None # (-3.2, "Invalid move, not enough fruits")
				else:
					return None # (-3.6, "Invalid move, all numbers should be equal")
			else:
				return None # (-4, "Not your goal")
		elif rule == 13: #orchard (all self.animals are in self.lands with as much trees as their fruits)
			if self.goals[player] == rule:
				if self.animals[0].fruits==self.lands[self.animals[0].land].trees and self.animals[1].fruits==self.lands[self.animals[1].land].trees and self.animals[2].fruits==self.lands[self.animals[2].land].trees and self.animals[3].fruits==self.lands[self.animals[3].land].trees:
	            			return (self.animals,self.lands)
				else:
					return None # (-3.6, "Invalid move, all numbers should be equal")
			else:
				return None # (-4, "Not your goal")
		elif rule == 14: #plant valley (an animal at a land with no plants that is between adjacent self.lands with the same amount of plants >0)
			if self.goals[player] == rule:
				if self.lands[self.animals[animal].land].plants == 0:
					if self.animals[animal].land > 0 and self.animals[animal].land < 4:
						if self.lands[self.animals[animal].land+1].plants > 0:
							if self.lands[self.animals[animal].land+1].plants==self.lands[self.animals[animal].land-1].plants:
	            						return (self.animals,self.lands)
							else:
								return None # (-3.6, "Invalid move, all numbers should be equal")
						else:
							return None # (-3.4, "Invalid move, not enough plants")
					else:
						return None # (-3.7, "Invalid move, not enough self.lands")
				else:
					return None # (-3.8, "Invalid move, too much fruits")
			else:
				return None # (-4, "Not your goal")
		elif rule == 15: #chicken farm (all self.lands have seeds)
			if self.goals[player] == rule:
				if self.lands[0].seeds > 0 and self.lands[1].seeds > 0 and self.lands[2].seeds > 0 and self.lands[3].seeds > 0 and self.lands[4].seeds > 0:
        	    			return (self.animals,self.lands)
				else:
					return None # (-3.3, "Invalid move, not enough seeds")
			else:
				return None # (-4, "Not your goal")
		elif rule == 16: #jungle hierarchy (all self.animals have different numbers of fruits)
			if self.goals[player] == rule:
				if self.animals[0].fruits != self.animals[1].fruits and self.animals[0].fruits != self.animals[2].fruits and self.animals[0].fruits != self.animals[3].fruits and self.animals[1].fruits != self.animals[2].fruits and self.animals[1].fruits != self.animals[3].fruits and self.animals[2].fruits != self.animals[3].fruits:
        	    			return (self.animals,self.lands)
				else:
					return None # (-3.9, "Invalid move, all numbers should be different")
			else:
				return None # (-4, "Not your goal")
		elif rule == 17: #treehouse party (all self.animals together at a land that has 4+ trees)
			if self.goals[player] == rule:
				if self.animals[0].land == self.animals[1].land and self.animals[0].land == self.animals[2].land and self.animals[0].land == self.animals[3].land:
					if self.lands[self.animals[0].land].trees > 4:
        	    				return (self.animals,self.lands)
					else:
						return None # (-3.1, "Invalid move, not enough trees")
				else:
					return None # (-3.6, "Invalid move, all numbers should be equal")
			else:
				return None # (-4, "Not your goal")
		# Add self.goals here
		#elif rule == 18: #goal name (goal description)
		#	if self.goals[player] == rule:
		#		if goal condition:
		#			return (self.animals,self.lands)
		#		else:
		#			return None # (errorID, "Invalid move, error message")
		#	else:
		#		return None # (-4, "Not your goal")
		else:
			return None # (-4, "Invalid rule")
	
	
    # Returns a list of moves that would be successful at the current state of the board
	def get_available_moves(self,player):
		moves = []
		for animal in range(len(self.animals)):
			for land in range(len(self.lands)):
				for rule in range(6):
					if self.preview_move(player,rule,animal,land)!= None:
						moves.append((rule,animal,land))
				if self.preview_move(player,self.goals[player],animal,land)!=None:
					moves.append((self.goals[player],animal,land))
		return moves

    # Returns a list of all possible boards from the current
	def get_available_boards(self,player):
		boards = []
		for animal in range(len(self.animals)):
			for land in range(len(self.lands)):
				for rule in range(6):
					newboard = self.preview_move(player,rule,animal,land)
					if newboard != None:
						boards.append(newboard)
				winboard = self.preview_move(player,self.goals[player],animal,land)
				if winboard!=None:
					boards.append(winboard)
		return boards

###### SERVER ######



@app.route("/movimentos")
def movimentos():
	player = int(request.args.get('player'))
	if request.args.get('format') == "json":
		return jsonify(game.get_available_moves(player))
	else:
		return str(game.get_available_moves(player))



    # Alterar se utilizar outro host
host = "http://localhost:8080"

player = 1

goal = []
resp = urllib.request.urlopen("%s/goals?player=0" % host)
goal.append(eval(resp.read()))
resp = urllib.request.urlopen("%s/goals?player=1" % host)
goal.append(eval(resp.read()))

done = False
while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == -1, o jogo acabou e o cliente perdeu
    if player_turn==-1:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos?player=%d" % (host,player))
        movimentos = eval(resp.read())
        
        #game = Game()
        #game.init_board(2)

        #   CODIGO DO MINIMAX AQUI
        #   
        resp = urllib.request.urlopen("%s/tab" % host)
        board = eval(resp.read())
        auxBoard = []
        for i in range(int(board[0]))

        head = mmTree(-1,-1,-1,,goal)
        mmTemp2 = []
        mmTemp2.append(head)
        aux = []
        #k = 0

        for i in range(6):
            actual = movimentos
            mmActual = len(mmTemp2)
            for j in range(mmActual):
                mmTemp = mmTemp2.pop(0)
                for k in range(mmActual):
                    mmTemp.mmNext.append(mmTree(actual[k][0],actual[k][1],actual[k2]))
                    #KDOXG: Falta implementar get_available_moves()
                    aux.append(get_available_moves(player,goal,movimentos[0]))
                    del movimentos[0]
                mmTemp2.append(mmTemp.mmNext)
            movimentos = aux
            actual = []
            aux = []

        movimento = Minimax()   #KDOXG: Falta implementar Minimax()

        #movimento = get_available_moves(player,goal)

        # Escolhe um movimento aleatoriamente
        #movimento = random.choice(movimentos)

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&rule=%d&animal=%d&land=%d" % (host,player,movimento[0],movimento[1],movimento[2]))
        msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
    
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)

