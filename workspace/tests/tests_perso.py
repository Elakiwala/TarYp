from typing import *
from numbers import *

def add_or_replace2(queue: List, key:Any, value:int)->List:
    """
    This method adds or replaces an element in a min-heap.
    In:
        * queue:  une liste initiale qui va contenir les couples (key,value).
        * key:   The key of the element to add or replace.
        * value: The value of the element to add or replace.
    Out:
        * List.
    """
    for i, (k, v) in enumerate(queue):
        if k == key:
            if value < v:
                queue[i] = (key, value)
            return
    queue.append((key, value))

def add_or_replace(self: Self, key:Any, value:int)->Any:
    """
    This method adds or replaces an element in a min-heap.
    In:
        * queue:  une liste initiale qui va contenir les couples (key,value).
        * key:   The key of the element to add or replace.
        * value: The value of the element to add or replace.
    Out:
        * List.
    """
    index = None
    for i, (k, v) in enumerate(self):
        if k == key:
            index = i
            break
    add_new_element = True
    if index is not None:
        if value < self[index][1]:
            del self[index]
        else:
            add_new_element = False
    if add_new_element:
        self.append((key, value))
    return self   

def remove (self: Self):

    # We find the element with the smallest value
    min_index = 0
    for i in range(1, len(self)):
        if self[i][1] < self[min_index][1]:
            min_index = i

        # We remove the element with the smallest value
        key, value = self[min_index]
        del self[min_index]

    # We return the key and value of the element removed
    return key, value

if __name__=="__main__":
    heap = [(1, 2), (2, 3)]
    #print(heap.add_or_replace2( 1, 1))
    print(heap)
    print(heap.add_or_replace( 1, 1))
    print(heap)
    print(heap.remove())
    print(heap)
    