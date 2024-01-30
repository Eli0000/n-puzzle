
from typing import List, Type
import subprocess
import threading


Plate = Type[List[List[int]]]


class Node:
    def __init__(self, value):
        self.value: any = value
        self.next : Node = None
        

class ChainedList:
    def __init__(self):
        self.head_node : Node  = None

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
            # print("not  equal")
            # print("ligne1", ligne1, "ligne2", ligne2)
            return False
    
    return True




        









