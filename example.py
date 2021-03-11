import time
import random
from threading import Thread


def random_delay():
    return random.random() * 5


def random_countdown():
    return random.randrange(5)


def launch_rocket(delay, countdown):
    time.sleep(delay)
    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        time.sleep(1)
    print("Rocket launched!")


def rockets():
    return [(random_delay(), random_countdown()) for _ in range(10_000)]


def run_threads():
    threads = [
        Thread(target=launch_rocket, args=(delay, countdown))
        for delay, countdown in rockets()
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


class Rocket(Thread):

    def __init__(self, delay, countdown, name=None):
        super(Rocket, self).__init__(name=name)
        self.delay = delay
        self.countdown = countdown

    def run(self):
        launch_rocket(self.delay, self.countdown)


def run_rockets():
    threads = [Rocket(delay, countdown) for delay, countdown in rockets()]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    # for d, c in rockets():
    #     launch_rocket(d, c)

    # run_threads()

    run_rockets()
