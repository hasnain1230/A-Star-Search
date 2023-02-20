import sys


class BinaryHeap:
    def __init__(self):
        self.current_size = 0
        self.heap_list = [0]

    @staticmethod
    def parent(x):
        return x // 2

    @staticmethod
    def left_child(x):
        return x * 2

    @staticmethod
    def right_child(x):
        return x * 2 + 1

    def is_leaf(self, x):
        return x * 2 > self.current_size

    def is_empty(self):
        return self.current_size == 0

    def sift_up(self, x):
        stop = False

        while self.parent(x) > 0 and not stop:
            if self.heap_list[x] < self.heap_list[self.parent(x)]:
                self.heap_list[x], self.heap_list[self.parent(x)] = self.heap_list[self.parent(x)], self.heap_list[x]
                x = self.parent(x)
            else:
                stop = True

    def sift_down(self, x):
        stop = False

        while self.left_child(x) <= self.current_size and not stop:
            min_child = self.min_child(x)

            if self.heap_list[x] > self.heap_list[min_child]:
                self.heap_list[x], self.heap_list[min_child] = self.heap_list[min_child], self.heap_list[x]
                x = min_child
            else:
                stop = True

    def min_child(self, x):
        if self.right_child(x) > self.current_size:
            return self.left_child(x)
        else:
            if self.heap_list[self.left_child(x)] < self.heap_list[self.right_child(x)]:
                return self.left_child(x)
            else:
                return self.right_child(x)

    def insert(self, x):
        self.heap_list.append(x)
        self.current_size += 1
        self.sift_up(self.current_size)

    def pop(self):
        min_value = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size -= 1
        self.heap_list.pop()
        self.sift_down(1)
        return min_value

    def __contains__(self, item):
        return item in self.heap_list

    def __str__(self):
        return str(self.heap_list)

if __name__ == '__main__':
    heap = BinaryHeap()
    heap.insert(10)
    heap.insert(20)
    heap.insert(30)
    heap.insert(40)
    heap.insert(9)
    heap.insert(8)
    heap.insert(7)
    heap.insert(62)
    heap.insert(1)
    heap.insert(2)

    while not heap.is_empty():
        print(heap.pop())