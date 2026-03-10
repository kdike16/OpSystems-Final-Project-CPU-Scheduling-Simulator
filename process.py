from enum import Enum

# Define possible process states
class ProcessState(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        # Basic process info
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority

        # Process state
        self.state = ProcessState.NEW

        # Scheduling statistics
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None

    # Simulate running the process for one clock tick
    def run_one_tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1

    # Mark process as finished
    def complete(self, current_time):
        self.finish_time = current_time
        self.turnaround_time = self.finish_time - self.arrival_time
        self.state = ProcessState.TERMINATED

    # Nice print format for debugging
    def __repr__(self):
        return (f"Process(pid={self.pid}, state={self.state.value}, "
                f"arrival={self.arrival_time}, remaining={self.remaining_time})")
    
    def __str__(self):
        return f"P{self.pid}"


# Example test (can be removed later)
if __name__ == "__main__":
    p1 = Process(1, 0, 5)
    p2 = Process(2, 2, 3)

    print(p1)
    print(p2)
    
