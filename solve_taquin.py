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
import heapq






def solve_taquin(taquin: Taquin,  draw_taquin: Draw_Taquin): 
        draw_taquin.taquin = taquin
        time.sleep(2)
        avoided_boucle = 0 
        inutile = []
        while taquin.heuristic > 0:
            mouves : heapq = taquin.get_open_set()
            explored = False
            print("len mouves", len(mouves))
            best_mouve =  heapq.heappop(mouves)

            while taquin.detect_boucle(best_mouve[2]['plate']):
                do_break = True
                for elem in mouves:
                     if not taquin.detect_boucle(elem[2]['plate']):
                          do_break = False
                          print("detect not boucke")
                          break
                if do_break:
                     break    
                if len(mouves) <= 0:
                    idx = taquin.is_node_in_utile(best_mouve[2]['plate'])
                    if (idx != -1):
                        for b in range(len(taquin.utils_nodes) - 1, idx - 1  , -1):
                            taquin.utils_nodes.pop(b)
                        inutile.append(idx)
                        explored = True
                    print("break")
                    break
                best_mouve =  heapq.heappop(mouves)
                avoided_boucle += 1


            plate_to_str = ''.join(map(str, [element for col in taquin.plate for element in col]))
            taquin.explored_nodes.add(plate_to_str) 
            if not explored:
                taquin.utils_nodes.append({"plate": plate_to_str, "dir": best_mouve[2]['dir']})
            taquin.plate = best_mouve[2]["plate"]
           
            taquin.heuristic = best_mouve[0]
            taquin.last_move_dir = best_mouve[2]['dir']
            if False:
                taquin.set_lines_and_col_resolved()
            draw_taquin.taquin = taquin

        print("Total number of states ever selected :", len(taquin.explored_nodes))
        print("Number of moves required  :", len(taquin.utils_nodes))
        print("Maximum number of states ever represented in memory ")
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
           # test_mouves(taquin_test,  [mouve["dir"] for mouve in taquin.explored_nodes] )
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

