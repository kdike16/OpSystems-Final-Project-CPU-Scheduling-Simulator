from scheduler import Scheduler
from process import Process

scheduler = Scheduler()

scheduler.addProcess(Process(1, 0, 8))
scheduler.addProcess(Process(2, 1, 4)) #2
scheduler.addProcess(Process(3, 2, 2)) #4

scheduler.run()