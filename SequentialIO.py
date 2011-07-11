from time import time
from Environment import Environment

class SequentialIO:
    def __init__(self):
        self._name = "Sequential Write"
    def test_name(self):
        return self._name
    def _sequential_write(self, env, name, size):
        """Do a sequential write that is small enough to be entirely in ram"""
        env.test_start(name)
        r = env.load_last_result(name)
        result = r.split(' ')

        start = time()
        env.run_command(["dd", "if=/dev/zero", "of=" + env.dir + "/" + name,
            "bs=1M", "count=" + str(size)])
        end = time();
        env.test_result(name, 1, size, end - start)
        time_diff = end - start

        # Result is in this format
        # Name: <version> <number of mb written> <seconds>
        if len(result) == 4:
            diff = env.percent_difference_time(float(result[3]), time_diff)
            env.test_complete(name, diff)
        else:
            env.test_complete(name, 0)
        if env.verbose:
            print("\tTime: %.2f s, Throughput: %.2f Mb/s" % (time_diff, size / time_diff))

    def _sequential_write_ram(self, env):
        size = env.system_memory()
        size = int(size / 4)
        self._sequential_write(env, "SequentialWriteRam", size)

    def _sequential_write_large(self, env):
        size = env.system_memory()
        size = int(size * 2)
        self._sequential_write(env, "SequentialWriteLarge", size)

    def run(self, env):
        """Run the sequential IO tests

        env -- the environment that we are running in
        """
        self._sequential_write_ram(env)
        env.next_test()
        self._sequential_write_large(env)
# vim: set expandtab tabstop=4 shiftwidth=4
