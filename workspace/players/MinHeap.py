class ListBasedMinHeap ():
    
    def __init__ (self):

        # We create an attribute to store the elements
        self.elements = []

    def add_or_replace (self, key, value):
    
        # We check if the key is already in the heap
        index = None
        for i in range(len(self.elements)):
            if self.elements[i][0] == key:
                index = i
                break
        
        # If the key is already in the heap, we remove the previous element if the new value is lower
        add_new_element = True
        if index is not None:
            if value < self.elements[index][1]:
                del self.elements[index]
            else:
                add_new_element = False

        # We add the new element
        if add_new_element:
            self.elements.append((key, value))

    def remove (self):

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


# Tests des différentes fonctions :

if __name__=="__main__":
    # Create a min-heap
    heap = ListBasedMinHeap()
    
    # Add elements to the heap
    heap.add_or_replace("A", 50)
    heap.add_or_replace("B", 22)
    heap.add_or_replace("C", 10)

    # Show the elements of the heap
    print("Heap initial state:", heap.elements)

    # Remove the element with the smallest value
    key, value = heap.remove()
    print("Removed:", key, value)
    print("Heap after remove():", heap.elements)

    # Add a new element to the heap
    heap.add_or_replace("B", 45)
    print("Heap after add_or_replace(B, 45):", heap.elements)

    # Add a new element to the heap
    heap.add_or_replace("A", 35)
    print("Heap after add_or_replace(A, 35):", heap.elements)

    # Remove the element with the smallest value
    key, value = heap.remove()
    print("Removed:", key, value)
    print("Heap after remove():", heap.elements)