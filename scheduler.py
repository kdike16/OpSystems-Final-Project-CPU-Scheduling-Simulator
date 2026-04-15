from ready_queue import ReadyQueue
from process import ProcessState


class Scheduler:

    def __init__(self):
        self.ready_queue = ReadyQueue()
        self.clock = 0
        self.running = None
        self.processes = []
        self.completion_order = []   # NEW: track order processes finish
    
    # Adds Process to Ready Queue
    def addProcess(self, process):
        self.processes.append(process)

    # Checks if processes arrive at current clock time
    def checkArrivals(self):
        for proc in self.processes:
            if proc.arrival_time == self.clock:
                proc.state = ProcessState.READY   # FIXED (= not ==)
                self.ready_queue.enqueue(proc)

    # FCFS scheduling
    def scheduleNext(self):
        if self.running is None and not self.ready_queue.isEmpty():
            self.running = self.ready_queue.dequeue()
            self.running.state = ProcessState.RUNNING

            # NEW: record first time process runs
            if self.running.start_time is None:
                self.running.start_time = self.clock

    #SJF Scheduling 
    def scheduleShortestJob(self):
        if self.running is None and not self.ready_queue.isEmpty():

            # Finds job with shortest burst time
            shortest_job = min(self.ready_queue.queue, key=lambda p: p.burst_time)

            # Remove that job from the queue
            self.ready_queue.queue.remove(shortest_job)

            # Set it as the running process
            self.running = shortest_job
            self.running.state = ProcessState.RUNNING

            # Record first time the process runs
            if self.running.start_time is None:
                self.running.start_time = self.clock
            
                
    def runProcess(self):
        if self.running is not None:

            self.running.remaining_time -= 1
            print(f"Time {self.clock}: Running P{self.running.pid}")

            if self.running.remaining_time == 0:

                # NEW: record completion time
                self.running.finish_time = self.clock + 1

                # NEW: calculate turnaround time
                self.running.turnaround_time = (
                    self.running.finish_time - self.running.arrival_time
                )

                # NEW: calculate waiting time
                self.running.waiting_time = (
                    self.running.turnaround_time - self.running.burst_time
                )

                self.running.state = ProcessState.TERMINATED
                print(f"P{self.running.pid} finished at time {self.running.finish_time}")

                # NEW: record completion order
                self.completion_order.append(self.running.pid)

                self.running = None

    # NEW: print statistics
    def print_statistics(self):

        print("\nProcess Statistics")
        print("--------------------------")

        for proc in self.processes:
            print(
                f"P{proc.pid} | Waiting Time: {proc.waiting_time} | "
                f"Turnaround Time: {proc.turnaround_time}"
            )

        print("\nCompletion Order:")
        print(" -> ".join(f"P{pid}" for pid in self.completion_order))

    def run(self):
        while True:
            self.checkArrivals()
            self.scheduleNext()
            self.runProcess()

            self.clock += 1

            if all(proc.state == ProcessState.TERMINATED for proc in self.processes):
                break

        # NEW: display results
        self.print_statistics()
