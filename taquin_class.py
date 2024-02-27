from cmath import sqrt
import random
import subprocess
from queue import Queue
import time
from utils import Plate, ChainedList, comp_double_tab
from typing import TypedDict
import copy
import sys
import heapq

class MouveType():
	x: int
	y: int
	dir: str
	plate: Plate

	def __lt__(self, other): 
		return True

	def __le__(self, other):
		return False


class Taquin:



	def __init__(self, plate: Plate, heuristic_choice: int = 0):
		self.plate = copy.deepcopy(plate)
		self.n = len(plate)
		self.last_move_dir = None
		self.heuristic = self.n * self.n
		self.explored_nodes = set()
		self.utils_nodes = []
		self.state_in_memory = 2

		self.snail_dir = ChainedList()
		self.snail_dir.add_elem('right')
		self.snail_dir.add_elem("down")
		self.snail_dir.add_elem('left')
		self.snail_dir.add_elem("up")
		self.final_state = self.get_final_state()
		self.lines_resolved = []
		self.col_resolved = []
		self.resolved = []
		self.top_indx = 0
		self.bottom_indx = self.n - 1
		self.right_indx = self.n - 1
		self.left_indx = 0
		self.i_0, self.j_0 = self.find_tuile_pos(0, self.plate)

		self.util_mouves = []
		match heuristic_choice:
			case 0: 
				self.heuristic_funct = self.manhatan_distance
			case 1:
				self.heuristic_funct = self.nb_bad_placed
			case 2:
				self.heuristic_funct = self.euclidean_distance
	
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

	
	def get_open_set(self, with_resolved = True) :
		open_set = []
		i_0, j_0 = self.find_tuile_pos(0, self.plate)
		self.i_0 = i_0
		self.j_0 = j_0
		dir_array = ["down", "up", "left", "right"]

		random.shuffle(dir_array)

		for dir in dir_array:

			if (dir == 'down'):
				if self.last_move_dir != 'up' and i_0 > 0:
					if ((i_0 - 1) in self.lines_resolved):
						pass
					elif with_resolved and self.plate[i_0 - 1][j_0] in self.resolved: 
						pass
					else:
						mouve : MouveType = {
								"y": i_0 - 1,
								"x": j_0,
								"dir": 'down'
						}
						plate_copy = copy.deepcopy(self.plate)
						self.mouve(mouve, plate_copy)
						mouve["plate"] = plate_copy
						heapq.heappush(open_set, (self.heuristic_funct(plate_copy), id(mouve), mouve))
						if self.plate[i_0 - 1][j_0] in self.resolved:
							self.resolved.remove(self.plate[i_0 - 1][j_0])


			if (dir == 'up'):
				if  self.last_move_dir != 'down' and i_0 < self.n - 1:
					if ((i_0 + 1) in self.lines_resolved):
						pass
					elif with_resolved and self.plate[i_0 + 1][j_0] in self.resolved: 
						pass
					else:
						mouve  : MouveType = {
								"y": i_0 + 1,
								"x": j_0,
								"dir": 'up'
						}
						plate_copy = copy.deepcopy(self.plate)
						self.mouve(mouve, plate_copy)
						mouve["plate"] = plate_copy
						heapq.heappush(open_set, (self.heuristic_funct(plate_copy),id(mouve), mouve))
						if self.plate[i_0 + 1][j_0] in self.resolved:
							self.resolved.remove(self.plate[i_0 + 1][j_0])

			if (dir == 'right'):
				if  self.last_move_dir != 'left' and  j_0 > 0:
					if  (j_0 - 1) in self.col_resolved:
						pass
					elif with_resolved and self.plate[i_0][j_0 - 1] in self.resolved: 
						pass
					else:
						mouve : MouveType = {
							"y": i_0,
							"x": j_0 - 1,
							"dir": 'right'
						}
						plate_copy = copy.deepcopy(self.plate)
						self.mouve(mouve, plate_copy)
						mouve["plate"] = plate_copy
						heapq.heappush(open_set, (self.heuristic_funct(plate_copy), id(mouve), mouve))
						if self.plate[i_0][j_0 - 1] in self.resolved:
							self.resolved.remove(self.plate[i_0 ][j_0 - 1])

			if (dir == 'left'):
				if  self.last_move_dir != 'right' and j_0 < self.n - 1:
					if  (j_0 + 1) in self.col_resolved:
						pass
					elif with_resolved and self.plate[i_0][j_0 + 1] in self.resolved: 
						pass
					else:
						mouve : MouveType ={
							"y": i_0,
							"x": j_0 + 1,
							"dir": 'left'
						}
						plate_copy = copy.deepcopy(self.plate)
						self.mouve(mouve, plate_copy)
						mouve["plate"] = plate_copy
						heapq.heappush(open_set, (self.heuristic_funct(mouve["plate"]), id(mouve), mouve))
						if self.plate[i_0][j_0 + 1] in self.resolved:
							self.resolved.remove(self.plate[i_0][j_0 + 1])

		if (len(open_set) == 0 and with_resolved):
			return self.get_open_set(False)
		return open_set
	

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
		
	   

	def find_tuile_pos(self, tuile: int, plate: Plate | None = None):
		if plate == None:
			plate = self.final_state
		for i in range(0, self.n):
			for j in range(0, self.n):
				if plate[i][j] == tuile:
					return i, j
		return -1, -1
	
	def manhatan_distance(self, given_plate: Plate):
		manhatan_distance = 0

		for i in range(0, self.n):
			for j in range(0, self.n):
				if given_plate[i][j] == 0:
					pass
				else:
					final_i, final_j = self.find_tuile_pos(given_plate[i][j])
					distance = abs(j - final_j) + abs(i - final_i)
					manhatan_distance += distance

		return manhatan_distance


	def euclidean_distance(self, given_plate : Plate):
		euclidean_distance = 0

		for i in range(0, self.n):
			for j in range(0, self.n):
				if given_plate[i][j] == 0:
					pass
				else:
					final_i, final_j = self.find_tuile_pos(given_plate[i][j])
					distance = sqrt(((j - final_j) ** 2) + ((i - final_i) ** 2))
					euclidean_distance += distance.real

		return euclidean_distance
	

	def nb_mouves(self, given_plate : Plate):
		nb_mouves = 0
		for i in range(0, self.n):
			for j in range(0, self.n):
				if given_plate[i][j] == 0:
					continue
				pos0_i, pos0_j = self.find_tuile_pos(0)
				distance0 = sqrt(((pos0_i - j) ** 2) + ((pos0_j - i) ** 2))

				final_i, final_j = self.find_tuile_pos(given_plate[i][j])
				distance = sqrt(((j - final_j) ** 2) + ((i - final_i) ** 2))



				nb_mouves += distance0.real + distance.real

		return nb_mouves

	def nb_bad_placed(self, given_plate: Plate):
		nb_bad_placed = 0
		for i in range(0, self.n):
			for j in range(0, self.n):
				if  given_plate[i][j] != 0 and given_plate[i][j] != self.final_state[i][j]:
					nb_bad_placed += 1

		return nb_bad_placed




	def count_inversion(self, given_plate: Plate):
		taquin = self
		inversion = set()
		current_dir_node = taquin.snail_dir.head_node
		i = 0
		j = 0
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
					numbers.append(given_plate[i][j])
				top += 1


			if current_dir == 'down':
				j = right - 1
				for i in  range(top, bottom):
					numbers.append(given_plate[i][j])
				right -= 1

			if current_dir == 'left':
				i = bottom - 1
				for j in range(right - 1, left - 1, -1):
					numbers.append(given_plate[i][j])
				bottom -= 1

			if current_dir == 'up':
				j =  left
				for i in range(bottom - 1, top - 1, -1):
					numbers.append(given_plate[i][j])
				left += 1
			

			current_dir_node = current_dir_node.next

		for i in range(len(numbers), 0, -1):
			for element in numbers[:-i]:
				if element != 0 and  numbers[-i] != 0 and element > numbers[-i]:
					inversion.add((element, numbers[-i]))



		return len(inversion)


	def is_puzzle_solvable(self):
		taquin = self
		nb_inversion = self.count_inversion(self.plate)

		empty_pos_i, empty_pos_j = taquin.find_tuile_pos(0, taquin.plate)
		final_empty_pos_i, final_empty_pos_j = taquin.find_tuile_pos(0)
		distance_empty_tuile = abs(empty_pos_j - final_empty_pos_j) + abs(empty_pos_i - final_empty_pos_i)


		match distance_empty_tuile % 2:	
			case 0:
				return nb_inversion % 2 == 0
			case 1:
				return nb_inversion % 2 != 0
			

	def is_node_in_utile(self, given_plate: Plate):
		if len(given_plate) <= 2:
			return -1
		plate_to_str = ''.join(map(str, [element for col in given_plate for element in col]))
		for i in range(len(self.utils_nodes) -1, 0, -1):
			if self.utils_nodes[i]["plate"] == plate_to_str:
				return i
		return -1


	def detect_boucle(self, given_plate):
		if len(self.explored_nodes) < 3:
			return False
		
		plate_to_str = ''.join(map(str, [element for col in given_plate for element in col]))
		if plate_to_str in self.explored_nodes:
			return True
		return False
		
		
	


	def is_3_tuiles_betwenn(self, i: int, j: int, dir: str):
		space : int

		if not((j == self.left_indx or j == self.right_indx) and (i == self.top_indx or i == self.bottom_indx)):
			match dir:
				case "down":
					if (i + 3 >= self.n):
						return False
				case "up":
					if (i - 3 < 0):
						return False
				case "right":
					if (j + 3 >= self.n):
						return False
				case "left":
					if (j - 3 < 0):
						return False
				
		if (j + 3 < self.n):
			space = 3
		else:
			space = self.n - j - 1
		if (j < self.n - 1 and i not in self.lines_resolved ):
			if (self.plate[i][j + 1] not in self.resolved and j + 1 not in self.col_resolved)\
			and (j + space in self.col_resolved or self.plate[i][j + space] in self.resolved or self.plate[i][j + space] == 0):
				return False
				
		if (j - 3 >= 0):
			space = 3
		else :
			space = j
		if (j > 0 and i not in self.lines_resolved  ):
			if (self.plate[i][j - 1] not in self.resolved and j - 1 not in self.col_resolved)\
			and (j - space in self.col_resolved or self.plate[i][j - space] in self.resolved or self.plate[i][j - space] == 0):
				return False
			
		if (i + 3 < self.n):
			space = 3
		else:
			space = self.n - i - 1
		if (i < self.n - 1  and j not in self.col_resolved ):
			if (self.plate[i + 1][j] not in self.resolved and i + 1 not in self.lines_resolved)\
			and (i + space in self.lines_resolved or self.plate[i + space][j] in self.resolved or self.plate[i + space][j] == 0):
				return False
			
		if (i - 3 >= 0):
			space = 3
		else :
			space = i
		if (i > 0 ):
			if (self.plate[i - 1][j] not in self.resolved and i - 1 not in self.lines_resolved)\
			and (i - space in self.lines_resolved or self.plate[i - space][j] in self.resolved or self.plate[i - space][j] == 0):
				return False
				
		return True

	def set_lines_and_col_resolved(self):

		
		if (self.n -  len(self.lines_resolved) <= 3 or self.n -  len(self.col_resolved) <= 3):
			self.resolved.clear()

		found_line = 0
		found_col = 0

		if self.n -  len(self.lines_resolved) > 3:
			# Check lines from index 0
			for i in range(0, self.n):	
				if self.plate[i] == self.final_state[i] and 0 not in self.plate[i]:
					if  i not in self.lines_resolved:
						self.lines_resolved.append(i)
						found_line += 1
				else:
					break 
				if self.n -  len(self.lines_resolved) <= 3:
					break

			# Check lines from index n - 1
			for i in range(self.n - 1, 0, -1):
				if self.plate[i] == self.final_state[i]  and 0 not in self.plate[i]:
					if  i not in self.lines_resolved:
						self.lines_resolved.append(i)
						found_line += 1
				else:
					break 
				if self.n -  len(self.lines_resolved) <= 3:
					break
		
	
		if self.n -  len(self.col_resolved) > 3:
			# Check cols from index 0
			for i in range(0, self.n):
				col = [elem[i] for elem in self.plate]
				col_resolved = [elem[i] for elem in self.final_state]
				if col == col_resolved  and 0 not in col:
					if  i not in self.col_resolved:
						self.col_resolved.append(i)
						found_col += 1
				else:
					break 
				if self.n -  len(self.col_resolved) <= 3:
					break
			
			# Check cols from index n - 1
			for i in range(self.n - 1, 0, -1):
				col = [elem[i] for elem in self.plate]
				col_resolved = [elem[i] for elem in self.final_state]
				if col == col_resolved and 0 not in col:
					if i not in self.col_resolved:
						self.col_resolved.append(i)
						found_col += 1
				else:
					break
				if self.n -  len(self.col_resolved) <= 3:
					break
			
		if (not (self.n -  len(self.lines_resolved) <= 3 or self.n -  len(self.col_resolved) <= 3))\
		and (found_line > 0 or found_col > 0) and len(self.resolved)  > 5 :
			to_pop = []
			for i in range(len(self.resolved) - 1, len(self.resolved) - 5, -1):
				i_res, j_res = self.find_tuile_pos(self.resolved[i], self.plate)
				if i_res in self.lines_resolved or j_res in self.col_resolved:
					continue
				for u in range(found_line):
					if (u > i_res and (self.lines_resolved[u] - i_res) < 3):
						to_pop.append(i)
						continue
					if (u < i_res and (i_res - self.lines_resolved[u] ) < 3):
						to_pop.append(i)
						continue

				for k in range(found_col):
					if (k > j_res and (self.col_resolved[k] - j_res) < 3):
						to_pop.append(i)
						continue
					if (k < j_res and (j_res - self.col_resolved[k] ) < 3):
						to_pop.append(i)
						continue
			for idx in to_pop:
				self.resolved.pop(idx)



		if self.n -  len(self.col_resolved) <= 3 and self.n -  len(self.lines_resolved) <= 3:
			return
		
		if (self.bottom_indx) - (self.top_indx + 1) >= 3:
			while self.top_indx + 1 < self.n and self.top_indx in self.lines_resolved:
				self.top_indx += 1

		if (self.bottom_indx) - (self.top_indx + 1) >= 3:
			while  self.bottom_indx - 1 > 0 and  self.bottom_indx  in self.lines_resolved:
				self.bottom_indx -= 1

		if (self.right_indx) - (self.left_indx + 1) >= 3:
			while self.left_indx + 1 < self.n and self.left_indx in self.col_resolved:
				self.left_indx += 1

		if (self.right_indx) - (self.left_indx + 1) >= 3:
			while  self.right_indx - 1 > 0 and  self.right_indx in self.col_resolved:
				self.right_indx -= 1

		# print("top:" , self.top_indx)
		# print("bottom:" , self.bottom_indx)
		# print("left:" , self.left_indx)
		# print("right:" , self.right_indx)
	

		i = self.top_indx 
		while i < self.n\
			and (self.plate[i][self.left_indx] == self.final_state[i][self.left_indx] and self.is_3_tuiles_betwenn(i, self.left_indx, "down")):
			if (self.plate[i][self.left_indx] not in self.resolved):
				self.resolved.append(self.plate[i][self.left_indx])
			i += 1
		i = self.left_indx
		while i < self.n\
			and ((self.plate[self.top_indx][i] == self.final_state[self.top_indx][i]) and self.is_3_tuiles_betwenn(self.top_indx, i, "right")):
			if (self.plate[self.top_indx][i] not in self.resolved):
				self.resolved.append(self.plate[self.top_indx][i])
			i += 1
	

		i = self.bottom_indx 
		while i >= 0\
		and ((self.plate[i][self.left_indx] == self.final_state[i][self.left_indx]) and self.is_3_tuiles_betwenn(i, self.left_indx, 'up')):
			if (self.plate[i][self.left_indx] not in self.resolved):
				self.resolved.append(self.plate[i][self.left_indx])
			i -= 1
		i = self.left_indx 
		while i < self.n\
		and ((self.plate[self.bottom_indx][i] == self.final_state[self.bottom_indx][i]) and self.is_3_tuiles_betwenn(self.bottom_indx, i, "right")):
			if (self.plate[self.bottom_indx][i] not in self.resolved):
				self.resolved.append(self.plate[self.bottom_indx][i])
			i += 1


		i = self.top_indx 
		while i < self.n\
		and ((self.plate[i][self.right_indx] == self.final_state[i][self.right_indx])  and  self.is_3_tuiles_betwenn(i, self.right_indx, 'down')):
			if (self.plate[i][self.right_indx] not in self.resolved):
				self.resolved.append(self.plate[i][self.right_indx])
			i += 1
		i = self.right_indx
		while i >= 0\
		and ((self.plate[self.top_indx][i] == self.final_state[self.top_indx][i])  and self.is_3_tuiles_betwenn(self.top_indx, i, "left")):
			if (self.plate[self.top_indx][i] not in self.resolved):
				self.resolved.append(self.plate[self.top_indx][i])
			i -= 1

		i = self.bottom_indx 
		while i >= 0\
		and ((self.plate[i][self.right_indx] == self.final_state[i][self.right_indx])  and self.is_3_tuiles_betwenn(i, self.right_indx, "up")):
			if (self.plate[i][self.right_indx] not in self.resolved):
				self.resolved.append(self.plate[i][self.right_indx])
			i -= 1
		i = self.right_indx 
		while i >= 0\
		and ((self.plate[self.bottom_indx][i] == self.final_state[self.bottom_indx][i]) and self.is_3_tuiles_betwenn(self.bottom_indx, i, "left")):
			if (self.plate[self.bottom_indx][i] not in self.resolved):
				self.resolved.append(self.plate[self.bottom_indx][i])
			i -= 1
	
							

	def is_corner_mouvable(self, mouve: MouveType):
		if self.plate[mouve['y']][mouve["x"]] != self.final_state[mouve['y']][mouve["x"]] and (mouve["y"] == self.top_indx or mouve["y"] == self.bottom_indx) and (mouve["x"] == self.left_indx or mouve["x"] == self.right_indx):
			return True
		return False
	

	def is_corner_closer(self, mouve: MouveType):
		if self.plate[mouve['y']][mouve['x']] == self.final_state[mouve['y']][mouve['x']]:
			return False
		if self.plate[mouve['y']][mouve['x']] == self.final_state[self.top_indx][self.right_indx]:
			cur_dist= abs(mouve['x']- self.right_indx) + abs(mouve['y'] - self.top_indx)
			dist =  abs(self.j_0 - self.right_indx) + abs(self.i_0 - self.top_indx)
			if dist < cur_dist:
				return True
		if  self.plate[mouve['y']][mouve['x']] == self.final_state[self.bottom_indx][self.right_indx]:
			cur_dist= abs(mouve['x']- self.right_indx) + abs(mouve['y'] - self.bottom_indx)
			dist =  abs(self.j_0 - self.right_indx) + abs(self.i_0 - self.bottom_indx)
			if dist < cur_dist :
				return True
		if self.plate[mouve['y']][mouve['x']] == self.final_state[self.top_indx][self.left_indx]:
			cur_dist= abs(mouve['x']- self.left_indx) + abs(mouve['y'] - self.top_indx)
			dist =  abs(self.j_0 - self.left_indx) + abs(self.i_0 - self.top_indx)
			if dist < cur_dist:
				return True
		if  self.plate[mouve['y']][mouve['x']] == self.final_state[self.bottom_indx][self.left_indx]:
			cur_dist= abs(mouve['x']- self.left_indx) + abs(mouve['y'] - self.bottom_indx)
			dist =  abs(self.j_0 - self.left_indx) + abs(self.i_0 - self.bottom_indx)
			if dist < cur_dist :
				return True
		return False
		



	# def closer_to_corner(self, mouve: MouveType):
	# 	if self.plate[mouve['y']][mouve['x']] == self.final_state[self.top_indx][self.right_indx]:


	def mask_final_state(self):
		mask = self.n * self.n + 1
		self.masked_final_state = copy.deepcopy(self.final_state)
		for i in range(self.top_indx + 1, self.bottom_indx):
			for j in range(self.left_indx + 1, self.right_indx):
				self.masked_final_state[i][j] = mask







def test_mouves(taquin_test: Taquin, mouves: list[str]):
	i_0, j_0 = taquin_test.find_tuile_pos(0, taquin_test.plate)
	for mouve in mouves:
		match mouve:
			case 'down':
				taquin_test.plate[i_0][j_0] = taquin_test.plate[i_0 - 1][j_0]
				taquin_test.plate[i_0 - 1][j_0] = 0
				i_0 -= 1
			case 'up':
				
				taquin_test.plate[i_0][j_0] = taquin_test.plate[i_0 + 1][j_0]
				taquin_test.plate[i_0 + 1][j_0] = 0
				i_0 += 1
			case 'right':
				taquin_test.plate[i_0][j_0] = taquin_test.plate[i_0][j_0 - 1]
				taquin_test.plate[i_0][j_0 - 1] = 0
				j_0 -= 1
			case 'left':
				taquin_test.plate[i_0][j_0] = taquin_test.plate[i_0][j_0 + 1]
				taquin_test.plate[i_0][j_0 + 1] = 0
				j_0 += 1

	if (taquin_test.plate == taquin_test.final_state):
		print("Le taquin est resolue")

	else:
		 print("Le taquin n'est pas resolue")