import time


class Pacemaker:
    """
    The Pacemaker class keeps a loop operating at a steady rhythm,
    according to a wall clock. It's useful for coordinating the activities
    of several asynchronous and real-time processes.

    Initialize Pacemaker(clock_freq) with the desired clock frequency in Hz.
    Call Pacemaker.beat() in a loop to ensure that the loop doesn't run
    faster than the clock frequency.

    beat() returns the amount of time elapsed for that cycle that was
    in excess of the desired clock period. A return value of 0 means it
    was exactly correct. If it's higher than that, it means that the
    cycle took a little longer to run than desired.
    It will usually be off by a little. You can
    set of checks on the return value if it's important to keep the cycle
    time tightly controlled.

    For consistency, all the time units are in seconds.
    """

    def __init__(self, clock_freq_Hz):
        self.clock_period = 1 / float(clock_freq_Hz)
        self.last_run_completed = time.time()
        self.this_run_completed = time.time()

        # Account for the overhead time it takes to call sleep().
        # It seems to vary depending on clock frequency.
        # At higher frequencies it's on the order of
        # one percent of the sleep duration.
        self.sleep_overhead_correction = 0.99

    def beat(self):
        self.last_run_completed = self.this_run_completed
        elapsed = time.time() - self.last_run_completed

        wait = (self.clock_period - elapsed) * self.sleep_overhead_correction
        if wait > 0:
            time.sleep(wait)

        self.this_run_completed = time.time()
        dt = self.this_run_completed - self.last_run_completed
        over = dt - self.clock_period
        return over
