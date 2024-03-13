from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from taquin_class import Taquin
import pygame
import time
from utils import Plate
from math import floor
import sys



def get_num_array():
    if len(sys.argv) < 2:
        raise Exception("Please provide one argument")
    array = []
    for i in range(1, len(sys.argv)):
        str_arg = sys.argv[i].split()
        num_arg = [int(element) for element in str_arg]
        if len(num_arg) != len(sys.argv) - 1:
            raise Exception('The plate_draw must be a square')
        array.append(num_arg)
        i += 1
    return array


# num_array = get_num_array()


class Draw_Taquin:

    def __init__(self) -> None:
        self.run_draw = True
        self.taquin: Plate = None
        self.n = 0
        self.square_size = 0
        self.font = 0
        self.canceled = False

    def draw(self):
        pygame.init()
        global canceled
        while self.taquin == None:
            time.sleep(0.1)

        self.n = len(self.taquin)
        self.square_size = floor((1000 - 10) / self.n)
        self.font = pygame.font.Font(None, floor(self.square_size / 2))
        # Initialisation de Pygame

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

        # Boucle principale
        while self.run_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.canceled = True
                    self.run_draw = False
                    pygame.quit()
                    sys.exit()

            # Efface l'écran avec une couleur blanche
            screen.fill(white)

            # Dessine les rectangles

            j = 0
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if self.taquin[i][j] == 0:
                        continue
                    x = 5 + (j * self.square_size)
                    y = 5 + (i * self.square_size)

                    # if (i in self.taquin.lines_resolved or j in self.taquin.col_resolved):
                    #         color = green
                    # elif (self.taquin.plate[i][j] in self.taquin.resolved):
                    #         color = black

                    color = brown

                    pygame.draw.rect(
                        screen, color, (x, y, self.square_size, self.square_size))
                    text = self.font.render(
                        str(self.taquin[i][j]), True, white)
                    text_rect = text.get_rect(
                        center=(x + self.square_size / 2, y + self.square_size / 2))
                    screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        return


def draw_soluce(taquin: Taquin, draw: Draw_Taquin):
    draw.taquin = taquin.plate

    i_0, j_0 = taquin.find_tuile_pos(0, taquin.plate)
    to_draw = taquin.plate
    for mouve in taquin.mouves_soluce:
        match mouve:
            case 'down':
                to_draw[i_0][j_0] = to_draw[i_0 - 1][j_0]
                to_draw[i_0 - 1][j_0] = 0
                i_0 -= 1
            case 'up':

                to_draw[i_0][j_0] = to_draw[i_0 + 1][j_0]
                to_draw[i_0 + 1][j_0] = 0
                i_0 += 1
            case 'right':
                to_draw[i_0][j_0] = to_draw[i_0][j_0 - 1]
                to_draw[i_0][j_0 - 1] = 0
                j_0 -= 1
            case 'left':
                to_draw[i_0][j_0] = to_draw[i_0][j_0 + 1]
                to_draw[i_0][j_0 + 1] = 0
                j_0 += 1

        draw.taquin = to_draw

        time.sleep(0.1)

    time.sleep(3)
    if (to_draw == taquin.final_state):
        print("Le taquin est resolue")

    else:
        print("Le taquin n'est pas resolue")

    draw.run_draw = False
