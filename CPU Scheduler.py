from collections import deque

#Creates Ready Queue
ready_queue = deque()

#Adding Processes to Queue
ready_queue.append("P1")
ready_queue.append("P2")
ready_queue.append("P3")

print("Queue:", ready_queue)

#Scheduling Next Process
running = ready_queue.popleft()

print("Running:", running)
print("Queue after scheduling:", ready_queue)