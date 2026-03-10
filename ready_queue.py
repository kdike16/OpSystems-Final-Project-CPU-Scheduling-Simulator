from collections import deque

class ReadyQueue:
    def __init__(self):
        self.queue = deque()
    
    #Adds Process to Ready Queue
    def enqueue(self, process):
        self.queue.append(process)

    #Removes Oldest Process Out of the Queue
    def dequeue(self):
        return self.queue.popleft()
    
    #Checks to see if Ready Queue is Empty
    def isEmpty(self):
        return len(self.queue) == 0
    
    def __str__(self):
        return str(list(self.queue))
    
    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.queue) + "]"


