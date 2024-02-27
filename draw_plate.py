from math import floor
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from utils import Plate
import time
import pygame
from taquin_class import Taquin

def get_num_array():
    if len(sys.argv) < 2:
        raise Exception("Please provide one argument")
    array = [] 
    for i in range (1, len(sys.argv)):
        str_arg = sys.argv[i].split()
        num_arg = [int(element) for element in str_arg]
        if len(num_arg) != len(sys.argv) - 1:
              raise Exception('The plate_draw must be a square')
        array.append(num_arg)
        i += 1
    return array
        

#num_array = get_num_array()


class Draw_Taquin:


    def __init__(self) -> None:
        self.run_draw = True
        self.taquin : Taquin = None

    def draw(self):
        while self.taquin == None:
            time.sleep(0.1)
        n = len(self.taquin.plate)
        square_size = floor((1000 - 10) / n)

        # Initialisation de Pygame
        pygame.init()

        # Dimensions de la fenêtre
        width, height = 1000, 1000

        # Création de la fenêtre
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Taquin Game")

        # Couleurs
        white = (255, 255, 255)
        brown = (88, 41, 0)
        black = (0, 0, 0)
        green = (0, 0, 100)


        # Chargement d'une police
        font = pygame.font.Font(None, floor(square_size / 2))

        # Boucle principale
        while self.run_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_draw = False
                    pygame.quit()
                    sys.exit()


            # Efface l'écran avec une couleur blanche
            screen.fill(white)

            # Dessine les rectangles
           


            j = 0
            for i in range(0, n):
                for j in range(0, n):
                        if self.taquin.plate[i][j] == 0:
                                continue
                        x = 5 + (j * square_size)
                        y = 5 + (i * square_size)
                        

                        if (self.taquin.heuristic == 0):
                            color = green
                        else:
                            if (i in self.taquin.lines_resolved or j in self.taquin.col_resolved):
                                    color = green
                            elif (self.taquin.plate[i][j] in self.taquin.resolved):
                                    color = black
                            else:
                                    color = brown


                        pygame.draw.rect(screen, color, (x, y, square_size, square_size))
                   #     pygame.draw.rect(screen, white, (x, y, square_size, square_size), floor(square_size * 0.015) )
                        text = font.render(str(self.taquin.plate[i][j]), True, white)
                        text_rect = text.get_rect(center=(x + square_size / 2, y + square_size / 2))
                        screen.blit(text, text_rect)

            # Met à jour l'affichage
            pygame.display.flip()

        # Quitte Pygame
        pygame.quit()
        return
        sys.exit()







