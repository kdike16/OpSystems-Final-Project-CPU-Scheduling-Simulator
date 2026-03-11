from ready_queue import ReadyQueue
from process import ProcessState


class Scheduler:

    def __init__(self):
        self.ready_queue = ReadyQueue()
        self.clock = 0
        self.running = None
        self.processes = []   # list of all processes
    
    #Adds Proccess to Ready Queue 
    def addProcces(self, process):
        self.processes.append(process)

    #Checks to see if any Processes are ready to be scheduled (Assigns next state to "READY")
    def checkArrivals(self):
        for proc in self.processes:
            if proc.arrival_time == self.clock:
                proc.state == ProcessState.READY
                self.ready_queue.enqueue(proc)

    #Schedule next available Process in Queue (FCFS Scheduling)
    def scheduleNext(self):
        if self.running is None and not self.ready_queue.isEmpty():
            self.running = self.ready_queue.dequeue()
            self.running.state = ProcessState.RUNNING
    
    def runProcess(self):
         if self.running is not None:
            self.running.remaining_time -= 1
            print(f"Time {self.clock}: Running P{self.running.pid}")

            if self.running.remaining_time == 0:
                self.running.state = ProcessState.TERMINATED
                print(f"P{self.running.pid} finished")
                self.running = None

    def run(self):
        while True:
            self.checkArrivals()
            self.scheduleNext()
            self.runProcess()
            self.clock += 1
            if all(proc.state == ProcessState.TERMINATED for proc in self.processes):
                break

