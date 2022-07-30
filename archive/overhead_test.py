import time


def main():
    # time_test()
    sleep_test()


def sleep_test():
    # Measure the overhead in calling time.sleep()
    n_iter = 10000
    sleep_duration = 0.0001
    # It looks like it's on the order of one percent error
    # 1 s : 1.2 ms
    # .1 s : .42 ms
    # .01 s : .39 ms
    # .001 s : .3 ms
    # .0001 s : .06 ms

    tick = time.time()
    for _ in range(n_iter):
        time.sleep(sleep_duration)

    elapsed = time.time() - tick - n_iter * sleep_duration
    print(f"{1000 * elapsed / n_iter} ms")


def time_test():
    # Measure the overhead in calling time.time()
    # ~.2 us
    n_iter = 10000000
    start = time.time()

    tick = time.time()
    for _ in range(n_iter):
        end = time.time()
        dt = end - start
        start = end
    elapsed = time.time() - tick
    print(dt)
    print(f"{1000 * elapsed / n_iter} ms")


main()
