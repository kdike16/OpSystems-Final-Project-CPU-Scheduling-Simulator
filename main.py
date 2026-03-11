from scheduler import Scheduler
from process import Process

scheduler = Scheduler()

scheduler.addProcces(Process(1, 0, 5))
scheduler.addProcces(Process(2, 2, 3))
scheduler.addProcces(Process(3, 4, 2))

scheduler.run()