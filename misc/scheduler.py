

from datetime import datetime

from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()


def job_function():
    print "Hello World"

# Schedule job_function to be called every two hours
sched.add_interval_job(job_function, seconds=2)
sched.start()

while True:
	pass