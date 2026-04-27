from ready_queue import ReadyQueue
from process import ProcessState


class Scheduler:

    def __init__(self):
        self.ready_queue = ReadyQueue()
        self.clock = 0
        self.running = None
        self.processes = []
        self.completion_order = []
    
    def addProcess(self, process):
        self.processes.append(process)

    def checkArrivals(self):
        for proc in self.processes:
            if proc.arrival_time == self.clock:
                proc.state = ProcessState.READY
                self.ready_queue.enqueue(proc)

    # FCFS scheduling
    def schedule_Next(self):
        if self.running is None and not self.ready_queue.isEmpty():
            self.running = self.ready_queue.dequeue()
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

    # SJF Scheduling 
    def schedule_Shortest_Job(self):
        if self.running is None and not self.ready_queue.isEmpty():
            shortest_job = min(self.ready_queue.queue, key=lambda p: p.burst_time)
            self.ready_queue.queue.remove(shortest_job)
            self.running = shortest_job
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

    # SRTF Scheduling 
    def schedule_Shortest_Remaining_Time(self):
        if self.ready_queue.isEmpty():
            return
        shortest_remaining_time = min(self.ready_queue.queue, key=lambda p: p.remaining_time)

        if self.running is None:
            self.ready_queue.queue.remove(shortest_remaining_time)
            self.running = shortest_remaining_time
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

        elif shortest_remaining_time.remaining_time < self.running.remaining_time:
            self.running.state = ProcessState.READY
            self.ready_queue.enqueue(self.running)
            self.ready_queue.queue.remove(shortest_remaining_time)
            self.running = shortest_remaining_time
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

    # Non-Preemptive Priority Scheduling
    def schedule_Priority_NonPreemptive(self):
        if self.running is None and not self.ready_queue.isEmpty():
            highest_priority = min(self.ready_queue.queue, key=lambda p: p.priority)
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

    # Preemptive Priority Scheduling
    def schedule_Priority_Preemptive(self):
        if self.ready_queue.isEmpty():
            return
        highest_priority = min(self.ready_queue.queue, key=lambda p: p.priority)

        if self.running is None:
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

        elif highest_priority.priority < self.running.priority:
            self.running.state = ProcessState.READY
            self.ready_queue.enqueue(self.running)
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock

    # Round Robin Scheduling
    def schedule_Round_Robin(self, quantum=2):
        if not hasattr(self, 'rr_quantum_remaining'):
            self.rr_quantum_remaining = 0

        if self.running is not None and self.rr_quantum_remaining == 0:
            if self.running.remaining_time > 0:
                self.running.state = ProcessState.READY
                self.ready_queue.enqueue(self.running)
                self.running = None

        if self.running is None and not self.ready_queue.isEmpty():
            self.running = self.ready_queue.dequeue()
            self.running.state = ProcessState.RUNNING
            self.rr_quantum_remaining = quantum
            if self.running.start_time is None:
                self.running.start_time = self.clock

        if self.running is not None:
            self.rr_quantum_remaining -= 1
            self.running.remaining_time -= 1
            print(f"Time {self.clock}: Running P{self.running.pid} | Quantum left: {self.rr_quantum_remaining}")

            if self.running.remaining_time == 0:
                self.running.finish_time = self.clock + 1
                self.running.turnaround_time = self.running.finish_time - self.running.arrival_time
                self.running.waiting_time = self.running.turnaround_time - self.running.burst_time
                self.running.state = ProcessState.TERMINATED
                print(f"P{self.running.pid} finished at time {self.running.finish_time}")
                self.completion_order.append(self.running.pid)
                self.running = None
                self.rr_quantum_remaining = 0

    def runProcess(self):
        if self.running is not None:
            self.running.remaining_time -= 1
            print(f"Time {self.clock}: Running P{self.running.pid}")

            if self.running.remaining_time == 0:
                self.running.finish_time = self.clock + 1
                self.running.turnaround_time = self.running.finish_time - self.running.arrival_time
                self.running.waiting_time = self.running.turnaround_time - self.running.burst_time
                self.running.state = ProcessState.TERMINATED
                print(f"P{self.running.pid} finished at time {self.running.finish_time}")
                self.completion_order.append(self.running.pid)
                self.running = None

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

    def run(self, scheduling_function, quantum=None):
        while True:
            self.checkArrivals()

            if scheduling_function == self.schedule_Round_Robin:
                 scheduling_function(quantum)
            else:
                scheduling_function()
                self.runProcess()

            self.clock += 1

            if all(proc.state == ProcessState.TERMINATED for proc in self.processes):
                break

        self.print_statistics()