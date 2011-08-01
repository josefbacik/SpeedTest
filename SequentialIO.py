from time import time
from Environment import Environment

class SequentialIO:
    def __init__(self):
        # This space intentially left blank
        pass

    def compare_results(self, str1, str2):
        first = str1.split(' ')
        second = str2.split(' ')
        if float(first[3]) < float(second[3]):
            return str1
        return str2

    def _sequential_write(self, env, name, size):
        """Do a sequential write that is small enough to be entirely in ram"""
        env.test_start(name)
        result = env.load_best_result(name, self.compare_results).split(' ');

        start = time()
        env.run_command(["dd", "if=/dev/zero", "of=" + env.dir + "/" + name,
            "bs=1M", "count=" + str(size)])
        end = time();
        time_diff = end - start

        # Result is in this format
        # Name: <version> <number of mb written> <seconds>
        if len(result) == 4 and int(result[1]) == 1:
            diff = env.percent_difference_time(float(result[3]), time_diff)
            env.test_complete(name, diff)
        else:
            env.test_complete(name, 0)
        env.test_result(name + ": 1 " + str(size) + " " + str(time_diff) + "\n")
        if env.verbose:
            print("\tTime: %.2f s, Throughput: %.2f Mb/s" % (time_diff, size / time_diff))
        return size

    def _sequential_write_ram(self, env):
        size = env.system_memory()
        size = int(size / 4)
        return self._sequential_write(env, "SequentialWriteRam", size)

    def _sequential_write_large(self, env):
        size = env.system_memory()
        size = int(size * 2)
        return self._sequential_write(env, "SequentialWriteLarge", size)

    def _sequential_read(self, env, name, size):
        """Do a sequential read of the large sequential write file we created"""
        env.test_start(name)
        result = env.load_best_result(name, self.compare_results).split(' ');

        start = time()
        env.run_command(["dd", "if=" + env.dir + "/SequentialWriteRam",
            "of=/dev/null", "bs=1M"])
        end = time();
        time_diff = end - start

        if len(result) == 4 and int(result[1]) == 1:
            diff = env.percent_difference_time(float(result[3]), time_diff)
            env.test_complete(name, diff)
        else:
            env.test_complete(name, 0)
        if env.verbose:
            print("\t Time: %.2f s, Throughput: %.2f Mb/s" % (time_diff, size / time_diff))
        env.test_result(name + ": 1 " + str(size) + " " + str(time_diff) + "\n")

    def run(self, env):
        """Run the sequential IO tests

        env -- the environment that we are running in
        """
        size = self._sequential_write_ram(env)
        # do a read immediately for a hot read time
        env.next_test()
        self._sequential_write_large(env)
        env.next_test()
        self._sequential_read(env, "SequentialColdRead", size)
        self._sequential_read(env, "SequentialReRead", size)

# vim: set expandtab tabstop=4 shiftwidth=4
