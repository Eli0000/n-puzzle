import curses
import random
from taquin_class import Taquin, MouveType, test_mouves
from utils import Plate, choice_heuristic, comp_double_tab, parse_file
import time
import threading
from draw_plate import Draw_Taquin
import copy
from functools import cmp_to_key
import sys





def solve_taquin(taquin: Taquin,  draw_taquin: Draw_Taquin): 
    
        draw_taquin.taquin = taquin
        time.sleep(2)
        avoided_boucle = 0 
        inutile = []
        while taquin.heuristic > 0:
            #print('manhanan:', taquin.manhatan_distance(taquin.plate))
            mouves: list[MouveType] = taquin.possible_mouve()
    
            random.shuffle(mouves)
            for mouve in mouves:
                plate_cpy = copy.deepcopy(taquin.plate)
                taquin.mouve(mouve, plate_cpy)
                mouve['heuristic'] = taquin.heuristic_funct(plate_cpy)
                mouve['plate'] = plate_cpy
                # if taquin.is_corner_mouvable(mouve):
                #       mouve['heuristic'] = 1
                     
              #  sys.exit()
     
               

        
    
           # print(len(mouves))
            explored = False
            best_mouve =  min(mouves, key=lambda x: x['heuristic'])
            idx = taquin.is_node_in_utile(taquin.plate, mouve)
            if (idx != -1):
                for b in range(len(taquin.utils_nodes) - 1, idx - 1 , -1):
                    taquin.utils_nodes.pop(b)
                inutile.append(idx)

        
            while taquin.detect_boucle(best_mouve['plate'], mouve) and (len(mouves) > 1):
                print("cherche boucle")
                mouves.remove(best_mouve)
                best_mouve =  min(mouves, key=lambda x: x['heuristic'])
                avoided_boucle += 1
            #print("mouve", [x['dir'] for x in mouves ])
           # print("best mouve", best_mouve)
            taquin.explored_nodes.append({"plate": copy.deepcopy(taquin.plate), "dir": best_mouve['dir']}) 
            if not explored:
                taquin.utils_nodes.append({"plate": copy.deepcopy(taquin.plate), "dir": best_mouve['dir']})
            taquin.mouve(best_mouve, taquin.plate)
           
            taquin.heuristic = best_mouve['heuristic']
            taquin.last_move_dir = best_mouve['dir']
            taquin.set_lines_and_col_resolved()
            draw_taquin.taquin = taquin
            #print("resokved: ", taquin.resolved)
            # print("line res: ", taquin.lines_resolved)
            # print("col res: ", taquin.col_resolved)
            # print("col res: ", taquin.col_resolved)
            # if len(taquin.lines_resolved) > 0 or len(taquin.col_resolved) > 0:
            #      sys.exit()
          #  time.sleep(0.5)


        # required_mouve = []
        
        # for i in range(0, len(taquin.explored_nodes)): 
        #     for j in range(0, len(required_mouve)):

        #         if taquin.explored_nodes[i]["plate"] == required_mouve[j]["plate"] :
        #             print("same")
        #             for k in range(len(required_mouve) - 1, j - 1, -1):
        #                 print(k,  len(required_mouve) )
        #                 required_mouve.pop(k)
        #             break
        #     required_mouve.append(taquin.explored_nodes[i])
        print("Total number of states ever selected :", len(taquin.explored_nodes))
        print("Number of moves required  :", len(taquin.utils_nodes))
      #  print("Mouves required: ", [mouve["dir"] for mouve in taquin.utils_nodes])
        print("boucle evité  :", avoided_boucle)
        print("inutuke :", inutile)
        time.sleep(3)
        draw_taquin.run_draw = False

        












if __name__ ==  '__main__':
        test: Taquin
        try:
            plate = parse_file()
            opt, choice = curses.wrapper(choice_heuristic)
            print("Your choose ", opt[choice], " as heuristic.")
        
            taquin = Taquin(plate, choice) 
            if not taquin.is_puzzle_solvable():
                print("The taquin configuration is not soluble")
                sys.exit()

            draw_taquin = Draw_Taquin()
            process_thread = threading.Thread(target=solve_taquin, args=[taquin, draw_taquin ])
            process_thread.start()
            draw_taquin.draw()
            process_thread.join()

            
            taquin_test =  Taquin(plate, choice) 
            test_mouves(taquin_test,  [mouve["dir"] for mouve in taquin.explored_nodes] )
            taquin_test.plate = plate
            test_mouves(taquin_test,  [mouve["dir"] for mouve in taquin.utils_nodes] )
            
            # draw_taquin.taquin = taquin_test
            # draw_taquin.run_draw = True
            # process_thread = threading.Thread(target=test_mouves, args=[taquin_test,  [mouve["dir"] for mouve in taquin.explored_nodes] ])
            # process_thread.start()
            # draw_taquin.draw()
            # process_thread.join()
            # draw_taquin.run_draw = False


        except  EOFError as e :
             print(e)

