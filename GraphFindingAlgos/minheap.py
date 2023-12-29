"""Each node is a tuple (NodeID,Weight,Heuristic) Example: (A,15,10) Second element would be the numerical value associated"""
import math
class MinHeap:
    """A min-heap is a tree structure where
    - the root element is the smallest
    - each node can only have 2 children lest the last 2 layers
    - the value of each node is smaller than or equal to the values of its children."""

    def __init__(self):
        self.heap = []

    def check_empty(self):
        return len(self.heap)==0

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, item):
        self.heap.append(item)
        self.heapify_insert(len(self.heap) - 1)

    def heapify_insert(self, i):
        while i > 0 and self.heap[i][1]  < self.heap[self.parent(i)][1] :
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def get_root(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_remove(0)
        return min_item

    def heapify_remove(self, i):
        left = self.left_child(i)
        right = self.right_child(i)
        smallest = i

        if left < len(self.heap) and self.heap[left][1] < self.heap[smallest][1] :
            smallest = left

        if right < len(self.heap) and self.heap[right][1]< self.heap[smallest][1] :
            smallest = right

        if smallest != i:
            self.swap(i, smallest)
            self.heapify_remove(smallest)
