from math import floor
from multiprocessing import Pipe, Process
import pygame
import sys
from utils import Plate
import time




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
        self.plate_draw = None 

    def draw(self):
        while self.plate_draw == None:
            time.sleep(1)
        print("sellllffff", self.plate_draw)
        n = len(self.plate_draw)
        square_size = floor((1000 - 10) / n)

        # Initialisation de Pygame
        pygame.init()

        # Dimensions de la fenêtre
        width, height = 1000, 1000

        # Création de la fenêtre
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Fenêtre avec rectangles")

        # Couleurs
        white = (255, 255, 255)
        black = (88, 41, 0)


        # Chargement d'une police
        font = pygame.font.Font(None, floor(square_size / 2))

        # Boucle principale
        while self.run_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_draw = False

            # Efface l'écran avec une couleur blanche
            screen.fill(white)

            # Dessine les rectangles
           


            j = 0
            for i in range(0, n):
                for j in range(0, n):
                        if self.plate_draw[i][j] == 0:
                                continue
                        x = 5 + (j * square_size)
                        y = 5 + (i * square_size)
                        
                        pygame.draw.rect(screen, black, (x, y, square_size, square_size))
                        pygame.draw.rect(screen, white, (x, y, square_size, square_size), floor(square_size * 0.015) )
                        text = font.render(str(self.plate_draw[i][j]), True, white)
                        text_rect = text.get_rect(center=(x + square_size / 2, y + square_size / 2))
                        screen.blit(text, text_rect)

            # Met à jour l'affichage
            pygame.display.flip()

        # Quitte Pygame
        pygame.quit()
        sys.exit()


def processus_recepteur(conn, draw: Draw_Taquin):
        # Recevoir des données par le pipe
        while True:
            print('await message')
            message = conn.recv()
            print(message)
            if message == "STOP":
                print("received stop")
                draw.run_draw = False
                break
            print("Reçu:", message)
            draw.plate_draw = message
        conn.close()





