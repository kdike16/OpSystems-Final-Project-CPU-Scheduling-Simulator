from scheduler import Scheduler
from process import Process

scheduler = Scheduler()

scheduler.addProcess(Process(1, 0, 5))
scheduler.addProcess(Process(2, 2, 3))
scheduler.addProcess(Process(3, 4, 2))

scheduler.run()