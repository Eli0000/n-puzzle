
import curses
import random
import sys
import time
from typing import List, Type


Plate = Type[List[List[int]]]


class Node:
    def __init__(self, value):
        self.value: any = value
        self.next: Node = None


class CircularChainedList:
    def __init__(self):
        self.head_node: Node = None

    def add_elem(self, value):
        new_node = Node(value)
        if self.head_node is None:
            self.head_node = new_node
            new_node.next = self.head_node
        else:
            iter_node = self.head_node
            while iter_node.next != self.head_node:
                iter_node = iter_node.next
            new_node.next = self.head_node
            iter_node.next = new_node


def comp_double_tab(tableau1, tableau2):
    if len(tableau1) != len(tableau2):
        return False

    for ligne1, ligne2 in zip(tableau1, tableau2):
        if ligne1 != ligne2:
            return False

    return True


def afficher_menu(win, options, choix_actuel):
    win.clear()
    height, width = win.getmaxyx()
    for index, option in enumerate(options):
        x = width // 2 - len(option) // 2
        y = height // 2 - len(options) // 2 + index
        if index == choix_actuel:
            win.addstr(y, x, option, curses.color_pair(1))
        else:
            win.addstr(y, x, option)
    win.refresh()


def choisir_option(win, options):
    choix_actuel = 0
    afficher_menu(win, options, choix_actuel)

    while True:
        key = win.getch()
        if key == curses.KEY_DOWN and choix_actuel < len(options) - 1:
            choix_actuel += 1
        elif key == curses.KEY_UP and choix_actuel > 0:
            choix_actuel -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return choix_actuel
        afficher_menu(win, options, choix_actuel)


def choice_heuristic(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    options = ["Manathan distance", "Pondered Manathan distance", "Euclidean distance", "Number of mouves"]
    choice = choisir_option(stdscr, options)
    curses.endwin()
    return options, choice


def choice_algorithm(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    options = ["Standard A*", "Greedy search", "Uniform cost"]
    choice = choisir_option(stdscr, options)
    match choice:
        case 0:
            choice = "standard A*"
        case 1:
            choice = "Greedy search"
        case 2:
            choice = 'Uniform cost'
    curses.endwin()
    return options, choice


def parse_file(file_path):
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
                    raise Exception(
                        "Taquin tuiles must be numbers only.")

            if len(clear_line) == 0:
                continue
            # Utilise la méthode split() pour diviser la ligne en une liste d'éléments
            elements = clear_line.split()
            # Convertis les éléments en entiers si nécessaire
            row = [int(element) for element in elements]

            # Ajoute la ligne à la liste à deux dimensions
            plate_conf.append(row)
        if len(plate_conf[0]) <= 0:
            raise Exception(
                "Taquin plate must not contain empty line.")
        n = plate_conf[0][0]
        plate_conf.pop(0)
        if (n < 3):
            raise Exception(
                "Taquin plate must have a size of 3 minimum.")
        if len(plate_conf) != n:
            raise Exception("Taquin plate must be squared.")
        for elem in plate_conf:
            if len(elem) != n:
                raise Exception(
                    "Taquin plate must be squared.")

    return plate_conf

def generate_plate(size: str):
    if not size.isdigit():
        raise Exception("Invalid size")
    
    size = int(size)
    if (size < 3):
        raise Exception("The size must be minimum 3")
    
    array = [i for i in range(0, size * size)]
    random.shuffle(array)
    plate = []
    i = 0
    while i < len(array):
        plate.append(array[i:i + size])
        i += size
    
    return plate

def get_plate(argv: list[str]):
    if (len(argv) != 3):
            raise Exception("Error: specify -f (--file) <path> option to use a input file\
                            or -r (--random) <size> to randomly generated state")
    match argv[1]:
        case '-f' | '--file':
            return parse_file(argv[2])

        case '-r' | '--random':
            return generate_plate(argv[2])
        case _:
            raise Exception('Invalid option -r (--random) | -f (--file)')