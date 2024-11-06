def add_or_replace2(self: Self, queue: List,key:int, value:int)->List:
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

def remove (self: Self):

    # We find the element with the smallest value
    min_index = 0
    for i in range(1, len(self.elements)):
        if self.elements[i][1] < self.elements[min_index][1]:
            min_index = i

        # We remove the element with the smallest value
        key, value = self.elements[min_index]
        del self.elements[min_index]

    # We return the key and value of the element removed
    return key, value

if __name__=="__main__":
    heap = []
    print(heap.add_or_replace2([(1, 2), (2, 3)], 1, 1))
    rezjrkezl