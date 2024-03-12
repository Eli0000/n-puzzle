from cmath import sqrt
import copy
import heapq
import random
from utils import CircularChainedList, Plate

canceled = False

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

	def __init__(self, plate: Plate, algo_choice = "standard A*", heuristic_choice: int = 0):
		self.plate = copy.deepcopy(plate)
		self.plate_simple_array = [element for sous_liste in self.plate for element in sous_liste]
		self.n = len(plate)
		self.last_move_dir = None
		self.open_set: heapq = [] 
		self.closed_set = set()
		self.heuristic_weight = 1 if self.n < 4 else self.n - 1
		self.snail_dir = CircularChainedList()
		self.snail_dir.add_elem('right')
		self.snail_dir.add_elem("down")
		self.snail_dir.add_elem('left')
		self.snail_dir.add_elem("up")
		self.final_state = self.get_final_state()
		self.final_state_simple_array =  [element for sous_liste in self.final_state for element in sous_liste]
		self.final_state_hash = hash(tuple(self.final_state_simple_array))
		self.i_0, self.j_0 = self.find_tuile_pos(0, self.plate)
		self.mouves_soluce = None
		self.algo_choice = algo_choice

		if (self.algo_choice == "Uniform cost"):
			self.heuristic_funct = lambda x: 0
		else:
			match heuristic_choice:
				case 0: 
					self.heuristic_funct = self.pondered_manhatan_distance
				case 1:
					self.heuristic_funct = self.nb_mouves
				case 2:
					self.heuristic_funct = self.euclidean_distance
	

	def g(self, current_node):
		if (self.algo_choice  == "Greedy search"):
			return 0
		return current_node[3] + 1 


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
	

	def get_open_nodes(self, current_node) :
		i_0, j_0 = self.find_tuile_pos(0, current_node[5])
		self.i_0 = i_0
		self.j_0 = j_0
		dir_array = ["down", "up", "left", "right"]

		random.shuffle(dir_array)

		for dir in dir_array:

			if (dir == 'down'):
				if current_node[2] != 'up' and i_0 > 0:
						mouve : MouveType = {
								"y": i_0 - 1,
								"x": j_0,
								"dir": 'down'
						}
						plate_copy = copy.deepcopy(current_node[5])
						self.mouve(mouve, plate_copy)
						plate_simple_array =  [element for sous_liste in plate_copy for element in sous_liste]
						if  not(any(tuple_element[0] ==  current_node[4]  for tuple_element in self.closed_set)):
							g = self.g(current_node)
							h = self.heuristic_funct(plate_copy) ** self.heuristic_weight
							hash_current_plate = hash(tuple(plate_simple_array))
							heapq.heappush(self.open_set, (g + h, id(plate_copy), 'down', g, hash_current_plate, plate_copy, current_node[4]))


			if (dir == 'up'):
				if  current_node[2] != 'down' and i_0 < self.n - 1:
						mouve  : MouveType = {
								"y": i_0 + 1,
								"x": j_0,
								"dir": 'up'
						}
						plate_copy = copy.deepcopy(current_node[5])
						self.mouve(mouve, plate_copy)
						plate_simple_array =  [element for sous_liste in plate_copy for element in sous_liste]
						if  not(any(tuple_element[0] ==  current_node[4]  for tuple_element in self.closed_set)):
							g = self.g(current_node)
							h = self.heuristic_funct(plate_copy) ** self.heuristic_weight
							hash_current_plate = hash(tuple(plate_simple_array))
							heapq.heappush(self.open_set, (g + h, id(plate_copy), 'up', g, hash_current_plate, plate_copy, current_node[4]))

			if (dir == 'right'):
				if  current_node[2] != 'left' and  j_0 > 0:
						mouve : MouveType = {
							"y": i_0,
							"x": j_0 - 1,
							"dir": 'right'
						}
						plate_copy = copy.deepcopy(current_node[5])
						self.mouve(mouve, plate_copy)
						plate_simple_array =  [element for sous_liste in plate_copy for element in sous_liste]
						if  not(any(tuple_element[0] ==  current_node[4]  for tuple_element in self.closed_set)):
							g = self.g(current_node)
							h = self.heuristic_funct(plate_copy) ** self.heuristic_weight
							hash_current_plate = hash(tuple(plate_simple_array))
							heapq.heappush(self.open_set, (g + h, id(plate_copy), 'right', g, hash_current_plate, plate_copy, current_node[4]))

			if (dir == 'left'):
				if  current_node[2] != 'right' and j_0 < self.n - 1:
						mouve : MouveType ={
							"y": i_0,
							"x": j_0 + 1,
							"dir": 'left'
						}
						plate_copy = copy.deepcopy(current_node[5])
						self.mouve(mouve, plate_copy)
						plate_simple_array =  [element for sous_liste in plate_copy for element in sous_liste]
						if  not(any(tuple_element[0] ==  current_node[4]  for tuple_element in self.closed_set)):
							g = self.g(current_node)
							h = self.heuristic_funct(plate_copy) ** self.heuristic_weight
							hash_current_plate = hash(tuple(plate_simple_array))
							heapq.heappush(self.open_set, (g + h, id(plate_copy), 'left', g, hash_current_plate, plate_copy, current_node[4]))



	def find_tuile_pos(self, tuile: int, plate: Plate | None = None):
		if plate == None:
			plate = self.final_state
		for i in range(0, self.n):
			for j in range(0, self.n):
				if plate[i][j] == tuile:
					return i, j
		return -1, -1
	

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
	

	def pondered_manhatan_distance(self, given_plate: Plate):
		manhatan_distance = 0

		for i in range(0, self.n):
			for j in range(0, self.n):
				if given_plate[i][j] == 0:
					pass
				else:
					final_i, final_j = self.find_tuile_pos(given_plate[i][j])
					distance = abs(j - final_j) + abs(i - final_i)
					weight = 1
					if (i > self.n):
						weight += i ** 2
					elif (i < self.n):
						weight += abs(i - self.n) ** 2
					if (j > self.n):
						weight += j ** 2
					elif (j < self.n):
						weight += abs(j - self.n)  ** 2
					manhatan_distance += distance * weight

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


	def nb_bad_placed(self, given_plate: Plate):
		nb_bad_placed = 0
		for i in range(0, self.n):
			for j in range(0, self.n):
				if  given_plate[i][j] != 0 and given_plate[i][j] != self.final_state[i][j]:
					nb_bad_placed += 1

		return nb_bad_placed
	


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

	def is_puzzle_solvable(self):
		taquin = self
		nb_inversion = self.count_inversion(self.plate)

		empty_pos_i, empty_pos_j = taquin.find_tuile_pos(0, taquin.plate)
		final_empty_pos_i, final_empty_pos_j = taquin.find_tuile_pos(0)
		distance_empty_tuile = abs(empty_pos_j - final_empty_pos_j) + abs(empty_pos_i - final_empty_pos_i)


		if distance_empty_tuile % 2 == 0:
			return nb_inversion % 2 == 0
		else:
			return nb_inversion % 2 != 0
			


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

		numbers =  [self.n ** 2 if x == 0 else x for x in numbers]
		for i in range(len(numbers), 0, -1):
			for element in numbers[:-i]:
				if element > numbers[-i]:
					inversion.add((element, numbers[-i]))

		return len(inversion)
	

