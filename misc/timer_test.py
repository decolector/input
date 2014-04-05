from threading import Thread, Event
from time import sleep


class Repeat(Thread):
    def __init__(self,delay,function,*args,**kwargs):
        Thread.__init__(self)
        self.abort = Event()
        self.delay = delay
        self.args = args
        self.kwargs = kwargs
        self.function = function

    def stop(self):
        self.abort.set()

    def run(self):
        while not self.abort.isSet():
            self.function(*self.args,**self.kwargs)
            self.abort.wait(self.delay)



def do_work(foo):
    print "busy printing: ", foo


if __name__ == "__main__":

    try: 
        r = Repeat(1,do_work, "hello") # execute do_work(3.14) every second
        r.start() # start the thread
        #sleep(5)  # let this demo run for 5s

    except  KeyboardInterrupt:
        print "terminating"
        r.stop()  # tell the thread to wake up and stop
        r.join()  # don't forget to .join() before your script ends