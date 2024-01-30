import subprocess
from queue import Queue
from utils import Plate, ChainedList, comp_double_tab
from typing import TypedDict
import copy



class MouveType(TypedDict):
    x: int
    y: int
    dir: str
    heuristic : float


class Taquin:



	def __init__(self, plate: Plate, heuristic: int = 1):
		self.plate = plate
		self.n = len(plate)
		self.cost = 0
		self.last_move_dir = None
		test = 2
		self.misplaced = self.n * self.n
		self.explored_nodes = [{
			"plate":[],
			"dir": []
		}]
		self.state_in_memory = 2

		self.snail_dir = ChainedList()
		self.snail_dir.add_elem('right')
		self.snail_dir.add_elem("down")
		self.snail_dir.add_elem('left')
		self.snail_dir.add_elem("up")
		self.final_state = self.get_final_state()
		match test:
			case 1: 
				self.heuristic = self.manhatan_distance
			case _:
				self.heuristic = self.manhatan_distance

	
	def get_final_state(self) -> Plate:
		final_state: Plate = [[0] * self.n for _ in range(self.n)]
	     
		i = 0
		j = 0
		current_dir_node = self.snail_dir.head_node
		num = 1
		while num < (self.n * self.n):
			current_dir = current_dir_node.value
			if current_dir == 'right':
				while 0 <= i < self.n and 0 <= j < self.n and final_state[i][j] == 0:
					final_state[i][j] = num
					num += 1
					j += 1
				i += 1
				j -= 1
					
			if current_dir == 'down':
				while 0 <= i < self.n and 0 <= j < self.n and final_state[i][j] == 0:
					final_state[i][j] = num
					num += 1
					i += 1
				j -= 1
				i -= 1

			if current_dir == 'left':
				while 0 <= i < self.n and 0 <= j < self.n and final_state[i][j] == 0:
					final_state[i][j] = num
					num += 1
					j -= 1
				i -= 1
				j += 1

			if current_dir == 'up':
				while 0 <= i < self.n and 0 <= j < self.n and final_state[i][j] == 0:
					final_state[i][j] = num
					num += 1
					i -= 1
				j += 1
				i += 1
		
			current_dir_node = current_dir_node.next
			    
				
		return final_state

    
	def possible_mouve(self) -> list[MouveType]:
		i_0 = None
		j_0 = None
		tile = None
		for i in range(0, self.n):
			for j in range(0, self.n):
				if (self.plate[i][j] == 0):
					i_0 = i
					j_0 = j
					break

		possible_mouves = []
		if self.last_move_dir != 'up' and i_0 > 0:
			# taquin_copy = copy.deepcopy(self.plate)
			mouve = {
					"y": i_0 - 1,
					"x": j_0,
					"dir": 'down'
			}
			# if not self.is_node_explored(self.mouve(mouve, taquin_copy), mouve["dir"]):
			possible_mouves.append(mouve)
		if  self.last_move_dir != 'down' and i_0 < self.n - 1: 
			# taquin_copy = copy.deepcopy(self.plate)
			mouve = {
					"y": i_0 + 1,
					"x": j_0,
					"dir": 'up'
			}
			# if not self.is_node_explored(self.mouve(mouve, taquin_copy), mouve["dir"]):
			possible_mouves.append(mouve)
		if  self.last_move_dir != 'left' and  j_0 > 0:
			# taquin_copy = copy.deepcopy(self.plate)
			mouve = {
				"y": i_0,
				"x": j_0 - 1,
				"dir": 'right'
			}
			# if not self.is_node_explored(self.mouve(mouve, taquin_copy), mouve["dir"]):
			possible_mouves.append(mouve)
		if  self.last_move_dir != 'right' and j_0 < self.n - 1:
			# taquin_copy = copy.deepcopy(self.plate)
			mouve = {
				"y": i_0,
				"x": j_0 + 1,
				"dir": 'left'
			}
			# if not self.is_node_explored(self.mouve(mouve, taquin_copy), mouve["dir"]):
			possible_mouves.append(mouve)
		return possible_mouves
    

	def mouve(self, mouve : MouveType, given_plate: Plate):
		match mouve["dir"]:
			case 'down':
				given_plate[mouve["y"] + 1][mouve["x"]] = given_plate[mouve["y"]][mouve["x"]]
			case 'up':
				given_plate[mouve["y"] - 1][mouve["x"]] = given_plate[mouve["y"]][mouve["x"]]
			case 'right':
				given_plate[mouve["y"]][mouve["x"] + 1] = given_plate[mouve["y"]][mouve["x"]]
			case 'left':
				given_plate[mouve["y"]][mouve["x"] - 1] = given_plate[mouve["y"]][mouve["x"]]

		given_plate[mouve["y"]][mouve["x"]] = 0

		return given_plate
		
	  
	

	def is_node_explored(self, given_Plate: Plate, dir):
		# print("\n\n\n_________\n\n\n")
		#print(self.explored_nodes)
		i = 0
		for node in self.explored_nodes:
			# print("is explored\n", plate, "\n",given_Plate)
		#  print(self.explored_dir[i])
			if comp_double_tab(node["plate"], given_Plate):
				return True
			i += 1
		# print("\n\n\n_________\n\n\n")
		return False
	   

	def find_tuile_pos(self, tuile: int, plate: Plate | None = None):
		if plate == None:
			plate = self.final_state
		for i in range(0, self.n):
			for j in range(0, self.n):
				if plate[i][j] == tuile:
					return i, j
	   

	def manhatan_distance(self, given_plate: Plate):
		manhatan_distance = 0
		for i in range(0, self.n):
			for j in range(0, self.n):
				final_i, final_j = self.find_tuile_pos(given_plate[i][j])
				distance = abs(j - final_j) + abs(i - final_i)
				manhatan_distance += distance

		return manhatan_distance

		      
	def is_puzzle_solvable(self):
		taquin = self
		
		empty_pos_i, empty_pos_j = taquin.find_tuile_pos(0, taquin.plate)
		final_empty_pos_i, final_empty_pos_j = taquin.find_tuile_pos(0)
		distance_empty_tuile = abs(empty_pos_j - final_empty_pos_j) + abs(empty_pos_i - final_empty_pos_i)
		
		inveversions = set()
		current_dir_node = taquin.snail_dir.head_node
		i = 0
		j = 0
		num = 1
		top = 0
		bottom = taquin.n 
		left = 0
		right = taquin.n 
		numbers = []
		while len(numbers) < (taquin.n * taquin.n):
			current_dir = current_dir_node.value
			if current_dir == 'right':
				i = top 
				for j in range(left, right):
					numbers.append(taquin.plate[i][j])
				top += 1

						
			if current_dir == 'down':
				j = right - 1
				for i in  range(top, bottom):
					numbers.append(taquin.plate[i][j])
				right -= 1

			if current_dir == 'left':
				i = bottom - 1
				for j in range(right - 1, left - 1, -1):
					numbers.append(taquin.plate[i][j])
				bottom -= 1

			if current_dir == 'up':
				j =  left
				for i in range(bottom - 1, top - 1, -1):
					numbers.append(taquin.plate[i][j])
				left += 1
			

			current_dir_node = current_dir_node.next


		for i in range(len(numbers), 0, -1):
			for element in numbers[:-i]:
				if element != 0 and numbers[-i] != 0 and element > numbers[-i]:
					inveversions.add((element, numbers[-i]))

		match distance_empty_tuile % 2:	
			case 0:
				return len(inveversions) % 2 == 0
			case 1:
				return len(inveversions) % 2 != 0