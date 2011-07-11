from time import time
from Environment import Environment

class SequentialIO:
    def __init__(self):
        self._name = "Sequential Write"
    def test_name(self):
        return self._name
    def _sequential_write_ram(self, env):
        """Do a sequential write that is small enough to be entirely in ram"""
        r = env.load_last_result("SequentialWriteRam")
        result = r.split(' ')

        size = env.system_memory()
        size = int(size / 4)

        start = time()
        env.run_command(["dd", "if=/dev/zero", "of=" + env.dir + "/SequentialWrite",
            "bs=1M", "count=" + str(size)])
        end = time();
        env.test_result("SequentialWriteRam", 1, size, end - start)
        if env.verbose:
            print("Time: %.2f" % (end - start))
            print("Mb/s: %.2f" % (size / (end - start)))

        # Result is in this format
        # Name: <version> <number of mb written> <seconds>
        if len(result) == 4:
            diff = env.percent_difference_time(float(result[3]), end - start)
            env.test_complete("SequentialWriteRam", diff)
        else:
            env.test_complete("SequentialWriteRam", 0)

    def run(self, env):
        """Run the sequential IO tests

        env -- the environment that we are running in
        """
        self._sequential_write_ram(env)
# vim: set expandtab tabstop=4 shiftwidth=4
