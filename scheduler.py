from ready_queue import ReadyQueue
from process import ProcessState


class Scheduler:

    def __init__(self):
        self.ready_queue = ReadyQueue()
        self.clock = 0
        self.running = None
        self.processes = []
        self.completion_order = []
        self.context_switches = 0
        self.cpu_busy_time = 0
    
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
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

    # SJF Scheduling 
    def schedule_Shortest_Job(self):
        if self.running is None and not self.ready_queue.isEmpty():
            shortest_job = min(self.ready_queue.queue, key=lambda p: p.burst_time)
            self.ready_queue.queue.remove(shortest_job)
            self.running = shortest_job
            self.running.state = ProcessState.RUNNING
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

    # SRTF Scheduling 
    def schedule_Shortest_Remaining_Time(self):
        if self.ready_queue.isEmpty():
            return
        shortest_remaining_time = min(self.ready_queue.queue, key=lambda p: p.remaining_time)

        if self.running is None:
            self.ready_queue.queue.remove(shortest_remaining_time)
            self.running = shortest_remaining_time
            self.running.state = ProcessState.RUNNING
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

        elif shortest_remaining_time.remaining_time < self.running.remaining_time:
            self.running.state = ProcessState.READY
            self.ready_queue.enqueue(self.running)
            self.ready_queue.queue.remove(shortest_remaining_time)
            self.running = shortest_remaining_time
            self.running.state = ProcessState.RUNNING
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

    # Non-Preemptive Priority Scheduling
    def schedule_Priority_NonPreemptive(self):
        if self.running is None and not self.ready_queue.isEmpty():
            highest_priority = min(self.ready_queue.queue, key=lambda p: p.priority)
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

    # Preemptive Priority Scheduling
    def schedule_Priority_Preemptive(self):
        if self.ready_queue.isEmpty():
            return
        highest_priority = min(self.ready_queue.queue, key=lambda p: p.priority)

        if self.running is None:
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

        elif highest_priority.priority < self.running.priority:
            self.running.state = ProcessState.READY
            self.ready_queue.enqueue(self.running)
            self.ready_queue.queue.remove(highest_priority)
            self.running = highest_priority
            self.running.state = ProcessState.RUNNING
            self.context_switches += 1
            if self.running.start_time is None:
                self.running.start_time = self.clock
                self.running.response_time = self.clock - self.running.arrival_time

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
            self.context_switches += 1
            self.rr_quantum_remaining = quantum
            if self.running.start_time is None:
                self.running.start_time = self.clock

        if self.running is not None:
            self.cpu_busy_time += 1
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
            self.cpu_busy_time += 1
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
        self.print_statistics()
        self.print_final_metrics()

    def print_final_metrics(self):

        n = len(self.processes)
    
        avg_waiting = sum(p.waiting_time for p in self.processes) / n
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / n
        avg_response = sum(p.response_time for p in self.processes) / n
    
        total_time = self.clock
        throughput = n / total_time
    
        cpu_utilization = (self.cpu_busy_time / total_time) * 100
    
        waiting_times = [p.waiting_time for p in self.processes]
        fairness = min(waiting_times) / max(waiting_times) if max(waiting_times) > 0 else 1
    
        print("\n=== Performance Metrics ===")
        print(f"Average Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Response Time: {avg_response:.2f}")
        print(f"Throughput: {throughput:.2f} processes/unit time")
        print(f"CPU Utilization: {cpu_utilization:.2f}%")
        print(f"Context Switches: {self.context_switches}")
        print(f"Fairness: {fairness:.2f}")
