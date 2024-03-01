from ctypes import addressof
import curses
from taquin_class import Taquin
from utils import Plate, choice_algorithm, choice_heuristic, parse_file
import time
import threading
from draw_plate import Draw_Taquin, draw_soluce
import sys
import heapq






def solve_taquin(taquin: Taquin, draw_taquin: Draw_Taquin): 
		

		draw_taquin.taquin = taquin.plate
		time.sleep(3)
		plate_simple_array =  [element for sous_liste in taquin.plate for element in sous_liste]
		hash_current_plate = hash(tuple(plate_simple_array))
		current_node = tuple((0 + taquin.heuristic_funct(taquin.plate), id(taquin.plate), '', 0, hash_current_plate, taquin.plate, None))
		


		while current_node[4] != taquin.final_state_hash:

			draw_taquin.taquin = current_node[5]
			taquin.get_open_nodes(current_node)
			taquin.closed_set.add(tuple((current_node[4], current_node[2], current_node[6])))
			current_node =  heapq.heappop(taquin.open_set)
			while any(tuple_element[0] ==  current_node[4]  for tuple_element in taquin.closed_set):
				current_node =  heapq.heappop(taquin.open_set)

	

		draw_taquin.taquin = current_node[5]
		taquin.closed_set.add(tuple((current_node[4], current_node[2], current_node[6])))
		time.sleep(2)

		draw_taquin.run_draw = False

		mouves_required = []
		iter_node =  next((element for element in taquin.closed_set if element[0] == taquin.final_state_hash), None)
		while iter_node[2] != None:
			mouves_required.append(iter_node[1])
			iter_node =  next((element for element in taquin.closed_set if element[0] == iter_node[2]), None)
		mouves_required.reverse()



		print("Total number of states ever selected :", len(taquin.closed_set))
		print("Number of moves required  :", len(mouves_required))
		print("Maximum number of states ever represented in memory ", len(taquin.closed_set) + len(taquin.open_set))
		print("Mouves required: ", mouves_required)

		taquin.mouves_soluce = mouves_required



			#time.sleep(2)



		









if __name__ ==  '__main__':
		test: Taquin
		try:
			plate = parse_file()

			opt_algo, choice_algo = curses.wrapper(choice_algorithm)
			if (choice_algo != "uniform-cost"):
				opt_heur, choice_heur = curses.wrapper(choice_heuristic)
				print("Your chose ", choice_algo, " with ", opt_heur[choice_heur], " as heuristic.")
			else:
				choice_heur = None
				print("Your chose ", choice_algo, ".")
		
			taquin = Taquin(plate, choice_algo, choice_heur) 
			if not taquin.is_puzzle_solvable():
				print("The taquin configuration is not soluble")
				sys.exit()

			draw_taquin = Draw_Taquin()
			process_thread = threading.Thread(target=solve_taquin, args=[taquin, draw_taquin ])
			process_thread.start()
			draw_taquin.draw()
			process_thread.join()
			
			
			# draw_taquin.run_draw = True	
			# process_thread = threading.Thread(target=draw_soluce, args=[taquin, draw_taquin ])
			# process_thread.start()
			# draw_taquin.draw()
			# process_thread.join()
			

			sys.exit()
			
			
	

		except  EOFError as e :
			 print(e)

