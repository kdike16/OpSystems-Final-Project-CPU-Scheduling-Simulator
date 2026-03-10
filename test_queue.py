from ready_queue import ReadyQueue
from process import ProcessState
from process import Process

#Creates Ready Queue
ready_queue = ReadyQueue()

#Creating Processes
P1 = Process(1, 0, 5)
P2 = Process(2, 2, 3)
P3 = Process(3, 4, 2)

#Adding Processes to Queue
ready_queue.enqueue(P1)
ready_queue.enqueue(P2)
ready_queue.enqueue(P3)

print("Queue:", ready_queue)

#Scheduling Next Process
if not ready_queue.isEmpty():
    running = ready_queue.dequeue()
    print("Running:", running)
    print("Queue after scheduling:", ready_queue)

