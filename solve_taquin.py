from multiprocessing import Pipe, Process
import random
from taquin_class import Taquin, MouveType
from utils import Plate, comp_double_tab
import time
import threading
from draw_plate import Draw_Taquin
import copy
from functools import cmp_to_key
import sys

def parse_file():
    file_path = './npuzzle.txt'
    plate_conf = []
    
    with open(file_path, 'r') as file:
        for line in file:
            clear_line = line
            for char in line:
                if char == '#':
                    split_comment = line.split('#', 1)
                    clear_line = split_comment[0]
            
            for char in clear_line:
                if not char.isdigit() and not char.isspace():
                    raise Exception("Error in puzzle : Taquin tuiles must be numbers only.")

            if len(clear_line) == 0:
                 continue
            # Utilise la méthode split() pour diviser la ligne en une liste d'éléments
            elements = clear_line.split()
            # Convertis les éléments en entiers si nécessaire
            row = [int(element) for element in elements]
            
            # Ajoute la ligne à la liste à deux dimensions
            plate_conf.append(row)
        n = plate_conf[0][0]
        plate_conf.pop(0)
        if len(plate_conf) != n:
                raise Exception("Error in puzzle : Taquin plate must be squared.")
        for elem in plate_conf:
             if len(elem) != n:
                raise Exception("Error in puzzle : Taquin plate must be squared.")

                
    return plate_conf





def solve_taquin(taquin: Taquin,  draw_taquin: Draw_Taquin): 
    
        draw_taquin.plate_draw = taquin.plate
        time.sleep(2)
        while taquin.misplaced > 0:
            #print('manhanan:', taquin.manhatan_distance(taquin.plate))
            mouves: MouveType = taquin.possible_mouve()
            for mouve in mouves:
                plate_cpy = copy.deepcopy(taquin.plate)
                taquin.mouve(mouve, plate_cpy)
                mouve['heuristic'] = taquin.heuristic(plate_cpy)
                if taquin.is_node_explored(plate_cpy, mouve['dir']):
                     print("already explored")
                     mouve['heuristic'] **= taquin.n
           
                  
            random.shuffle(mouves)
            #print('len mouves ', len(mouves))
            best_mouve =  min(mouves, key=lambda x: x['heuristic'])
            #print("mouve", mouves)
          #  print("best mouve", best_mouve)
            
            taquin.mouve(best_mouve, taquin.plate)
            taquin.explored_nodes.append({"plate": copy.deepcopy(taquin.plate), "dir": best_mouve['dir']})
            taquin.cost += 1
            taquin.misplaced = best_mouve['heuristic']
            taquin.last_move_dir = best_mouve['dir']
            draw_taquin.plate_draw =taquin.plate
            #time.sleep(0.02)


        required_mouve = []
        
        for i in range(0, len(taquin.explored_nodes)): 
            if taquin.explored_nodes[i] in required_mouve:
                for k in range(i + 1, len(required_mouve)):
                     required_mouve.pop(k)
            else:
                required_mouve.append(taquin.explored_nodes[i])
        print("Total number of states ever selected :", len(taquin.explored_nodes))
        print("Number of moves required  :", len(required_mouve))













if __name__ ==  '__main__':
        test: Taquin
        try:
            test = parse_file()
        
            taquin = Taquin(test) 
            if not taquin.is_puzzle_solvable():
                print("The taquin configuration is not soluble")
                sys.exit()

            draw_taquin = Draw_Taquin()
            process_thread = threading.Thread(target=solve_taquin, args=[taquin, draw_taquin ])
            process_thread.start()
            draw_taquin.draw()
            process_thread.join()
        except Exception as e:
             print(e)